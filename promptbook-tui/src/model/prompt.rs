use serde::Deserialize;
use std::collections::HashMap;

#[derive(Debug, Clone, Deserialize)]
pub struct Prompt {
    #[serde(default)]
    pub name: String,
    #[serde(default)]
    pub version_id: Option<String>, // e.g. "v1", "v2"
    #[serde(default)]
    pub description: String,
    #[serde(default)]
    pub args_description: String,
    #[serde(default)]
    pub version: String,
    #[serde(default)]
    pub last_updated: String,
    #[serde(default)]
    pub tags: Vec<String>,
    #[serde(default)]
    pub sensitive: bool,
    #[serde(default)]
    pub prompt: String,
    #[serde(default)]
    pub system_prompt: String,
    #[serde(default)]
    pub user_prompt: String,
    #[serde(flatten)]
    pub metadata: HashMap<String, toml::Value>,
}

#[derive(Debug, Clone)]
pub struct PromptGroup {
    pub name: String,
    pub versions: Vec<Prompt>,
    pub selected_version_index: usize,
}

#[derive(Debug, Clone)]
pub enum Action {
    CopyPrompt(String),
}

pub struct ConfirmationModal {
    pub title: String,
    pub message: String,
    pub action: Action,
}

pub struct InputModal {
    pub prompt_name: String,
    pub version_id: Option<String>,
    pub variables: Vec<String>,
    pub current_var_index: usize,
    pub values: HashMap<String, String>,
    pub input_buffer: String,
    pub args_description: String,
    pub error_message: Option<String>,
}
