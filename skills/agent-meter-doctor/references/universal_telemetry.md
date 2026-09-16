# Universal AI Agent Telemetry and Observability Guide

This guide establishes how to observe, measure, and optimize token efficiency, code quality, and skill health across all major AI coding agents: Claude Code, Google Antigravity, Cursor IDE, Windsurf Cascade, Roo Code, Aider, OpenAI Codex, Hermes Agent, and any unlisted or custom AI agent.

## Cross Agent Telemetry Matrix

| Agent Platform | Primary Telemetry Store | Context and Token Meter | Friction and Error Signal | Dead Skill Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Claude Code** | `~/.claude/usage-data/`, session history | `/context`, `/usage`, prompt cache line | `likely cause: tool definitions changed`, failed test loops | `/skill-doctor` dormant skill scan |
| **Google Antigravity** | `transcript.jsonl` and full logs | Step metrics, thoughts vs content tokens | `status: ERROR` in tool steps, repeated rollbacks | Loaded skill paths vs tool invocations |
| **Cursor IDE** | Dashboard Usage and Admin Events API | Context bar (200k window), event tokens | Linter red squiggles, repeated composer retries | Dormant `.cursor/rules` files |
| **Windsurf (Cascade)** | Cascade chat history and AI gateway logs | Quota meter, Terse CLI token plugin | Failed terminal commands, repetitive edits | Outdated `.windsurfrules` blocks |
| **Roo Code (Cline)** | `~/.roo/usage-tracking.json` | AI Inference Summary card, cache read/write | Checkpoint rollbacks, rejected tool executions | Mode definitions and heavy custom prompts |
| **Aider** | `.aider.chat.history.md` | `/tokens` command, repo map token counter | Test and lint failures reported by `/test` | Inactive system prompt templates |
| **OpenAI Codex** | Execution logs, Codex CLI and Copilot logs | Token breakdown, completion usage stats | API parse failures, tool call rejection codes | Unused function definitions and schema bloat |
| **Hermes Agent** | `~/.hermes/logs/` (`errors.log`, `agent.log`) | SQLite `state.db` token analytics | Reflexion tracebacks, failing spans in logs | `hermes doctor` dormant skill scan |
| **Unlisted Agents** | Stdout, stderr, or HTTP request headers | Character estimation (4 chars per token) | Non zero exit codes, traceback pattern matches | Injected prompt tools vs actual calls |

## Claude Code Telemetry and Error Signals

### Visibility Channels
* Terminal Command Suite: Direct execution of `/context`, `/context all`, `/usage`, `/skill-doctor`, and `/insights`.
* Persistent Session Data: Stored locally in `~/.claude/usage-data/` with HTML reports at `~/.claude/usage-data/report.html`.
* Prompt Cache Analytics: Real time line tracking request count, hit share, miss count, and active cache TTL.

### Concrete Error Signals to Watch
* Tool Definition Invalidation: The prompt cache line displays `likely cause: tool definitions changed`, indicating a mid session tool or plugin toggle that destroyed prompt cache reuse.
* Memory Bloat Warning: `/context` alerts that `CLAUDE.md` exceeds 200 lines or consumes over 15% of active memory.
* High Attribution Skew: `/usage` attribution reporting that an uninvoked MCP server or plugin accounts for more than 10% of total spend.
* Repetitive Prompt Friction: `/insights` HTML report flagging tasks where the user repeated instructions or where code failed tests multiple times.
* Idle Loop Drains: Background cron or scheduled tasks appearing under the Loops breakdown in `/usage`, resending full context while idle.

### Remediation Protocol
* Lock tool definitions and MCP connections at session inception; never modify them mid stream.
* Run `/compact` with focus criteria or execute `/clear` between unrelated engineering initiatives.
* Trim `CLAUDE.md` to under 200 lines and extract procedures into modular skills.

## Google Antigravity Telemetry and Error Signals

### Log Structure and Location
All session operations are recorded in JSON Lines format inside the conversation transcript:
```text
<appDataDir>\brain\<conversation-id>\.system_generated\logs\transcript.jsonl
```

### Diagnostic Telemetry Fields
* `step_index`: Sequential integer indicating turn depth.
* `source`: `USER_INPUT`, `MODEL`, or `SYSTEM`.
* `type`: Action type such as `USER_INPUT` or `PLANNER_RESPONSE`.
* `status`: Execution state (`DONE` or `ERROR`).
* `thinking`: Model internal chain of thought tokens. Excessive thinking length flags need for effort calibration.
* `tool_calls`: Array containing invoked tool names, arguments, and return codes.

### Concrete Error Signals to Watch
* Tool Execution Failures: `status: ERROR` on file write, replacement, or terminal commands.
* Runaway Thinking: Steps where `thinking` token count exceeds 60% of total response tokens on simple tasks.
* Unbounded Loop Multipliers: Background tasks or subagents lingering in active state without yielding results.
* Broken Diff Rejections: String replacement errors due to non unique or unmatched target code chunks.

### Remediation Protocol
* Check `transcript.jsonl` regularly with `scripts/audit_session.py`.
* Ensure subagents terminate immediately upon delivering outputs.
* Enforce surgical file diffs to prevent pattern mismatch errors.

## Cursor IDE Telemetry and Error Signals

### Visibility Channels
* Dashboard Usage Panel: Tracks token consumption across fast and slow models.
* Admin Events API: Provides enterprise grade event logs with granular input, output, and cache metrics.
* Codebase Index: `@Codebase` scans can inadvertently pull massive build directories if exclusions are missing.

### Concrete Error Signals to Watch
* Terminal Linter Feedback: Repeated compiler or linter errors surfacing after composer emissions.
* Context Saturation Warning: Context bar reaching orange or red threshold (approaching 200k limit).
* Hallucinated Import Failures: Imports referencing nonexistent modules or deprecated methods.
* Redundant Composer Retries: Multiple edits touching identical code blocks across consecutive prompts.

### Remediation Protocol
* Exclude large build folders (`dist`, `node_modules`, `target`, `.git`) in `.cursorignore`.
* Modularize `.cursor/rules` into specific file matching rules rather than maintaining a monolithic `.cursorrules` file.
* Pay attention to compiler warnings in terminal runs to catch agent hallucinations before code merges.

## Windsurf Cascade Telemetry and Error Signals

### State and Memory Layers
* Cascade stores memories and scratchpads inside `.codeium/windsurf/cascade/` and global storage.
* Conversation turns send complete open file context and RAG retrieved blocks.

### Concrete Error Signals to Watch
* Terminal Command Rejections: Command errors caused by non zero exit codes or unrecognized syntax.
* Stale Context Injections: Inactive editor tabs silently sending thousands of tokens into prompt context.
* Cascade Loop Warnings: Agent attempting circular file edits without reaching resolution.
* Quota Depletion Spikes: Rapid credit burn caused by sending full file trees on small edits.

### Remediation Protocol
* Close inactive editor tabs to prevent open buffer context injection on every prompt.
* Integrate with AI Gateway observability proxies (such as LiteLLM or Portkey) to obtain exact per task token attribution.
* Review Cascade memory periodically to prune outdated workspace assumptions.

## Roo Code (Cline) Telemetry and Error Signals

### Visibility Channels
* AI Inference Summary Card: Surfaces total cost, token volume, and mode specific spend (Code, Architect, Ask, Debug).
* Persistent Storage: Tracks historical metrics in `~/.roo/usage-tracking.json`.

### Concrete Error Signals to Watch
* Checkpoint Rollbacks: Frequent user rollbacks signaling rejected or broken implementations.
* Permission Rejections: Denied bash executions or declined file modifications.
* Context Exhaustion Alerts: Context window warnings indicating model attention degradation.
* API Parameter Errors: Tool calling errors caused by missing required schema arguments.

### Remediation Protocol
* Enable prompt caching across supported providers to reuse system instructions.
* Configure custom modes to only include tools necessary for the specific role.
* Utilize checkpoints to rollback failed code explorations without polluting conversation context.

## Aider Telemetry and Error Signals

### Visibility Channels
* Interactive Token Commands: Execute `/tokens` to view prompt, history, and repo map token allocation.
* History Stores: Full conversational logs persisted in `.aider.chat.history.md`.

### Concrete Error Signals to Watch
* Test Execution Failures: Non zero exit codes during automated `/test` runs.
* Linter Feedback Loops: Syntax or formatting violations detected during `/lint` verification.
* Edit Block Rejections: Failed unified diff applications due to fuzzy line matching.
* Repo Map Bloat: Map size exceeding allocated token budget, starving context for edits.

### Remediation Protocol
* Keep repo map token limits configured according to repository size.
* Enforce `/test` and `/lint` execution before accepting proposed edits.
* Compact chat history using `/clear` or `/tokens` whenever switching subtasks.

## OpenAI Codex and Copilot Telemetry and Error Signals

### Visibility Channels
* Completion Usage Metadata: Input tokens, completion tokens, and cached prompt tokens returned in API headers.
* Copilot Agent Diagnostics: Local execution logs in IDE output channels and CLI traces.
* Schema Registry: Tool call definitions sent on every API completion request.

### Concrete Error Signals to Watch
* Tool Schema Parsing Errors: Model outputting malformed JSON arguments for tool calls.
* Silent Hallucinations: Generating non existent parameters or inventing deprecated APIs.
* Uncached Turn Penalties: Complete context re-tokenization caused by inconsistent system prompt formatting.
* Repetitive Code Infilling: Infinite loops or code duplication during multi line inline completions.

### Remediation Protocol
* Enforce strict JSON Schema validation on all tool specifications to eliminate argument parse failures.
* Maintain static system prompt prefixes so OpenAI automatic prompt caching hits at maximum rate.
* Use surgical file replacements rather than wholesale file regenerations.

## Hermes Agent Telemetry and Error Signals

### Layered Memory Model
* Hot Prompt Memory: `~/.hermes/memories/MEMORY.md` and `USER.md` injected into system prompts.
* Cold Archive: SQLite `state.db` preserving full historical sessions.
* Procedural Skills: Reusable `SKILL.md` documents synthesized from completed tasks.
* Reflective Phase: `hermes reflect` inspects performance, extracts learnings, and logs errors into `~/.hermes/logs/errors.log`.

### Concrete Error Signals to Watch
* Traceback Spans in `errors.log`: Unhandled exceptions during tool execution.
* Reflection Stalls: Errors during memory synthesis or failure to distill procedural rules.
* Tool Gateway Disconnects: Gateway timeout errors recorded in `gateway.log`.
* Outdated Memory Conflicts: Inconsistencies between `MEMORY.md` rules and current codebases.

### Synthesis with Agent Meter Doctor
* Agent Meter Doctor adapts Hermes episodic memory by maintaining `anti_patterns_ledger.md`.
* Every agent executes a post turn reflection step mirroring the Hermes reflective phase.

## Universal Fallback Protocol for Unlisted and Custom AI Agents

If an agent is not explicitly enumerated above (for instance: Devin, OpenHands, SWE agent, Goose, AutoGPT, custom enterprise agents, or local Ollama instances), Agent Meter Doctor operates through three universal primitives:

### 1. Zero Dependency Diagnostic Sniffing
* Standard Stream Auditing: Inspect stdout, stderr, and terminal exit codes. Any exit code other than 0 signals friction.
* Regex Error Capture: Scan agent outputs for universal error signatures: `Traceback (most recent call last)`, `SyntaxError`, `TypeError`, `UnhandledPromiseRejection`, `Build failed`, `Fatal error`.
* Context Estimation: In the absence of API token headers, calculate context volume using the universal formula: Total Characters divided by 4 equals estimated tokens.

### 2. Autonomous Model Centric Reflection
The post turn reflection loop operates purely within the model cognitive reasoning space:
* Regardless of the host interface or runtime, any LLM can perform the four point self check after completing a turn:
  1. Did I answer concisely without token bloat?
  2. Did my code pass verification or did commands fail?
  3. Were all tools I loaded actively utilized?
  4. Did I avoid making unverified assumptions?
* If any check fails, the unlisted agent extracts the failure mode and updates the shared memory ledger.

### 3. File System Memory Interoperability
* `memory/anti_patterns_ledger.md` is standard Markdown, and `scripts/reflect_and_learn.py` is standard library Python.
* Any AI agent equipped with basic file reading and writing tools or terminal execution can read the ledger before planning, and append new anti patterns upon discovering bugs.
* This ensures that unlisted, emerging, or bespoke agents gain the full benefit of historical error prevention and token waste elimination immediately upon deployment.
