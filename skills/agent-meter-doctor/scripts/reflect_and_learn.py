#!/usr/bin/env python3
"""
reflect_and_learn.py - Autonomous Post-Turn Reflection & Mistake Ledger Manager

Inspired by Hermes agent reflective memory, this script manages the persistent
anti-pattern ledger to record mistakes, extract learnings, and prevent repeated
errors across all AI agents.
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

LEDGER_PATH = Path("F:/Agent Skills/agent-meter-doctor/memory/anti_patterns_ledger.md")

def get_next_entry_id(ledger_text):
    ids = re.findall(r"Entry AP(\d{3})", ledger_text)
    if not ids:
        return "AP001"
    max_id = max(int(i) for i in ids)
    return f"AP{max_id + 1:03d}"

def list_entries():
    if not LEDGER_PATH.exists():
        print("Ledger file not found.")
        return

    content = LEDGER_PATH.read_text(encoding="utf-8")
    entries = re.findall(r"### Entry (AP\d{3}):\s*(.+)", content)
    print(f"Total Logged Anti-Patterns: {len(entries)}")
    print("=" * 60)
    for eid, title in entries:
        print(f"* [{eid}] {title}")

def search_entries(query):
    if not LEDGER_PATH.exists():
        print("Ledger file not found.")
        return

    content = LEDGER_PATH.read_text(encoding="utf-8")
    sections = content.split("### Entry ")
    results = []
    q_lower = query.lower()

    for sec in sections[1:]:
        if q_lower in sec.lower():
            results.append("### Entry " + sec.strip())

    if results:
        print(f"Found {len(results)} matching entries:")
        print("=" * 60)
        for r in results:
            print(r)
            print("-" * 40)
    else:
        print(f"No anti-patterns found matching '{query}'.")

def log_entry(category, title, failure_mode, root_cause, rule, tokens_saved):
    if not LEDGER_PATH.exists():
        print("Ledger file does not exist.")
        return

    content = LEDGER_PATH.read_text(encoding="utf-8")
    next_id = get_next_entry_id(content)
    today = datetime.date.today().isoformat()

    new_block = f"""
### Entry {next_id}: {title}
* Category: {category}
* Detected Date: {today}
* Failure Mode: {failure_mode}
* Root Cause: {root_cause}
* Detection Signal: Autonomous Post Turn Reflection
* Strict Prevention Rule: {rule}
* Efficiency Gain: {tokens_saved}
"""

    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(new_block)

    print(f"Successfully logged new entry {next_id}: {title}")

def main():
    parser = argparse.ArgumentParser(description="Manage agent anti-pattern memory and reflections.")
    subparsers = parser.add_subparsers(dest="command")

    # List command
    subparsers.add_parser("list", help="List all anti-patterns in the ledger")

    # Search command
    search_p = subparsers.add_parser("search", help="Search the ledger for keywords")
    search_p.add_argument("query", help="Keyword or phrase to search")

    # Log command
    log_p = subparsers.add_parser("log", help="Log a newly discovered mistake or anti-pattern")
    log_p.add_argument("--category", required=True, help="Category (e.g. Buggy Code, Token Waste)")
    log_p.add_argument("--title", required=True, help="Short title")
    log_p.add_argument("--failure", required=True, help="Description of failure")
    log_p.add_argument("--cause", required=True, help="Root cause")
    log_p.add_argument("--rule", required=True, help="Strict rule to prevent recurrence")
    log_p.add_argument("--saved", default="Estimated 10,000 to 30,000 tokens", help="Efficiency gain")

    args = parser.parse_args()

    if args.command == "list":
        list_entries()
    elif args.command == "search":
        search_entries(args.query)
    elif args.command == "log":
        log_entry(args.category, args.title, args.failure, args.cause, args.rule, args.saved)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
