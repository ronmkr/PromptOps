# promptbook

**Promptbook is a structured library of 150+ expert prompt templates for AI CLI tools — organized, versioned, and ready to use.**

[![Validated Prompts](https://github.com/ronmkr/promptbook/actions/workflows/validate-prompts.yml/badge.svg)](https://github.com/ronmkr/promptbook/actions/workflows/validate-prompts.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Install

Get up and running in seconds with our universal installer:

```bash
curl -fsSL https://raw.githubusercontent.com/ronmkr/Promptbook/main/scripts/install.sh | bash
```

*This clonse the library to `~/.promptbook` and sets up the `pop` alias in `~/.local/bin`.*

## 🔍 What is this?

**promptbook** is a curated collection of standardized, high-quality prompt templates designed specifically for **developers, architects, and data engineers**. It provides a unified interface to discover and use prompts across any AI agent or CLI tool (Gemini, Claude Code, Aider, etc.).

Unlike loose collections of snippets, Promptbook treats prompts as **first-class code assets** with metadata, versioning, dynamic context resolution, and conditional extraction.

## 💡 Why do I need it?

- **Consistency**: Stop reinventing the prompt. Use battle-tested templates for security audits, architectural reviews, and debugging.
- **Context Awareness**: Templates use dynamic variables like `{{file}}`, `{{language}}`, and `{{context}}` to inject your project's state automatically.
- **Dynamic Execution**: Pull live system context into your prompts using `{{$(git diff)}}` or `{{env.AWS_REGION}}`.
- **Context Efficiency**: Surgical extraction using `<if language="...">` blocks ensures the AI only sees what it needs, reducing token bloat.
- **Portability**: Write a prompt once, use it everywhere—in your terminal, in your IDE extension, or in web-based LLMs.

## 🖥 What does it look like?

### The TUI Explorer
Lightning-fast fuzzy search and interactive variable hydration directly in your terminal.

![Promptbook TUI Demo](https://raw.githubusercontent.com/ronmkr/promptbook/main/docs/assets/tui-demo.gif)
*(Run `make tui` to launch)*

### Usage Examples

**1. Security Audit (with Language Context)**
```bash
# Review a Python file for vulnerabilities, ignoring irrelevant logic
pop use security-scan --language python --args @main.py
```

**2. Dynamic Architectural Context**
```bash
# Generate a summary based on the current git state
pop use pr-template --args "{{$(git diff HEAD)}}"
```

**3. Debugging Stack Traces**
```bash
# Analyze a log file to find root cause and suggest fixes
cat server.log | pop use debug-error
```

## 🚀 Key Features

- **Massive Catalog:** 180+ unique prompts across Engineering, Security, AI, DevOps, and specialized developer domains.
- **Dynamic Context:** Support for dynamic shell execution `{{$(cmd)}}` and environment variables `{{env.VAR}}`.
- **Conditional Extraction:** Surgical prompt pruning using `<if language="...">` blocks to minimize context bloat.
- **TUI Browser:** A high-performance Rust-based TUI for browsing and previewing templates.
- **Native Integrations:** First-class support for Gemini CLI, Claude Code, and Aider.

## 🛠 Installation

```bash
git clone https://github.com/ronmkr/promptbook.git
cd promptbook
chmod +x promptbook
sudo ln -s $(pwd)/promptbook /usr/local/bin/pop
```

## 📂 Documentation

- [Full Prompt Catalog](docs/FULL_CATALOG.md)
- [Domain-Specific Catalogs](docs/catalog/README.md)
- [Gemini CLI Extension Guide](docs/agents/gemini.md)
- [Claude Code Integration](docs/agents/claude-code.md)
- [Aider & Web-LLM Usage](docs/agents/aider.md)

## Available Templates

Templates are categorized by domain. Click a category to view its full reference catalog.

### [AI Agents & Infrastructure](docs/catalog/ai-agents-and-infrastructure.md)
- `/prompts:agent-harness-architect` - Expert-level design and optimization of AI agent action spaces, tool definitions, and observation formatting for high completion rates
- `/prompts:agentic-identity-trust` - Architectural specialist for agentic identity, cryptographic trust verification, and verifiable audit trails in multi-agent environments
- `/prompts:agentic-principles` - Unified model for Agentic and AI-First Engineering. Focuses on eval-driven execution, task decomposition, and AI-assisted architecture
- `/prompts:ai-engineer-agent` - Expert AI/ML engineer for model development, deployment, and production integration. Focuses on scalable features and intelligent data pipelines
- `/prompts:autonomous-loop` - Unified guide for autonomous AI agent loops. Covers sequential pipelines, REPLs, infinite generation, PR loops, and RFC-driven DAG orchestration
- `/prompts:claude-devfleet-specialist` - Orchestrate multi-agent coding tasks via Claude DevFleet, enabling project planning, parallel agent dispatch, and automated progress monitoring
- `/prompts:common-agents` - Agent orchestration: available agents, parallel execution, multi-perspective analysis
- `/prompts:content-engine-specialist` - Create platform-native content systems for social media, newsletters, and repurposed campaigns. Ensures consistency and high impact across channels
- `/prompts:context-budget-specialist` - Audits the AI agent context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and produces
- `/prompts:data-consolidation-agent` - AI specialist for consolidating sales metrics into real-time reporting dashboards with territory, representative, and pipeline summaries
- `/prompts:enterprise-agent-ops-specialist` - Operate long-lived agent workloads with observability, security boundaries, and lifecycle management
- `/prompts:eval-harness` - Unified evaluation framework for AI agents, implementing eval-driven development (EDD), head-to-head benchmarking, and harness optimization
- `/prompts:llm-pipeline-specialist` - Unified specialist for LLM API integration and cost-aware pipelines. Covers Claude API, SDK patterns, model routing, and budget optimization
- `/prompts:mcp-master` - Unified MCP Master for designing, building, and deploying Model Context Protocol servers. Covers SDK patterns, tool design, and transport
- `/prompts:multi-agent-pipeline` - Unified Autonomous Pipeline Orchestration framework for high-velocity multi-agent development workflows
- `/prompts:observer` - Background agent that analyzes session observations to detect patterns and create instincts. Uses Haiku for cost-efficiency. v2.1 adds project-sco
- `/prompts:specialized-model-qa` - Independent model QA expert who audits ML and statistical models end-to-end - from documentation review and data reconstruction to replication, ca

### [Architecture & Design](docs/catalog/architecture-and-design.md)
- `/prompts:architect` - Senior software architect for system design, domain-driven design, scalability, and technical decision-making with ADR and C4 support
- `/prompts:architecture-decision-records` - Capture architectural decisions as structured ADR documents. Tracks context, alternatives, consequences, and decision status
- `/prompts:autonomous-optimization-architect` - System governor for autonomous API shadow-testing and optimization with financial and security guardrails
- `/prompts:design-patterns` - Comprehensive guide for selecting and implementing software design patterns. Includes code examples, trade-offs, and testing considerations

### [Code Review & Analysis](docs/catalog/code-review-and-analysis.md)
- `/prompts:code-reviewer-agent` - Comprehensive code review specialist for quality, security, and performance. Provides actionable feedback and constructive refactoring suggestions
- `/prompts:codebase-onboarding` - Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAU
- `/prompts:compare-technologies` - Framework for comparing software technologies, frameworks, and libraries with a focus on trade-offs, syntax, and performance
- `/prompts:continuous-learning-specialist` - Master specialist for the Continuous Learning system. Manages session observation, atomic instinct extraction, and knowledge evolution
- `/prompts:documentation-lookup` - Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples,
- `/prompts:engineering-standards-specialist` - Unified engineering standards for coding style, design patterns, automation hooks, and performance optimization across the development lifecycle
- `/prompts:engineering-threat-detection-engineer` - Expert detection engineer specializing in SIEM rule development, MITRE ATT&CK coverage mapping, threat hunting, alert tuning, and detection-as-cod
- `/prompts:error-resolution-agent` - Master specialist for diagnosing and resolving build, type, and runtime errors. Expert in root cause analysis and minimal-diff error fixing
- `/prompts:lsp-specialist` - Language Server Protocol specialist building unified code intelligence systems through LSP client orchestration and semantic indexing
- `/prompts:performance-profile` - Expert guide for performance profiling, bottleneck identification, and optimization across frontend, backend, and database layers
- `/prompts:prompt-specialist` - Master specialist for prompt engineering: optimize, create, improve, and manage the lifecycle of high-quality prompts and templates
- `/prompts:refactor-agent` - Expert refactoring specialist for code cleanup, dead code removal, duplicate elimination, and architectural improvements with a focus on safety
- `/prompts:regex-builder` - Generate and explain complex Regular Expressions
- `/prompts:regex-vs-llm-structured-text` - Decision framework for choosing between regex and LLM when parsing structured text — start with regex, add LLM only for low-confidence edge cases

### [DevOps & Infrastructure](docs/catalog/devops-and-infrastructure.md)
- `/prompts:bun-runtime` - Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support
- `/prompts:cloud-infrastructure-specialist` - Expert in cloud infrastructure (AWS/GCP/Azure) using Terraform and IAM. Focuses on security, least-privilege policies, and modular IaC
- `/prompts:container-orchestration-specialist` - Expert in containerization and orchestration using Docker and Kubernetes. Handles Dockerfiles, Compose, and Kubernetes manifests
- `/prompts:devops-specialist` - Expert DevOps/SRE specialist for CI/CD, IaC, SLOs, observability, and lifecycle management of long-lived agent workloads
- `/prompts:incident-response-specialist` - Expert incident commander for production management. Coordinates response, severity frameworks, blameless post-mortems, and on-call culture

### [Backend & Systems](docs/catalog/backend-and-systems.md)
- `/prompts:backend-architect-agent` - Senior backend architect specializing in scalable system design, database architecture, API development, and cloud infrastructure
- `/prompts:backend-specialist` - Expert backend architect for API design, database optimization, and scalable server-side patterns
- `/prompts:clickhouse-io` - ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads
- `/prompts:content-hash-cache-pattern` - Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation
- `/prompts:database-architect-agent` - Expert database architect for schema design, migrations, query optimization, and performance tuning. Specialized in SQL and NoSQL systems
- `/prompts:postgres-patterns` - PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices

### [Frontend & UI/UX](docs/catalog/frontend-and-ui-ux.md)
- `/prompts:frontend-specialist` - Comprehensive frontend specialist for modern web apps. Covers Accessibility, Tailwind, Next.js, Nuxt 4, React patterns, and performance
- `/prompts:image-prompt-engineer` - Expert in AI image prompt engineering and media generation via fal.ai MCP for images, video, and audio
- `/prompts:ui-ux-specialist` - Expert UI/UX specialist for design systems, user research, and Storybook component generation
- `/prompts:visual-design-specialist` - Comprehensive visual design expert covering brand identity, storytelling, inclusivity, Liquid Glass, and style presets
- `/prompts:xr-specialist` - Expert XR specialist for immersive AR/VR/XR experiences, spatial interaction design, and browser-based 3D applications

### [Security & Compliance](docs/catalog/security-and-compliance.md)
- `/prompts:blockchain-security-auditor` - Expert smart contract security auditor specializing in vulnerability detection, formal verification, and exploit analysis
- `/prompts:security-architect` - Expert security architect specializing in threat modeling, secure code review, and defense-in-depth across the entire application stack
- `/prompts:security-policy` - Draft a SECURITY.md or vulnerability disclosure policy
- `/prompts:security-reviewer` - Internal security auditor specialized in project-wide vulnerability assessment and emergency response
- `/prompts:security-scan` - Comprehensive, tool-agnostic security audit for codebases, configurations, and dependencies. Focused on OWASP, secrets, and supply-chain risks
- `/prompts:threat-modeling` - Generate a STRIDE threat model for a proposed architecture
- `/prompts:zk-steward` - Knowledge-base steward in the spirit of Niklas Luhmann's Zettelkasten. Default perspective: Luhmann; switches to domain experts (Feynman, Munger,

### [Testing & QA](docs/catalog/testing-and-qa.md)
- `/prompts:common-testing` - Testing requirements: 80% coverage, TDD workflow, test types
- `/prompts:e2e-runner` - End-to-end testing specialist using Vercel Agent Browser and Playwright for creating and maintaining reliable browser-based test suites
- `/prompts:e2e-testing` - Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies
- `/prompts:generate-e2e-tests` - Create end-to-end tests
- `/prompts:generate-unit-tests` - Create unit tests for code
- `/prompts:mock-data-gen` - Create realistic JSON/CSV mock data schemas for testing
- `/prompts:research` - Research Context
- `/prompts:review` - Code Review Context
- `/prompts:review-test-coverage` - Analyze test coverage gaps
- `/prompts:tdd-guide` - TDD specialist enforcing the write-tests-first methodology for new features, bug fixes, and refactoring with high coverage standards
- `/prompts:tdd-workflow` - Enforces TDD with 80%+ coverage for unit, integration, and E2E tests during feature development, bug fixes, and refactors
- `/prompts:test-edge-cases` - Identify and test edge cases
- `/prompts:testing` - Python Testing
- `/prompts:testing-specialist` - Comprehensive testing specialist covering AI regression patterns, accessibility, API validation, performance benchmarking, and QA workflows

### [Language Specialists](docs/catalog/language-specialists.md)
- `/prompts:android-clean-architecture` - Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, and data l
- `/prompts:compose-multiplatform-patterns` - Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-specific UI
- `/prompts:cpp-build-resolver` - Expert in resolving C++ build errors, CMake configuration issues, and linker warnings using surgical, minimal changes to restore project stability
- `/prompts:cpp-reviewer` - Senior C++ code reviewer focused on modern idioms, memory safety, concurrency, and performance to ensure high-quality and secure codebases
- `/prompts:cpp-specialist` - Unified C++ specialist for coding standards, style, patterns, security, and testing. Covers Modern C++, RAII, GoogleTest, and memory safety
- `/prompts:csharp-specialist` - Unified C# specialist for coding style, architectural patterns, security, and testing. Covers .NET conventions, async, xUnit, and security
- `/prompts:django-specialist` - Expert Django specialist for architecture patterns, REST APIs, TDD, security best practices, and comprehensive verification workflows
- `/prompts:engineering-embedded-firmware-engineer` - Specialist in bare-metal and RTOS firmware - ESP32/ESP-IDF, PlatformIO, Arduino, ARM Cortex-M, STM32 HAL/LL, Nordic nRF5/nRF Connect SDK, FreeRTOS
- `/prompts:flutter-dart-code-review` - Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider, GetX, Mob
- `/prompts:flutter-reviewer` - Flutter and Dart code reviewer. Reviews Flutter code for widget best practices, state management patterns, Dart idioms, performance pitfalls, acce
- `/prompts:go-build-resolver` - Go build and compilation error resolution specialist. Fixes build errors, vet issues, and linter warnings with minimal, surgical changes
- `/prompts:go-reviewer` - Expert Go code reviewer for idiomatic code, concurrency, error handling, and performance. Ensures high standards and best practices in Go
- `/prompts:go-specialist` - Expert Go specialist for idiomatic coding, patterns, security, testing, and automation. Your go-to guide for robust Go development
- `/prompts:java-build-resolver` - Java/Maven/Gradle build, compilation, and dependency error resolution specialist. Fixes build errors, Java compiler errors, and Maven/Gradle issue
- `/prompts:java-reviewer` - Expert Java and Spring Boot code reviewer specializing in layered architecture, JPA patterns, security, and concurrency. Use for all Java code cha
- `/prompts:java-specialist` - Unified Java specialist for coding style, patterns, security, and testing. Covers Java 17+, Records, Streams, JUnit 5, and security best practices
- `/prompts:jpa-patterns` - JPA/Hibernate patterns for entity design, query optimization, transactions, auditing, indexing, and pagination in Spring Boot
- `/prompts:kotlin-build-resolver` - Kotlin/Gradle build, compilation, and dependency error resolution specialist. Fixes build errors, Kotlin compiler errors, and Gradle issues with m
- `/prompts:kotlin-exposed-patterns` - JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pa
- `/prompts:kotlin-ktor-patterns` - Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication testing
- `/prompts:kotlin-reviewer` - Kotlin and Android/KMP code reviewer. Reviews Kotlin code for idiomatic patterns, coroutine safety, Compose best practices, clean architecture vio
- `/prompts:kotlin-specialist` - Unified Kotlin specialist for style, architecture, coroutines, security, and testing. Covers ktlint, MVVM, Flows, and Kotest
- `/prompts:laravel-patterns` - Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for production apps
- `/prompts:laravel-security` - Laravel security best practices for authn/authz, validation, CSRF, mass assignment, file uploads, secrets, rate limiting, and secure deployment
- `/prompts:laravel-tdd` - Test-driven development for Laravel with PHPUnit and Pest, factories, database testing, fakes, and coverage targets
- `/prompts:laravel-verification` - Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readiness
- `/prompts:macos-spatial-metal-engineer` - Native Swift and Metal specialist building high-performance 3D rendering systems and spatial computing experiences for macOS and Vision Pro
- `/prompts:mobile-specialist` - Expert mobile developer for native (iOS/Android) and cross-platform apps, including on-device AI integration with Apple's FoundationModels
- `/prompts:perl-specialist` - Comprehensive Perl specialist for modern Perl 5.36+, including coding style, patterns, security, testing, and architecture
- `/prompts:php-specialist` - Unified PHP specialist for coding style, architecture, security, and testing. Covers PSR-12, DTOs, PHPUnit/Pest, and security best practices
- `/prompts:python-reviewer` - Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance for all Python code changes
- `/prompts:python-specialist` - Comprehensive Python specialist for coding style, patterns, testing, security, and automation hooks following PEP 8 and modern best practices
- `/prompts:pytorch-specialist` - Unified PyTorch specialist for development patterns, best practices, and runtime/CUDA error resolution
- `/prompts:rust-build-resolver` - Specialist in resolving Rust build, compilation, and dependency errors. Fixes borrow checker, lifetime, and Cargo.toml issues with surgical chan
- `/prompts:rust-reviewer` - Expert Rust reviewer specializing in safety, idiomatic patterns, and performance. Focuses on ownership, error handling, and unsafe usage
- `/prompts:rust-specialist` - Expert Rust developer proficient in ownership, error handling, traits, async, and performance optimization. Adheres to strict safety and idiomat
- `/prompts:springboot-specialist` - Unified Spring Boot specialist for architecture, security, TDD, and verification. Covers REST APIs, Spring Security, and production verification
- `/prompts:swift-advanced-patterns` - Advanced Swift patterns: actor-based persistence, Swift 6.2 concurrency, and protocol-based dependency injection for testing
- `/prompts:swift-specialist` - Comprehensive guide for Swift development: coding style, patterns, security, testing, and automation hooks
- `/prompts:swiftui-patterns` - SwiftUI architecture patterns: state management with @Observable, view composition, navigation, and performance optimization
- `/prompts:typescript-reviewer` - Expert TypeScript code reviewer ensuring type safety, async correctness, security, and idiomatic patterns in TS/JS codebases
- `/prompts:typescript-specialist` - Expert TypeScript specialist providing guidance on coding style, hooks, patterns, security, and testing for high-quality TS/JS development
- `/prompts:visionos-spatial-engineer` - Expert in native visionOS spatial computing, SwiftUI volumetric interfaces, and Liquid Glass design implementation

### [Shell & Scripting](docs/catalog/shell-and-scripting.md)
- `/prompts:bash-script-generator` - Write robust, POSIX-compliant bash scripts
- `/prompts:cli-command-explainer` - Deeply explain obscure terminal commands/flags
- `/prompts:engineering-git-workflow-master` - Expert in Git workflows, branching strategies, and version control best practices including conventional commits, rebasing, worktrees, and CI-frie
- `/prompts:git-workflow` - Standard Git workflow: conventional commits, PR process, and recovery strategies
- `/prompts:pr-template` - Generate a Pull Request template for a repository
- `/prompts:terminal-integration-specialist` - Terminal emulation, text rendering optimization, and SwiftTerm integration for modern Swift applications

### [Engineering Management & Workflow](docs/catalog/engineering-management-and-workflow.md)
- `/prompts:automation-governance-architect` - Governance-first architect for business automations (n8n-first) who audits value, risk, and maintainability before implementation
- `/prompts:chief-of-staff` - Personal communication chief of staff for triaging email, Slack, and messaging apps into a 4-tier system with automated draft replies
- `/prompts:compliance-auditor` - Technical compliance auditor specializing in SOC 2, ISO 27001, HIPAA, and PCI-DSS readiness assessments and evidence collection
- `/prompts:dev-workflow-specialist` - Orchestrator for the full development lifecycle, from discovery and strategy to build, hardening, and operation. Manages the NEXUS pipeline
- `/prompts:executive-brief` - High-level executive summary of the Autonomous Pipeline orchestration framework and its strategic impact
- `/prompts:handoff-templates` - NEXUS Handoff Templates for standardized agent-to-agent work transfers, QA feedback, escalations, and phase gates
- `/prompts:product-behavioral-nudge-engine` - Behavioral psychology specialist that adapts software interaction cadences and styles to maximize user motivation and success
- `/prompts:product-feedback-synthesizer` - Expert in collecting, analyzing, and synthesizing user feedback from multiple channels to extract actionable product insights
- `/prompts:product-manager` - Holistic product leader managing the full lifecycle from discovery and strategy to roadmap, stakeholder alignment, and go-to-market
- `/prompts:product-trend-researcher` - Expert market intelligence analyst specializing in identifying emerging trends, competitive analysis, and opportunity assessment
- `/prompts:project-guidelines` - Example project-specific skill template based on a real production application
- `/prompts:project-management-master` - Comprehensive project management lead specializing in agile, Jira/Git workflows, experimentation, operations, and portfolio strategy
- `/prompts:project-manager-senior` - Converts specs to tasks and remembers previous projects
- `/prompts:rapid-prototyper` - Senior rapid prototyping engineer specializing in high-fidelity prototypes, interaction design, and iterative front-end development
- `/prompts:rules-distill` - Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files
- `/prompts:specialized-cultural-intelligence-strategist` - CQ specialist detecting invisible exclusion and ensuring software resonates authentically across diverse global and intersectional identities
- `/prompts:specialized-developer-advocate` - Expert developer advocate specializing in community building, technical content creation, and optimizing developer experience (DX)
- `/prompts:specialized-french-consulting-market` - Guide to the French IT consulting market, covering ESN margin models, freelance platforms, portage salarial, and rate positioning
- `/prompts:specialized-korean-business-navigator` - Guide to Korean business culture for professionals, covering the pumi decision process, nunchi, etiquette, and hierarchy navigation
- `/prompts:strategic-compact` - Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction
- `/prompts:team-builder` - Interactive agent picker for composing and dispatching parallel teams
- `/prompts:unified-workflow-strategy` - Complete operational playbook for multi-agent orchestration and autonomous pipeline deployment
- `/prompts:verification-loop` - A comprehensive verification system for the AI agent sessions
- `/prompts:workflow-master` - Master workflow specialist for planning, handoffs, scenario runbooks, and cross-functional use cases

### [Documentation & Learning](docs/catalog/documentation-and-learning.md)
- `/prompts:academic-researcher` - Multidisciplinary academic expert in anthropology, geography, history, narratology, and psychology for holistic world-building and analysis
- `/prompts:article-writing` - Expert long-form writer specialized in blog posts, tutorials, and newsletters with a focus on distinct, human-sounding voices and structured copy
- `/prompts:crosspost` - Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never pos
- `/prompts:doc-updater` - Documentation and codemap specialist. Use PROACTIVELY for updating codemaps and documentation. Runs /update-codemaps and /update-docs, generates d
- `/prompts:docs-lookup` - When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and
- `/prompts:eli5` - Explain like I'm 5 (simple explanations)
- `/prompts:learning-path` - Create learning roadmaps
- `/prompts:narrative-designer` - Story systems and dialogue architect - Masters GDD-aligned narrative design, branching dialogue, lore architecture, and environmental storytelling
- `/prompts:simplify-jargon` - Simplify technical jargon
- `/prompts:technical-writing-specialist` - Expert technical writer for developer docs, API references, tutorials, and technical blogs. Bridges the gap between engineers and users

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new templates to our hierarchical structure.

---
*promptbook is open source under the MIT License.*
