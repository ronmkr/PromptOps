# promptbook TUI

A high-performance, Rust-based Terminal User Interface (TUI) for browsing and using prompts from the promptbook library.

## Features

- **Real-time Fuzzy Search:** Instantly find prompts by name, description, or tags.
- **Syntax Highlighting:** Live previews of prompt templates.
- **Clipboard Integration:** Quickly copy prompts to use in any AI agent.
- **Zero-Config:** Automatically finds the `commands/prompts/` directory.

## Installation

The TUI is built using Cargo. If you have Rust installed, the `pop` command will offer to build it for you.

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
Or use the `pop` helper from the root:
```bash
./promptbook
```
