# TO-DO
## Project Identity and Messaging
- [x] **Define Project Identity**: Decided: Developer-focused (Developers, Architects, Data Engineers). Influenced README tagline, GEMINI.md intro, and project messaging.
- [x] **Craft a Clear One-Sentence Pitch**: "Promptbook is a structured library of 150+ expert prompt templates for AI CLI tools — organized, versioned, and ready to use."
- [x] **Update README**:
    - [x] Add the new one-liner pitch at the top.
    - [x] Include a GIF/screenshot of the TUI in action (Placeholder linked).
    - [x] Provide 3 concrete examples of a prompt being used.
- [x] **Update GEMINI.md**:
    - [x] Use the developer-focused intro.
    - [x] Add developer-centric categories (AI Agents, Language Specialists, Engineering Management, etc.).
    - [x] Update variable reference to include dynamic context.
- [x] **Create CLAUDE.md**: Created in the root to provide a first-class experience for Claude Code users.

## Distribution and Discoverability
- [x] **Implement Zero-Friction Install:**
    - [ ] `brew install promptbook` for macOS users.
    - [ ] `cargo install promptbook` for Rust/Linux users.
    - [ ] `pip install promptbook` for Python users.
    - [x] `curl -fsSL https://raw.githubusercontent.com/ronmkr/Promptbook/main/scripts/install.sh | bash` as a universal installer.
- [ ] **Publish to Package Registries:**
    - Publish the Python CLI to PyPI as `promptbook`.
    - Publish the Rust TUI to `crates.io`.
    - Create a Homebrew tap and formula.
- [ ] **Create a Web Presence:**
    - [ ] Set up a GitHub Pages site for the project.
    - [ ] Auto-generate a searchable and filterable catalog from TOML metadata.

## Community and Engagement
- [ ] **Build Community Infrastructure:**
    - [ ] Enable the GitHub Discussions tab.
    - [ ] Create a Discord server.
- [ ] **Add Social Proof and Showcase:**
    - [ ] Add a "Used by" or "Featured in" section to the README.
    - [ ] Include testimonials.
- [ ] **Create a Template Changelog:**
    - [ ] Maintain a `TEMPLATES.md` changelog.

## Technical Improvements
- [x] **Abstract the Eval Framework**: Modified `make evaluate` to support any OpenAI-compatible endpoint, with fallback to Gemini.
- [ ] **Consolidate Workflow Prompts:**
    - [ ] Review and consolidate prompts in the `workflow/` directory.
- [x] **Dynamic Context Execution**: Extended Python/Rust parser to evaluate `{{$(cmd)}}` and `{{env.VAR}}` right before hydration.
- [x] **Responsive TUI Focus Feedback**: Implemented visual dimming for unfocused panes and highlighted selected items for better UX.
- [ ] **Model Context Protocol (MCP) Integration**: Wrap library in a lightweight MCP server.
- [ ] **Expand the Pre-Commit Configuration**: Include strict TOML linting (taplo).
- [x] **Breaking Downstream Workflows (The Pathing Issue)**: Implemented `redirects.json` strategy to handle directory reorganization without breaking old paths.

## 🛡️ Security and Best Practices
- [x] **Formalize Security Guidelines**: Created `SECURITY.md` with mandatory checks and secret management protocols.
- [x] **Emergency Response Prompt**: Implemented `security-reviewer` template for rapid incident audit.
- [x] **Strict Metadata Validation**: Enforced via `scripts/validate_prompts.py` and pre-commit hooks.
- [x] **Automated Linting**: Integrated `taplo` (TOML), `ruff` (Python), and `rust-fmt`/`clippy` (Rust) into CI/CD and pre-commit.

## 🚧 Safety and Robustness
- [ ] **The "Agnostic" Dilution Trap**: Introduce tool-specific execution flags (e.g., `[tool_overrides.claude]`).
- [ ] **TOML String Escaping (Prompt Injection)**: Ensure parsing logic sanitizes/escapes triple quotes in payloads.
- [ ] **Dual-Client Feature Drift**: Consider consolidating logic into a single core engine (likely Rust).
