#!/usr/bin/env python3
"""
reflect_and_learn.py - Autonomous Post-Turn Reflection & Mistake Ledger Manager

Inspired by Hermes agent reflective memory and enhanced with TypeSafe Jev System One:
- Semantic search and relevance re-ranking for anti-pattern retrieval
- Automatic classification into the 5 standard ledger categories
- Semantic duplicate detection on write to prevent ledger bloat
- Fully portable relative path resolution
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Dynamic relative path resolution
LEDGER_PATH = Path(__file__).resolve().parent.parent / "memory" / "anti_patterns_ledger.md"

try:
    from jev_service import JevService
    from jev_definitions import FIXED_CATEGORIES, LEDGER_DEDUP_THRESHOLD, LEDGER_SEARCH_SHORTLIST_MAX
    JEV_AVAILABLE = True
except ImportError:
    JEV_AVAILABLE = False


def parse_ledger_entries(ledger_text: str) -> List[Dict[str, Any]]:
    """Parse anti_patterns_ledger.md into structured entry dictionaries."""
    entries = []
    # Split by ### Entry APxxx:
    pattern = re.compile(r"### Entry (AP\d{3}):\s*(.+?)(?=\n### Entry |\Z)", re.DOTALL)
    for match in pattern.finditer(ledger_text):
        eid = match.group(1).strip()
        title = match.group(2).split("\n")[0].strip()
        body = match.group(2)

        def extract_field(field_name: str) -> str:
            m = re.search(rf"\*\s*{field_name}:\s*(.*?)(?=\n\*|\Z)", body, re.DOTALL | re.IGNORECASE)
            return m.group(1).strip() if m else ""

        entries.append({
            "id": eid,
            "title": title,
            "category": extract_field("Category"),
            "date": extract_field("Detected Date"),
            "failure": extract_field("Failure Mode"),
            "cause": extract_field("Root Cause"),
            "signal": extract_field("Detection Signal"),
            "rule": extract_field("Strict Prevention Rule"),
            "saved": extract_field("Efficiency Gain"),
            "raw_block": f"### Entry {eid}: {match.group(2).strip()}"
        })
    return entries


def get_next_entry_id(ledger_text: str) -> str:
    ids = re.findall(r"Entry AP(\d{3})", ledger_text)
    if not ids:
        return "AP001"
    max_id = max(int(i) for i in ids)
    return f"AP{max_id + 1:03d}"


def list_entries() -> None:
    if not LEDGER_PATH.exists():
        print("Ledger file not found.")
        return

    content = LEDGER_PATH.read_text(encoding="utf-8")
    entries = parse_ledger_entries(content)
    print(f"Total Logged Anti-Patterns: {len(entries)}")
    print("=" * 60)
    for e in entries:
        print(f"* [{e['id']}] ({e['category']}) {e['title']}")


def calculate_keyword_overlap(query: str, entry: Dict[str, Any]) -> float:
    """Fast pre-filter scoring based on keyword overlap."""
    stop_words = {"the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "with", "is", "was", "it"}
    query_tokens = set(re.findall(r"\w+", query.lower())) - stop_words
    if not query_tokens:
        return 0.0

    title_tokens = set(re.findall(r"\w+", entry["title"].lower()))
    rule_tokens = set(re.findall(r"\w+", entry["rule"].lower()))
    body_tokens = set(re.findall(r"\w+", (entry["failure"] + " " + entry["cause"]).lower()))

    # Weighted overlap: title matches x3, rule matches x2, body matches x1
    score = (
        len(query_tokens & title_tokens) * 3.0 +
        len(query_tokens & rule_tokens) * 2.0 +
        len(query_tokens & body_tokens) * 1.0
    )
    return score


def search_entries(query: str, top_k: int = 3, use_jev: bool = True) -> None:
    """
    Search ledger entries:
    1. Fast keyword overlap pre-filter to shortlist candidates
    2. Optional batched Jev Score query to re-rank shortlist by relevance
    """
    if not LEDGER_PATH.exists():
        print("Ledger file not found.")
        return

    content = LEDGER_PATH.read_text(encoding="utf-8")
    all_entries = parse_ledger_entries(content)
    if not all_entries:
        print("No entries recorded in ledger.")
        return

    # Step 1: Pre-filter in code
    for entry in all_entries:
        entry["keyword_score"] = calculate_keyword_overlap(query, entry)

    # Sort by keyword score
    shortlist = sorted(all_entries, key=lambda x: x["keyword_score"], reverse=True)
    # Take candidates (either matching keywords or up to shortlist max)
    matching_shortlist = [e for e in shortlist if e["keyword_score"] > 0]
    if not matching_shortlist:
        candidates = shortlist[:LEDGER_SEARCH_SHORTLIST_MAX]
    else:
        candidates = matching_shortlist[:LEDGER_SEARCH_SHORTLIST_MAX]

    # Step 2: Jev Score Re-ranking
    ranked_entries = candidates
    jev_used = False

    if use_jev and JEV_AVAILABLE:
        jev_service = JevService()
        if jev_service.is_available():
            scored = jev_service.score_ledger_entries(query, candidates)
            if scored:
                ranked_entries = scored
                jev_used = True

    # Limit to top_k
    final_results = ranked_entries[:top_k]

    print("=" * 60)
    mode_label = "TypeSafe Jev Semantic Ranking" if jev_used else "Keyword Overlap Filter"
    print(f"Anti-Pattern Search Results ({mode_label})")
    print(f"Query: \"{query}\"")
    print("=" * 60)

    if not final_results:
        print(f"No anti-patterns found matching '{query}'.")
        return

    for entry in final_results:
        score_info = ""
        if jev_used and "jev_relevance_score" in entry:
            score_info = f" [Relevance Score: {entry['jev_relevance_score']:.2f}]"
        elif entry.get("keyword_score", 0) > 0:
            score_info = f" [Keyword Matches: {int(entry['keyword_score'])}]"

        print(f"\n### Entry {entry['id']}: {entry['title']}{score_info}")
        print(f"* Category: {entry['category']}")
        print(f"* Failure Mode: {entry['failure']}")
        print(f"* Root Cause: {entry['cause']}")
        print(f"* Strict Prevention Rule: {entry['rule']}")
        if entry.get("saved"):
            print(f"* Efficiency Gain: {entry['saved']}")
        print("-" * 40)


def log_entry(
    category: Optional[str],
    title: str,
    failure_mode: str,
    root_cause: str,
    rule: str,
    tokens_saved: Optional[str] = None,
    force: bool = False,
    use_jev: bool = True,
) -> None:
    """
    Log a new anti-pattern entry:
    - Jev semantic dedup: checks against existing entries before appending
    - Jev classification: maps to the 5 standard categories
    - Saves computed tokens or leaves field blank if no measurement exists
    """
    if not LEDGER_PATH.exists():
        print(f"Ledger file does not exist at {LEDGER_PATH}.")
        return

    content = LEDGER_PATH.read_text(encoding="utf-8")
    existing_entries = parse_ledger_entries(content)

    final_category = category
    if final_category and final_category not in FIXED_CATEGORIES:
        # Default to passed category if non-standard, or allow Jev to reclassify
        pass

    # Jev Categorization and Dedup
    if use_jev and JEV_AVAILABLE:
        jev_service = JevService()
        if jev_service.is_available():
            eval_res = jev_service.classify_and_dedup_entry(
                title=title,
                failure=failure_mode,
                cause=root_cause,
                rule=rule,
                existing_entries=existing_entries,
            )

            if eval_res:
                # Use standard category from Jev
                final_category = eval_res.get("classified_category") or final_category

                # Check for duplicate
                if eval_res.get("is_duplicate") and not force:
                    dup = eval_res["duplicate_matches"][0]
                    print("\n> [!WARNING]")
                    print(f"> Duplicate mistake detected: This entry is substantively identical to existing entry [{dup['id']}] '{dup['title']}' (similarity probability: {dup['similarity_prob']:.2f}).")
                    print("> Operation aborted to prevent ledger duplication. Use --force to record anyway.")
                    return

    if not final_category:
        final_category = "Buggy Code"

    next_id = get_next_entry_id(content)
    today = datetime.date.today().isoformat()

    # Efficiency gain handling: use real computation if provided, else leave blank
    gain_field = tokens_saved if (tokens_saved and tokens_saved.strip()) else ""

    new_block = f"""
### Entry {next_id}: {title}
* Category: {final_category}
* Detected Date: {today}
* Failure Mode: {failure_mode}
* Root Cause: {root_cause}
* Detection Signal: Autonomous Post Turn Reflection
* Strict Prevention Rule: {rule}
* Efficiency Gain: {gain_field}
"""

    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(new_block)

    print(f"Successfully logged new entry {next_id}: {title} (Category: {final_category})")


def main():
    parser = argparse.ArgumentParser(description="Manage agent anti-pattern memory and reflections.")
    subparsers = parser.add_subparsers(dest="command")

    # List command
    subparsers.add_parser("list", help="List all anti-patterns in the ledger")

    # Search command
    search_p = subparsers.add_parser("search", help="Search the ledger with keyword pre-filter and Jev semantic ranking")
    search_p.add_argument("query", help="Keyword, phrase, or task to search")
    search_p.add_argument("--top-k", type=int, default=3, help="Number of results to display (default: 3)")
    search_p.add_argument("--no-jev", action="store_true", help="Disable Jev semantic re-ranking")

    # Log command
    log_p = subparsers.add_parser("log", help="Log a newly discovered mistake or anti-pattern")
    log_p.add_argument("--category", default=None, help=f"Category (Standard: {', '.join(FIXED_CATEGORIES.keys())})")
    log_p.add_argument("--title", required=True, help="Short title")
    log_p.add_argument("--failure", required=True, help="Description of failure")
    log_p.add_argument("--cause", required=True, help="Root cause")
    log_p.add_argument("--rule", required=True, help="Strict rule to prevent recurrence")
    log_p.add_argument("--saved", default=None, help="Efficiency gain (real computed tokens, or leave blank)")
    log_p.add_argument("--force", action="store_true", help="Force logging even if duplicate detected")
    log_p.add_argument("--no-jev", action="store_true", help="Disable Jev classification and dedup")

    args = parser.parse_args()

    if args.command == "list":
        list_entries()
    elif args.command == "search":
        search_entries(args.query, top_k=args.top_k, use_jev=not args.no_jev)
    elif args.command == "log":
        log_entry(
            category=args.category,
            title=args.title,
            failure_mode=args.failure,
            root_cause=args.cause,
            rule=args.rule,
            tokens_saved=args.saved,
            force=args.force,
            use_jev=not args.no_jev,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
