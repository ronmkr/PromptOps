use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PromptMetadata {
    pub name: String,
    pub display_name: String,
    pub description: String,
    pub args_description: String,
    pub version: String,
    pub last_updated: String,
    pub tags: Vec<String>,
    pub sensitive: bool,
    pub version_id: Option<String>,
    pub path: String,
    pub category: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Prompt {
    pub metadata: PromptMetadata,
    pub prompt: String,
    pub system_prompt: String,
    pub user_prompt: String,
    pub raw_data: HashMap<String, serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContextProfile {
    pub name: String,
    pub variables: HashMap<String, String>,
}
