# PromptOps: The Universal Prompt Library for AI Agents

PromptOps is a curated collection of 180+ standardized, high-quality prompt templates designed for developers, architects, and AI engineers. It provides a unified interface to discover and use prompts across any AI agent.

## 🚀 Key Features

- **Massive Catalog:** 180+ unique prompts across 40+ categories (Engineering, Security, AI, DevOps, etc.).
- **TUI Explorer:** High-performance terminal UI for lightning-fast search and discovery.
- **Agent Agnostic:** Specialized guides for Gemini, Cursor, Claude Code, Aider, and more.
- **Standardized Schema:** Every prompt includes metadata, versioning, and context-aware variable injection.

## 🛠 Installation

```bash
git clone https://github.com/your-repo/PromptOps.git
cd PromptOps
pip install -r requirements.txt
alias pop="$(pwd)/promptops"
```

## 📖 Usage

### Launch the Explorer
```bash
pop
```

### Search via CLI
```bash
pop search "security audit"
```

### Use in Gemini CLI
```bash
/prompts:code-review-security {{file}}
```

## 📂 Documentation

- [Full Prompt Catalog](docs/catalog/FULL_CATALOG.md)
- **Agent How-To Guides:**
  - [Gemini CLI](docs/agents/gemini.md)
  - [Cursor](docs/agents/cursor.md)
  - [Claude Code](docs/agents/claude-code.md)
  - [Aider](docs/agents/aider.md)
  - [GitHub Copilot / Codex](docs/agents/codex.md)
  - [Windsurf](docs/agents/windsurf.md)

## Available Templates

Templates are categorized by domain. Click a category to view its full reference notebook.

### [DevOps & Infrastructure](docs/catalog/devops-and-infrastructure.ipynb)
- `/prompts:bun-runtime` - Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support
- `/prompts:cloud-infrastructure-specialist` - Expert in cloud infrastructure (AWS/GCP/Azure) using Terraform and IAM. Focuses on security, least-privilege policies, and modular IaC
- `/prompts:container-orchestration-specialist` - Expert in containerization and orchestration using Docker and Kubernetes. Handles Dockerfiles, Compose, and Kubernetes manifests
- `/prompts:devops-specialist` - Expert DevOps/SRE specialist for CI/CD, IaC, SLOs, observability, and lifecycle management of long-lived agent workloads
- `/prompts:incident-response-specialist` - Expert incident commander for production management. Coordinates response, severity frameworks, blameless post-mortems, and on-call culture

### [Security & Compliance](docs/catalog/security-and-compliance.ipynb)
- `/prompts:security-architect` - Expert security architect specializing in threat modeling, secure code review, and defense-in-depth across the entire application stack
- `/prompts:security-policy` - Draft a SECURITY.md or vulnerability disclosure policy
- `/prompts:threat-modeling` - Generate a STRIDE threat model for a proposed architecture

### [UI / UX & Frontend](docs/catalog/ui-ux-and-frontend.ipynb)
- `/prompts:frontend-specialist` - Comprehensive frontend specialist for modern web apps. Covers Accessibility, Tailwind, Next.js, Nuxt 4, React patterns, and performance

### [Architecture & Design](docs/catalog/architecture-and-design.ipynb)
- `/prompts:architect` - Senior software architect for system design, domain-driven design, scalability, and technical decision-making with ADR and C4 support
- `/prompts:architecture-decision-records` - Capture architectural decisions as structured ADR documents. Tracks context, alternatives, consequences, and decision status
- `/prompts:autonomous-optimization-architect` - System governor for autonomous API shadow-testing and optimization with financial and security guardrails
- `/prompts:design-patterns` - Comprehensive guide for selecting and implementing software design patterns. Includes code examples, trade-offs, and testing considerations

### [Shell & Scripting](docs/catalog/shell-and-scripting.ipynb)
- `/prompts:bash-script-generator` - Write robust, POSIX-compliant bash scripts
- `/prompts:cli-command-explainer` - Deeply explain obscure terminal commands/flags
- `/prompts:terminal-integration-specialist` - Terminal emulation, text rendering optimization, and SwiftTerm integration for modern Swift applications

### [Documentation & Learning](docs/catalog/documentation-and-learning.ipynb)
- `/prompts:article-writing` - Expert long-form writer specialized in blog posts, tutorials, and newsletters with a focus on distinct, human-sounding voices and structured copy
- `/prompts:crosspost` - Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never pos
- `/prompts:doc-updater` - Documentation and codemap specialist. Use PROACTIVELY for updating codemaps and documentation. Runs /update-codemaps and /update-docs, generates d
- `/prompts:docs-lookup` - When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and
- `/prompts:eli5` - Explain like I'm 5 (simple explanations)
- `/prompts:learning-path` - Create learning roadmaps
- `/prompts:narrative-designer` - Story systems and dialogue architect - Masters GDD-aligned narrative design, branching dialogue, lore architecture, and environmental storytelling
- `/prompts:simplify-jargon` - Simplify technical jargon
- `/prompts:technical-writing-specialist` - Expert technical writer for developer docs, API references, tutorials, and technical blogs. Bridges the gap between engineers and users
- `/prompts:video-editing` - AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture through FFmpe
- `/prompts:visa-doc-translate` - Translate visa application documents (images) to English and create a bilingual PDF with original and translation

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new templates to our hierarchical structure.

## 📜 Acknowledgements

PromptOps is inspired by and incorporates patterns from these excellent community resources:
- [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
- [harish-garg/gemini-cli-prompt-library](https://github.com/harish-garg/gemini-cli-prompt-library)
