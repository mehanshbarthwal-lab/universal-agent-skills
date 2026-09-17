# Project Attribution and Provenance Matrix

This document provides transparent attribution for all skills, tools, workflows, and reference materials contained in this ecosystem.

Every entry in this collection falls into one of four verified categories:
1. Original work created by Mehansh Barthwal
2. Adapted open source software with upstream maintainer credit
3. Methodology inspired by published research or technical essays
4. External reference documentation for third party systems

---

## 1. Original Works by Mehansh Barthwal

The following items are original tools, skills, and architectures designed and authored by Mehansh Barthwal:

### Zero Hallucination Coder
* Category: Autonomous Coding
* Path: `skills/zero-hallucination-coder/SKILL.md`
* Status: Original work by Mehansh Barthwal. Officially contributed to and merged into the upstream community repository `alirezarezvani/claude-skills` under Pull Request #870.
* Purpose: Enforces a disciplined five phase loop (Discuss, Map, Decompose, Execute, Verify) to eliminate fabricated APIs and phantom libraries in language models.

### Universal Scraping Architect
* Category: Web Intelligence and Data Extraction
* Path: `skills/universal-scraping-architect/SKILL.md`
* Status: Original work by Mehansh Barthwal. Contributed to `alirezarezvani/claude-skills`.
* Purpose: A resilient multi mode data harvesting framework selecting between Firecrawl, local Python, and hybrid pipelines with built in token budgeting and state checkpointing.

### Pain Point Miner
* Category: Market Research and Discovery
* Path: `skills/pain-point-miner/SKILL.md`
* Status: Original work by Mehansh Barthwal. Developed during the Content Intelligence research internship at SVS Aqua Technologies LLP to mine and verify consumer problem reports across web forums without fabrication.
* Purpose: Extracts genuine consumer complaints from social threads, reviews, and forums into structured, deduplicated datasets.

### ArXivist
* Category: Research and Code Generation
* Path: `skills/arxivist/SKILL.md`
* Status: Agent skill implementation authored by Mehansh Barthwal, inspired by and attributed to the original repository by qosi org.
* Upstream Repository: https://github.com/qosi-org/arxivist
* Purpose: A six agent pipeline converting scientific research papers into executable, reproducible code repositories through intermediate representations and validation loops.

### Loop Until Done
* Category: Autonomous Workflows
* Path: `skills/loop-until-done/SKILL.md`
* Status: Original work by Mehansh Barthwal.
* Purpose: Wraps tasks in a self correcting evaluation loop that grades outputs against an objective rubric and rewrites weak areas until quality criteria are met.

### JD to Job
* Category: Career Intelligence
* Path: `skills/jd-to-job/SKILL.md`
* Status: Original work by Mehansh Barthwal.
* Purpose: Deconstructs target job specifications into core operational requirements and builds tailored application material matching employer needs.

### Resume Unrejectable
* Category: Career Intelligence
* Path: `skills/resume-unrejectable/SKILL.md`
* Status: Original work by Mehansh Barthwal.
* Purpose: A four stage evaluation pipeline simulating ATS parsers, recruiter keyword matrices, XYZ bullet rephrasing, and hiring manager stress tests.

### Locality Delivery Scraper
* Category: Web Scraping
* Path: `skills/locality-delivery-scraper/SKILL.md`
* Status: Original research methodology and scraping playbook by Mehansh Barthwal.
* Purpose: Structures food delivery listings, pricing indices, and customer sentiment across locality platforms.

### IPYNB Editor
* Category: Development Tooling
* Path: `skills/ipynb-editor/SKILL.md`
* Status: Original utility by Mehansh Barthwal.
* Purpose: Enables language models to inspect and patch Jupyter Notebook cells structurally without corrupting the underlying JSON schema.

### Markdown Converter Router
* Category: Document Processing
* Path: `skills/markdown-converter/SKILL.md`
* Status: Original routing architecture by Mehansh Barthwal.
* Purpose: Dynamically routes binary files, spreadsheets, presentations, and URLs to the optimal parsing engine between AnyDoc and MarkItDown.

### Agent Meter Doctor
* Category: Systems Architecture and Telemetry
* Path: `skills/agent-meter-doctor/SKILL.md`
* Status: Original engineering by Mehansh Barthwal. Universal agent telemetry framework bridging Claude Code four meters (/context, /usage, /skill-doctor, /insights) with multi agent observability and an autonomous post turn learning loop.
* References and Attribution: Based on official Anthropic Claude Code documentation (`code.claude.com/docs/en/costs`, `code.claude.com/docs/en/commands`) and Implicator (`implicator.ai`) taxonomy on `/skill-doctor` and per turn context tax.
* Purpose: Provides cross platform telemetry, prompt cache optimization, dead skill auditing, and records prevention rules into a persistent mistake ledger.

---

## 2. Adapted and Upstream Open Source Works

The following packages represent adapted or integrated open source projects. Original copyright notices, licenses, and maintainers are preserved:

### Humanizer
* Original Author: Siqi Chen
* Upstream Repository: `https://github.com/blader/humanizer`
* License: MIT License (Copyright 2025 Siqi Chen)
* Relationship: Adapted into skill format. Cleans machine generated text by removing predictable AI writing tells based on Wikipedia guidelines.

### Stop Slop
* Original Author: Hardik Pandya
* Upstream Repository: `https://github.com/hardikpandya/stop-slop`
* License: MIT License (Copyright 2025 Hardik Pandya)
* Relationship: Adapted into prompt and skill format. Enforces concise, direct drafting rules that block formulaic filler before generation.

### Ponytail
* Original Author: DietrichGebert
* Upstream Repository: `https://github.com/DietrichGebert/ponytail`
* License: MIT License (Copyright 2026 DietrichGebert)
* Relationship: Integrated senior developer posture prioritizing standard libraries, eliminating unnecessary abstractions, and auditing overengineering.

### Graphify
* Original Author: Safi Shamsi
* Upstream Repository: `https://github.com/safishamsi/graphify`
* License: Apache License 2.0 / MIT License (Copyright 2026 Safi Shamsi)
* Relationship: Integrated codebase knowledge graph generator building relational entity maps and Obsidian vaults.

### GSD Core
* Original Author: Open GSD
* Upstream Repository: `https://github.com/opengsd/gsd-core`
* License: MIT License (Copyright 2026 Open GSD)
* Relationship: Integrated spec driven autonomous development framework featuring modular phases and user acceptance gates.

### Agent Reach
* Original Author: Agent Eyes
* Upstream Repository: `https://github.com/agent-eyes/agent-reach`
* License: MIT License (Copyright 2025 Agent Eyes)
* Relationship: Multi platform research CLI and Model Context Protocol server covering fifteen social and information networks.

### Agent Video (Watch)
* Original Author: Bradley Bonanno
* Upstream Repository: `https://github.com/bradleybonanno/agent-video`
* License: MIT License (Copyright 2026 Bradley Bonanno)
* Relationship: Autonomous video processing pipeline downloading via yt dlp, extracting keyframes with FFmpeg, and transcribing with Whisper.

### Frontend Slides
* Original Author: Zara Zhang
* Upstream Repository: `https://github.com/zarazhang/frontend-slides`
* License: MIT License (Copyright 2025 Zara Zhang)
* Relationship: Web presentation generator and PowerPoint to HTML slide converter.

### Ralph
* Original Author: snarktank
* Upstream Repository: `https://github.com/snarktank/ralph`
* License: MIT License (Copyright 2026 snarktank)
* Relationship: PRD parser and autonomous execution system translating specifications into deterministic code.

### SkillOpt
* Original Author: Microsoft Corporation
* Upstream Repository: `https://github.com/microsoft/SkillOpt`
* License: MIT License (Copyright 2026 Microsoft Corporation)
* Relationship: Offline agent self optimization cycle analyzing past session transcripts to propose continuous skill refinements.

### MarkItDown
* Original Author: Microsoft Corporation
* Upstream Repository: `https://github.com/microsoft/markitdown`
* License: MIT License (Copyright Microsoft Corporation)
* Relationship: Python utility converting office documents, PDFs, audio, and archives into Markdown.

### Beautify GitHub Profile
* Original Author: Reza Shakeri
* Upstream Repository: `https://github.com/rzashakeri/beautify-github-profile`
* License: MIT License (Copyright 2024 Reza Shakeri)
* Relationship: Adapted into repository documentation standard with local mirror, badge catalog, and layout templates.

---

## 3. Methodology Inspired Works

### LLM Council
* Methodology Credit: Inspired by Andrej Karpathy's LLM Council concept.
* Implementation: Formatted into a five agent anonymous peer review and synthesis protocol.

### Karpathy Guidelines
* Methodology Credit: Distilled from public observations and engineering reflections by Andrej Karpathy on LLM failure modes.
* Implementation: Formatted as four standing instincts (state assumptions, minimal surgical diffs, define completion criteria, delete speculative code).

### Taste Skill
* Methodology Credit: Inspired by modern anti slop frontend engineering and typography design systems.
* Implementation: Modular guidance suite instructing agents on typography, layout balance, and responsive design standards.

### Truth Prompt
* Methodology Credit: Grounded in epistemic calibration principles.
* Implementation: Structural prompt requiring language models to explicitly label assertions as verified fact, inference, or assumption.

---

## 4. External System Reference and Internal Material

### OpenHuman
* Upstream Project: `tinyhumansai/openhuman`
* Purpose: Architecture reference skill loaded when assisting on the OpenHuman repository.

### Zapier MCP
* Purpose: Private account connection documentation for personal automation. Marked internal.

### Knowledge Base
* Purpose: Personal engineering playbook and troubleshooting runbook compiled across deployments and environments. Marked internal.
