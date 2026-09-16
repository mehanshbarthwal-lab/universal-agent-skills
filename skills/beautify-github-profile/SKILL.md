---
name: beautify-github-profile
description: Transform repository README files and profiles into elite, publication grade developer documentation. Enforces centered headers, stylized shields.io badges, custom visual architecture banners, live retina preview screenshots, Mermaid flowcharts, comprehensive feature tables, copyable quick start guides, and GitHub REST API metadata synchronization. Backed by the complete local catalog of badge templates and layout components from rzashakeri/beautify-github-profile.
---

# Beautify GitHub Profile & Repository Standard

Transform repository README files and profiles into elite, publication grade developer documentation.

## Reference Catalog
Agents have full access to both:
- Local catalog and templates: `<skills-directory>/beautify-github-profile/readme.md`
- Upstream reference: `https://github.com/rzashakeri/beautify-github-profile`

## Standards & Requirements

1. **Centered Header and Badges**:
   - Centered alignment `<div align="center">`.
   - Clear title and compelling elevator pitch.
   - Stylized `shields.io` badges with `style=for-the-badge` (License, Runtime, Stack, Live Demo or Case Study link, Build status, Author).
   - Anchor navigation bar linking to core sections.

2. **Visual Banners and Working Previews**:
   - Always embed a custom visual architectural banner (`assets/banner.png`) or a real retina screenshot of the working web application and deployed case study (`assets/app-preview.png`, `assets/showcase-preview.png`).
   - Apply subtle rounded corners and drop shadows (`border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);`).

3. **Core Problem and Value Proposition**:
   - Clarify the exact problem the repository solves, why naive approaches fail, and target audience.
   - Use structured alerts (`> [!NOTE]`, `> [!IMPORTANT]`) for emphasis.

4. **Architecture and Flow Diagrams**:
   - Include a clean Mermaid flowchart (`flowchart TB` or `flowchart LR`) tracing data flows from inputs through execution pipelines to final outputs.

5. **Feature Catalogs and Technical Tables**:
   - Provide comprehensive markdown tables for tools, APIs, pipeline stages, or features with explicit parameters and rationale.

6. **Quick Start and Verification**:
   - Provide copyable step by step terminal commands for prerequisites, installation, environment setup, local execution, and test verification.

7. **GitHub Metadata and Topics Synchronization**:
   - Whenever pushing a repository to GitHub, synchronize metadata: update description, configure homepage link, and populate relevant search tags.
