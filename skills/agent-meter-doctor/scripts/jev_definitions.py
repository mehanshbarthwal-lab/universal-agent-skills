"""
jev_definitions.py - TypeSafe AI Jev Question Definitions and Calibration Constants

Contains prompt instructions, criteria mappings, score levels, and conservative
probability thresholds for all Jev System One semantic evaluations.

Calibration Note:
Thresholds defined here are set conservatively. As Jev is actively evolving,
these thresholds should be periodically calibrated against hand-labeled session transcripts.
"""

from typing import Dict, List

# Conservative decision thresholds (0.0 to 1.0)
# Calibrate against hand-labeled transcripts for optimal recall vs precision.
FRICTION_PUSHBACK_THRESHOLD = 0.65
FRICTION_STEALTH_ERROR_THRESHOLD = 0.70
FRICTION_REDUNDANCY_THRESHOLD = 0.75

DORMANT_SKILL_TRIGGER_THRESHOLD = 0.60

LEDGER_DEDUP_THRESHOLD = 0.75
LEDGER_SEARCH_SHORTLIST_MAX = 8

# Tool pruning threshold: tool calls with usefulness probability below this value
# are marked as safe to prune from context.
PRUNE_USEFUL_THRESHOLD = 0.35

# Fixed ledger categories specified by anti_patterns_ledger.md
FIXED_CATEGORIES: Dict[str, str] = {
    "Token Waste": "Unnecessary token consumption, redundant operations, or prompt cache invalidations.",
    "Buggy Code": "Code syntax errors, logic flaws, unchecked generation, or script collisions.",
    "Tool Loop": "Repetitive tool execution loops, retry churn, or failing command sequences.",
    "Context Bloat": "Excessive context usage, bloated memory files, or oversized system instructions.",
    "Dead Skill": "Unused monolithic skills, inactive components, or missing skill triggers.",
}

# Task 1: Friction & Stealth Failure Questions
FRICTION_QUESTIONS = {
    "user_pushback": (
        "Did the user's message correct, reject, or push back on the assistant's previous response?"
    ),
    "stealth_error": (
        "Does the tool call result indicate a real failure, empty or meaningless response, "
        "permission denial, or crash, even though the status was not explicitly reported as ERROR?"
    ),
    "redundant_tool": (
        "Was this tool call redundant given the prior tool calls in this session (e.g. retrieving "
        "the exact same information or repeating an already executed command)?"
    ),
}

# Task 2: Dormant Skill Question Template
def get_dormant_skill_instruction(skill_name: str, skill_description: str) -> str:
    return (
        f"Based on the work and user requests in this session, did the tasks fall under the "
        f"domain of the skill '{skill_name}'? Skill description: {skill_description}"
    )

# Task 3: Ledger Classification & Dedup
CATEGORIZE_INSTRUCTION = (
    "Which of the five standard anti-pattern categories best classifies this mistake, failure mode, and root cause?"
)

def get_dedup_instruction(existing_title: str, existing_failure: str, existing_cause: str) -> str:
    return (
        f"Is this new failure substantively the same mistake as documented entry '{existing_title}'? "
        f"Existing failure description: {existing_failure}. Existing root cause: {existing_cause}."
    )

# Task 3: Ledger Search Relevance Score
LEDGER_SEARCH_LEVELS: List[str] = [
    "Irrelevant: This entry does not apply to the task or query.",
    "Partially relevant: Touches a related subject, tool, or general potential pitfall.",
    "Directly relevant: The task directly risks encountering or repeating this specific documented mistake.",
]

def get_ledger_search_instruction(entry_id: str, title: str, rule: str) -> str:
    return (
        f"How relevant is the prevention rule in entry {entry_id} ('{title}') to preventing mistakes "
        f"in the given task? Strict rule: {rule}"
    )

# Task 6: Session Pruning Question Template
def get_prune_useful_instruction(tool_name: str, step_index: int) -> str:
    return (
        f"Was the result of tool call #{step_index} ('{tool_name}') actually used, cited, "
        f"or directly relevant to producing the final solution and response?"
    )
