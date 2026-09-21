#!/usr/bin/env python3
"""
audit_session.py - Universal Agent Session and Telemetry Auditor

Parses agent session logs (Antigravity transcript.jsonl, Claude Code logs,
generic JSONL/JSON traces) to audit:
- Token consumption and thought expansion
- Tool call success vs failure rates (buggy code detection)
- Loaded skills vs actually invoked skills (dead components)
- Prompt friction, stealth failures, and repetitive loops via TypeSafe Jev
- Optional session context pruning
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Dynamic relative path to Agent Skills parent directory
DEFAULT_SKILLS_DIR = Path(__file__).resolve().parent.parent.parent

# Import JevService safely with fallback
try:
    from jev_service import JevService
    from jev_definitions import (
        DORMANT_SKILL_TRIGGER_THRESHOLD,
        FRICTION_PUSHBACK_THRESHOLD,
        FRICTION_REDUNDANCY_THRESHOLD,
        FRICTION_STEALTH_ERROR_THRESHOLD,
    )
    JEV_SUPPORT_AVAILABLE = True
except ImportError:
    JEV_SUPPORT_AVAILABLE = False


def extract_skill_description(skill_path: Path) -> str:
    """Extract description from SKILL.md frontmatter or first paragraph."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return ""
    try:
        content = skill_md.read_text(encoding="utf-8", errors="replace")
        # Match YAML frontmatter description
        fm_match = re.search(r"^description:\s*['\"]?(.*?)['\"]?$", content, re.MULTILINE)
        if fm_match:
            return fm_match.group(1).strip()
        # Fallback to first non-heading paragraph
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip() and not p.strip().startswith("#")]
        if paragraphs:
            return paragraphs[0][:200].strip()
    except Exception:
        pass
    return ""


def parse_antigravity_transcript(file_path: Path, use_jev: bool = False, max_jev_turns: int = 15) -> Dict[str, Any]:
    total_steps = 0
    user_inputs = 0
    planner_responses = 0
    tool_calls_total = 0
    tool_errors = 0
    tools_invoked = {}
    total_content_len = 0
    total_thinking_len = 0
    errors_list = []

    # Transcript turns structure for friction and pruning analysis
    steps_data = []
    user_messages = []
    raw_tool_calls = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                step = json.loads(line)
            except Exception:
                continue

            total_steps += 1
            step_type = step.get("type", "")
            step_status = step.get("status", "")
            content = step.get("content", "") or ""
            thinking = step.get("thinking", "") or ""
            step_idx = step.get("step_index", total_steps)

            total_content_len += len(content)
            total_thinking_len += len(thinking)

            if step_type == "USER_INPUT":
                user_inputs += 1
                user_messages.append(content)
            elif step_type == "PLANNER_RESPONSE":
                planner_responses += 1

            if step_status == "ERROR":
                tool_errors += 1
                errors_list.append({
                    "step": step_idx,
                    "error": content[:200] if content else "Unknown error",
                    "raw_length": len(content)
                })

            t_calls = step.get("tool_calls", [])
            steps_data.append({
                "step_index": step_idx,
                "type": step_type,
                "status": step_status,
                "content": content,
                "thinking": thinking,
                "tool_calls": t_calls
            })

    # Link tool outputs and compute accurate raw lengths
    for i, step in enumerate(steps_data):
        t_calls = step.get("tool_calls", [])
        if t_calls:
            next_output = ""
            if i + 1 < len(steps_data):
                next_output = steps_data[i + 1].get("content", "") or ""
            for tc in t_calls:
                tool_calls_total += 1
                t_name = tc.get("name") or tc.get("ToolName") or "unnamed_tool"
                tools_invoked[t_name] = tools_invoked.get(t_name, 0) + 1
                t_args = str(tc.get("parameters") or tc.get("Arguments") or "")
                raw_tool_calls.append({
                    "step_index": step.get("step_index", i + 1),
                    "name": t_name,
                    "args": t_args[:300],
                    "output": next_output[:400],
                    "raw_length": len(next_output) + len(t_args)
                })

    estimated_tokens = int((total_content_len + total_thinking_len) / 4)
    estimated_thinking_tokens = int(total_thinking_len / 4)

    telemetry = {
        "platform": "Antigravity",
        "file": str(file_path),
        "total_steps": total_steps,
        "user_inputs": user_inputs,
        "planner_responses": planner_responses,
        "estimated_total_tokens": estimated_tokens,
        "estimated_thinking_tokens": estimated_thinking_tokens,
        "tool_calls_total": tool_calls_total,
        "tool_errors": tool_errors,
        "tool_success_rate": round(100.0 * (tool_calls_total - tool_errors) / max(tool_calls_total, 1), 2),
        "tools_invoked": tools_invoked,
        "errors_sample": errors_list[:5],
        "friction_audit": None,
        "raw_tool_calls": raw_tool_calls,
        "session_goal": user_messages[0][:600] if user_messages else "",
        "final_response": steps_data[-1]["content"][:800] if steps_data else "",
    }

    # Task 1: Jev-backed prompt friction, stealth failure, and redundancy detection
    if use_jev and JEV_SUPPORT_AVAILABLE:
        jev_service = JevService()
        if jev_service.is_available():
            friction_results = audit_friction_with_jev(steps_data, jev_service, max_turns=max_jev_turns)
            telemetry["friction_audit"] = friction_results

    return telemetry


def audit_friction_with_jev(steps_data: List[Dict[str, Any]], jev_service: "JevService", max_turns: int = 15) -> Dict[str, Any]:
    """
    Evaluates conversational turns for:
    1. User pushback on previous assistant response
    2. Stealth tool error with non-ERROR status
    3. Tool redundancy given prior tool calls
    """
    user_pushbacks = []
    stealth_errors = []
    redundant_tools = []
    prior_tools_seen = []
    warranted_items = []
    evaluated_turns = 0
    wasted_chars_estimate = 0

    last_assistant_text = ""

    for i, step in enumerate(steps_data):
        step_type = step["type"]
        content = step.get("content", "")

        if step_type == "PLANNER_RESPONSE":
            last_assistant_text = content
            continue

        if step_type == "USER_INPUT" and last_assistant_text:
            # Check for user pushback and inspect recent tool call if present
            evaluated_turns += 1
            if evaluated_turns > max_turns:
                break

            prior_summary = ", ".join(prior_tools_seen[-5:]) if prior_tools_seen else "None"
            current_tool_name = "user_turn"
            current_tool_input = ""
            current_tool_output = ""

            # If adjacent step had a tool execution
            if i > 0 and steps_data[i - 1].get("tool_calls"):
                tcs = steps_data[i - 1]["tool_calls"]
                current_tool_name = tcs[0].get("name") or tcs[0].get("ToolName") or "tool"
                current_tool_input = str(tcs[0].get("parameters") or "")[:200]
                current_tool_output = steps_data[i - 1].get("content", "")[:300]

            eval_res = jev_service.check_friction(
                previous_assistant_response=last_assistant_text,
                user_message=content,
                prior_tools_summary=prior_summary,
                current_tool_name=current_tool_name,
                current_tool_input=current_tool_input,
                current_tool_output=current_tool_output,
            )

            if eval_res:
                if eval_res["is_pushback"]:
                    user_pushbacks.append({
                        "step": step.get("step_index", i + 1),
                        "user_message": content[:180],
                        "probability": eval_res["user_pushback_prob"]
                    })
                    wasted_chars_estimate += len(last_assistant_text) + len(content)

                if eval_res["is_stealth_error"] and current_tool_name != "user_turn":
                    stealth_errors.append({
                        "step": step.get("step_index", i + 1),
                        "tool": current_tool_name,
                        "output": current_tool_output[:180],
                        "probability": eval_res["stealth_error_prob"]
                    })
                    wasted_chars_estimate += len(current_tool_output)

                if eval_res["is_redundant"] and current_tool_name != "user_turn":
                    redundant_tools.append({
                        "step": step.get("step_index", i + 1),
                        "tool": current_tool_name,
                        "probability": eval_res["redundant_tool_prob"]
                    })
                    wasted_chars_estimate += len(current_tool_output) + len(current_tool_input)

                if eval_res["friction_warranted"]:
                    warranted_items.append({
                        "step": step.get("step_index", i + 1),
                        "pushback_p": eval_res["user_pushback_prob"],
                        "stealth_p": eval_res["stealth_error_prob"],
                        "redundant_p": eval_res["redundant_tool_prob"],
                    })

        # Track tools seen
        t_calls = step.get("tool_calls", [])
        for tc in t_calls:
            t_name = tc.get("name") or tc.get("ToolName") or "tool"
            prior_tools_seen.append(t_name)

    wasted_tokens_estimate = int(wasted_chars_estimate / 4)

    return {
        "evaluated_turns": evaluated_turns,
        "user_pushbacks": user_pushbacks,
        "stealth_errors": stealth_errors,
        "redundant_tools": redundant_tools,
        "warranted_for_reflection": len(warranted_items) > 0,
        "warranted_count": len(warranted_items),
        "estimated_wasted_tokens": wasted_tokens_estimate,
    }


def detect_dormant_skills(
    tools_invoked: Dict[str, int],
    available_skills_dir: Path = DEFAULT_SKILLS_DIR,
    use_jev: bool = False,
    session_summary: str = "",
) -> Dict[str, Any]:
    """
    Audits dormant skills.
    In plain mode: returns candidate folders not matched by substring.
    In Jev mode: batches Noul question per candidate to classify 'missed' vs 'rightly idle'.
    """
    dormant_candidates = []
    if not os.path.exists(available_skills_dir):
        return {"all_dormant": [], "missed_skills": [], "rightly_idle_skills": []}

    try:
        entries = os.listdir(available_skills_dir)
        for entry in entries:
            p = Path(available_skills_dir) / entry
            if p.is_dir() and not entry.startswith("."):
                # Substring check pre-filter
                was_used = False
                for t in tools_invoked.keys():
                    if entry.lower() in t.lower():
                        was_used = True
                        break
                if not was_used:
                    desc = extract_skill_description(p)
                    dormant_candidates.append({
                        "name": entry,
                        "description": desc or f"Domain skill for {entry}"
                    })
    except Exception:
        pass

    dormant_names = [d["name"] for d in dormant_candidates]

    # Task 2: Jev Noul semantic check to separate missed from rightly idle
    if use_jev and JEV_SUPPORT_AVAILABLE and dormant_candidates:
        jev_service = JevService()
        if jev_service.is_available():
            # Send top 12 candidate skills to avoid oversized batches
            shortlist = dormant_candidates[:12]
            jev_res = jev_service.check_dormant_skills(session_summary, shortlist)
            if jev_res:
                return {
                    "all_dormant": dormant_names,
                    "missed_skills": jev_res["missed_skills"],
                    "rightly_idle_skills": jev_res["rightly_idle_skills"],
                }

    return {
        "all_dormant": dormant_names,
        "missed_skills": [],
        "rightly_idle_skills": [],
    }


def generate_report(telemetry: Dict[str, Any], dormant_info: Dict[str, Any], json_output: bool = False) -> str:
    if json_output:
        data = dict(telemetry)
        data["dormant_skills"] = dormant_info
        return json.dumps(data, indent=2)

    lines = []
    lines.append("# Agent Session Telemetry and Health Report")
    lines.append("")
    lines.append(f"* Platform: {telemetry['platform']}")
    lines.append(f"* Source File: {telemetry['file']}")
    lines.append(f"* Total Session Steps: {telemetry['total_steps']}")
    lines.append(f"* User Turns: {telemetry['user_inputs']} | Agent Responses: {telemetry['planner_responses']}")
    lines.append(f"* Estimated Tokens: {telemetry['estimated_total_tokens']:,} (Thinking tokens: {telemetry['estimated_thinking_tokens']:,})")
    lines.append(f"* Tool Calls: {telemetry['tool_calls_total']} (Explicit Errors: {telemetry['tool_errors']})")
    lines.append(f"* Tool Success Rate: {telemetry['tool_success_rate']}%")
    lines.append("")

    lines.append("## Tool Invocation Frequency")
    if telemetry['tools_invoked']:
        for t, c in sorted(telemetry['tools_invoked'].items(), key=lambda x: x[1], reverse=True):
            lines.append(f"* `{t}`: {c} invocations")
    else:
        lines.append("* No tool calls recorded")
    lines.append("")

    if telemetry['tool_errors'] > 0:
        lines.append("## Buggy Code and Execution Friction Detected")
        lines.append("> [!WARNING]")
        lines.append(f"> Detected {telemetry['tool_errors']} tool execution errors. Frequent errors burn tokens and indicate code syntax or parameter mismatches.")
        for err in telemetry['errors_sample']:
            lines.append(f"* Step {err['step']}: {err['error']}")
        lines.append("")

    # Task 1 Jev Friction Report Section
    friction = telemetry.get("friction_audit")
    if friction:
        lines.append("## Jev System One Friction and Redundancy Audit")
        if friction["warranted_for_reflection"]:
            lines.append("> [!IMPORTANT]")
            lines.append(f"> Semantic friction detected across {friction['warranted_count']} turn(s). Estimated tokens consumed by friction: {friction['estimated_wasted_tokens']:,}.")
            lines.append("> Root cause diagnosis and prevention rule generation is warranted for the Main Model.")
        else:
            lines.append("* No significant user pushback, stealth failure, or tool redundancy detected.")

        if friction["user_pushbacks"]:
            lines.append("")
            lines.append("### User Pushbacks and Corrections")
            for item in friction["user_pushbacks"]:
                lines.append(f"* Step {item['step']} (p={item['probability']}): \"{item['user_message']}\"")

        if friction["stealth_errors"]:
            lines.append("")
            lines.append("### Stealth Tool Errors (Non ERROR Status)")
            for item in friction["stealth_errors"]:
                lines.append(f"* Step {item['step']} `{item['tool']}` (p={item['probability']}): \"{item['output']}\"")

        if friction["redundant_tools"]:
            lines.append("")
            lines.append("### Redundant Tool Calls")
            for item in friction["redundant_tools"]:
                lines.append(f"* Step {item['step']} `{item['tool']}` (p={item['probability']})")
        lines.append("")

    # Task 2 Dormant Skills Section
    missed = dormant_info.get("missed_skills", [])
    rightly_idle = dormant_info.get("rightly_idle_skills", [])
    all_dormant = dormant_info.get("all_dormant", [])

    if missed:
        lines.append("## Missed Skills (Should Have Triggered)")
        lines.append("> [!WARNING]")
        lines.append("> Jev semantic evaluation determined the following skills matched the session's tasks but were never invoked:")
        for s in missed:
            lines.append(f"* `{s['name']}` (probability: {s['probability']}): {s['description']}")
        lines.append("")

    if rightly_idle:
        lines.append("## Rightly Idle Skills (Correctly Inactive)")
        lines.append("> [!NOTE]")
        lines.append("> Jev confirmed these skills were correctly inactive during this session:")
        for s in rightly_idle[:6]:
            lines.append(f"* `{s['name']}` (p={s['probability']})")
        if len(rightly_idle) > 6:
            lines.append(f"* ...and {len(rightly_idle) - 6} more correctly idle skills")
        lines.append("")
    elif all_dormant:
        lines.append("## Inactive Skills Audit (Pre Jev Filter)")
        lines.append("> [!NOTE]")
        lines.append("> The following skills had zero recorded invocations in this session:")
        for s in all_dormant[:8]:
            lines.append(f"* `{s}`")
        if len(all_dormant) > 8:
            lines.append(f"* ...and {len(all_dormant) - 8} more dormant skills")
        lines.append("")

    lines.append("## Optimization Recommendations")
    if telemetry['tool_success_rate'] < 85:
        lines.append("* High error rate: Add verification steps before emitting file edits to stop repeated syntax fixes.")
    if telemetry['estimated_thinking_tokens'] > (telemetry['estimated_total_tokens'] * 0.5):
        lines.append("* Excessive thinking tokens: Consider lowering effort level for straightforward mechanical tasks.")
    if telemetry['total_steps'] > 40:
        lines.append("* High session length: Run compaction or clear session to maintain sharp context focus.")
    if friction and friction["warranted_for_reflection"]:
        lines.append(f"* Log anti-pattern: Record friction root causes to memory ledger to save estimated {friction['estimated_wasted_tokens']:,} tokens.")
    if not (telemetry['tool_success_rate'] < 85 or telemetry['total_steps'] > 40):
        lines.append("* Session parameters are within optimal token efficiency thresholds.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit agent session logs for token waste and errors.")
    parser.add_argument("logfile", nargs="?", help="Path to session log (e.g. transcript.jsonl)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--skills-dir", default=str(DEFAULT_SKILLS_DIR), help="Directory containing installed skills")
    parser.add_argument("--use-jev", action="store_true", help="Enable Jev System One semantic friction and dormant skill audit")
    parser.add_argument("--prune", action="store_true", help="Run optional session tool call pruning evaluation")
    parser.add_argument("--max-jev-turns", type=int, default=15, help="Maximum turns to audit with Jev")

    args = parser.parse_args()

    if not args.logfile:
        print("Usage: python audit_session.py <path_to_transcript.jsonl> [--json] [--use-jev] [--prune]")
        print("Please provide a log file to audit.")
        sys.exit(1)

    log_path = Path(args.logfile)
    if not log_path.exists():
        print(f"Error: Log file not found at {args.logfile}")
        sys.exit(1)

    skills_dir = Path(args.skills_dir)
    telemetry = parse_antigravity_transcript(log_path, use_jev=args.use_jev, max_jev_turns=args.max_jev_turns)

    # Dormant skill analysis
    session_work_summary = f"Goal: {telemetry['session_goal']}\nTools: {', '.join(telemetry['tools_invoked'].keys())}\nFinal: {telemetry['final_response'][:400]}"
    dormant_info = detect_dormant_skills(
        telemetry["tools_invoked"],
        available_skills_dir=skills_dir,
        use_jev=args.use_jev,
        session_summary=session_work_summary,
    )

    print(generate_report(telemetry, dormant_info, args.json))

    # Task 6: Session pruning if requested
    if args.prune:
        if not JEV_SUPPORT_AVAILABLE:
            print("\nError: typesafe-sdk is not available for session pruning.")
            sys.exit(1)
        jev_service = JevService()
        if not jev_service.is_available():
            print("\nNotice: TYPESAFE_API_KEY is unset. Session pruning requires a valid TypeSafe key.")
            sys.exit(0)

        tool_calls = telemetry.get("raw_tool_calls", [])
        if not tool_calls:
            print("\nNotice: No tool calls recorded in session to prune.")
            return

        print("\n" + "=" * 60)
        print("Session Tool Call Pruning Evaluation (TypeSafe Jev)")
        print("=" * 60)
        prune_results = jev_service.evaluate_tool_calls_for_pruning(
            session_goal=telemetry["session_goal"],
            final_response=telemetry["final_response"],
            tool_calls=tool_calls[:25],  # Prune batch
        )

        if prune_results:
            prune_count = sum(1 for r in prune_results if r["safe_to_prune"])
            retained_count = len(prune_results) - prune_count
            pruned_chars = sum(r["raw_length"] for r in prune_results if r["safe_to_prune"])
            pruned_tokens = int(pruned_chars / 4)

            print(f"Total Evaluated Calls: {len(prune_results)}")
            print(f"Safe to Prune: {prune_count} calls | Retained: {retained_count} calls")
            print(f"Estimated Context Tokens Saved: {pruned_tokens:,}")
            print("-" * 60)
            for r in prune_results:
                tag = "[PRUNE]" if r["safe_to_prune"] else "[KEEP] "
                print(f"{tag} Step {r['step_index']}: `{r['name']}` (usefulness p={r['usefulness_prob']})")


if __name__ == "__main__":
    main()
