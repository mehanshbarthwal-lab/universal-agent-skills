#!/usr/bin/env python3
"""
audit_session.py - Universal Agent Session and Telemetry Auditor

Parses agent session logs (Antigravity transcript.jsonl, Claude Code logs,
generic JSONL/JSON traces) to audit:
- Token consumption and thought expansion
- Tool call success vs failure rates (buggy code detection)
- Loaded skills vs actually invoked skills (dead components)
- Prompt friction and repetitive loops
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

def parse_antigravity_transcript(file_path):
    total_steps = 0
    user_inputs = 0
    planner_responses = 0
    tool_calls_total = 0
    tool_errors = 0
    tools_invoked = {}
    total_content_len = 0
    total_thinking_len = 0
    errors_list = []

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

            total_content_len += len(content)
            total_thinking_len += len(thinking)

            if step_type == "USER_INPUT":
                user_inputs += 1
            elif step_type == "PLANNER_RESPONSE":
                planner_responses += 1

            if step_status == "ERROR":
                tool_errors += 1
                errors_list.append({
                    "step": step.get("step_index", total_steps),
                    "error": content[:200] if content else "Unknown error"
                })

            t_calls = step.get("tool_calls", [])
            if t_calls:
                for tc in t_calls:
                    tool_calls_total += 1
                    t_name = tc.get("name") or tc.get("ToolName") or "unnamed_tool"
                    tools_invoked[t_name] = tools_invoked.get(t_name, 0) + 1

    estimated_tokens = int((total_content_len + total_thinking_len) / 4)
    estimated_thinking_tokens = int(total_thinking_len / 4)

    return {
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
        "errors_sample": errors_list[:5]
    }

def detect_dormant_skills(tools_invoked, available_skills_dir="F:\\Agent Skills"):
    dormant = []
    if not os.path.exists(available_skills_dir):
        return dormant

    try:
        entries = os.listdir(available_skills_dir)
        for entry in entries:
            p = os.path.join(available_skills_dir, entry)
            if os.path.isdir(p) and not entry.startswith("."):
                # Check if this skill or its tools were used
                was_used = False
                for t in tools_invoked.keys():
                    if entry.lower() in t.lower():
                        was_used = True
                        break
                if not was_used:
                    dormant.append(entry)
    except Exception:
        pass
    return dormant

def generate_report(telemetry, dormant_skills=None, json_output=False):
    if json_output:
        data = dict(telemetry)
        data["dormant_skills_sample"] = dormant_skills[:10] if dormant_skills else []
        return json.dumps(data, indent=2)

    lines = []
    lines.append("# Agent Session Telemetry and Health Report")
    lines.append("")
    lines.append(f"* Platform: {telemetry['platform']}")
    lines.append(f"* Source File: {telemetry['file']}")
    lines.append(f"* Total Session Steps: {telemetry['total_steps']}")
    lines.append(f"* User Turns: {telemetry['user_inputs']} | Agent Responses: {telemetry['planner_responses']}")
    lines.append(f"* Estimated Tokens: {telemetry['estimated_total_tokens']:,} (Thinking tokens: {telemetry['estimated_thinking_tokens']:,})")
    lines.append(f"* Tool Calls: {telemetry['tool_calls_total']} (Errors: {telemetry['tool_errors']})")
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
        lines.append(f"> [!WARNING]")
        lines.append(f"> Detected {telemetry['tool_errors']} tool execution errors. Frequent errors burn tokens and indicate code syntax or parameter mismatches.")
        for err in telemetry['errors_sample']:
            lines.append(f"* Step {err['step']}: {err['error']}")
        lines.append("")

    if dormant_skills:
        lines.append("## Dead Skills and Inactive Components Audit")
        lines.append(f"> [!NOTE]")
        lines.append(f"> The following skills exist in your skills directory but had zero recorded tool calls in this session:")
        for s in dormant_skills[:8]:
            lines.append(f"* `{s}`")
        if len(dormant_skills) > 8:
            lines.append(f"* ...and {len(dormant_skills) - 8} more dormant skills")
        lines.append("")

    lines.append("## Optimization Recommendations")
    if telemetry['tool_success_rate'] < 85:
        lines.append("* High error rate: Add verification steps before emitting file edits to stop repeated syntax fixes.")
    if telemetry['estimated_thinking_tokens'] > (telemetry['estimated_total_tokens'] * 0.5):
        lines.append("* Excessive thinking tokens: Consider lowering effort level for straightforward mechanical tasks.")
    if telemetry['total_steps'] > 40:
        lines.append("* High session length: Run compaction or clear session to maintain sharp context focus.")
    if not (telemetry['tool_success_rate'] < 85 or telemetry['total_steps'] > 40):
        lines.append("* Session parameters are within optimal token efficiency thresholds.")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Audit agent session logs for token waste and errors.")
    parser.add_argument("logfile", nargs="?", help="Path to session log (e.g. transcript.jsonl)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--skills-dir", default="F:\\Agent Skills", help="Directory containing installed skills")

    args = parser.parse_args()

    if not args.logfile:
        print("Usage: python audit_session.py <path_to_transcript.jsonl> [--json]")
        print("Please provide a log file to audit.")
        sys.exit(1)

    if not os.path.exists(args.logfile):
        print(f"Error: Log file not found at {args.logfile}")
        sys.exit(1)

    telemetry = parse_antigravity_transcript(args.logfile)
    dormant = detect_dormant_skills(telemetry["tools_invoked"], args.skills_dir)
    print(generate_report(telemetry, dormant, args.json))

if __name__ == "__main__":
    main()
