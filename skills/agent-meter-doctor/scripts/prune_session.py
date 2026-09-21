#!/usr/bin/env python3
"""
prune_session.py - Context-Aware Session Tool Call Pruner (TypeSafe Jev)

Inspired by the Jev tool call pruning plugin that reduced session context
from ~1M tokens to 86K tokens.

Given an agent session transcript, this opt-in tool batches one Noul question
per tool call:
  'Was this tool call result actually used or relevant to producing the final response?'

Returns which calls are safe to prune from context, computes real token savings,
and can optionally write out a pruned transcript copy.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Dynamic relative path resolution
BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from jev_service import JevService
    from jev_definitions import PRUNE_USEFUL_THRESHOLD
    JEV_AVAILABLE = True
except ImportError:
    JEV_AVAILABLE = False


def extract_session_tool_calls(file_path: Path) -> Dict[str, Any]:
    """Parse transcript and extract tool calls and context."""
    user_prompts = []
    final_solution = ""
    tool_calls = []
    total_raw_chars = 0
    all_steps = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                step = json.loads(line)
            except Exception:
                continue

            all_steps.append(step)
            step_type = step.get("type", "")
            content = step.get("content", "") or ""
            step_idx = step.get("step_index", len(all_steps))

    for i, step in enumerate(all_steps):
        step_type = step.get("type", "")
        content = step.get("content", "") or ""

        if step_type == "USER_INPUT":
            user_prompts.append(content)
        elif step_type == "PLANNER_RESPONSE" and content:
            final_solution = content

        t_calls = step.get("tool_calls", [])
        if t_calls:
            # The tool output is in the subsequent step
            next_output = ""
            if i + 1 < len(all_steps):
                next_output = all_steps[i + 1].get("content", "") or ""

            for tc in t_calls:
                t_name = tc.get("name") or tc.get("ToolName") or "unnamed_tool"
                t_args = str(tc.get("parameters") or tc.get("Arguments") or "")
                chars = len(next_output) + len(t_args)
                total_raw_chars += chars
                tool_calls.append({
                    "step_index": step.get("step_index", i + 1),
                    "name": t_name,
                    "args": t_args[:300],
                    "output": next_output[:400],
                    "raw_length": chars,
                })

    return {
        "user_goal": user_prompts[0][:600] if user_prompts else "",
        "final_solution": final_solution[:1200],
        "tool_calls": tool_calls,
        "total_tool_chars": total_raw_chars,
        "all_steps": all_steps,
    }


def prune_session(
    transcript_path: Path,
    output_path: Optional[Path] = None,
    batch_size: int = 30,
) -> None:
    if not JEV_AVAILABLE:
        print("Error: typesafe-sdk is not installed. Run 'pip install typesafe-sdk' to enable pruning.")
        sys.exit(1)

    jev_service = JevService()
    if not jev_service.is_available():
        print("Notice: TYPESAFE_API_KEY is not configured in .env or environment.")
        print("Session pruning requires a valid TypeSafe key to judge tool usefulness.")
        sys.exit(0)

    data = extract_session_tool_calls(transcript_path)
    tool_calls = data["tool_calls"]

    if not tool_calls:
        print("No tool calls found in transcript to prune.")
        return

    print("=" * 65)
    print("Session Context Pruning Analysis (TypeSafe Jev System One)")
    print("=" * 65)
    print(f"Transcript: {transcript_path.name}")
    print(f"Total Tool Invocations: {len(tool_calls)}")
    print(f"Evaluating first {min(len(tool_calls), batch_size)} calls with batched Jev queries...")

    eval_batch = tool_calls[:batch_size]
    prune_eval = jev_service.evaluate_tool_calls_for_pruning(
        session_goal=data["user_goal"],
        final_response=data["final_solution"],
        tool_calls=eval_batch,
    )

    if not prune_eval:
        print("Pruning evaluation could not be completed.")
        return

    pruned_items = [r for r in prune_eval if r["safe_to_prune"]]
    retained_items = [r for r in prune_eval if not r["safe_to_prune"]]

    pruned_chars = sum(r["raw_length"] for r in pruned_items)
    pruned_tokens = int(pruned_chars / 4)
    total_tokens = int(data["total_tool_chars"] / 4)

    print("\n## Pruning Results Summary")
    print(f"* Evaluated: {len(prune_eval)} tool calls")
    print(f"* Recommended to Prune: {len(pruned_items)} calls ({len(pruned_items)/len(prune_eval):.1%})")
    print(f"* Retained (Useful to solution): {len(retained_items)} calls")
    print(f"* Estimated Tokens Saved: {pruned_tokens:,} tokens (out of {total_tokens:,} total tool tokens)")
    print("")

    print("## Step-by-Step Manifest")
    print(f"{'Status':<9} {'Step':<6} {'Tool Name':<28} {'Usefulness p':<14} {'Tokens Saved'}")
    print("-" * 72)
    for r in prune_eval:
        status = "[PRUNE]" if r["safe_to_prune"] else "[KEEP]"
        tok = f"{int(r['raw_length'] / 4):,}" if r["safe_to_prune"] else "-"
        print(f"{status:<9} {r['step_index']:<6} {r['name'][:26]:<28} {r['usefulness_prob']:<14.3f} {tok}")

    if output_path:
        pruned_step_indices = {r["step_index"] for r in pruned_items}
        with open(output_path, "w", encoding="utf-8") as out_f:
            for step in data["all_steps"]:
                step_copy = dict(step)
                s_idx = step_copy.get("step_index")
                if s_idx in pruned_step_indices:
                    # Strip verbose content
                    if step_copy.get("content"):
                        step_copy["content"] = "[PRUNED: tool output not required for final solution]"
                out_f.write(json.dumps(step_copy) + "\n")
        print(f"\nSuccessfully generated pruned transcript copy at: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Prune unnecessary tool calls from session context using TypeSafe Jev."
    )
    parser.add_argument("logfile", help="Path to transcript.jsonl file")
    parser.add_argument("--output", help="Optional path to write pruned transcript copy")
    parser.add_argument("--batch-size", type=int, default=30, help="Max tool calls to evaluate (default: 30)")

    args = parser.parse_args()

    log_path = Path(args.logfile)
    if not log_path.exists():
        print(f"Error: Transcript not found at {args.logfile}")
        sys.exit(1)

    out_path = Path(args.output) if args.output else None
    prune_session(log_path, output_path=out_path, batch_size=args.batch_size)


if __name__ == "__main__":
    main()
