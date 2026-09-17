# Persistent Mistake and Anti Pattern Ledger

This ledger acts as a permanent procedural memory bank. Every AI agent must consult this file before generating code, altering configurations, or calling tools. When an agent experiences an error, buggy implementation, tool failure, or user correction, it must log the occurrence here to prevent recurrence.

## Entry Structure Standard

Each entry in this ledger adheres to the following specification:

* Identifier: AP followed by sequential three digit integer
* Category: Token Waste, Buggy Code, Tool Loop, Context Bloat, or Dead Skill
* Detected Date: ISO timestamp
* Failure Mode: Concrete description of what went wrong
* Root Cause: Mechanism that induced the error
* Detection Signal: How the agent or meter identified the fault
* Strict Prevention Rule: Absolute command that all agents must obey
* Efficiency Gain: Estimated tokens saved or friction eliminated

## Active Anti Pattern Registry

### Entry AP001: Mid Session Tool and Extension Modification
* Category: Token Waste and Cache Invalidation
* Detected Date: 2026-09-09
* Failure Mode: Enabling an MCP server, loading a new plugin, or altering tool schemas midway through an active multi turn session.
* Root Cause: Modifying the tool definition list invalidates the entire prompt cache prefix, forcing the provider to reprocess all prior conversation context from scratch.
* Detection Signal: Claude Code `/usage` prompt cache line reports `likely cause: tool definitions changed`, accompanied by sudden cache miss spikes.
* Strict Prevention Rule: Initialize all required MCP servers, tools, and plugins at the very beginning of a session. Never toggle or install tools mid session. If tool changes are unavoidable, compact or start a clean session immediately.
* Efficiency Gain: Eliminates full context cache invalidations saving 50,000 to 180,000 input tokens per affected turn.

### Entry AP002: Unchecked File Generation Without Verification
* Category: Buggy Code and Logic Errors
* Detected Date: 2026-09-12
* Failure Mode: Emitting code changes across multiple files without executing syntax checks, build scripts, or unit tests.
* Root Cause: Overconfidence and haste. The agent assumed generated code was correct without confirming against the runtime environment.
* Detection Signal: User prompt friction, immediate compile errors, or subsequent correction turns.
* Strict Prevention Rule: Never claim a coding task is complete without running verification commands. Always execute the project test runner or syntax validator before reporting task completion.
* Efficiency Gain: Eliminates iterative error correction loops saving 15,000 to 45,000 tokens per bug.

### Entry AP003: Monolithic Skill Ingestion and Per Turn Tax
* Category: Dead Skill and Context Bloat
* Detected Date: 2026-09-14
* Failure Mode: Loading massive, multi domain skills into active memory when only a single sub utility is required.
* Root Cause: Failure to decompose complex skills into modular, selectively invoked components.
* Detection Signal: Claude Code `/skill-doctor` flags the skill as uninvoked, showing continuous per turn token penalties.
* Strict Prevention Rule: Skills must use deferred loading. Place specialized sub routines in dedicated references or plugins that only enter context upon explicit command invocation.
* Efficiency Gain: Reduces baseline per turn context consumption by 2,500 to 12,000 tokens across every message turn.

### Entry AP004: Unbounded Memory File Inflation
* Category: Context Bloat
* Detected Date: 2026-09-15
* Failure Mode: Allowing global instructions or memory files to expand beyond 200 lines with redundant or outdated instructions.
* Root Cause: Appending historical logs and project specific scratch notes directly into persistent root instruction files.
* Detection Signal: Claude Code `/context` displays memory blocks exceeding 15% of the total context window.
* Strict Prevention Rule: Keep primary instructions under 200 lines. Move domain specific workflows into dedicated skills and move transient context into graphify reports or scratch files.
* Efficiency Gain: Reclaims 4,000 to 10,000 tokens on every single turn.

### Entry AP005: Uncontrolled Teammate and Subagent Spawning
* Category: Token Waste
* Detected Date: 2026-09-16
* Failure Mode: Spawning full subagent fleets for minor linear tasks that could be resolved in a single step.
* Root Cause: Naive delegation without estimating the 7x context multiplication inherent to multi agent architectures.
* Detection Signal: Extreme token spikes in session usage attribution without proportional code output.
* Strict Prevention Rule: Default to linear execution under lazy senior developer protocols. Only spawn subagents for genuinely parallel, decoupled workstreams. Immediately terminate subagents upon completion.
* Efficiency Gain: Prevents 700% token multipliers on simple maintenance tasks.

### Entry AP006: Silent Speculative Assumptions
* Category: Buggy Code and Prompt Friction
* Detected Date: 2026-09-17
* Failure Mode: Guessing user intent on ambiguous specifications instead of presenting explicit options or stating assumptions.
* Root Cause: Agent hallucinated requirements to avoid pausing execution.
* Detection Signal: User feedback indicating the delivered solution answered the wrong problem.
* Strict Prevention Rule: If a requirement has multiple viable interpretations, state assumptions explicitly or present a structured choice before writing code.
* Efficiency Gain: Avoids complete rewrites saving 30,000 to 100,000 tokens per task.

### Entry AP007: Shell Script Expansion and Log Encoding Collisions
* Category: Buggy Code and Tool Loop
* Detected Date: 2026-09-17
* Failure Mode: Emitting scripts using double quoted here strings that prematurely expand variables into empty strings, or writing logs with default PowerShell encodings causing UTF 16 collisions.
* Root Cause: PowerShell double quoted here strings expand internal variables during file generation, and default Out File produces UTF 16LE while Python appends in UTF 8.
* Detection Signal: Script failure due to blank commands, or file inspection errors reporting invalid byte sequences.
* Strict Prevention Rule: Always use single quoted here strings when generating scripts containing shell variables, and always pass explicit UTF 8 encoding parameters to all file writing commands.
* Efficiency Gain: Prevents broken background tasks and logging corruption saving 15,000 tokens in debugging loops.

