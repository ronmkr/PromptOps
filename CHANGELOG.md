# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-24
### Added
- **Project Identity**: Refined focus as a developer-centric library (Developers, Architects, Data Engineers).
- **Dynamic Context**: Implemented `{{$(cmd)}}` and `{{env.VAR}}` resolution in both Python CLI and Rust TUI.
- **TUI Improvements**: Added responsive focus feedback. Selected items, borders, and background highlights dim when a pane loses focus or a modal is active for absolute visual priority.
- **CLAUDE.md**: Added first-class support and documentation for Claude Code users.
- **New Categories**: AI Agents, Backend & Systems, Language Specialists (Rust, Go, Swift, etc.).
### Changed
- **Documentation Sync**: Enhanced `scripts/sync_all_docs.py` to auto-generate catalogs across GEMINI.md, README.md, and CLAUDE.md.
- **Path Deprecation**: Implemented `redirects.json` strategy for backward compatibility during directory reorganization.

## [1.0.0] - 2026-03-21
### Added
- Expanded library with new high-value prompt templates.
- Added support for universal AI CLI tools (Claude Code, Aider, etc.).
- Created specialized categories: DevOps, Security, Database, Frontend, Agile.
- Added `/prompts:prompt-versioning` tool.
- Consistent metadata and formatting across all prompts.
### Changed
- Reorganized directory structure for better tool compatibility.
- Fixed TOML syntax and escape character issues.
- Updated documentation for multi-tool usage.
