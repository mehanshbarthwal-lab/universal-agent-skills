"""
jev_service.py - TypeSafe AI Jev Integration Service

Thin wrapper around the typesafe-sdk providing:
- Safe environment initialization and graceful fallback when TYPESAFE_API_KEY is unset
- State redaction and context trimming to avoid context rot and credential leakage
- Batched parallel question execution (System One)
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import dotenv
    # Find .env in project root (two levels up from scripts/ or current dir)
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / ".env"
    if env_file.exists():
        dotenv.load_dotenv(env_file)
    else:
        dotenv.load_dotenv()
except Exception:
    pass

try:
    from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
    TYPESAFE_SDK_AVAILABLE = True
except ImportError:
    TYPESAFE_SDK_AVAILABLE = False

from jev_definitions import (
    CATEGORIZE_INSTRUCTION,
    LEDGER_DEDUP_THRESHOLD,
    DORMANT_SKILL_TRIGGER_THRESHOLD,
    FIXED_CATEGORIES,
    FRICTION_PUSHBACK_THRESHOLD,
    FRICTION_QUESTIONS,
    FRICTION_REDUNDANCY_THRESHOLD,
    FRICTION_STEALTH_ERROR_THRESHOLD,
    LEDGER_SEARCH_LEVELS,
    PRUNE_USEFUL_THRESHOLD,
    get_dedup_instruction,
    get_dormant_skill_instruction,
    get_ledger_search_instruction,
    get_prune_useful_instruction,
)

# Secrets redaction patterns
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|auth|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{8,})['\"]?"),
    re.compile(r"(ghp|gho|ghu|ghs|ghr|glpat|sk-[a-zA-Z0-9]{20,})"),
    re.compile(r"-----BEGIN [A-Z ]+ PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+ PRIVATE KEY-----"),
]

def sanitize_state_text(text: Any, max_length: int = 600) -> str:
    """Trim and redact sensitive tokens from state text."""
    if not text:
        return ""
    s = str(text)
    # Redact key-value secrets
    s = SECRET_PATTERNS[0].sub(r"\1: [REDACTED]", s)
    # Redact raw tokens
    s = SECRET_PATTERNS[1].sub(r"[REDACTED_TOKEN]", s)
    # Redact private keys
    s = SECRET_PATTERNS[2].sub(r"[REDACTED_PRIVATE_KEY]", s)
    s = s.strip()
    if len(s) > max_length:
        return s[:max_length] + " [TRUNCATED]"
    return s

class JevService:
    """Service wrapping TypeSafe Jev API calls with automatic pre-Jev fallback."""

    def __init__(self, api_key: Optional[str] = None, timeout: float = 30.0):
        self.api_key = api_key or os.environ.get("TYPESAFE_API_KEY")
        self.timeout = timeout
        self._client: Optional[Any] = None

    def is_available(self) -> bool:
        """Return True if typesafe-sdk is installed and API key is set."""
        return bool(TYPESAFE_SDK_AVAILABLE and self.api_key and self.api_key.strip())

    def _get_client(self) -> Optional[Any]:
        if not self.is_available():
            return None
        if self._client is None:
            try:
                self._client = TypeSafeClient(api_key=self.api_key, timeout=self.timeout)
            except Exception:
                return None
        return self._client

    def check_friction(
        self,
        previous_assistant_response: str,
        user_message: str,
        prior_tools_summary: str,
        current_tool_name: str,
        current_tool_input: str,
        current_tool_output: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Batch 3 Noul questions for a single conversational turn:
        1. User pushback / correction
        2. Stealth tool error
        3. Redundant tool call
        """
        client = self._get_client()
        if not client:
            return None

        state = {
            "previous_assistant_response": sanitize_state_text(previous_assistant_response, 500),
            "user_message": sanitize_state_text(user_message, 500),
            "prior_tools_called": sanitize_state_text(prior_tools_summary, 400),
            "current_tool_name": current_tool_name,
            "current_tool_args": sanitize_state_text(current_tool_input, 300),
            "current_tool_output": sanitize_state_text(current_tool_output, 500),
        }

        questions = {
            "user_pushback": Noul(instructions=FRICTION_QUESTIONS["user_pushback"]),
            "stealth_error": Noul(instructions=FRICTION_QUESTIONS["stealth_error"]),
            "redundant_tool": Noul(instructions=FRICTION_QUESTIONS["redundant_tool"]),
        }

        try:
            response = client.system_one(state=state, questions=questions)
            pushback_p = response.nouls["user_pushback"].noul
            stealth_p = response.nouls["stealth_error"].noul
            redundant_p = response.nouls["redundant_tool"].noul

            return {
                "user_pushback_prob": round(pushback_p, 3),
                "is_pushback": pushback_p >= FRICTION_PUSHBACK_THRESHOLD,
                "stealth_error_prob": round(stealth_p, 3),
                "is_stealth_error": stealth_p >= FRICTION_STEALTH_ERROR_THRESHOLD,
                "redundant_tool_prob": round(redundant_p, 3),
                "is_redundant": redundant_p >= FRICTION_REDUNDANCY_THRESHOLD,
                "friction_warranted": (
                    pushback_p >= FRICTION_PUSHBACK_THRESHOLD
                    or stealth_p >= FRICTION_STEALTH_ERROR_THRESHOLD
                    or redundant_p >= FRICTION_REDUNDANCY_THRESHOLD
                ),
            }
        except Exception as e:
            return None

    def check_dormant_skills(
        self,
        session_summary: str,
        candidate_skills: List[Dict[str, str]],
    ) -> Optional[Dict[str, Any]]:
        """
        Batch 1 Noul question per candidate dormant skill against session summary.
        Separates skills that were rightly idle from skills that should have triggered.
        """
        client = self._get_client()
        if not client or not candidate_skills:
            return None

        state = {
            "session_summary": sanitize_state_text(session_summary, 1200),
        }

        questions = {}
        for skill in candidate_skills:
            s_name = skill["name"]
            s_desc = skill.get("description", "")
            questions[f"skill::{s_name}"] = Noul(
                instructions=get_dormant_skill_instruction(s_name, s_desc)
            )

        try:
            response = client.system_one(state=state, questions=questions)
            missed_skills = []
            rightly_idle_skills = []

            for skill in candidate_skills:
                s_name = skill["name"]
                key = f"skill::{s_name}"
                p = response.nouls[key].noul if key in response.nouls else 0.0
                info = {
                    "name": s_name,
                    "probability": round(p, 3),
                    "description": skill.get("description", ""),
                }
                if p >= DORMANT_SKILL_TRIGGER_THRESHOLD:
                    missed_skills.append(info)
                else:
                    rightly_idle_skills.append(info)

            # Sort missed skills by descending probability
            missed_skills.sort(key=lambda x: x["probability"], reverse=True)
            rightly_idle_skills.sort(key=lambda x: x["probability"])

            return {
                "missed_skills": missed_skills,
                "rightly_idle_skills": rightly_idle_skills,
            }
        except Exception:
            return None

    def score_ledger_entries(
        self,
        query: str,
        shortlist: List[Dict[str, Any]],
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Batch 1 Score question per candidate entry against the user's task or query.
        Returns candidates ordered by score.
        """
        client = self._get_client()
        if not client or not shortlist:
            return None

        state = {
            "user_task_or_query": sanitize_state_text(query, 600),
        }

        questions = {}
        for entry in shortlist:
            eid = entry["id"]
            questions[f"relevance::{eid}"] = Score(
                instructions=get_ledger_search_instruction(
                    eid, entry.get("title", ""), entry.get("rule", "")
                ),
                criteria=LEDGER_SEARCH_LEVELS,
            )

        try:
            response = client.system_one(state=state, questions=questions)
            scored_entries = []
            for entry in shortlist:
                eid = entry["id"]
                key = f"relevance::{eid}"
                if key in response.scores:
                    s_val = response.scores[key].score
                    e_copy = dict(entry)
                    e_copy["jev_relevance_score"] = round(s_val, 2)
                    scored_entries.append(e_copy)
                else:
                    scored_entries.append(dict(entry))

            scored_entries.sort(
                key=lambda x: x.get("jev_relevance_score", 0.0), reverse=True
            )
            return scored_entries
        except Exception:
            return None

    def classify_and_dedup_entry(
        self,
        title: str,
        failure: str,
        cause: str,
        rule: str,
        existing_entries: List[Dict[str, str]],
    ) -> Optional[Dict[str, Any]]:
        """
        Batch:
        1. Choice question for the 5 fixed categories
        2. Noul question for each existing entry testing for semantic duplicates
        """
        client = self._get_client()
        if not client:
            return None

        state = {
            "new_title": sanitize_state_text(title, 200),
            "new_failure_mode": sanitize_state_text(failure, 500),
            "new_root_cause": sanitize_state_text(cause, 500),
            "new_prevention_rule": sanitize_state_text(rule, 500),
        }

        questions = {
            "category": Choice(
                instructions=CATEGORIZE_INSTRUCTION,
                criteria=FIXED_CATEGORIES,
            )
        }

        for entry in existing_entries:
            eid = entry["id"]
            questions[f"dedup::{eid}"] = Noul(
                instructions=get_dedup_instruction(
                    entry.get("title", ""),
                    entry.get("failure", ""),
                    entry.get("cause", ""),
                )
            )

        try:
            response = client.system_one(state=state, questions=questions)
            chosen_category = response.choices["category"].choice
            duplicates = []

            for entry in existing_entries:
                eid = entry["id"]
                key = f"dedup::{eid}"
                if key in response.nouls:
                    p = response.nouls[key].noul
                    if p >= LEDGER_DEDUP_THRESHOLD:
                        duplicates.append({
                            "id": eid,
                            "title": entry.get("title", ""),
                            "similarity_prob": round(p, 3),
                        })

            duplicates.sort(key=lambda x: x["similarity_prob"], reverse=True)

            return {
                "classified_category": chosen_category,
                "is_duplicate": len(duplicates) > 0,
                "duplicate_matches": duplicates,
            }
        except Exception:
            return None

    def evaluate_tool_calls_for_pruning(
        self,
        session_goal: str,
        final_response: str,
        tool_calls: List[Dict[str, Any]],
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Batch 1 Noul question per tool call:
        'Was this tool call's result actually used or relevant to producing the final response?'
        """
        client = self._get_client()
        if not client or not tool_calls:
            return None

        # Build compact state
        state = {
            "session_user_goal": sanitize_state_text(session_goal, 600),
            "final_assistant_solution": sanitize_state_text(final_response, 1000),
            "tool_calls_manifest": [
                {
                    "index": tc.get("step_index", i + 1),
                    "name": tc.get("name", "unnamed_tool"),
                    "summary_args": sanitize_state_text(tc.get("args", ""), 200),
                    "summary_output": sanitize_state_text(tc.get("output", ""), 250),
                }
                for i, tc in enumerate(tool_calls)
            ],
        }

        questions = {}
        for i, tc in enumerate(tool_calls):
            step_idx = tc.get("step_index", i + 1)
            t_name = tc.get("name", "unnamed_tool")
            questions[f"call_{step_idx}"] = Noul(
                instructions=get_prune_useful_instruction(t_name, step_idx)
            )

        try:
            response = client.system_one(state=state, questions=questions)
            results = []

            for i, tc in enumerate(tool_calls):
                step_idx = tc.get("step_index", i + 1)
                key = f"call_{step_idx}"
                prob = response.nouls[key].noul if key in response.nouls else 1.0
                prune_safe = prob < PRUNE_USEFUL_THRESHOLD

                results.append({
                    "step_index": step_idx,
                    "name": tc.get("name", "unnamed_tool"),
                    "usefulness_prob": round(prob, 3),
                    "safe_to_prune": prune_safe,
                    "raw_length": tc.get("raw_length", 0),
                })

            return results
        except Exception:
            return None
