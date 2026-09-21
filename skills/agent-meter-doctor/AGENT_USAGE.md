# Agent Meter Doctor: Operational Agent Guide

This document instructs any local or autonomous AI agent on how to integrate Agent Meter Doctor into its execution workflow.

## Operational Lifecycle for AI Agents

Every AI agent operating in this workspace must follow this execution lifecycle:

### Step 1: Pre Execution Verification
Before executing code, creating files, or modifying configuration:
1. Consult the Anti Pattern Ledger: Check `F:\Agent Skills\agent-meter-doctor\memory\anti_patterns_ledger.md` or execute:
   ```bash
   python "F:\Agent Skills\agent-meter-doctor\scripts\reflect_and_learn.py" search "<topic>"
   ```
2. Verify Constraints: Confirm your planned approach does not violate any documented prevention rule (for example, mid session tool loading or unchecked multi file edits).
3. Think Before Coding: Adhere to `karpathy-guidelines` by stating assumptions and defining done criteria before taking action.

### Step 2: In Session Telemetry Monitoring
During active sessions, observe platform specific meters:
* Claude Code: Run `/context` to inspect memory distribution and `/usage` to review cache efficiency and attribution.
* Antigravity: Ensure tool calls do not trigger cascading `status: ERROR` entries in `transcript.jsonl`.
* Cursor or Windsurf: Verify terminal test execution passes cleanly before completing the turn.

### Step 3: Autonomous Post Turn Reflection
Immediately after emitting an answer or completing a task, execute this mental self audit:
1. Did the task complete with zero tool execution failures?
2. Were all changes minimal, surgical, and verified?
3. Did I avoid sending unnecessary token heavy preamble?
4. Was any loaded skill left completely uninvoked?

### Step 4: Ledger Logging (When Errors Occur)
If you encountered a tool failure, syntax error, hallucinated API, or received a user correction:
1. Isolate the exact failure mode and root cause.
2. Formulate a strict prevention rule.
3. Record the entry into the ledger:
   ```bash
   python "F:\Agent Skills\agent-meter-doctor\scripts\reflect_and_learn.py" log --category "<Category>" --title "<Title>" --failure "<Description>" --cause "<Cause>" --rule "<Prevention Rule>"
   ```

### Step 5: Periodic Telemetry and Skill Audit
* To audit an entire session transcript:
  ```bash
  python "F:\Agent Skills\agent-meter-doctor\scripts\audit_session.py" "<path_to_transcript.jsonl>"
  ```
* To synchronize agent documentation and upstream telemetry definitions:
  ```bash
  python "F:\Agent Skills\agent-meter-doctor\scripts\sync_agent_telemetry.py"
  ```
