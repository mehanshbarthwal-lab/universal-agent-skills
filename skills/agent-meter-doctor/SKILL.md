---
name: agent-meter-doctor
description: "Universal AI Agent Telemetry, Token Waste Auditing, Buggy Code Diagnostics, and Autonomous Self Improvement Loop. Bridges Claude Code four meters (/context, /usage, /skill-doctor, /insights) with universal telemetry across all AI agents (Antigravity, Cursor, Windsurf, Roo Code, Aider, Hermes). Enforces an automatic post turn reflection loop after every prompt to identify token waste, code defects, and unused skill components, recording hard prevention rules into a persistent anti pattern ledger."
---

# Agent Meter Doctor: Universal Telemetry and Self Improvement Engine

A permanent default skill providing deep telemetry, token waste prevention, buggy code friction analysis, dead skill component auditing, and an autonomous post turn learning loop across all AI agents.

## Core Mandates

All AI agents must adhere to the following principles:

1. Autonomous Post Turn Reflection: After generating any response or executing code, silently evaluate whether tokens were wasted, tools failed, or bugs were introduced.
2. Check the Mistake Ledger First: Before writing code or modifying configs, consult the persistent mistake ledger in `memory/anti_patterns_ledger.md` to avoid repeating documented errors.
3. Keep Memory Lean: Restrict system prompts and persistent instruction files to under 200 lines. Move domain procedures into modular skills.
4. Eliminate Dead Components: Audit loaded skills and plugins. Defer loading specialized tools until actively invoked.
5. Zero Dashes in Documentation: Avoid hyphens, en dashes, and em dashes in all documentation, headers, and bullet lists.

## Part 1: The Four Meters Deep Dive (Claude Code)

### Meter 1: Context Meter (`/context`)
* Command: `/context` (or `/context all` to view expanded component breakdown).
* What it reveals: Coloured grid of everything loaded in the active context window: system prompts, tool schemas, memory instructions, loaded skill listings, MCP server definitions, and turn history.
* Optimization indicators: Flags context heavy tool schemas, bloated memory files, and capacity limits.
* Actionable fixes:
  * Keep `CLAUDE.md` under 200 lines. Move workflow specific procedures into modular skills.
  * Disable inactive MCP servers with `/mcp`.
  * Compact long conversation history using `/compact`.
  * Reset context completely between unrelated tasks using `/clear`.

### Meter 2: Usage and Cost Meter (`/usage`)
* Command: `/usage` (alias `/cost`). Toggle timeframes with `d` (24 hours) or `w` (7 days).
* What it reveals:
  * Session Block: Estimated cost, API duration, lines changed, and token counts (input, output, cache read, cache write).
  * Prompt Cache Line: Request count, cache hit ratio, miss count, expected rebuilds, and warmth state with active TTL.
  * Cache Miss Diagnostics: From v2.1.260, reports the likely cause (for example: `likely cause: tool definitions changed`).
  * Plan Usage Breakdown: Attribution percentages across skills, plugins, subagents, and MCP servers; behavior flags for long context or excessive misses; loop costs for scheduled tasks.
* Actionable fixes:
  * Lock tool and plugin configurations at session start. Modifying tools mid session invalidates prompt cache prefixes.
  * Disable heavy MCP servers that account for large attribution slices without active use.
  * Verify scheduled task intervals to stop background context resends while idle.

### Meter 3: Skill Doctor (`/skill-doctor`)
* Command: `/skill-doctor` (shipped in v2.1.261).
* What it reveals: Lists loaded skills that were never invoked during the session and calculates their exact per turn context tax. Flags dormant plugins and identifies configuration file locations.
* Actionable fixes:
  * Deactivate unneeded skills at their source: personal (`~/.claude/skills`), project (`.claude/skills`), or plugins (`/plugin`).
  * Evaluate skills across multiple sessions before removal.
  * Bundle infrequent workflows into togglable plugins rather than permanent global skills.

### Meter 4: Insights and Friction Doctor (`/insights`)
* Command: `/insights`.
* What it reveals: Analyzes up to 200 sessions, outputting an HTML diagnostic report to `~/.claude/usage-data/report.html`. Identifies user tasks, friction points (misunderstood prompts, buggy code loops), and optimization suggestions.
* Actionable fixes:
  * Address friction entries first. Repeated prompts indicate ambiguous requirements; resolve by refining prompts or adding concise instructions to memory.
  * Convert repetitive task patterns into dedicated skills or hooks.

## Part 2: Universal Telemetry for All AI Agents

### Cross Platform Monitoring Architecture

* Claude Code:
  * Audit active memory distribution via `/context` and `/context all`.
  * Track prompt cache hits, miss causes, and attribution breakdown in `/usage`.
  * Prune uninvoked skills with `/skill-doctor` and inspect friction reports via `/insights`.
* Google Antigravity:
  * Inspect `transcript.jsonl` for `status: ERROR` tool steps.
  * Track chain of thought expansion (`thinking` field) versus productive code output.
  * Audit background tasks and subagents to ensure clean termination.
* Cursor IDE:
  * Inspect Dashboard Usage and Admin Events API for token spikes.
  * Exclude large build folders (`dist`, `node_modules`) in `.cursorignore` to prevent `@Codebase` context inflation.
  * Split rules into targeted `.cursor/rules/` rather than a monolithic `.cursorrules`.
* Windsurf (Cascade):
  * Monitor daily quota consumption and review Cascade memory files.
  * Close inactive editor tabs to avoid injecting open buffers into every conversation turn.
* Roo Code (Cline):
  * Monitor the AI Inference Summary card for cost and token distribution.
  * Review `~/.roo/usage-tracking.json` to identify expensive modes.
  * Leverage prompt caching and selective folder exclusions.
* Aider:
  * Run `/tokens` to inspect current chat and repo map token overhead.
  * Run `/test` and `/lint` to catch buggy code before committing.
* OpenAI Codex:
  * Audit completion usage metadata and prompt caching efficiency.
  * Validate JSON Schema tool signatures to eliminate argument parsing failures.
  * Enforce surgical line edits to prevent infinite loop infilling.
* Hermes Agent:
  * Utilize layered memory (`MEMORY.md`, `USER.md`, SQLite `state.db`).
  * Run `hermes reflect` to audit recent sessions and review `errors.log`.
* Unlisted and Custom AI Agents:
  * Audit stdout, stderr, and non zero terminal exit codes for friction.
  * Estimate token volume using the universal heuristic of 4 characters per token.
  * Execute the model centric post turn reflection loop and consult the persistent mistake ledger.

## Part 3: Autonomous Post Turn Reflection Loop

Every agent must execute this lightweight self audit at the conclusion of every turn:

### Reflection Checklist (Silent Execution)
1. Token Spend Check: Was the response concise and surgical? Did I emit unnecessary preamble or duplicate code?
2. Code Quality Check: Did any tool call fail or return an error? Was the code verified against project tests or linters?
3. Tool and Skill Efficiency Check: Did I invoke unnecessary tools? Did I load a monolithic skill when only a small script was required?
4. Assumption Check: Did I make silent guesses on ambiguous requirements instead of clarifying?

### Learning and Ledger Action
* If a bug, failed tool call, cache busting event, or user correction occurred, extract the root cause immediately.
* Record the entry into `F:\Agent Skills\agent-meter-doctor\memory\anti_patterns_ledger.md` using `scripts/reflect_and_learn.py`.
* Ensure that future prompts check this ledger so the mistake is never repeated.

## Part 4: TypeSafe Jev System One Semantic Judgments

TypeSafe AI Jev provides fast System One decisions (Noul probabilities, Choice selection, Score ratings) without generative overhead.

### Capabilities and Usage
1. Semantic Friction Auditing: Run `python scripts/audit_session.py <logfile> --use-jev` to detect user pushbacks, stealth tool errors with non ERROR status, and redundant tool calls.
2. Dormant Skill Classification: Automatically separates skills that were rightly idle from skills that matched the session tasks and should have triggered.
3. Ledger Re ranking and Deduplication: Run `python scripts/reflect_and_learn.py search "<task>"` for semantic relevance scores. When logging new entries, Jev maps failures to the five standard categories and blocks duplicate entries.
4. Session Context Pruning: Run `python scripts/prune_session.py <logfile>` to identify tool calls whose outputs did not contribute to the final response, calculating reclaimable context tokens.
5. Configuration and Fallback: Set `TYPESAFE_API_KEY` in `.env`. When the key is unset, all scripts gracefully fall back to default deterministic heuristics.

## Part 5: Automated Documentation and Telemetry Synchronization

* Periodic Sync: As agent platforms evolve, telemetry formats and CLI meters change.
* Automated Synchronizer: Run `scripts/sync_agent_telemetry.py` or trigger the monthly update script in `F:\Agent Skills\bin\update-skills.ps1`.
* Upstream Tracking: Automatically monitors changelogs and release endpoints for Claude Code, Antigravity, Cursor, Windsurf, Roo Code, Aider, OpenAI Codex, and Hermes Agent.

## Part 6: Cross Skill Integration Matrix

* `SkillOpt`: Feeds recurring entries from `anti_patterns_ledger.md` into the nightly optimization cycle to refine existing skills.
* `karpathy-guidelines`: Enforces surgical diffs and thinking before coding, preventing bug driven token burn.
* `ponytail`: Prevents speculative abstractions and eliminates dead code, keeping context lean.
* `knowledge_base.md`: Consults historical deployment and debugging knowledge before attempting complex fixes.
* `stop-slop`: Removes verbose AI writing patterns from explanations, reducing output token consumption.

## Part 7: References and Attribution

* TypeSafe AI Documentation: Official specifications for Jev System One model, Noul, Choice, and Score primitives (`docs.typesafe.ai`).
* Anthropic Claude Code Documentation: Official specifications for `/context`, `/usage`, `/skill-doctor`, `/insights`, and prompt caching (`code.claude.com/docs/en/costs`, `code.claude.com/docs/en/commands`, `code.claude.com/docs/en/changelog`).
* Implicator (`implicator.ai`): Original industry analysis and breakdown of `/skill-doctor` and the four meters taxonomy (September 2026).

