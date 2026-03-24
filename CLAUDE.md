# promptbook — AI CLI Prompt Template Library

**Promptbook is a structured library of expert prompt templates for AI CLI tools — organized, versioned, and ready to use.**

You are a prompt engineering specialist and developer productivity assistant integrated with the **promptbook** library. Your role is to help users discover, use, customize, and author prompt templates for AI CLI workflows.

> **Context**: This file is loaded automatically by Claude Code when working in the promptbook repository. All templates are accessible by reading `.toml` files from `commands/prompts/`.

---

## Your Responsibilities
When assisting users, you should:
- **Proactively suggest** relevant templates when a user describes a task that maps to an available prompt (e.g., "I need to review this code for security issues" → suggest reading `commands/prompts/security/security-scan.toml` and applying it).
- **Read and hydrate templates** by loading the `.toml` file, extracting the `prompt` field, and substituting `{{variables}}` with the user's context.
- **Support Advanced Logic**: Handle dynamic context like `{{$(cmd)}}` and conditional extraction blocks `<if language="...">`.
- **Guide template authoring** when a user wants to create or modify a template.
- **Diagnose issues** with the CLI helper, TUI, or template validation errors.

---

## How Prompts Are Executed
When using a promptbook template, follow this pipeline:
1. **Load** — Read the `.toml` template from `commands/prompts/`.
2. **Hydrate** — Substitute variables such as `{{args}}`, `{{code}}`, `{{file}}`, and `{{language}}`. Dynamic context like `{{$(cmd)}}` and `{{env.VAR}}` is resolved at this stage.
3. **Prune** — Evaluate `<if language="...">` blocks to remove irrelevant content.
4. **Confirm** (if `sensitive = true`) — Warn the user before proceeding with security-sensitive prompts.
5. **Execute** — Apply the fully hydrated prompt to the current task.

### Usage Patterns
```bash
# Read a template and apply it to a task
claude "Read commands/prompts/architecture/design-api.toml and design a REST API for a task management app"

# Use pop CLI to hydrate and copy to clipboard, then paste
pop use security-scan --args @main.py

# Pipe file content into a template
cat main.py | pop use refactor-suggestions
```

---

## Variable Reference
Templates support the following placeholders for dynamic input injection:

| Variable | Purpose | Typical Source |
|---|---|---|
| `{{args}}` | Primary user input — the default catch-all | CLI argument, piped stdin, or `@file` flag |
| `{{code}}` | Code snippet for analysis or transformation | Inline paste or `--args @file.py` |
| `{{file}}` | Full file content | `--args @path/to/file` or `cat file \| pop use <tool>` |
| `{{language}}` | Programming language context | User-specified or inferred |
| `{{$(cmd)}}` | Shell command output | Evaluated at hydration time |
| `{{env.VAR}}` | Environment variable | System environment |

---

## CLI Reference (`pop`)
The `promptbook` binary is aliased as `pop`.

### Common Commands
| Command | Description |
|---|---|
| `pop list` | List all available templates with descriptions |
| `pop search <term>` | Full-text search across names and descriptions |
| `pop use <tool>` | Interactively run a template, prompting for variable values |
| `pop use <tool> --language <lang>` | Inject language context for surgical extraction |
| `pop use <tool> --args @file.py` | Inject file content directly into `{{args}}` |
| `pop tags` | List all unique category tags |

---

## TUI Browser
The promptbook TUI is a high-performance, Rust-based terminal interface for browsing, previewing, and hydrating prompts interactively.

**Launch:**
```bash
make tui
```

---

## 📂 Documentation
- [Full Prompt Catalog](docs/FULL_CATALOG.md)
- [Domain-Specific Catalogs](docs/catalog/README.md)

## Template Catalog
Templates are organized by domain. When a user asks for help with a task, map it to the most relevant template below.

### AI Agents & Infrastructure
- `agent-harness-architect`: Expert-level design and optimization of AI agent action spaces, tool definitions, and observation formatting for high completion rates
- `agentic-identity-trust`: Architectural specialist for agentic identity, cryptographic trust verification, and verifiable audit trails in multi-agent environments
- `agentic-principles`: Unified model for Agentic and AI-First Engineering. Focuses on eval-driven execution, task decomposition, and AI-assisted architecture
- `ai-engineer-agent`: Expert AI/ML engineer for model development, deployment, and production integration. Focuses on scalable features and intelligent data pipelines
- `autonomous-loop`: Unified guide for autonomous AI agent loops. Covers sequential pipelines, REPLs, infinite generation, PR loops, and RFC-driven DAG orchestration
- `claude-devfleet-specialist`: Orchestrate multi-agent coding tasks via Claude DevFleet, enabling project planning, parallel agent dispatch, and automated progress monitoring
- `common-agents`: Agent orchestration: available agents, parallel execution, multi-perspective analysis
- `content-engine-specialist`: Create platform-native content systems for social media, newsletters, and repurposed campaigns. Ensures consistency and high impact across channels
- `context-budget-specialist`: Audits the AI agent context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and produces
- `data-consolidation-agent`: AI specialist for consolidating sales metrics into real-time reporting dashboards with territory, representative, and pipeline summaries
- `enterprise-agent-ops-specialist`: Operate long-lived agent workloads with observability, security boundaries, and lifecycle management
- `eval-harness`: Unified evaluation framework for AI agents, implementing eval-driven development (EDD), head-to-head benchmarking, and harness optimization
- `llm-pipeline-specialist`: Unified specialist for LLM API integration and cost-aware pipelines. Covers Claude API, SDK patterns, model routing, and budget optimization
- `mcp-master`: Unified MCP Master for designing, building, and deploying Model Context Protocol servers. Covers SDK patterns, tool design, and transport
- `multi-agent-pipeline`: Unified Autonomous Pipeline Orchestration framework for high-velocity multi-agent development workflows
- `observer`: Background agent that analyzes session observations to detect patterns and create instincts. Uses Haiku for cost-efficiency. v2.1 adds project-sco
- `specialized-model-qa`: Independent model QA expert who audits ML and statistical models end-to-end - from documentation review and data reconstruction to replication, ca

### Architecture & Design
- `architect`: Senior software architect for system design, domain-driven design, scalability, and technical decision-making with ADR and C4 support
- `architecture-decision-records`: Capture architectural decisions as structured ADR documents. Tracks context, alternatives, consequences, and decision status
- `autonomous-optimization-architect`: System governor for autonomous API shadow-testing and optimization with financial and security guardrails
- `design-patterns`: Comprehensive guide for selecting and implementing software design patterns. Includes code examples, trade-offs, and testing considerations

### Code Review & Analysis
- `code-reviewer-agent`: Comprehensive code review specialist for quality, security, and performance. Provides actionable feedback and constructive refactoring suggestions
- `codebase-onboarding`: Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAU
- `compare-technologies`: Framework for comparing software technologies, frameworks, and libraries with a focus on trade-offs, syntax, and performance
- `continuous-learning-specialist`: Master specialist for the Continuous Learning system. Manages session observation, atomic instinct extraction, and knowledge evolution
- `documentation-lookup`: Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples,
- `engineering-standards-specialist`: Unified engineering standards for coding style, design patterns, automation hooks, and performance optimization across the development lifecycle
- `engineering-threat-detection-engineer`: Expert detection engineer specializing in SIEM rule development, MITRE ATT&CK coverage mapping, threat hunting, alert tuning, and detection-as-cod
- `error-resolution-agent`: Master specialist for diagnosing and resolving build, type, and runtime errors. Expert in root cause analysis and minimal-diff error fixing
- `lsp-specialist`: Language Server Protocol specialist building unified code intelligence systems through LSP client orchestration and semantic indexing
- `performance-profile`: Expert guide for performance profiling, bottleneck identification, and optimization across frontend, backend, and database layers
- `prompt-specialist`: Master specialist for prompt engineering: optimize, create, improve, and manage the lifecycle of high-quality prompts and templates
- `refactor-agent`: Expert refactoring specialist for code cleanup, dead code removal, duplicate elimination, and architectural improvements with a focus on safety
- `regex-builder`: Generate and explain complex Regular Expressions
- `regex-vs-llm-structured-text`: Decision framework for choosing between regex and LLM when parsing structured text — start with regex, add LLM only for low-confidence edge cases

### DevOps & Infrastructure
- `bun-runtime`: Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support
- `cloud-infrastructure-specialist`: Expert in cloud infrastructure (AWS/GCP/Azure) using Terraform and IAM. Focuses on security, least-privilege policies, and modular IaC
- `container-orchestration-specialist`: Expert in containerization and orchestration using Docker and Kubernetes. Handles Dockerfiles, Compose, and Kubernetes manifests
- `devops-specialist`: Expert DevOps/SRE specialist for CI/CD, IaC, SLOs, observability, and lifecycle management of long-lived agent workloads
- `incident-response-specialist`: Expert incident commander for production management. Coordinates response, severity frameworks, blameless post-mortems, and on-call culture

### Backend & Systems
- `backend-architect-agent`: Senior backend architect specializing in scalable system design, database architecture, API development, and cloud infrastructure
- `backend-specialist`: Expert backend architect for API design, database optimization, and scalable server-side patterns
- `clickhouse-io`: ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads
- `content-hash-cache-pattern`: Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation
- `database-architect-agent`: Expert database architect for schema design, migrations, query optimization, and performance tuning. Specialized in SQL and NoSQL systems
- `postgres-patterns`: PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices

### Frontend & UI/UX
- `frontend-specialist`: Comprehensive frontend specialist for modern web apps. Covers Accessibility, Tailwind, Next.js, Nuxt 4, React patterns, and performance
- `image-prompt-engineer`: Expert in AI image prompt engineering and media generation via fal.ai MCP for images, video, and audio
- `ui-ux-specialist`: Expert UI/UX specialist for design systems, user research, and Storybook component generation
- `visual-design-specialist`: Comprehensive visual design expert covering brand identity, storytelling, inclusivity, Liquid Glass, and style presets
- `xr-specialist`: Expert XR specialist for immersive AR/VR/XR experiences, spatial interaction design, and browser-based 3D applications

### Security & Compliance
- `blockchain-security-auditor`: Expert smart contract security auditor specializing in vulnerability detection, formal verification, and exploit analysis
- `security-architect`: Expert security architect specializing in threat modeling, secure code review, and defense-in-depth across the entire application stack
- `security-policy`: Draft a SECURITY.md or vulnerability disclosure policy
- `security-scan`: Comprehensive, tool-agnostic security audit for codebases, configurations, and dependencies. Focused on OWASP, secrets, and supply-chain risks
- `threat-modeling`: Generate a STRIDE threat model for a proposed architecture
- `zk-steward`: Knowledge-base steward in the spirit of Niklas Luhmann's Zettelkasten. Default perspective: Luhmann; switches to domain experts (Feynman, Munger,

### Testing & QA
- `common-testing`: Testing requirements: 80% coverage, TDD workflow, test types
- `e2e-runner`: End-to-end testing specialist using Vercel Agent Browser and Playwright for creating and maintaining reliable browser-based test suites
- `e2e-testing`: Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies
- `generate-e2e-tests`: Create end-to-end tests
- `generate-unit-tests`: Create unit tests for code
- `mock-data-gen`: Create realistic JSON/CSV mock data schemas for testing
- `research`: Research Context
- `review`: Code Review Context
- `review-test-coverage`: Analyze test coverage gaps
- `tdd-guide`: TDD specialist enforcing the write-tests-first methodology for new features, bug fixes, and refactoring with high coverage standards
- `tdd-workflow`: Enforces TDD with 80%+ coverage for unit, integration, and E2E tests during feature development, bug fixes, and refactors
- `test-edge-cases`: Identify and test edge cases
- `testing`: Python Testing
- `testing-specialist`: Comprehensive testing specialist covering AI regression patterns, accessibility, API validation, performance benchmarking, and QA workflows

### Language Specialists
- `android-clean-architecture`: Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data l
- `compose-multiplatform-patterns`: Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI
- `cpp-build-resolver`: Expert in resolving C++ build errors, CMake configuration issues, and linker warnings using surgical, minimal changes to restore project stability
- `cpp-reviewer`: Senior C++ code reviewer focused on modern idioms, memory safety, concurrency, and performance to ensure high-quality and secure codebases
- `cpp-specialist`: Unified C++ specialist for coding standards, style, patterns, security, and testing. Covers Modern C++, RAII, GoogleTest, and memory safety
- `csharp-specialist`: Unified C# specialist for coding style, architectural patterns, security, and testing. Covers .NET conventions, async, xUnit, and security
- `django-specialist`: Expert Django specialist for architecture patterns, REST APIs, TDD, security best practices, and comprehensive verification workflows
- `engineering-embedded-firmware-engineer`: Specialist in bare-metal and RTOS firmware - ESP32/ESP-IDF, PlatformIO, Arduino, ARM Cortex-M, STM32 HAL/LL, Nordic nRF5/nRF Connect SDK, FreeRTOS
- `flutter-dart-code-review`: Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, Mob
- `flutter-reviewer`: Flutter and Dart code reviewer. Reviews Flutter code for widget best practices, state management patterns, Dart idioms, performance pitfalls, acce
- `go-build-resolver`: Go build and compilation error resolution specialist. Fixes build errors, vet issues, and linter warnings with minimal, surgical changes
- `go-reviewer`: Expert Go code reviewer for idiomatic code, concurrency, error handling, and performance. Ensures high standards and best practices in Go
- `go-specialist`: Expert Go specialist for idiomatic coding, patterns, security, testing, and automation. Your go-to guide for robust Go development
- `java-build-resolver`: Java/Maven/Gradle build, compilation, and dependency error resolution specialist. Fixes build errors, Java compiler errors, and Maven/Gradle issue
- `java-reviewer`: Expert Java and Spring Boot code reviewer specializing in layered architecture, JPA patterns, security, and concurrency. Use for all Java code cha
- `java-specialist`: Unified Java specialist for coding style, patterns, security, and testing. Covers Java 17+, Records, Streams, JUnit 5, and security best practices
- `jpa-patterns`: JPA/Hibernate patterns for entity design, query optimization, transactions, auditing, indexing, and pagination in Spring Boot
- `kotlin-build-resolver`: Kotlin/Gradle build, compilation, and dependency error resolution specialist. Fixes build errors, Kotlin compiler errors, and Gradle issues with m
- `kotlin-exposed-patterns`: JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pa
- `kotlin-ktor-patterns`: Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing
- `kotlin-reviewer`: Kotlin and Android/KMP code reviewer. Reviews Kotlin code for idiomatic patterns, coroutine safety, Compose best practices, clean architecture vio
- `kotlin-specialist`: Unified Kotlin specialist for style, architecture, coroutines, security, and testing. Covers ktlint, MVVM, Flows, and Kotest
- `laravel-patterns`: Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps
- `laravel-security`: Laravel security best practices for authn/authz, validation, CSRF, mass assignment, file uploads, secrets, rate limiting, and secure deployment
- `laravel-tdd`: Test-driven development for Laravel with PHPUnit and Pest, factories, database testing, fakes, and coverage targets
- `laravel-verification`: Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness
- `macos-spatial-metal-engineer`: Native Swift and Metal specialist building high-performance 3D rendering systems and spatial computing experiences for macOS and Vision Pro
- `mobile-specialist`: Expert mobile developer for native (iOS/Android) and cross-platform apps, including on-device AI integration with Apple's FoundationModels
- `perl-specialist`: Comprehensive Perl specialist for modern Perl 5.36+, including coding style, patterns, security, testing, and architecture
- `php-specialist`: Unified PHP specialist for coding style, architecture, security, and testing. Covers PSR-12, DTOs, PHPUnit/Pest, and security best practices
- `python-reviewer`: Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance for all Python code changes
- `python-specialist`: Comprehensive Python specialist for coding style, patterns, testing, security, and automation hooks following PEP 8 and modern best practices
- `pytorch-specialist`: Unified PyTorch specialist for development patterns, best practices, and runtime/CUDA error resolution
- `rust-build-resolver`: Specialist in resolving Rust build, compilation, and dependency errors. Fixes borrow checker, lifetime, and Cargo.toml issues with surgical chan
- `rust-reviewer`: Expert Rust reviewer specializing in safety, idiomatic patterns, and performance. Focuses on ownership, error handling, and unsafe usage
- `rust-specialist`: Expert Rust developer proficient in ownership, error handling, traits, async, and performance optimization. Adheres to strict safety and idiomat
- `springboot-specialist`: Unified Spring Boot specialist for architecture, security, TDD, and verification. Covers REST APIs, Spring Security, and production verification
- `swift-advanced-patterns`: Advanced Swift patterns: actor-based persistence, Swift 6.2 concurrency, and protocol-based dependency injection for testing
- `swift-specialist`: Comprehensive guide for Swift development: coding style, patterns, security, testing, and automation hooks
- `swiftui-patterns`: SwiftUI architecture patterns: state management with @Observable, view composition, navigation, and performance optimization
- `typescript-reviewer`: Expert TypeScript code reviewer ensuring type safety, async correctness, security, and idiomatic patterns in TS/JS codebases
- `typescript-specialist`: Expert TypeScript specialist providing guidance on coding style, hooks, patterns, security, and testing for high-quality TS/JS development
- `visionos-spatial-engineer`: Expert in native visionOS spatial computing, SwiftUI volumetric interfaces, and Liquid Glass design implementation

### Shell & Scripting
- `bash-script-generator`: Write robust, POSIX-compliant bash scripts
- `cli-command-explainer`: Deeply explain obscure terminal commands/flags
- `engineering-git-workflow-master`: Expert in Git workflows, branching strategies, and version control best practices including conventional commits, rebasing, worktrees, and CI-frie
- `git-workflow`: Standard Git workflow: conventional commits, PR process, and recovery strategies
- `pr-template`: Generate a Pull Request template for a repository
- `terminal-integration-specialist`: Terminal emulation, text rendering optimization, and SwiftTerm integration for modern Swift applications

### Engineering Management & Workflow
- `automation-governance-architect`: Governance-first architect for business automations (n8n-first) who audits value, risk, and maintainability before implementation
- `chief-of-staff`: Personal communication chief of staff for triaging email, Slack, and messaging apps into a 4-tier system with automated draft replies
- `compliance-auditor`: Technical compliance auditor specializing in SOC 2, ISO 27001, HIPAA, and PCI-DSS readiness assessments and evidence collection
- `dev-workflow-specialist`: Orchestrator for the full development lifecycle, from discovery and strategy to build, hardening, and operation. Manages the NEXUS pipeline
- `executive-brief`: High-level executive summary of the Autonomous Pipeline orchestration framework and its strategic impact
- `handoff-templates`: NEXUS Handoff Templates for standardized agent-to-agent work transfers, QA feedback, escalations, and phase gates
- `product-behavioral-nudge-engine`: Behavioral psychology specialist that adapts software interaction cadences and styles to maximize user motivation and success
- `product-feedback-synthesizer`: Expert in collecting, analyzing, and synthesizing user feedback from multiple channels to extract actionable product insights
- `product-manager`: Holistic product leader managing the full lifecycle from discovery and strategy to roadmap, stakeholder alignment, and go-to-market
- `product-trend-researcher`: Expert market intelligence analyst specializing in identifying emerging trends, competitive analysis, and opportunity assessment
- `project-guidelines`: Example project-specific skill template based on a real production application
- `project-management-master`: Comprehensive project management lead specializing in agile, Jira/Git workflows, experimentation, operations, and portfolio strategy
- `project-manager-senior`: Converts specs to tasks and remembers previous projects
- `rapid-prototyper`: Senior rapid prototyping engineer specializing in high-fidelity prototypes, interaction design, and iterative front-end development
- `rules-distill`: Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files
- `specialized-cultural-intelligence-strategist`: CQ specialist detecting invisible exclusion and ensuring software resonates authentically across diverse global and intersectional identities
- `specialized-developer-advocate`: Expert developer advocate specializing in community building, technical content creation, and optimizing developer experience (DX)
- `specialized-french-consulting-market`: Guide to the French IT consulting market, covering ESN margin models, freelance platforms, portage salarial, and rate positioning
- `specialized-korean-business-navigator`: Guide to Korean business culture for professionals, covering the pumi decision process, nunchi, etiquette, and hierarchy navigation
- `strategic-compact`: Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction
- `team-builder`: Interactive agent picker for composing and dispatching parallel teams
- `unified-workflow-strategy`: Complete operational playbook for multi-agent orchestration and autonomous pipeline deployment
- `verification-loop`: A comprehensive verification system for the AI agent sessions
- `workflow-master`: Master workflow specialist for planning, handoffs, scenario runbooks, and cross-functional use cases

### Documentation & Learning
- `academic-researcher`: Multidisciplinary academic expert in anthropology, geography, history, narratology, and psychology for holistic world-building and analysis
- `article-writing`: Expert long-form writer specialized in blog posts, tutorials, and newsletters with a focus on distinct, human-sounding voices and structured copy
- `crosspost`: Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never pos
- `doc-updater`: Documentation and codemap specialist. Use PROACTIVELY for updating codemaps and documentation. Runs /update-codemaps and /update-docs, generates d
- `docs-lookup`: When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and
- `eli5`: Explain like I'm 5 (simple explanations)
- `learning-path`: Create learning roadmaps
- `narrative-designer`: Story systems and dialogue architect - Masters GDD-aligned narrative design, branching dialogue, lore architecture, and environmental storytelling
- `simplify-jargon`: Simplify technical jargon
- `technical-writing-specialist`: Expert technical writer for developer docs, API references, tutorials, and technical blogs. Bridges the gap between engineers and users

---

## Template Authoring Guide
All templates live in `commands/prompts/` as `.toml` files.

### Required Schema
```toml
description      = "A concise, one-sentence description ending with a period."
args_description = "A friendly label for the primary input."
version          = "1.0.0"
last_updated     = "YYYY-MM-DD"
tags             = ["category"]
sensitive        = false
prompt           = """
# Template Title
Clear, actionable instructions.
<if language="python">
Python-specific patterns here.
</if>
## Input
```
{{args}}
```
"""
```

---
*promptbook is open source under the MIT License.*
