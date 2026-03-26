# promptbook TUI

A high-performance, Rust-based Terminal User Interface (TUI) for browsing and using prompts from the promptbook library. Built with `ratatui` and `crossterm`.

## Features

- **Real-time Fuzzy Search:** Instantly find prompts by name, description, or tags.
- **Adaptive Layout:** Responsive 3-pane (large), 2-pane (medium), or 1-pane (small) layouts based on terminal width.
- **Interactive Hydration:** Step-by-step variable entry with multi-line support and back-navigation.
- **Version Management:** Easily switch between different versions of the same prompt.
- **Security First:** Explicit confirmation modals for prompts marked as `sensitive`.
- **Clipboard Integration:** Automatic copying of hydrated prompts for use in any AI tool.

## Internal Architecture

The codebase is modularized for better maintainability:

- `src/model/`: Data structures for prompts, groups, and application state.
- `src/ui/`: Rendering logic organized into components (header, footer, panes, modals).
- `src/events/`: Specialized input handlers for navigation, search, and modal interactions.
- `src/hydrate.rs`: Core logic for variable extraction and template hydration.
- `src/loader.rs`: Filesystem interaction for loading TOML templates.

## Installation

The TUI is built using Cargo. If you have Rust installed, the `pop` command will offer to build it for you automatically.

To build manually:
```bash
cd promptbook-tui
cargo build --release
```

The binary will be located at `target/release/promptbook-tui`.

## Usage

Run the TUI directly:
```bash
./target/release/promptbook-tui
```
Or use the `pop` wrapper from the root:
```bash
./promptbook
```
