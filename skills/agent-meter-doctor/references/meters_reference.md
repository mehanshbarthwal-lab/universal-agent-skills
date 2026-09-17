# Claude Code Four Meters Technical Reference

This document provides the definitive guide to the four native meters within Claude Code: `/context`, `/usage`, `/skill-doctor`, and `/insights`. It covers operational commands, diagnostic interpretations, version requirements, and remediation procedures.

## Version Requirements and Preflight Checks

Run the following command in the terminal to inspect the current version:
```bash
claude --version
```

Exact version constraints:
* Version v2.1.261 or later is required for the full four meter suite.
* Version v2.1.260 introduced the prompt cache likely cause diagnostic line.
* Version v2.1.261 introduced `/skill-doctor` (minimum requirement v2.1.252 engine).
* Update via terminal with `claude update` or by restarting the application.

Plan specific capabilities:
* Plan attribution breakdown in `/usage` (attributing consumption across skills, plugins, and MCP servers) is available on Pro, Max, Team, and Enterprise tiers.
* API key users receive the complete Session block, token telemetry, and the prompt cache diagnostic line.
* The four meters must run inside an active session with real work. A brand new session contains negligible telemetry.
* `/skill-doctor` must be executed inside a local terminal session. It cannot generate reports from mobile or browser Remote Control sessions.

## Meter 1: `/context` (Current Memory Window)

### Purpose
Provides a visual breakdown of everything loaded into the current conversation context window: system prompts, tool schemas, memory files like `CLAUDE.md`, active skill listings, MCP server specifications, and full conversation history.

### Execution Commands
```text
/context
/context all
```
Running `/context` displays a collapsed colored grid. Running `/context all` expands individual component breakdowns.

### Telemetry Interpretation
* Inspect the largest blocks first. Tool definitions and memory instructions are frequent bloat vectors.
* Review optimization alerts printed beneath the grid. Claude Code flags oversized tools, memory file bloat, and context capacity warnings.
* Capacity warnings report exact token overage and specify commands to reclaim context.

### Remediation Protocol
* Instruction files: `CLAUDE.md` loads on every turn. Restrict it to fewer than 200 lines. Move specialized procedures into skills that load only upon invocation.
* Tool schema management: MCP tool definitions are deferred by default, meaning only server names and root instructions enter context until a specific tool is called. If a server remains heavy, execute `/mcp` to disable unused servers.
* Conversation history pruning: When conversation history dominates the grid, run `/compact` with focus instructions (for instance: `/compact keep the test output and file changes`). When pivoting to completely unrelated tasks, run `/clear` to reset context at zero cost.
* Continuous monitoring: Configure the status line to display context window usage continuously.

## Meter 2: `/usage` (Attribution and Token Telemetry)

### Purpose
Monitors token spend, prompt caching efficiency, and cost attribution across models, tools, and scheduled tasks. Alias: `/cost`.

### Execution Commands
```text
/usage
```
Toggle timeframes by pressing `d` for the previous 24 hours or `w` for the previous 7 days.

### Telemetry Interpretation Top to Bottom
* Session Block: Displays list price cost estimates, total API duration, lines of code modified, and model specific breakdown of input, output, cache read, and cache write tokens.
* Prompt Cache Line: Appears following the first API response. Shows total request count, percentage of input tokens served from cache, total cache misses, anticipated rebuilds (triggered by compaction or tool result clearing), and cache warmth state along with active TTL.
* Cache Miss Diagnosis: On version v2.1.260 and later, Claude Code outputs a likely cause diagnosis for misses, such as `likely cause: tool definitions changed`.
* Plan Usage Breakdown:
  * Attribution: Percentage of token spend attributable to specific skills, subagents, plugins, and MCP servers.
  * Behavior Flags: Flags long context sessions or excessive cache misses when either accounts for 10% or more of recent usage.
  * Loops: Displays heaviest running scheduled tasks alongside per run token consumption.

### Remediation Protocol
* Cache lifetime: Cache lifetime is 1 hour on subscription plans and drops to 5 minutes when drawing on usage credits or default API keys. Resuming work after breaks will reprocess context once. On Pro and Max plans, resume large sessions from a summary rather than raw history.
* Mid session tool changes: If `likely cause: tool definitions changed` appears, tools or plugins were modified midway through work. Lock tool configurations at session start.
* Unused heavy integrations: If an MCP server or plugin accounts for substantial attribution without commensurate usage, disable it immediately.
* Scheduled loops: Loops resend full context on every iteration even while idle. Audit schedule intervals and terminate unnecessary background loops.

## Meter 3: `/skill-doctor` (Dead Skill Audit)

### Purpose
Identifies loaded skills that were never invoked during the session and quantifies the per turn token tax incurred simply by keeping their definitions in context. Also flags dormant plugins and indicates exact configuration files for deactivation.

### Execution Commands
```text
/skill-doctor
```

### Telemetry Interpretation
* Lists every uninvoked skill alongside its per turn token tax.
* Pinpoints source locations: personal skills in `~/.claude/skills`, project skills in `.claude/skills`, or installed plugins.

### Remediation Protocol
* `/skill-doctor` performs an audit without modifying files automatically. The engineer or agent decides what to deactivate.
* Disable individual skills at the named source location, or disable entire plugins with `/plugin`.
* Evaluate skills across several sessions before deletion. A skill used weekly should not be deleted based on a single session.
* For rare workflows, bundle skills inside togglable plugins rather than keeping them permanently active in global directories.

## Meter 4: `/insights` (Workflow and Friction Analysis)

### Purpose
Analyzes recent local sessions to produce a comprehensive HTML diagnostic report covering user tasks, friction points (misunderstood prompts, buggy code loops), and optimization suggestions.

### Execution Commands
```text
/insights
```

### Telemetry Interpretation
* Analyzes up to 200 unreviewed sessions per run.
* Generates report at `~/.claude/usage-data/report.html` and saves timestamped archival copies in the same directory. Open this file in any browser.
* Friction Section: Identifies tasks where prompts were repeated, tool calls failed, or buggy code required multiple rollbacks.

### Remediation Protocol
* Address friction entries first. Repeated prompts indicate ambiguous instructions; solve this by creating clear prompts or adding a concise rule to `CLAUDE.md`.
* Frequent task patterns should be converted into dedicated skills or hooks so that instructions load cleanly rather than requiring manual prompting.

## The Universal Five Minute Maintenance Routine

Perform this five step sequence weekly inside an active working session:
1. Run `/context`: Challenge any component larger than the conversation itself.
2. Run `/usage` and press `w`: Audit prompt cache efficiency and attribution percentages.
3. Run `/skill-doctor`: Note uninvoked skills; remove those that remained dormant for consecutive weeks.
4. Run `/insights`: Review friction logs; add targeted prevention rules to instruction files.
5. Run `/clear`: Reset context before commencing new tasks.

## Hidden Multipliers Outside Standard Meters

* Extended Thinking: Billed as output tokens and active by default. Adjust down with `/effort` or `/model` for straightforward tasks.
* Multi Agent Teams: Agent teams consume approximately 7x the tokens of a standard session because every teammate runs an independent context window. Keep agent teams lean and terminate teammates immediately upon task completion.
* Model Tier Selection: Sonnet handles most engineering tasks efficiently; leaving Opus as the default selection is the primary driver of excessive API spend.

## Sources and Attribution

* Anthropic Claude Code Documentation:
  * Official changelog and version history covering v2.1.257 through v2.1.266 (September 2026): `https://code.claude.com/docs/en/changelog`
  * Cost management guide, prompt caching diagnostics, and attribution: `https://code.claude.com/docs/en/costs`
  * Commands reference covering `/context`, `/cost` alias, `/compact`, and `/effort`: `https://code.claude.com/docs/en/commands`
* Implicator (`https://implicator.ai`):
  * Analysis of `/skill-doctor` shipped in v2.1.261 and per turn context tax calculations (September 2026).
  * Synthesis of the Four Meters concept and the five minute weekly maintenance routine.

