use rmcp::{
    ErrorData as McpError, RoleServer, ServerHandler, ServiceExt,
    model::*,
    service::RequestContext,
};
use promptbook_core::{get_prompts_dir, TemplateEngine};
use serde_json::{json, Map, Value};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{stdin, stdout};
use anyhow::Result;

#[derive(Clone)]
struct PromptBookServer {
    engine: TemplateEngine,
}

impl PromptBookServer {
    fn new() -> Self {
        let prompts_dir = get_prompts_dir();
        Self {
            engine: TemplateEngine::new(&prompts_dir.to_string_lossy()),
        }
    }

    fn to_map(v: Value) -> Arc<Map<String, Value>> {
        match v {
            Value::Object(m) => Arc::new(m),
            _ => Arc::new(Map::new()),
        }
    }
}

impl ServerHandler for PromptBookServer {
    fn get_info(&self) -> InitializeResult {
        let caps = ServerCapabilities::builder()
            .enable_resources()
            .enable_tools()
            .build();
        
        let mut result = InitializeResult::new(caps);
        result.server_info = Implementation::new("promptbook-server", "0.1.0");
        result.protocol_version = ProtocolVersion::LATEST;
        result
    }

    // --- Resources: Read raw templates ---
    async fn list_resources(
        &self,
        _request: Option<PaginatedRequestParams>,
        _context: RequestContext<RoleServer>,
    ) -> Result<ListResourcesResult, McpError> {
        let prompts = self.engine.get_all_prompts();
        let resources = prompts
            .into_iter()
            .map(|p| {
                let uri = format!("promptbook://prompts/{}", p.name);
                RawResource::new(uri, p.description).no_annotation()
            })
            .collect();

        Ok(ListResourcesResult {
            resources,
            next_cursor: None,
            meta: None,
        })
    }

    async fn read_resource(
        &self,
        request: ReadResourceRequestParams,
        _context: RequestContext<RoleServer>,
    ) -> Result<ReadResourceResult, McpError> {
        let name = request.uri.strip_prefix("promptbook://prompts/").ok_or_else(|| {
            McpError::invalid_params("Invalid promptbook URI", None)
        })?;

        match self.engine.load_prompt(name, None) {
            Ok(prompt) => {
                Ok(ReadResourceResult::new(vec![ResourceContents::text(prompt.prompt, &request.uri)]))
            },
            Err(_) => Err(McpError::resource_not_found("Prompt not found", None)),
        }
    }

    // --- Tools: List and Hydrate prompts ---
    async fn list_tools(
        &self,
        _request: Option<PaginatedRequestParams>,
        _context: RequestContext<RoleServer>,
    ) -> Result<ListToolsResult, McpError> {
        let list_tool = Tool::new(
            "list_prompts",
            "List all available prompt templates in PromptBook",
            Self::to_map(json!({
                "type": "object",
                "properties": {
                    "tag": { "type": "string", "description": "Filter by category tag" }
                }
            }))
        );

        let get_tool = Tool::new(
            "get_prompt",
            "Hydrate and return a prompt template by name",
            Self::to_map(json!({
                "type": "object",
                "properties": {
                    "name": { "type": "string", "description": "Name of the prompt" },
                    "arguments": { 
                        "type": "object", 
                        "description": "Variable values to inject into the template (e.g., {{args}})" 
                    }
                },
                "required": ["name"]
            }))
        );

        Ok(ListToolsResult {
            tools: vec![list_tool, get_tool],
            next_cursor: None,
            meta: None,
        })
    }

    async fn call_tool(
        &self,
        request: CallToolRequestParams,
        _context: RequestContext<RoleServer>,
    ) -> Result<CallToolResult, McpError> {
        match request.name.as_ref() {
            "list_prompts" => {
                let tag_filter = request.arguments.as_ref()
                    .and_then(|m| m.get("tag"))
                    .and_then(|v| v.as_str());
                
                let mut prompts = self.engine.get_all_prompts();
                
                if let Some(tag) = tag_filter {
                    let tag_lower = tag.to_lowercase();
                    prompts.retain(|p| p.tags.iter().any(|t| t.to_lowercase() == tag_lower));
                }

                let response_text = prompts
                    .iter()
                    .map(|p| format!("- {} : {}", p.name, p.description))
                    .collect::<Vec<_>>()
                    .join("\n");

                Ok(CallToolResult::success(vec![Content::text(response_text)]))
            }
            "get_prompt" => {
                let name = request.arguments.as_ref()
                    .and_then(|m| m.get("name"))
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| McpError::invalid_params("Missing prompt name", None))?;
                
                let prompt_data = self.engine.load_prompt(name, None)
                    .map_err(|e| McpError::resource_not_found(e.to_string(), None))?;

                let mut vars = HashMap::new();
                if let Some(args_obj) = request.arguments.as_ref()
                    .and_then(|m| m.get("arguments"))
                    .and_then(|v| v.as_object()) {
                    for (k, v) in args_obj {
                        vars.insert(k.clone(), v.as_str().unwrap_or_default().to_string());
                    }
                }

                let hydrated = TemplateEngine::hydrate(&prompt_data.prompt, &vars, false);
                
                Ok(CallToolResult::success(vec![Content::text(hydrated)]))
            }
            _ => Err(McpError::method_not_found::<CallToolRequestMethod>()),
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let transport = (stdin(), stdout());
    let service = PromptBookServer::new();
    let server = service.serve(transport).await?;
    server.waiting().await?;
    Ok(())
}
