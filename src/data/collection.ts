import { rawSkillContents } from "./skillContents";

export type EntryKind = "skill" | "tool" | "writeup" | "workflow";

export type Provenance = "original" | "adapted" | "inspired" | "external" | "internal";

export type Category =
  "Coding" | "Design" | "Research" | "Writing" | "Orchestration" | "Career" | "Architecture";

export type Entry = {
  slug: string;
  name: string;
  kind: EntryKind;
  category: Category;
  tagline: string;
  what: string;
  why: string;
  provenance: Provenance;
  author: string;
  attributionNotes?: string;
  license: string;
  upstreamUrl?: string;
  link: { href: string; label: string } | null;
  whenToUse?: string[];
  whenNotToUse?: string[];
  howToUse?: string;
  compatibility: string[];
  tags: string[];
  files?: number;
  skillMdContent?: string;
  triggerPrompts?: string[];
  installation?: {
    antigravity?: string;
    claudeCode?: string;
    cursor?: string;
    chatgpt?: string;
    curlCommand?: string;
  };
};

export function getSkillInstallation(entry: Entry) {
  if (entry.installation) return entry.installation;
  const rawUrl = `https://raw.githubusercontent.com/mehanshbarthwal-lab/universal-agent-skills/main/skills/${entry.slug}/SKILL.md`;
  return {
    antigravity: `Copy to <skills-directory>/${entry.slug}/SKILL.md`,
    claudeCode: `claude skill add https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/${entry.slug}`,
    cursor: `Save instructions to .cursor/rules/${entry.slug}.mdc`,
    chatgpt: `Paste the full SKILL.md specification into your Custom GPT or Project Instructions.`,
    curlCommand: `curl -fsSL ${rawUrl} -o SKILL.md`,
  };
}

export function getSkillMdContent(entry: Entry) {
  if (rawSkillContents[entry.slug]) return rawSkillContents[entry.slug];
  if (entry.skillMdContent) return entry.skillMdContent;
  return `# ${entry.name} Specification

## Overview
${entry.what}

## Rationale
${entry.why}

## Core Principles
* Always verify environment constraints and dependencies before executing.
* Enforce negative constraints and reject speculative abstractions.
* Validate output against stated acceptance rubrics.

## Execution Workflow
1. Discovery: Map requirements and inspect active context.
2. Decomposition: Break down the task into discrete, verifiable phases.
3. Execution: Implement surgical changes preserving existing code architecture.
4. Verification: Test all criteria before declaring completion.`;
}

export const KIND_LABEL: Record<EntryKind, string> = {
  skill: "Skill",
  tool: "Tool",
  workflow: "Workflow",
  writeup: "Writeup",
};

export const PROVENANCE_LABEL: Record<Provenance, string> = {
  original: "Original by Mehansh",
  adapted: "Adapted Open Source",
  inspired: "Methodology Inspired",
  external: "External Project",
  internal: "Internal Workflow",
};

export const KIND_BLURB: Record<EntryKind, string> = {
  skill:
    "Modular instruction sets that enforce domain discipline, negative constraints, and precise task handling.",
  tool: "Functional utilities, multi agent pipelines, and command line tools with verified execution.",
  workflow:
    "Structured multi stage procedures and evaluation loops that guarantee consistent outcomes.",
  writeup: "Technical reflections on system design, model constraints, and runtime portability.",
};

export const entries: Entry[] = [
  // ---------------------------------------------------------------- ORIGINAL WORKS
  {
    slug: "zero-hallucination-coder",
    name: "Zero Hallucination Coder",
    kind: "skill",
    category: "Coding",
    tagline: "Enforces verified reasoning before any code is generated.",
    what: "Requires the model to complete a five phase sequence (Discuss, Map, Decompose, Execute, Verify) before writing code, inspecting installed dependencies and local source rather than inventing hypothetical APIs.",
    why: "Hallucinated methods and speculative abstractions consume substantial debugging time. Forcing structural discovery eliminates invented syntax at the source.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes:
      "Original engineering by Mehansh Barthwal. Officially merged into the community repository alirezarezvani/claude-skills under Pull Request #870.",
    license: "MIT",
    upstreamUrl:
      "https://github.com/alirezarezvani/claude-skills/tree/main/engineering/zero-hallucination-coder",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/zero-hallucination-coder",
      label: "View Skill Source",
    },
    whenToUse: [
      "User asks to build, architect, or implement a code feature",
      "User requests refactoring or structural debugging",
      "User wants production grade code with zero speculative dependencies",
    ],
    whenNotToUse: [
      "Purely theoretical explanations of basic concepts",
      "Casual syntax questions with no implementation intent",
    ],
    howToUse: "Install into .claude/skills/zero-hallucination-coder or append to .cursorrules.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["coding", "verification", "engineering"],
    files: 1,
  },
  {
    slug: "universal-scraping-architect",
    name: "Universal Scraping Architect",
    kind: "skill",
    category: "Research",
    tagline: "Dynamic scraping strategy router with token budgeting and checkpointing.",
    what: "Analyzes target web pages and data extraction goals, selecting the optimal method across Firecrawl, local Python, or hybrid pipelines while planning token quotas and checkpointing state.",
    why: "Most scraping scripts fail due to poor architectural decisions chosen early in development rather than syntax errors.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes:
      "Original engineering by Mehansh Barthwal. Contributed to alirezarezvani/claude-skills.",
    license: "MIT",
    upstreamUrl:
      "https://github.com/alirezarezvani/claude-skills/tree/main/engineering/universal-scraping-architect",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/universal-scraping-architect",
      label: "View Skill Source",
    },
    whenToUse: [
      "Planning web extraction, automated crawling, or document ingestion",
      "Harvesting structured datasets from challenging web structures",
      "Configuring Firecrawl workflows with strict token limits",
    ],
    whenNotToUse: ["Simple single page text fetches that need only basic cURL requests"],
    howToUse: "Load the skill before writing any web scraper to configure extraction parameters.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["scraping", "architecture", "data"],
    files: 1,
  },
  {
    slug: "pain-point-miner",
    name: "Pain Point Miner",
    kind: "skill",
    category: "Research",
    tagline: "Authentic customer complaint extraction with mechanical deduplication.",
    what: "Extracts real user complaints and product frustrations from forums, subreddits, and customer reviews into structured tabular data, enforcing mechanical fetch verification and deduplication.",
    why: "Created during research work at SVS Aqua Technologies LLP to collect over four hundred verified consumer odor complaints without generating synthetic text.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes:
      "Original methodology developed and verified during industry research at SVS Aqua Technologies LLP.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/pain-point-miner",
      label: "View Skill Source",
    },
    whenToUse: [
      "Conducting voice of customer research or competitor complaint analysis",
      "Harvesting pain points from Reddit, Quora, or review forums",
      "Building verified problem banks for product discovery",
    ],
    whenNotToUse: ["Generating synthetic marketing personas or speculative feedback"],
    howToUse: "Trigger with: research customer complaints about [product or topic].",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["research", "voice-of-customer", "market-analysis"],
    files: 5,
  },
  {
    slug: "arxivist",
    name: "ArXivist",
    kind: "tool",
    category: "Research",
    tagline: "Translates scientific research papers into runnable code repositories.",
    what: "A six agent orchestration pipeline (Paper Parser, SIR Registry, Architecture Planner, Code Generator, Notebook Generator, Results Comparator) that converts academic PDFs into reproducible GitHub codebases.",
    why: "Reproducing paper methodologies manually involves tedious parameter extraction and code boilerplate. Schemas between stages prevent errors from compounding.",
    provenance: "adapted",
    author: "Mehansh Barthwal (Skill) and qosi org (Original Repository)",
    attributionNotes:
      "Agent skill implementation crafted by Mehansh Barthwal based on the original concept and repository by qosi org at https://github.com/qosi-org/arxivist.",
    license: "MIT",
    upstreamUrl: "https://github.com/qosi-org/arxivist",
    link: {
      href: "https://github.com/qosi-org/arxivist",
      label: "Original Repository by qosi org",
    },
    whenToUse: [
      "Converting an arXiv paper PDF or abstract into a runnable code repository",
      "Generating verified Jupyter notebooks directly from research papers",
      "Validating academic intermediate representations against published metrics",
    ],
    whenNotToUse: ["Generating informal paper summaries with no implementation goal"],
    howToUse: "Invoke with: reproduce arXiv paper [URL or PDF].",
    compatibility: ["Claude Code", "Antigravity", "Python 3.10+"],
    tags: ["multi-agent", "research", "paper-to-code", "python"],
    files: 14,
  },
  {
    slug: "loop-until-done",
    name: "Loop Until Done",
    kind: "workflow",
    category: "Orchestration",
    tagline: "Autonomous self evaluation loop rewriting drafts until rubric bars clear.",
    what: "Wraps multi step tasks in an iterative cycle where the agent plans, produces, grades its output against objective criteria, identifies weaknesses, and rewrites until all requirements pass.",
    why: "Initial agent completions frequently stop at minimum viable drafts. Substantial quality gains emerge from iterative evaluation against explicit rubrics.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes: "Original iterative workflow protocol authored by Mehansh Barthwal.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/loop-until-done",
      label: "View Skill Source",
    },
    whenToUse: [
      "Tasks requiring verified completion against objective criteria",
      "Repeated generation cycles where criteria can be strictly scored",
      "Self correcting drafting processes that operate without human intervention",
    ],
    whenNotToUse: ["Subjective design decisions or quick factual lookups"],
    howToUse: "Trigger with: loop until done using criteria [list of criteria].",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["workflow", "rubric", "quality"],
    files: 1,
  },
  {
    slug: "jd-to-job",
    name: "JD to Job",
    kind: "skill",
    category: "Career",
    tagline: "Extracts operational role requirements into tailored application materials.",
    what: "Analyzes job postings to identify technical shortages, team priorities, and unstated operational needs, drafting materials targeted specifically to role demands.",
    why: "Generic resume keyword matching fails to demonstrate technical alignment. Tailoring applications to operational realities yields stronger outcomes.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes: "Original career engineering skill authored by Mehansh Barthwal.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/jd-to-job",
      label: "View Skill Source",
    },
    whenToUse: [
      "Analyzing technical job postings and internship listings",
      "Drafting cover letters and portfolio alignment summaries",
      "Identifying skill mismatches between candidate experience and role needs",
    ],
    whenNotToUse: ["Indiscriminate keyword stuffing across unrelated resumes"],
    howToUse: "Trigger with: analyze job description [paste text].",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["career", "applications", "strategy"],
    files: 2,
  },
  {
    slug: "resume-unrejectable",
    name: "Resume Unrejectable",
    kind: "skill",
    category: "Career",
    tagline: "Four stage evaluation gauntlet reflecting actual hiring pipelines.",
    what: "Runs candidate resumes through an ATS parser simulation, recruiter keyword gap analysis, bullet by bullet XYZ metric rewrite, and a mock hiring manager interview.",
    why: "Candidates often optimize for ATS scanners while failing recruiter review, or impress recruiters while failing technical screens. A multi stage audit evaluates each barrier.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes: "Original recruitment audit skill authored by Mehansh Barthwal.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/resume-unrejectable",
      label: "View Skill Source",
    },
    whenToUse: [
      "Auditing resumes for senior engineering and analytical positions",
      "Transforming passive bullet points into quantified XYZ accomplishments",
      "Simulating recruiter screening interviews against candidate backgrounds",
    ],
    whenNotToUse: ["Generating fictional achievements or fabricating metrics"],
    howToUse: "Trigger with: audit my resume against [target role].",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["career", "resume", "audit"],
    files: 1,
  },
  {
    slug: "locality-delivery-scraper",
    name: "Locality Delivery Scraper",
    kind: "skill",
    category: "Research",
    tagline: "Methodology playbook for mapping urban food delivery markets.",
    what: "Prescribes an ordered sequence for harvesting restaurant menus, pricing structures, delivery fees, and review sentiments across platforms in a defined urban market.",
    why: "Geographic data extraction requires strict ordering of operations to maintain comparability and avoid platform anti bot tripwires.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes: "Original scraping playbook authored by Mehansh Barthwal.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/locality-delivery-scraper",
      label: "View Skill Source",
    },
    whenToUse: [
      "Conducting locality food delivery market research",
      "Collecting restaurant catalog data across multiple ordering platforms",
      "Standardizing unstructured menu items into relational database schemas",
    ],
    whenNotToUse: ["Simple single restaurant menu lookups"],
    howToUse: "Load skill to guide systematic regional data collection.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["scraping", "market-research", "playbook"],
    files: 1,
  },
  {
    slug: "ipynb-editor",
    name: "IPYNB Editor",
    kind: "tool",
    category: "Coding",
    tagline: "Programmatic cell manipulation preserving notebook JSON integrity.",
    what: "A specialized script and skill interface allowing agents to read, patch, and execute specific Jupyter Notebook cells without corrupting underlying notebook schemas.",
    why: "Standard text replacement tools frequently corrupt raw .ipynb JSON formatting. Structural parsing prevents broken notebook files.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes: "Original notebook manipulation tool authored by Mehansh Barthwal.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/ipynb-editor",
      label: "View Tool Source",
    },
    whenToUse: [
      "Inspecting or editing specific cells in Jupyter Notebooks",
      "Patching notebook code without disturbing output metadata",
      "Automating notebook verification inside terminal sessions",
    ],
    whenNotToUse: ["Editing plain Python (.py) scripts"],
    howToUse: "python scripts/notebook_editor.py list <notebook.ipynb>",
    compatibility: ["Claude Code", "Antigravity", "Cursor", "Python 3.8+"],
    tags: ["jupyter", "notebooks", "tooling"],
    files: 2,
  },
  {
    slug: "markdown-converter",
    name: "Markdown Converter Router",
    kind: "skill",
    category: "Research",
    tagline: "Intelligent format routing across AnyDoc and MarkItDown.",
    what: "Evaluates input file formats (PDF, Word, Excel, PowerPoint, EPUB, CSV, images, audio, ZIP) and routes each document to either AnyDoc or MarkItDown depending on format superiority.",
    why: "No single document converter outperforms all others across every format. Routing each format to its strongest parser ensures optimal Markdown extraction.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes:
      "Original routing architecture by Mehansh Barthwal. Routes across AnyDoc (Firecrawl) and MarkItDown (Microsoft).",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/markdown-converter",
      label: "View Skill Source",
    },
    whenToUse: [
      "Converting complex documents and spreadsheets into clean Markdown",
      "Ingesting PDFs, Office documents, and audio transcripts into agent context",
      "Choosing between Rust based AnyDoc and Python based MarkItDown",
    ],
    whenNotToUse: ["Files that already exist as plain text or clean Markdown"],
    howToUse: "Trigger with: convert this document to markdown.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["documents", "markdown", "extraction"],
    files: 1,
  },

  // ----------------------------------------------------------- ADAPTED UPSTREAM WORKS
  {
    slug: "humanizer",
    name: "Humanizer",
    kind: "skill",
    category: "Writing",
    tagline: "Strips robotic hallmarks and promotional padding from machine prose.",
    what: "Audits text against established machine writing patterns (inflated symbolism, promotional adjectives, superficial participle clauses, rule of three lists) and rewrites issues in place.",
    why: "Complete regeneration often discards original arguments. Targeted rewriting cleans artificial phrasing while preserving technical points.",
    provenance: "adapted",
    author: "Siqi Chen",
    attributionNotes:
      "Adapted from Siqi Chen's open source humanizer skill (blader/humanizer). Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/blader/humanizer",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/humanizer",
      label: "View Skill Source",
    },
    whenToUse: [
      "Polishing first draft documentation, essays, and technical writeups",
      "Removing artificial promotional buzzwords from published text",
      "De-biasing text that exhibits formulaic machine rhythm",
    ],
    whenNotToUse: ["Writing raw code or strictly structured JSON documents"],
    howToUse: "Trigger with: humanize this draft.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["writing", "editing", "tone"],
    files: 6,
  },
  {
    slug: "stop-slop",
    name: "Stop Slop",
    kind: "skill",
    category: "Writing",
    tagline: "Compact prompt rules that block formulaic filler during initial generation.",
    what: "A lightweight rule set loaded during initial drafting that halts predictable machine tropes before they reach the draft.",
    why: "Preventing unnatural phrasing during generation is faster and less expensive than correcting it post hoc.",
    provenance: "adapted",
    author: "Hardik Pandya",
    attributionNotes:
      "Adapted from Hardik Pandya's open source stop-slop project (hardikpandya/stop-slop). Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/hardikpandya/stop-slop",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/stop-slop",
      label: "View Skill Source",
    },
    whenToUse: [
      "Drafting professional correspondence, documentation, and articles",
      "Enforcing natural, direct sentences without ceremonial filler",
      "Setting strict negative writing constraints in system instructions",
    ],
    whenNotToUse: ["Pure code generation where prose styling is absent"],
    howToUse: "Include in system instructions or trigger before drafting prose.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["writing", "drafting", "clarity"],
    files: 7,
  },
  {
    slug: "ai-watermarks-remover",
    name: "AI Watermarks Remover",
    kind: "skill",
    category: "Writing",
    tagline: "Combines zero width character scrubbing with stylistic rephrasing.",
    what: "Clears invisible Unicode artifacts and zero width character signatures while applying stylistic de-biasing to ensure a natural conversational register.",
    why: "Statistical and invisible watermarks frequently co-occur with formulaic phrasing. Combining technical and stylistic cleaning addresses both in one pass.",
    provenance: "adapted",
    author: "Mehansh Barthwal / Community",
    attributionNotes:
      "Synthesizes technical Unicode cleaning with rules adapted from Stop Slop (Hardik Pandya) and Humanizer (Siqi Chen).",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/ai-watermarks-remover",
      label: "View Skill Source",
    },
    whenToUse: [
      "Cleaning text extracted from web platforms that contain hidden Unicode markers",
      "Ensuring prose sounds natural, calm, and grounded",
    ],
    whenNotToUse: ["Sanitizing code containing deliberate non ASCII string literals"],
    howToUse: "Trigger with: remove watermarks and humanize this text.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["writing", "watermarks", "cleanup"],
    files: 1,
  },
  {
    slug: "ponytail",
    name: "Ponytail",
    kind: "skill",
    category: "Coding",
    tagline: "Senior developer minimalism prioritizing standard libraries and YAGNI.",
    what: "Enforces a deletion first engineering checklist before writing code, rejecting premature abstractions and tracking deferred decisions with explicit comments.",
    why: "Long agent sessions waste context and introduce fragility by inventing unnecessary helper classes. Preferring native platform features minimizes maintenance debt.",
    provenance: "adapted",
    author: "DietrichGebert",
    attributionNotes:
      "Adapted from DietrichGebert's open source ponytail project. Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/DietrichGebert/ponytail",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/ponytail",
      label: "View Skill Source",
    },
    whenToUse: [
      "Any software engineering task where minimal diffs and simplicity are valued",
      "Auditing repositories for speculative code and unused dependencies",
      "Keeping agent sessions focused on functional requirements",
    ],
    whenNotToUse: ["Initial architectural brainstorming where broad exploration is needed"],
    howToUse: "Activate ponytail mode in system prompt or coding workflow.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["coding", "minimalism", "yagni"],
    files: 122,
  },
  {
    slug: "graphify",
    name: "Graphify",
    kind: "tool",
    category: "Architecture",
    tagline: "Constructs queryable knowledge graphs from codebases and documents.",
    what: "A comprehensive analysis utility parsing codebases into relational knowledge graphs, identifying community clusters, and generating Obsidian vaults for navigational context.",
    why: "Vector similarity search returns syntactically similar snippets. Knowledge graphs return structural dependencies, essential for navigating large code repositories.",
    provenance: "adapted",
    author: "Safi Shamsi",
    attributionNotes:
      "Adapted from Safi Shamsi's open source graphify project. Distributed under Apache 2.0 and MIT licenses.",
    license: "Apache-2.0",
    upstreamUrl: "https://github.com/safishamsi/graphify",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/graphify",
      label: "View Tool Source",
    },
    whenToUse: [
      "Onboarding an agent onto large multi file repositories",
      "Mapping relationships across microservices, classes, and call trees",
      "Generating visual Obsidian graph vaults for architectural review",
    ],
    whenNotToUse: ["Simple single script projects with trivial structures"],
    howToUse: "Run python graphify.py against your project directory.",
    compatibility: ["Claude Code", "Antigravity", "Python 3.10+"],
    tags: ["knowledge-graph", "codebase", "architecture"],
    files: 766,
  },
  {
    slug: "gsd-core",
    name: "GSD Core",
    kind: "tool",
    category: "Orchestration",
    tagline: "Phase based autonomous development with user acceptance gates.",
    what: "A modular spec driven framework organizing autonomous development into distinct phases (Discuss, Plan, Execute, Verify) with automated testing before progressing.",
    why: "Unbounded autonomous agent runs frequently drift from requirements. Explicit phase boundaries prevent speculative errors from multiplying.",
    provenance: "adapted",
    author: "Open GSD",
    attributionNotes:
      "Adapted from the open source Open GSD project. Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/opengsd/gsd-core",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/gsd-core",
      label: "View Framework Source",
    },
    whenToUse: [
      "Building complex features spanning multiple files and components",
      "Autonomous coding workflows requiring formal acceptance criteria",
      "Structured project lifecycle management with reproducible phases",
    ],
    whenNotToUse: ["Trivial one line script fixes"],
    howToUse: "Execute via GSD CLI commands or load phase skills sequentially.",
    compatibility: ["Claude Code", "Antigravity", "Cursor"],
    tags: ["orchestration", "spec-driven", "development"],
    files: 2189,
  },
  {
    slug: "agent-reach",
    name: "Agent Reach",
    kind: "tool",
    category: "Research",
    tagline: "Unified research interface and Model Context Protocol across fifteen networks.",
    what: "A Python CLI and Model Context Protocol server providing adapters for Twitter, Reddit, LinkedIn, GitHub, YouTube, Bilibili, and web searching, with credential safety checks.",
    why: "Each platform requires distinct authentication and rate limit handling. Unifying access behind one protocol simplifies research workflows.",
    provenance: "adapted",
    author: "Agent Eyes",
    attributionNotes:
      "Adapted from Agent Eyes' open source agent-reach project. Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/agent-eyes/agent-reach",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/agent-reach",
      label: "View Tool Source",
    },
    whenToUse: [
      "Cross platform research across social and developer platforms",
      "Inspecting GitHub discussions, Reddit threads, and technical articles",
      "Operating as a registered MCP server in Claude or Cursor",
    ],
    whenNotToUse: ["Writing social media posts or submitting automated comments"],
    howToUse: "agent-reach doctor --json to verify operational adapters.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "Python 3.10+"],
    tags: ["research", "mcp", "cli", "multi-platform"],
    files: 108,
  },
  {
    slug: "agent-video",
    name: "Agent Video",
    kind: "tool",
    category: "Research",
    tagline: "Transforms video recordings into structured frames and aligned transcripts.",
    what: "Downloads video through yt dlp, extracts auto scaled keyframes via FFmpeg, retrieves native captions or transcribes with Whisper, and packages timestamps for agent consumption.",
    why: "Reviewing lengthy video recordings to extract specific technical diagrams or decisions is time intensive. Timestamped frames enable direct inspection.",
    provenance: "adapted",
    author: "Bradley Bonanno",
    attributionNotes:
      "Adapted from Bradley Bonanno's open source agent-video project. Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/bradleybonanno/agent-video",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/agent-video",
      label: "View Tool Source",
    },
    whenToUse: [
      "Analyzing recorded conference talks, architectural demos, or lectures",
      "Extracting key slides and visual code samples from video streams",
      "Querying video content via synchronized transcript timestamps",
    ],
    whenNotToUse: ["Simple audio only podcast transcriptions"],
    howToUse: "Trigger with: watch video [URL or local path].",
    compatibility: ["Claude Code", "Antigravity", "Python 3.10+", "FFmpeg"],
    tags: ["video", "whisper", "ffmpeg", "multimodal"],
    files: 27,
  },
  {
    slug: "frontend-slides",
    name: "Frontend Slides",
    kind: "tool",
    category: "Design",
    tagline: "Builds animation rich HTML slide decks or converts from PowerPoint.",
    what: "Generates interactive web presentations with CSS and motion design, or converts existing PPTX decks into responsive, accessible web formats.",
    why: "Standard slide software limits typography and interactive controls. HTML slide decks enable live components and custom styling.",
    provenance: "adapted",
    author: "Zara Zhang",
    attributionNotes:
      "Adapted from Zara Zhang's open source frontend-slides project. Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/zarazhang/frontend-slides",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/frontend-slides",
      label: "View Tool Source",
    },
    whenToUse: [
      "Building web based slide decks for technical presentations",
      "Converting legacy PowerPoint files to responsive web formats",
      "Creating interactive presentations with embedded code playgrounds",
    ],
    whenNotToUse: ["Generating static print documents"],
    howToUse: "Trigger with: build presentation slides about [topic].",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "Vite"],
    tags: ["slides", "frontend", "presentations"],
    files: 160,
  },
  {
    slug: "markitdown",
    name: "MarkItDown",
    kind: "tool",
    category: "Research",
    tagline: "Microsoft utility converting diverse file formats into Markdown.",
    what: "A Python library and command line utility extracting structured text from PDFs, Office documents, audio files, images, and archives.",
    why: "Language model context windows require text. MarkItDown extracts structural tables and formatting from binary formats cleanly.",
    provenance: "adapted",
    author: "Microsoft Corporation",
    attributionNotes:
      "Open source software authored by Microsoft Corporation. Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/microsoft/markitdown",
    link: {
      href: "https://github.com/microsoft/markitdown",
      label: "View Microsoft Repository",
    },
    whenToUse: [
      "Extracting tables from Excel spreadsheets and PowerPoint files",
      "Converting complex Word and PDF documents into clean Markdown",
      "Running locally via CLI or as an MCP server",
    ],
    whenNotToUse: ["Converting pure plain text files"],
    howToUse: "markitdown path/to/document.pdf",
    compatibility: ["Python 3.10+", "Claude Desktop", "Antigravity"],
    tags: ["documents", "conversion", "python"],
    files: 158,
  },
  {
    slug: "ralph",
    name: "Ralph",
    kind: "tool",
    category: "Orchestration",
    tagline: "Converts requirements specifications into deterministic agent code.",
    what: "Parses Product Requirements Documents into structured JSON execution schemas and coordinates autonomous coding loops against verifiable acceptance criteria.",
    why: "Standard PRDs assume human intuition. Ralph structures requirements with explicit boundary tests so agents execute without drifting.",
    provenance: "adapted",
    author: "snarktank",
    attributionNotes:
      "Adapted from snarktank's open source ralph project. Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/snarktank/ralph",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/ralph",
      label: "View Tool Source",
    },
    whenToUse: [
      "Converting narrative product specifications into actionable agent tasks",
      "Running autonomous PRD execution loops in terminal environments",
    ],
    whenNotToUse: ["Informal exploratory coding sessions"],
    howToUse: "Trigger with: convert this PRD to ralph format.",
    compatibility: ["Claude Code", "Antigravity", "Cursor"],
    tags: ["prd", "planning", "autonomous"],
    files: 27,
  },
  {
    slug: "skillopt",
    name: "SkillOpt",
    kind: "tool",
    category: "Orchestration",
    tagline: "Offline agent review cycle consolidating recurring session corrections.",
    what: "Parses historical agent session transcripts offline, detects repeated human corrections, and proposes surgical skill refinements behind an evaluation gate.",
    why: "Repeatedly correcting the same model behaviors wastes effort. Consolidating corrections into permanent skill modifications improves future performance.",
    provenance: "adapted",
    author: "Microsoft Corporation",
    attributionNotes:
      "Adapted from Microsoft Corporation's SkillOpt project. Distributed under the MIT License.",
    license: "MIT",
    upstreamUrl: "https://github.com/microsoft/SkillOpt",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/skillopt",
      label: "View Tool Source",
    },
    whenToUse: [
      "Running nightly or offline agent self improvement routines",
      "Consolidating repeated engineering instructions into persistent rules",
    ],
    whenNotToUse: ["Active live coding sessions"],
    howToUse: "Trigger with: run skillopt cycle against recent logs.",
    compatibility: ["Claude Code", "Antigravity", "Python 3.10+"],
    tags: ["self-improvement", "memory", "optimization"],
    files: 368,
  },

  // -------------------------------------------------------- METHODOLOGY INSPIRED
  {
    slug: "claude-skills-llm-council",
    name: "LLM Council",
    kind: "skill",
    category: "Orchestration",
    tagline: "Five advisor debate protocol peer reviewing proposals anonymously.",
    what: "Runs complex decisions through five independent agent perspectives, executes anonymous peer review rounds, and synthesizes a balanced verdict accounting for disagreements.",
    why: "Individual model answers frequently convey unearned confidence. Anonymous review rounds surface vulnerabilities and trade offs.",
    provenance: "inspired",
    author: "Andrej Karpathy (Concept) / Mehansh Barthwal (Protocol)",
    attributionNotes:
      "Protocol implementation inspired by Andrej Karpathy's LLM Council methodology.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/claude-skills-llm-council",
      label: "View Skill Source",
    },
    whenToUse: [
      "Evaluating critical architectural decisions and tech stack tradeoffs",
      "Stress testing project proposals before committing engineering resources",
      "Surfacing subtle failure modes across complex decisions",
    ],
    whenNotToUse: ["Simple factual lookups or basic binary questions"],
    howToUse: "Trigger with: council this proposal [describe decision].",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["council", "multi-agent", "decisions"],
    files: 2,
  },
  {
    slug: "karpathy-guidelines",
    name: "Karpathy Guidelines",
    kind: "skill",
    category: "Coding",
    tagline: "Four always on instincts preventing common agent coding failures.",
    what: "A compact behavioral posture enforcing verified assumptions, minimal surgical diffs, explicit completion definitions, and deletion of speculative code.",
    why: "Distills the primary failure modes of agent coding sessions into concise standing rules small enough to remain active in context indefinitely.",
    provenance: "inspired",
    author: "Andrej Karpathy (Observations) / Mehansh Barthwal (Distillation)",
    attributionNotes:
      "Distilled from public reflections and engineering commentary by Andrej Karpathy.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/karpathy-guidelines",
      label: "View Skill Source",
    },
    whenToUse: [
      "Active coding, debugging, refactoring, and reviewing tasks",
      "Maintaining surgical pull request diffs during agent sessions",
    ],
    whenNotToUse: ["Non coding writing requests"],
    howToUse: "Load into global system prompt as standing background rules.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["coding", "posture", "guidelines"],
    files: 1,
  },
  {
    slug: "taste-skill",
    name: "Taste Skill",
    kind: "skill",
    category: "Design",
    tagline: "Anti slop frontend design direction for web applications.",
    what: "Comprehensive design guidance instructing agents to infer appropriate visual direction, select legitimate typography scales, and refuse generic template defaults.",
    why: "Coding agents default to predictable styles (purple gradients, excessive drop shadows, cards inside cards). Naming and banning poor defaults restores design intentionality.",
    provenance: "inspired",
    author: "Community Design Collective",
    attributionNotes:
      "Modular design system inspired by contemporary anti slop frontend engineering and typography practices.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/taste-skill",
      label: "View Skill Source",
    },
    whenToUse: [
      "Designing landing pages, portfolio interfaces, and web applications",
      "Redesigning existing user interfaces to remove generic styling",
      "Selecting typography scales, OKLCH color palettes, and balanced layouts",
    ],
    whenNotToUse: ["Pure backend API and CLI implementations"],
    howToUse: "Activate taste skill before authoring frontend CSS or JSX components.",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["design", "frontend", "typography"],
    files: 15,
  },
  {
    slug: "truth-prompt",
    name: "Truth Prompt",
    kind: "skill",
    category: "Research",
    tagline: "Strictly separates verified facts from inferences and assumptions.",
    what: "Forces completions to explicitly tag claims as verified fact, inference, or assumption, stating gaps and uncertainty openly rather than smoothing over unknowns.",
    why: "A confident erroneous assertion is more hazardous than an acknowledged knowledge gap.",
    provenance: "inspired",
    author: "Epistemic AI Research",
    attributionNotes:
      "Rooted in epistemic calibration research and structured intelligence analysis standards.",
    license: "MIT",
    link: {
      href: "https://github.com/mehanshbarthwal-lab/universal-agent-skills/tree/main/skills/truth-prompt",
      label: "View Skill Source",
    },
    whenToUse: [
      "Fact checking claims, historical data, and numerical estimates",
      "Technical evaluations where false positives carry significant consequences",
    ],
    whenNotToUse: ["Pure creative writing or brainstorming exercises"],
    howToUse: "Trigger with: verify truth status of [claim or question].",
    compatibility: ["Claude Code", "Cursor", "Antigravity", "ChatGPT", "Ollama"],
    tags: ["epistemics", "verification", "honesty"],
    files: 3,
  },

  // ---------------------------------------------------- EXTERNAL & INTERNAL REFERENCES
  {
    slug: "openhuman",
    name: "OpenHuman Context",
    kind: "skill",
    category: "Architecture",
    tagline: "Architecture context for the tinyhumansai/openhuman codebase.",
    what: "Provides architectural context on the OpenHuman repository (Rust core, Tauri shell, React frontend, event bus, skills runtime, memory layer) for coding agents.",
    why: "Re-exploring extensive multi language codebases each session exhausts context limits. Loading a structural map provides immediate orientation.",
    provenance: "external",
    author: "tinyhumansai",
    attributionNotes: "Architecture context document for tinyhumansai/openhuman.",
    license: "MIT",
    upstreamUrl: "https://github.com/tinyhumansai/openhuman",
    link: {
      href: "https://github.com/tinyhumansai/openhuman",
      label: "View Upstream Repository",
    },
    whenToUse: ["Developing or debugging within the OpenHuman codebase"],
    whenNotToUse: ["Working in independent projects unrelated to OpenHuman"],
    howToUse: "Load skill when initiating work on the OpenHuman repository.",
    compatibility: ["Claude Code", "Cursor", "Antigravity"],
    tags: ["openhuman", "rust", "tauri", "react"],
    files: 12,
  },
  {
    slug: "zapier-mcp",
    name: "Zapier MCP Config",
    kind: "skill",
    category: "Architecture",
    tagline: "Reference configuration for Zapier Model Context Protocol integrations.",
    what: "Documents authenticated connection parameters, scoped actions, and identifier schemas across connected Zapier services.",
    why: "Maintains private connection topology offline so future agent sessions avoid repeated discovery queries.",
    provenance: "internal",
    author: "Mehansh Barthwal",
    attributionNotes: "Personal automation topology and connection state documentation.",
    license: "Private",
    link: null,
    whenToUse: ["Referencing available Zapier MCP actions in personal automation workflows"],
    whenNotToUse: ["Public open source deployments"],
    howToUse: "Internal reference document.",
    compatibility: ["Claude Desktop", "Antigravity", "Zapier MCP"],
    tags: ["integrations", "mcp", "zapier"],
    files: 1,
  },
  {
    slug: "knowledge-base",
    name: "Knowledge Base",
    kind: "skill",
    category: "Architecture",
    tagline: "Engineering playbook and deployment patterns to avoid repeating past errors.",
    what: "A running record of solved deployment issues, environment configurations, and debugging resolutions loaded to prevent repeating historical mistakes.",
    why: "Agents retain no memory between independent sessions. A curated knowledge base provides persistent institutional knowledge.",
    provenance: "internal",
    author: "Mehansh Barthwal",
    attributionNotes:
      "Curated engineering runbook compiled across deployments and production workflows.",
    license: "Internal",
    link: null,
    whenToUse: [
      "Encountering persistent build, deployment, or path resolution issues",
      "Reviewing known workarounds for Colab, Vercel, or Node streaming quirks",
    ],
    whenNotToUse: ["Generic development tasks where no errors have occurred"],
    howToUse: "Read references/knowledge_base.md upon encountering persistent build errors.",
    compatibility: ["Claude Code", "Cursor", "Antigravity"],
    tags: ["memory", "debugging", "playbook"],
    files: 1,
  },

  // ------------------------------------------------------------------ WRITEUPS
    {
    slug: "agent-meter-doctor",
    name: "Agent Meter Doctor",
    kind: "skill",
    category: "Architecture",
    tagline: "Universal agent telemetry, token waste auditing, and autonomous self improvement loop.",
    what: "Bridges Claude Code four meters (/context, /usage, /skill-doctor, /insights) with universal telemetry across all AI agents. Enforces an automatic post turn reflection loop after every prompt to identify token waste, code defects, and unused skill components, recording prevention rules into a persistent anti pattern ledger.",
    why: "Agents silently burn tokens on cache invalidation and repeatedly repeat tool failure modes without persistent memory. Agent Meter Doctor installs live telemetry meters and an active post turn learning loop to continuously diagnose friction and eliminate errors at the source.",
    provenance: "original",
    author: "Mehansh Barthwal",
    attributionNotes: "Original engineering by Mehansh Barthwal. Universal telemetry framework bridging Claude Code four meters across multi agent environments.",
    license: "MIT",
    link: null,
    whenToUse: [
      "Auditing token waste, context limits, or cache invalidation across AI agents",
      "Debugging repetitive tool failures or buggy code loops",
      "Maintaining persistent anti pattern mistake ledgers to prevent recurring defects",
      "Optimizing loaded skills and trimming dormant plugin components",
    ],
    whenNotToUse: [
      "Simple single turn conversational queries with no code or tool execution",
      "Tasks where token usage and context budgets are completely unconstrained",
    ],
    howToUse: "Install via claude skill add or copy to <skills-directory>/agent-meter-doctor.",
    compatibility: ["Claude Code", "Cursor", "Google Antigravity", "ChatGPT", "Local LLMs"],
    tags: ["telemetry", "tokens", "debugging", "cache", "self-improvement"],
    files: 12,
    triggerPrompts: [
      "Run agent meter doctor to audit token spend and cache hit ratio",
      "Diagnose why the agent is repeating this coding mistake",
      "Audit loaded skills context tax and eliminate dead components",
      "Reflect on this turn and record the anti pattern prevention rule",
    ],
  },
  {
    slug: "beautify-github-profile",
    name: "Beautify GitHub Profile",
    kind: "skill",
    category: "Design",
    tagline: "Transforms repository documentation and profiles into elite publication grade showcases.",
    what: "Enforces centered headers, stylized shields.io badges, custom visual architecture banners, live retina preview screenshots, Mermaid flowcharts, comprehensive feature tables, copyable quick start guides, and GitHub REST API metadata synchronization.",
    why: "Standard GitHub repositories look plain, unstructured, and fail to convey technical craftsmanship. Transforming documentation with high aesthetic standards instantly elevates project presentation and developer trust.",
    provenance: "adapted",
    author: "Mehansh Barthwal and rzashakeri",
    attributionNotes: "Engineered by Mehansh Barthwal based on the component catalog and templates by rzashakeri at https://github.com/rzashakeri/beautify-github-profile.",
    license: "MIT",
    upstreamUrl: "https://github.com/rzashakeri/beautify-github-profile",
    link: {
      href: "https://github.com/rzashakeri/beautify-github-profile",
      label: "Original Repository by rzashakeri",
    },
    whenToUse: [
      "User asks to create, initialize, refactor, or beautify a repository README",
      "User wants publication grade developer documentation and centered badge layouts",
      "User asks to synchronize GitHub repository descriptions, homepages, and topics",
    ],
    whenNotToUse: [
      "Internal scratch notes or throwaway code with no documentation needs",
      "Casual markdown queries",
    ],
    howToUse: "Install via claude skill add or copy to <skills-directory>/beautify-github-profile.",
    compatibility: ["Claude Code", "Cursor", "Google Antigravity", "ChatGPT", "Local LLMs"],
    tags: ["design", "documentation", "readme", "github", "badges"],
    files: 1,
    triggerPrompts: [
      "Beautify this repository README following the design standard",
      "Create an elite documentation layout with centered badges and Mermaid diagrams",
      "Synchronize repository metadata and topics for this project",
    ],
  },
{
    slug: "on-the-catalog",
    name: "On Building the Catalog",
    kind: "writeup",
    category: "Architecture",
    tagline: "Why this collection maintains a machine readable registry.",
    what: "Examines why large skill collections require machine readable schemas, how semantic token overlap prevents redundant skills, and why automated categorization requires manual supervision.",
    why: "Collections exceeding twelve items become difficult to navigate without structured metadata. A programmatic registry allows both agents and web portals to discover capabilities cleanly.",
    provenance: "original",
    author: "Mehansh Barthwal",
    license: "MIT",
    link: null,
    whenToUse: ["Understanding the registry architecture and automated packaging utility"],
    howToUse: "Read writeup for architecture insights.",
    compatibility: ["Documentation"],
    tags: ["architecture", "registry", "metadata"],
  },
  {
    slug: "portability",
    name: "Portability Across Runtimes",
    kind: "writeup",
    category: "Architecture",
    tagline: "How one skill format operates across six agent runtimes.",
    what: "Technical notes exploring how skill files translate across Claude Code, Cursor IDE, Google Antigravity, ChatGPT Custom GPTs, OpenClaw, and local models via Ollama.",
    why: "Developers frequently switch agent interfaces. Normalizing skill files into universal instructions ensures behavioral consistency across different environments.",
    provenance: "original",
    author: "Mehansh Barthwal",
    license: "MIT",
    link: null,
    whenToUse: ["Configuring agent skills across diverse development environments"],
    howToUse: "Read writeup for runtime adaptation strategies.",
    compatibility: ["Documentation"],
    tags: ["portability", "adapters", "runtimes"],
  },
  {
    slug: "why-skills-not-prompts",
    name: "Skills, Not Prompts",
    kind: "writeup",
    category: "Architecture",
    tagline: "The essential difference lies in triggers and negative constraints.",
    what: "Explores why traditional prompts fail in production workflows, and how explicit trigger declarations, negative constraints, and output rubrics transform prompts into reliable skills.",
    why: "Prompts provide general guidance without boundaries. Skills define when to activate, what to refuse, and what a passing output requires.",
    provenance: "original",
    author: "Mehansh Barthwal",
    license: "MIT",
    link: null,
    whenToUse: ["Authoring new agent skills or evaluating model reliability"],
    howToUse: "Read writeup for skill design philosophy.",
    compatibility: ["Documentation"],
    tags: ["philosophy", "constraints", "methodology"],
  },
  {
    slug: "anti-slop",
    name: "Notes on Anti Slop Engineering",
    kind: "writeup",
    category: "Writing",
    tagline: "Applying intentional de-biasing to prose and user interfaces.",
    what: "Analyzes how Stop Slop, Humanizer, and Taste Skill tackle the same fundamental challenge: counteracting generic model defaults across text and frontend engineering.",
    why: "Model defaults tend toward ungrounded promotional prose and generic card based layouts. Explicitly identifying and banning defaults restores craftsmanship.",
    provenance: "original",
    author: "Mehansh Barthwal",
    license: "MIT",
    link: null,
    whenToUse: ["Understanding the connection between prose editing and frontend design standards"],
    howToUse: "Read writeup for anti slop design principles.",
    compatibility: ["Documentation"],
    tags: ["anti-slop", "design", "writing"],
  },
];

export const kinds: EntryKind[] = ["skill", "tool", "workflow", "writeup"];

export const categories: Category[] = [
  "Coding",
  "Research",
  "Design",
  "Writing",
  "Orchestration",
  "Career",
  "Architecture",
];

export const countByKind = (kind: EntryKind) => entries.filter((e) => e.kind === kind).length;

export const countByCategory = (cat: Category) => entries.filter((e) => e.category === cat).length;

export const countByProvenance = (prov: Provenance) =>
  entries.filter((e) => e.provenance === prov).length;

export const getEntry = (slug: string) => entries.find((e) => e.slug === slug);
