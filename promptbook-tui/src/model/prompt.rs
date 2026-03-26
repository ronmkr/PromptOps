use std::collections::HashMap;
pub use promptbook_core::Prompt;

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
