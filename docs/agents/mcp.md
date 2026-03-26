# Model Context Protocol (MCP) Integration

The PromptBook MCP Server allows you to expose the entire prompt library as **Tools** and **Resources** to any MCP-compliant AI agent, such as **Claude Desktop**, **Aider**, or **Cursor**.

## 🚀 Features

- **Prompt Discovery**: AI agents can search and list available templates.
- **Dynamic Hydration**: Agents can "call" a prompt as a tool, passing variables (like `{{args}}`) for real-time hydration.
- **Raw Access**: Direct access to the raw template TOML via `promptbook://` URIs.

## 🛠 Setup

### 1. Build the Server
Ensure you have the Rust toolchain installed, then build the MCP binary:
```bash
make mcp
# The binary will be at target/debug/promptbook-mcp (or target/release/promptbook-mcp if built with --release)
```

### 2. Configure Your Client

#### Claude Desktop
Add the following to your `claude_desktop_config.json`:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "promptbook": {
      "command": "/absolute/path/to/PromptBook/target/debug/promptbook-mcp",
      "args": []
    }
  }
}
```

#### Aider
Run Aider with the MCP server flag:
```bash
aider --mcp-server /absolute/path/to/PromptBook/target/debug/promptbook-mcp
```

## 🧰 Available Tools

### `list_prompts`
Returns a searchable list of all available templates in the PromptBook library.
- **Arguments**:
  - `tag` (optional): Filter by category (e.g., "security", "rust").

### `get_prompt`
Hydrates a specific template with provided arguments and returns the final text.
- **Arguments**:
  - `name`: The name of the prompt (e.g., `architect`).
  - `arguments`: A JSON object of variables to inject (e.g., `{"args": "my project logic"}`).

## 📂 Resources
You can also refer to prompts directly using their URI:
`promptbook://prompts/{name}`

Example: `promptbook://prompts/refactor-agent`

## 🧪 Testing the Connection
You can use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to verify the server:
```bash
npx @modelcontextprotocol/inspector /absolute/path/to/PromptBook/target/debug/promptbook-mcp
```
