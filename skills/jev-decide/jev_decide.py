"""
jev_decide.py: Generic decision primitive backed by TypeSafe AI Jev.

Jev cannot generate text. Given a situation and a set of typed questions, it
returns a decision for each one: a yes/no probability, a pick from a list of
options with a probability per option, or a position on a numbered scale, each
with probabilities attached. It does not write explanations, drafts, or code,
so this module is only ever the "which one / how sure / how bad" step inside a
larger task. Something else, an LLM or a person, still writes what happens
next.

CREDENTIAL HANDLING
    The API key is read from the TYPESAFE_API_KEY environment variable or a local
    .env file at call time. It is never hardcoded into public repositories, never
    written to git tracked files, and never logged. If the variable is unset or
    empty, every public function returns a result with available=False instead of
    raising, so a caller can always fall back to deciding with standard heuristics
    rather than crashing.

WHAT THIS FILE DOES NOT DO
    It does not decide anything by itself. It packages a question, sends it,
    and hands back a typed, structured answer. The calling code or the
    calling agent instructions decide what to do with that answer, per
    thresholds set by the caller.

Usage as a library:
    from jev_decide import ask_yes_no, ask_choice, ask_score, ask_batch

Usage from the command line, one question at a time:
    python jev_decide.py yes_no "Is this invoice suspicious?" --state '{"invoice_total": "$45,000"}'
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

try:
    from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False


DEFAULT_MODEL = "jev-latest"
DEFAULT_TIMEOUT_SECONDS = 15.0

# Jev documented cap on how many named options a single Choice question may carry
MAX_CHOICE_OPTIONS = 255


def _load_env_fallback() -> None:
    """Attempt to discover and load TYPESAFE_API_KEY from known .env files or Windows User env."""
    if os.environ.get("TYPESAFE_API_KEY"):
        return

    # Check Windows User environment variable if available
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
        val, _ = winreg.QueryValueEx(key, "TYPESAFE_API_KEY")
        if val and str(val).strip():
            os.environ["TYPESAFE_API_KEY"] = str(val).strip()
            return
    except Exception:
        pass

    candidate_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent / ".env",
        Path(__file__).resolve().parent.parent / ".env",
    ]
    if "AGENT_SKILLS_DIR" in os.environ:
        candidate_paths.append(Path(os.environ["AGENT_SKILLS_DIR"]) / "jev-decide" / ".env")
        candidate_paths.append(Path(os.environ["AGENT_SKILLS_DIR"]) / "agent-meter-doctor" / ".env")

    for p in candidate_paths:
        if p.exists() and p.is_file():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("TYPESAFE_API_KEY="):
                            val = line.split("=", 1)[1].strip().strip("\"'")
                            if val:
                                os.environ["TYPESAFE_API_KEY"] = val
                                return
            except Exception:
                pass


@dataclass
class JevAnswer:
    """One question result. available is False whenever no live call was
    made (no key, no SDK, or request failed), and callers should treat
    that as "use your fallback", not as a negative or zero answer."""

    available: bool
    kind: str  # "yes_no" | "choice" | "score"
    probability: Optional[float] = None          # yes_no
    choice: Optional[str] = None                 # choice: winning option
    choice_probabilities: Dict[str, float] = field(default_factory=dict)  # choice
    score: Optional[str] = None                  # score: winning level or description
    score_value: Optional[float] = None          # expected numeric score
    confidence: Optional[float] = None           # score confidence
    score_probabilities: Dict[str, float] = field(default_factory=dict)   # score
    error: Optional[str] = None
    input_tokens: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "available": self.available,
            "kind": self.kind,
            "probability": self.probability,
            "choice": self.choice,
            "choice_probabilities": self.choice_probabilities,
            "score": self.score,
            "score_value": self.score_value,
            "confidence": self.confidence,
            "score_probabilities": self.score_probabilities,
            "error": self.error,
            "input_tokens": self.input_tokens,
        }


def _unavailable(kind: str, error: str) -> JevAnswer:
    return JevAnswer(available=False, kind=kind, error=error)


def _get_client(
    model: str = DEFAULT_MODEL, timeout: float = DEFAULT_TIMEOUT_SECONDS
) -> Tuple[Optional[Any], Optional[str]]:
    """Build a client from the environment for this call only. Never caches
    the key anywhere outside this function local variables."""
    if not _SDK_AVAILABLE:
        return None, "typesafe-sdk is not installed (pip install typesafe-sdk)"

    _load_env_fallback()

    api_key = os.environ.get("TYPESAFE_API_KEY", "").strip()
    if not api_key:
        return None, "TYPESAFE_API_KEY is not set in the environment or .env file"

    try:
        client = TypeSafeClient(api_key=api_key, model=model, timeout=timeout)
    except Exception as exc:
        return None, f"failed to construct TypeSafeClient: {exc}"

    return client, None


def is_available() -> bool:
    """True only if the SDK is installed AND a non empty key is currently set."""
    client, _ = _get_client()
    return client is not None


def ask_yes_no(
    question: str,
    state: Optional[Dict[str, Any]] = None,
    model: str = DEFAULT_MODEL,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> JevAnswer:
    """A single Noul question: returns a probability that the answer is yes.

    question must state its exact condition and boundary cases, since Jev
    answers exactly what is written rather than what was implied.
    state is arbitrary JSON serializable context the question can refer to
    by key, e.g. {"invoice_total": "...", "vendor": "..."}.
    """
    client, err = _get_client(model=model, timeout=timeout)
    if client is None:
        return _unavailable("yes_no", err)

    try:
        response = client.system_one(
            state=state or {}, questions={"answer": Noul(instructions=question)}
        )
        answer = response.answers["answer"]
        return JevAnswer(
            available=True,
            kind="yes_no",
            probability=round(answer.noul, 4),
            input_tokens=getattr(response.usage, "input_tokens", None),
        )
    except Exception as exc:
        return _unavailable("yes_no", str(exc))


def ask_choice(
    question: str,
    options: Dict[str, str],
    state: Optional[Dict[str, Any]] = None,
    model: str = DEFAULT_MODEL,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> JevAnswer:
    """A single Choice question: pick one option from options and return
    a probability per option. choice is the highest probability option.
    """
    if not options:
        return _unavailable("choice", "options must be a non empty dict")
    if len(options) > MAX_CHOICE_OPTIONS:
        return _unavailable(
            "choice",
            f"{len(options)} options exceeds Jev {MAX_CHOICE_OPTIONS} option cap "
            "for a single Choice question; split into chunks and rank each, "
            "then run a second Choice over the winners",
        )

    client, err = _get_client(model=model, timeout=timeout)
    if client is None:
        return _unavailable("choice", err)

    try:
        response = client.system_one(
            state=state or {},
            questions={"answer": Choice(instructions=question, criteria=options)},
        )
        answer = response.answers["answer"]
        probs = {k: round(v, 4) for k, v in answer.probabilities.items()}
        return JevAnswer(
            available=True,
            kind="choice",
            choice=answer.choice,
            choice_probabilities=probs,
            input_tokens=getattr(response.usage, "input_tokens", None),
        )
    except Exception as exc:
        return _unavailable("choice", str(exc))


def _normalize_score_levels(
    levels: Union[Dict[str, str], Sequence[str]]
) -> Tuple[List[str], Dict[int, str]]:
    """Normalize score criteria into a Sequence of strings for TypeSafe SDK."""
    if isinstance(levels, dict):
        criteria_list = [f"{k}: {v}" for k, v in levels.items()]
        index_to_label = {i: k for i, k in enumerate(levels.keys())}
    else:
        criteria_list = list(levels)
        index_to_label = {i: item for i, item in enumerate(criteria_list)}
    return criteria_list, index_to_label


def ask_score(
    question: str,
    levels: Union[Dict[str, str], Sequence[str]],
    state: Optional[Dict[str, Any]] = None,
    model: str = DEFAULT_MODEL,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> JevAnswer:
    """A single Score question: place the situation on an ordered scale.
    levels can be a list of criteria strings, or a dict mapping level name to description.
    """
    if not levels:
        return _unavailable("score", "levels must be non empty")

    client, err = _get_client(model=model, timeout=timeout)
    if client is None:
        return _unavailable("score", err)

    criteria_list, index_to_label = _normalize_score_levels(levels)

    try:
        response = client.system_one(
            state=state or {},
            questions={"answer": Score(instructions=question, criteria=criteria_list)},
        )
        answer = response.answers["answer"]
        raw_probs = answer.probabilities
        probs = {}
        for idx, prob in raw_probs.items():
            label = index_to_label.get(int(idx), str(idx))
            probs[label] = round(float(prob), 4)

        # Winning level is the highest probability level
        winning_label = None
        if probs:
            winning_label = max(probs.items(), key=lambda item: item[1])[0]

        return JevAnswer(
            available=True,
            kind="score",
            score=winning_label,
            score_value=round(answer.score, 4) if getattr(answer, "score", None) is not None else None,
            confidence=round(answer.confidence, 4) if getattr(answer, "confidence", None) is not None else None,
            score_probabilities=probs,
            input_tokens=getattr(response.usage, "input_tokens", None),
        )
    except Exception as exc:
        return _unavailable("score", str(exc))


def ask_batch(
    questions: Dict[str, Any],
    state: Optional[Dict[str, Any]] = None,
    model: str = DEFAULT_MODEL,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> Dict[str, JevAnswer]:
    """Send several questions about the same situation in one request."""
    if not questions:
        return {}

    client, err = _get_client(model=model, timeout=timeout)
    if client is None:
        return {name: _unavailable(spec.get("type", "?"), err) for name, spec in questions.items()}

    built: Dict[str, Any] = {}
    kinds: Dict[str, str] = {}
    score_meta: Dict[str, Dict[int, str]] = {}
    broken: Dict[str, JevAnswer] = {}

    for name, spec in questions.items():
        qtype = spec.get("type")
        instructions = spec.get("instructions")
        if not instructions:
            broken[name] = _unavailable(qtype or "?", f"question '{name}' is missing instructions")
            continue
        if qtype == "yes_no":
            built[name] = Noul(instructions=instructions)
            kinds[name] = qtype
        elif qtype == "choice":
            options = spec.get("options") or {}
            if not options:
                broken[name] = _unavailable(qtype, f"question '{name}' (choice) has no options")
                continue
            built[name] = Choice(instructions=instructions, criteria=options)
            kinds[name] = qtype
        elif qtype == "score":
            levels = spec.get("levels") or []
            if not levels:
                broken[name] = _unavailable(qtype, f"question '{name}' (score) has no levels")
                continue
            criteria_list, index_to_label = _normalize_score_levels(levels)
            score_meta[name] = index_to_label
            built[name] = Score(instructions=instructions, criteria=criteria_list)
            kinds[name] = qtype
        else:
            broken[name] = _unavailable(qtype or "?", f"question '{name}' has unknown type '{qtype}'")

    if not built:
        return broken

    try:
        response = client.system_one(state=state or {}, questions=built)
        input_tokens = getattr(response.usage, "input_tokens", None)
        results: Dict[str, JevAnswer] = dict(broken)
        for name, kind in kinds.items():
            answer = response.answers[name]
            if kind == "yes_no":
                results[name] = JevAnswer(
                    available=True, kind="yes_no",
                    probability=round(answer.noul, 4), input_tokens=input_tokens,
                )
            elif kind == "choice":
                results[name] = JevAnswer(
                    available=True, kind="choice", choice=answer.choice,
                    choice_probabilities={k: round(v, 4) for k, v in answer.probabilities.items()},
                    input_tokens=input_tokens,
                )
            elif kind == "score":
                index_to_label = score_meta.get(name, {})
                probs = {}
                for idx, prob in answer.probabilities.items():
                    label = index_to_label.get(int(idx), str(idx))
                    probs[label] = round(float(prob), 4)
                winning_label = max(probs.items(), key=lambda item: item[1])[0] if probs else None
                results[name] = JevAnswer(
                    available=True, kind="score",
                    score=winning_label,
                    score_value=round(answer.score, 4) if getattr(answer, "score", None) is not None else None,
                    confidence=round(answer.confidence, 4) if getattr(answer, "confidence", None) is not None else None,
                    score_probabilities=probs,
                    input_tokens=input_tokens,
                )
        return results
    except Exception as exc:
        results = dict(broken)
        results.update({name: _unavailable(kind, str(exc)) for name, kind in kinds.items()})
        return results


def _cli() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Ask Jev a single typed decision question from the command line."
    )
    parser.add_argument("kind", choices=["yes_no", "choice", "score"])
    parser.add_argument("question", help="The instructions text for the question.")
    parser.add_argument(
        "--state", default="{}",
        help="JSON object of context the question can refer to, e.g. '{\"key\": \"value\"}'",
    )
    parser.add_argument(
        "--options", default=None,
        help="For 'choice': JSON object mapping option name to description.",
    )
    parser.add_argument(
        "--levels", default=None,
        help="For 'score': JSON object or list mapping level to description, ordered low to high.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    try:
        state = json.loads(args.state)
    except json.JSONDecodeError as exc:
        print(json.dumps({"available": False, "error": f"--state is not valid JSON: {exc}"}))
        return 1

    if args.kind == "yes_no":
        result = ask_yes_no(args.question, state=state, model=args.model)
    elif args.kind == "choice":
        if not args.options:
            print(json.dumps({"available": False, "error": "--options is required for 'choice'"}))
            return 1
        result = ask_choice(args.question, json.loads(args.options), state=state, model=args.model)
    else:
        if not args.levels:
            print(json.dumps({"available": False, "error": "--levels is required for 'score'"}))
            return 1
        result = ask_score(args.question, json.loads(args.levels), state=state, model=args.model)

    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.available else 2


if __name__ == "__main__":
    sys.exit(_cli())
