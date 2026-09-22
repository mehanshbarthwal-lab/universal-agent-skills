<div align="center">

# Universal Agent Skills

[![M8ven Verified](https://m8ven.ai/badge/mcp/mehanshbarthwal-lab-universal-agent-skills-1inwyb?variant=verified&v=e4e12e3044c88d440c2817aca1cdbdf7)](https://m8ven.ai/mcp/mehanshbarthwal-lab-universal-agent-skills-1inwyb)

<p><strong>Production AI agent skills and tool protocols across major runtimes</strong></p>

<p>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-success.svg?style=for-the-badge" alt="License MIT" /></a>
  <a href="#skill-catalog"><img src="https://img.shields.io/badge/Suites-35%20Cataloged-blue.svg?style=for-the-badge" alt="Suites 35 Cataloged" /></a>
  <a href="#authorship-and-attribution"><img src="https://img.shields.io/badge/Original%20Works-15-orange.svg?style=for-the-badge" alt="Original Works 15" /></a>
  <a href="#authorship-and-attribution"><img src="https://img.shields.io/badge/Community%20Upstream-18-purple.svg?style=for-the-badge" alt="Community Upstream 18" /></a>
  <a href="https://universal-agent-skills.vercel.app"><img src="https://img.shields.io/badge/Showcase-Live%20Portal-emerald.svg?style=for-the-badge" alt="Live Showcase" /></a>
</p>

<p>
  <a href="https://mehanshlabs.qzz.io/universal-agent-skills"><strong>Live Showcase (Portfolio)</strong></a> &nbsp;&bull;&nbsp;
  <a href="https://universal-agent-skills.vercel.app"><strong>Dedicated Portal</strong></a> &nbsp;&bull;&nbsp;
  <a href="ATTRIBUTIONS.md"><strong>Attribution Matrix</strong></a> &nbsp;&bull;&nbsp;
  <a href="CONTRIBUTING.md"><strong>Contributing Guide</strong></a> &nbsp;&bull;&nbsp;
  <a href="SECURITY.md"><strong>Security</strong></a> &nbsp;&bull;&nbsp;
  <a href="PRIVACY.md"><strong>Privacy Policy</strong></a>
</p>

<br/>

<a href="https://mehanshlabs.qzz.io/universal-agent-skills">
  <img src="assets/showcase-preview.png" alt="Universal Agent Skills Web Showcase" width="94%" style="border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);" />
</a>

<br/>
<br/>

</div>

---

## Overview

Modern language models frequently generate generic conversational filler, speculative code abstractions, and hallucinated library methods. This repository delivers specialized, battle tested skill protocols that enforce senior engineering rigor, verified web intelligence, anti generic design aesthetics, and epistemic calibration.

Every skill follows the Universal Agent Skill specification, ensuring seamless interoperability across:

* Anthropic Claude Code and Claude Desktop
* Cursor IDE
* Google Antigravity and Gemini CLI
* OpenAI ChatGPT Custom GPTs and Codex
* OpenClaw and Windsurf
* Ollama, LangChain, and Local Models

> **Target Audience**: Useful for anyone who wants to empower their AI agents or tools with production capabilities without technical friction, from independent creators to senior software engineers.

---

## Quick Start and Installation

Install any skill into your preferred AI agent environment using the following standard workflows:

| Runtime Environment | Installation Target | Command / Procedure |
| :--- | :--- | :--- |
| **Google Antigravity** | `<skills-directory>/<skill-name>/SKILL.md` | Copy the skill folder into your designated Antigravity skills directory. |
| **Claude Code CLI** | `~/.claude/skills/<skill-name>` | Run `claude skill add https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/<name>` |
| **Cursor IDE** | `.cursor/rules/<skill-name>.mdc` | Copy the SKILL.md content into your project rules directory. |
| **ChatGPT / Custom GPT** | System Prompt or Instructions | Paste the full SKILL.md specification into your prompt configuration. |
| **Direct cURL Download** | Any workspace | `curl -fsSL https://raw.githubusercontent.com/mehanshbarthwal-lab/universal-agent-skills/main/skills/<name>/SKILL.md -o SKILL.md` |

---

## Model Context Protocol Server and Tools

Universal Agent Skills exposes twelve specialized tools through the Model Context Protocol for codebase knowledge graphs, document conversion, and multi network research.

### Installation and Server Execution

To install and run the Model Context Protocol servers locally:

```bash
# Clone the repository
git clone https://github.com/mehanshbarthwal-lab/universal-agent-skills.git
cd universal-agent-skills

# Install dependencies for Python tool servers
pip install -e skills/graphify
pip install -e skills/markitdown/packages/markitdown
pip install -e skills/markitdown/packages/markitdown-mcp
pip install -e skills/agent-reach

# Run Graphify server over standard input and output
python -m graphify.serve path/to/graphify-out/graph.json

# Or run Graphify server over Streamable HTTP transport
python -m graphify.serve path/to/graphify-out/graph.json --transport http --port 8000

# Run MarkItDown server
python -m markitdown_mcp

# Run Agent Reach server
python -m agent_reach.integrations.mcp_server
```

### Twelve Tools Catalog

1. `get_status`: Returns installation status, configuration health, and connectivity readiness across all research channels.
2. `convert_to_markdown`: Converts documents from web, local filesystem, or data URIs into structured Markdown.
3. `query_graph`: Queries the knowledge graph using BFS or DFS traversal and returns structural context.
4. `get_node`: Retrieves full attribute details and relational connections for a specified node label or identifier.
5. `get_neighbors`: Returns all direct neighbors and relational edges for a given node.
6. `get_community`: Retrieves all nodes belonging to a designated community cluster.
7. `god_nodes`: Computes degree centrality ranking to surface the most connected core abstractions.
8. `graph_stats`: Generates summary metrics covering node count, edge count, and community distributions.
9. `shortest_path`: Computes the shortest traversal path connecting two concepts in the knowledge graph.
10. `list_prs`: Lists open pull requests with CI status, review state, and impacted graph communities.
11. `get_pr_impact`: Analyzes blast radius for a given pull request by mapping changed files to graph communities.
12. `triage_prs`: Ranks actionable pull requests by review priority and community conflict merge risk.

### Tool Annotations Specification

Every tool provides explicit boolean annotations matching its operational behavior:

| Tool Name | readOnlyHint | destructiveHint | idempotentHint | openWorldHint | Behavior Rationale |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `get_status` | `true` | `false` | `true` | `false` | Inspects local channel configuration without altering state or making external network requests. |
| `convert_to_markdown` | `true` | `false` | `true` | `true` | In memory conversion from web or local URIs without mutating sources; accesses external HTTP endpoints. |
| `query_graph` | `true` | `false` | `true` | `false` | Traverses local in memory graph structure without mutating graph topology. |
| `get_node` | `true` | `false` | `true` | `false` | Reads node properties from the local knowledge graph without mutating data. |
| `get_neighbors` | `true` | `false` | `true` | `false` | Reads direct neighboring nodes and edges in local graph memory. |
| `get_community` | `true` | `false` | `true` | `false` | Reads node cluster memberships for a community from local graph data. |
| `god_nodes` | `true` | `false` | `true` | `false` | Computes degree centrality ranking of local graph nodes without state mutation. |
| `graph_stats` | `true` | `false` | `true` | `false` | Computes summary metrics across the local graph without write operations. |
| `shortest_path` | `true` | `false` | `true` | `false` | Computes shortest path between two concepts within the local graph. |
| `list_prs` | `true` | `false` | `true` | `true` | Queries pull requests from GitHub and maps impact against local graph. |
| `get_pr_impact` | `true` | `false` | `true` | `true` | Queries pull request diff from GitHub and evaluates affected local graph communities. |
| `triage_prs` | `true` | `false` | `true` | `true` | Queries open pull requests from GitHub and computes priority ranking against local graph communities. |

### Network Access and External Hosts

* **Local Graphify Tools**: `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, and `shortest_path` operate entirely in memory and make zero network calls.
* **Pull Request Tools**: `list_prs`, `get_pr_impact`, and `triage_prs` make read only queries to `api.github.com` or invoke the local `gh` CLI.
* **Document Conversion**: `convert_to_markdown` queries remote HTTP and HTTPS hosts only when the user requests an external web URL. Loopback addresses, private IP ranges, and link local addresses are blocked by default.
* **Research Channels**: `agent-reach` communicates only with the specific host requested during active user searches (such as Reddit, GitHub, Bilibili, YouTube, or V2EX).

### Local Files Read and Written

* **Files Read**: Local graph data files such as `graphify-out/graph.json` or custom project files; local document paths passed to `convert_to_markdown` (sensitive operating system paths such as private keys, shadow files, and credential stores are blocked); local configuration files in standard configuration directories.
* **Files Written**: All twelve tools are marked read only and do not write to or mutate project files. Graphify export routines write files only when explicitly requested through CLI options. Temporary scripts and scratch files are cleaned up immediately.

---

## Credentials and Sensitive Files

Universal Agent Skills adheres to credential isolation and safety principles:

* **Zero Read of Legacy Credentials File**: The repository codebase never reads `~/.config/bird/credentials.env`. That legacy file is written only when a user explicitly runs `agent-reach config twitter-cookies --sync-legacy-twitter` to enable backwards compatibility with third party scripts, created with restrictive `0o600` permissions. The uninstallation routine inspects whether the file exists solely to advise the user to perform manual deletion if desired.
* **Lazy In Memory Evaluation**: All API credentials and authentication tokens are loaded lazily at the exact time their specific feature or upstream query executes. No credentials are read at import or server startup.
* **Strict Privacy and No Logging**: Credentials and tokens are never printed to terminal output, never written to log files, never included in error messages, and never returned in Model Context Protocol tool responses. Credentials transmit exclusively to the intended service endpoint over encrypted TLS connections.

---

## Environment Variables and Configuration

Variables used across the codebase are grouped into provider secrets, user settings, and ambient system detection. You only need to set a key if you actively use the corresponding feature.

### Secrets and Provider Credentials (Group A)

| Variable Name | Feature | Required or Optional | Secret | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `ANTHROPIC_API_KEY` | Graphify, SkillOpt | Optional | Yes | API key for Anthropic Claude models. Only needed for Claude backed extraction or optimization. |
| `OPENAI_API_KEY` | Graphify, SkillOpt | Optional | Yes | API key for OpenAI models. Only needed for OpenAI backed extraction or optimization. |
| `GEMINI_API_KEY` | Graphify, Skills | Optional | Yes | API key for Google Gemini models. |
| `GROQ_API_KEY` | Graphify | Optional | Yes | API key for Groq accelerated inference. |
| `DEEPSEEK_API_KEY` | Graphify | Optional | Yes | API key for DeepSeek models. |
| `AZURE_OPENAI_API_KEY` | Graphify | Optional | Yes | API key for Azure OpenAI endpoints. |
| `GITHUB_TOKEN` | Graphify PR Tools | Optional | Yes | GitHub personal access token for higher API rate limits when triaging pull requests. |
| `TWITTER_AUTH_TOKEN` | Agent Reach | Optional | Yes | Cookie token for Twitter channel searches. Only needed when using Twitter channel. |
| `AUTH_TOKEN` | Agent Reach | Optional | Yes | Alternative cookie token for Twitter channel searches. |
| `CT0` | Agent Reach | Optional | Yes | CSRF token cookie for Twitter channel searches. |
| `BILIBILI_COOKIE` | Agent Reach | Optional | Yes | Authentication cookie for Bilibili video and post searches. |
| `EXA_API_KEY` | Agent Reach | Optional | Yes | API key for Exa search backend. |
| `TAVILY_API_KEY` | Agent Reach | Optional | Yes | API key for Tavily search backend. |
| `JINA_API_KEY` | Agent Reach | Optional | Yes | API key for Jina Reader extraction backend. |
| `FIRECRAWL_API_KEY` | Scraping Architect | Optional | Yes | API key for Firecrawl extraction pipelines. |
| `GRAPHIFY_API_KEY` | Graphify HTTP | Optional | Yes | Bearer token authentication for Graphify Streamable HTTP server mode. |
| `NEO4J_PASSWORD` | Graphify Export | Optional | Yes | Authentication password for Neo4j database synchronization. |
| `FALKORDB_PASSWORD` | Graphify Export | Optional | Yes | Authentication password for FalkorDB graph database export. |

### User Configuration and Feature Flags (Group B)

| Variable Name | Feature | Required or Optional | Secret | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `GRAPHIFY_OUT` | Graphify | Optional | No | Directory path where generated graph.json files are stored. Defaults to `graphify-out`. |
| `GRAPHIFY_MAX_CONTEXTS` | Graphify Server | Optional | No | Maximum number of cached graph contexts in multi project server mode. Defaults to 8. |
| `GRAPHIFY_API_TIMEOUT` | Graphify | Optional | No | Timeout in seconds for upstream LLM graph extraction requests. |
| `GRAPHIFY_FORCE` | Graphify | Optional | No | Set to true to force full reindexing of codebase ignoring incremental cache. |
| `MARKITDOWN_ENABLE_PLUGINS` | MarkItDown | Optional | No | Enables third party plugin converters. Defaults to false. |
| `MARKITDOWN_ALLOW_PRIVATE_NETWORKS` | MarkItDown | Optional | No | Set to true to allow document conversion from local or private IP addresses. Defaults to false. |
| `MARKITDOWN_ALLOW_ALL_FILES` | MarkItDown | Optional | No | Set to true to bypass sensitive operating system path filtering for local file conversions. Defaults to false. |
| `SKILLOPT_JUDGE_MODEL` | SkillOpt | Optional | No | Model identifier used for benchmark scoring. Defaults to Claude 3.5 Sonnet. |
| `SKILLOPT_RUNNER_MODEL` | SkillOpt | Optional | No | Model identifier used for agent task execution during optimization runs. |
| `AGENT_REACH_LANG` | Agent Reach | Optional | No | Preferred language code for summarized search results. |
| `ANTHROPIC_BASE_URL` | Provider Proxy | Optional | No | Custom base URL for Anthropic compatible proxy services. |
| `OPENAI_BASE_URL` | Provider Proxy | Optional | No | Custom base URL for OpenAI compatible proxy services. |
| `OLLAMA_HOST` | Local Inference | Optional | No | Host address and port for local Ollama instances. |

### Ambient System State (Group C)

Variables representing ambient system state (such as `SSH_CONNECTION`, `SSH_CLIENT`, `DISPLAY`, `WAYLAND_DISPLAY`, `PYTEST_CURRENT_TEST`, `NVM_HOME`, `XDG_CONFIG_HOME`, `NO_COLOR`, `CLAUDE_PROJECT_DIR`, `APPDATA`, `HOME`, and `TERM`) are read strictly for environment detection, such as determining terminal color support or user configuration directory locations. These are not user configuration options and are never logged or stored.

---

## Limitations

While Universal Agent Skills implements multi layer security checks, the following operational limitations apply:

* **Network Level Egress**: MarkItDown inspects initial destination URIs and every subsequent HTTP redirect against private, loopback, and link local IP blocks. However, protections implemented at the application layer cannot defend against advanced infrastructure threats such as DNS rebinding attacks where IP resolution shifts between validation and socket connection, or network tunnels bypassing application routing. For zero trust deployments, pair this server with operating system firewall egress filters or network proxies.
* **Local Filesystem Sandboxing**: File URI validation verifies resolved canonical realpaths and blocks recognized sensitive configuration markers and credential paths. Environments requiring strict multi tenant isolation should run Model Context Protocol servers within containerized namespaces or sandboxed virtual machines.

---

## Authorship and Attribution

This repository places high value on open source transparency and honest provenance. Works are categorized into original engineering by Mehansh Barthwal, community upstreams, and methodology inspirations.

### Original Engineering by Mehansh Barthwal

* **Zero Hallucination Coder**: Disciplined Discuss, Map, Decompose, Execute, Verify loop eliminating fabricated APIs. Officially merged into the community repository `alirezarezvani/claude-skills` (Pull Request #870).
* **Universal Scraping Architect**: Multi strategy web extraction framework balancing Firecrawl, Python, and hybrid pipelines with token budgeting and atomic checkpointing.
* **Pain Point Miner**: Consumer problem extraction system capturing real customer complaints from forums and review threads with mechanical deduplication.
* **Loop Until Done**: Autonomous self evaluation loop rewriting drafts until all objective rubric criteria clear.
* **JD to Job**: Career matching engine translating complex job descriptions into targeted operational qualifications.
* **Resume Unrejectable**: Four stage recruitment pipeline simulating ATS parsers, recruiter scanning timing, and executive depth.
* **Locality Delivery Scraper**: End to end scraping playbook for mapping locality food delivery and grocery markets.
* **IPYNB Editor**: Programmatic Jupyter Notebook cell inspection and patching utility preserving JSON schema integrity.
* **Markdown Converter Router**: Dynamic architectural router directing documents across AnyDoc and MarkItDown.
* **Agent Meter Doctor**: Universal agent telemetry, token waste auditing, TypeSafe Jev System One semantic friction diagnostics, dormant skill classification, and session context pruning paired with an autonomous post turn learning loop.
* **Jev Decide**: Sub second typed decision primitive powered by TypeSafe AI Jev model. Offloads binary conditions, categorical selections, and ordered scale ratings to System One decision models, eliminating generative token waste while preserving quantitative confidence scoring.

### Adapted Open Source Projects

* **ArXivist**: Multi agent pipeline translating scientific research papers into executable codebases and Jupyter validation notebooks. Agent skill created by Mehansh Barthwal based on the original repository and concept by qosi org ([qosi-org/arxivist](https://github.com/qosi-org/arxivist)).
* **Humanizer**: Authored by Siqi Chen (MIT License). Cleans machine writing hallmarks using Wikipedia style guides.
* **Stop Slop**: Authored by Hardik Pandya (MIT License). Blocks formulaic transitions and robotic filler during initial generation.
* **Ponytail**: Authored by DietrichGebert (MIT License). Senior developer minimalism suite auditing speculative abstractions.
* **Graphify**: Authored by Safi Shamsi (Apache 2.0 / MIT). Codebase knowledge graph generator producing relational maps and structural reports.
* **GSD Core**: Authored by Open GSD (MIT License). Spec driven autonomous development framework featuring phased execution gates.
* **Agent Reach**: Authored by Agent Eyes (MIT License). Multi platform research CLI and Model Context Protocol server for fifteen networks.
* **Agent Video**: Authored by Bradley Bonanno (MIT License). Media intelligence tool combining yt dlp, FFmpeg, and Whisper.
* **Frontend Slides**: Authored by Zara Zhang (MIT License). Interactive web presentation builder and PowerPoint to HTML slide converter.
* **Ralph**: Authored by snarktank (MIT License). Autonomous PRD conversion and implementation system.
* **SkillOpt**: Developed by Microsoft Corporation (MIT License). Agent self optimization and offline memory consolidation loop.
* **MarkItDown**: Utility by Microsoft Corporation (MIT License). Python library for multi format document extraction.
* **Beautify GitHub Profile**: Authored by Reza Shakeri (MIT License). Publication grade repository README documentation standard with badge templates and visual showcases.

### Methodology Inspirations

* **LLM Council**: Multi persona deliberation methodology inspired by Andrej Karpathy.
* **Karpathy Guidelines**: Four lightweight coding instincts distilled from observations by Andrej Karpathy.
* **Taste Skill**: Modern anti slop frontend design guidelines enforcing typographic contrast.
* **Truth Prompt**: Epistemic calibration protocol separating verified fact from speculative inference.

Refer to [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md) for full license notices, upstream URLs, and maintainer details.

---

## Skill Catalog

<details open>
<summary><strong>1. Autonomous Coding and Software Engineering</strong></summary>

| Skill | Category | Provenance | Description | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Zero Hallucination Coder** | Coding | Original by Mehansh | Enforces verified reasoning before any code is generated | [`skills/zero-hallucination-coder`](skills/zero-hallucination-coder) |
| **Ponytail** | Coding | Adapted Open Source | Senior developer minimalism prioritizing standard libraries and YAGNI | [`skills/ponytail`](skills/ponytail) |
| **IPYNB Editor** | Coding | Original by Mehansh | Programmatic notebook cell manipulation preserving JSON schema integrity | [`skills/ipynb-editor`](skills/ipynb-editor) |
| **OpenHuman** | Coding | External Reference | Context engineering reference for the OpenHuman autonomous desktop agent | [`skills/openhuman`](skills/openhuman) |

</details>

<br/>

<details open>
<summary><strong>2. Web Intelligence, Scraping, and Research</strong></summary>

| Skill | Category | Provenance | Description | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Universal Scraping Architect** | Research | Original by Mehansh | Dynamic scraping strategy router with token budgeting and checkpointing | [`skills/universal-scraping-architect`](skills/universal-scraping-architect) |
| **Pain Point Miner** | Research | Original by Mehansh | Real customer complaint extraction with mechanical deduplication | [`skills/pain-point-miner`](skills/pain-point-miner) |
| **ArXivist** | Research | Adapted (Idea by qosi org) | Translates scientific research papers into runnable code repositories | [`skills/arxivist`](skills/arxivist) |
| **Locality Delivery Scraper** | Research | Original by Mehansh | Methodology playbook for mapping urban food delivery markets | [`skills/locality-delivery-scraper`](skills/locality-delivery-scraper) |
| **Markdown Converter Router** | Research | Original by Mehansh | Intelligent format routing across AnyDoc and MarkItDown | [`skills/markdown-converter`](skills/markdown-converter) |
| **Agent Reach** | Research | Adapted Open Source | Unified research interface and Model Context Protocol across fifteen networks | [`skills/agent-reach`](skills/agent-reach) |
| **Agent Video** | Research | Adapted Open Source | Transforms video recordings into structured frames and aligned transcripts | [`skills/agent-video`](skills/agent-video) |
| **MarkItDown** | Research | Adapted Open Source | Converts PDF, Word, PowerPoint, and Excel files into clean Markdown | [`skills/markitdown`](skills/markitdown) |

</details>

<br/>

<details open>
<summary><strong>3. Writing, Editing, and Anti Slop Protocols</strong></summary>

| Skill | Category | Provenance | Description | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Humanizer** | Writing | Adapted Open Source | Strips robotic hallmarks and promotional padding from machine prose | [`skills/humanizer`](skills/humanizer) |
| **Stop Slop** | Writing | Adapted Open Source | Compact prompt rules that block formulaic filler during initial generation | [`skills/stop-slop`](skills/stop-slop) |
| **AI Watermarks Remover** | Writing | Adapted Open Source | Combines zero width character scrubbing with stylistic rephrasing | [`skills/ai-watermarks-remover`](skills/ai-watermarks-remover) |
| **Truth Prompt** | Writing | Methodology Inspired | Epistemic calibration separating verified fact from speculative inference | [`skills/truth-prompt`](skills/truth-prompt) |

</details>

<br/>

<details open>
<summary><strong>4. Orchestration, Planning, and Autonomous Pipelines</strong></summary>

| Skill | Category | Provenance | Description | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Loop Until Done** | Orchestration | Original by Mehansh | Autonomous self evaluation loop rewriting drafts until rubric bars clear | [`skills/loop-until-done`](skills/loop-until-done) |
| **GSD Core** | Orchestration | Adapted Open Source | Phase based autonomous development with user acceptance gates | [`skills/gsd-core`](skills/gsd-core) |
| **Ralph** | Orchestration | Adapted Open Source | Converts PRDs to structured machine readable task pipelines | [`skills/ralph`](skills/ralph) |
| **SkillOpt** | Orchestration | Adapted Open Source | Continuous skill self optimization and memory consolidation engine | [`skills/skillopt`](skills/skillopt) |
| **LLM Council** | Orchestration | Methodology Inspired | Five persona council peer reviewing architectural decisions and tradeoffs | [`skills/claude-skills-llm-council`](skills/claude-skills-llm-council) |

</details>

<br/>

<details open>
<summary><strong>5. Visual Design and Presentation Engineering</strong></summary>

| Skill | Category | Provenance | Description | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Taste Skill** | Design | Adapted Open Source | Design system rules enforcing anti generic aesthetics and typographic contrast | [`skills/taste-skill`](skills/taste-skill) |
| **Frontend Slides** | Design | Adapted Open Source | Builds animation rich HTML slide decks or converts from PowerPoint | [`skills/frontend-slides`](skills/frontend-slides) |

</details>

<br/>

<details open>
<summary><strong>6. Career Intelligence and Operational Positioning</strong></summary>

| Skill | Category | Provenance | Description | Source |
| :--- | :--- | :--- | :--- | :--- |
| **JD to Job** | Career | Original by Mehansh | Extracts operational role requirements into tailored application materials | [`skills/jd-to-job`](skills/jd-to-job) |
| **Resume Unrejectable** | Career | Original by Mehansh | Four stage evaluation gauntlet reflecting actual hiring pipelines | [`skills/resume-unrejectable`](skills/resume-unrejectable) |
| **Happenstance Referrals** | Career | Internal Reference | Organic referral playbook and connection methodology | [`skills/happenstance-referrals`](skills/happenstance-referrals) |
| **LinkedIn AI Outreach** | Career | Internal Reference | Non promotional executive networking and professional outreach patterns | [`skills/linkedin-ai-outreach`](skills/linkedin-ai-outreach) |

</details>

<br/>

<details open>
<summary><strong>7. Systems Architecture and Knowledge Management</strong></summary>

| Skill | Category | Provenance | Description | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Graphify** | Architecture | Adapted Open Source | Constructs queryable knowledge graphs from codebases and documents | [`skills/graphify`](skills/graphify) |
| **Agent Meter Doctor** | Architecture | Original by Mehansh | Universal agent telemetry, token waste auditing, and post turn reflection loop | [`skills/agent-meter-doctor`](skills/agent-meter-doctor) |
| **Beautify GitHub Profile** | Architecture | Adapted Open Source | Elite repository README documentation standard with badge templates and visual showcase components | [`skills/beautify-github-profile`](skills/beautify-github-profile) |
| **Karpathy Guidelines** | Architecture | Methodology Inspired | Instinctual behavioral rules for disciplined agentic coding | [`skills/karpathy-guidelines`](skills/karpathy-guidelines) |
| **Knowledge Base** | Architecture | Internal Reference | Internal operational runbook and deployment troubleshooting reference | [`skills/knowledge-base`](skills/knowledge-base) |
| **Zapier MCP** | Architecture | Internal Reference | Model Context Protocol integration guidelines for external tools | [`skills/zapier-mcp`](skills/zapier-mcp) |

</details>

---

## Contributing

Contributions, new skill specifications, and bug reports are warmly welcomed. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for full architectural guidelines, prompt engineering criteria, and attribution requirements before opening a pull request.

---

## License

All original skill specifications and documentation authored by Mehansh Barthwal are released under the [MIT License](LICENSE). Upstream tools and adapted suites retain their respective original licenses as documented in [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md).
