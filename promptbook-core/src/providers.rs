use crate::config::StoragePaths;
use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;

/// Secure storage for API keys using the OS-native keyring or a local fallback.
pub struct Vault;

impl Vault {
    /// Stores an API key for a specific provider securely.
    pub fn set_key(provider: &str, key: &str) -> Result<()> {
        // 1. Try OS keyring first (Secure)
        let entry = keyring::Entry::new("promptbook", provider)?;
        match entry.set_password(key) {
            Ok(_) => return Ok(()),
            Err(e) => {
                eprintln!("Warning: Could not save to OS keyring: {}. Falling back to local vault.", e);
            }
        }

        // 2. Fallback to local JSON (Legacy)
        let vault_file = StoragePaths::vault_file();
        if let Some(parent) = vault_file.parent() {
            fs::create_dir_all(parent)?;
        }

        let mut data: HashMap<String, String> = if vault_file.exists() {
            let content = fs::read_to_string(&vault_file)?;
            serde_json::from_str(&content).unwrap_or_default()
        } else {
            HashMap::new()
        };

        data.insert(provider.to_string(), key.to_string());
        let content = serde_json::to_string(&data)?;
        fs::write(vault_file, content)?;
        Ok(())
    }

    /// Retrieves an API key for a specific provider.
    pub fn get_key(provider: &str) -> Option<String> {
        // 1. Check OS keyring first
        if let Ok(entry) = keyring::Entry::new("promptbook", provider) {
            if let Ok(pw) = entry.get_password() {
                return Some(pw);
            }
        }

        // 2. Fallback to local JSON
        let vault_file = StoragePaths::vault_file();
        if !vault_file.exists() {
            return None;
        }

        let content = fs::read_to_string(vault_file).ok()?;
        let data: HashMap<String, String> = serde_json::from_str(&content).ok()?;
        data.get(provider).cloned()
    }

    /// Lists all providers that have keys stored in the legacy local vault.
    pub fn list_keys() -> Vec<String> {
        // Since keyring doesn't support easy listing without iteration,
        // we mainly list what's in the local vault for now, 
        // or we could store a manifest. For now, let's just use local vault.
        let vault_file = StoragePaths::vault_file();
        if !vault_file.exists() {
            return Vec::new();
        }

        let content = fs::read_to_string(vault_file).unwrap_or_default();
        let data: HashMap<String, String> = serde_json::from_str(&content).unwrap_or_default();
        data.keys().cloned().collect()
    }

    /// Deletes a key for a specific provider from both the OS keyring and local vault.
    pub fn delete_key(provider: &str) -> bool {
        let mut success = false;
        
        // 1. Delete from OS keyring
        if let Ok(entry) = keyring::Entry::new("promptbook", provider) {
            success = entry.delete_password().is_ok();
        }

        // 2. Delete from local JSON
        let vault_file = StoragePaths::vault_file();
        if vault_file.exists() {
            if let Ok(content) = fs::read_to_string(&vault_file) {
                let mut data: HashMap<String, String> = serde_json::from_str(&content).unwrap_or_default();
                if data.remove(provider).is_some() {
                    if let Ok(content) = serde_json::to_string(&data) {
                        success = fs::write(vault_file, content).is_ok() || success;
                    }
                }
            }
        }
        success
    }
}

pub struct LLMProvider;

/// Internal request structure for OpenAI-compatible APIs.
#[derive(Serialize)]
struct OpenAIRequest {
    /// The model ID to use for completion.
    model: String,
    /// The conversation history or prompt.
    messages: Vec<ChatMessage>,
}

/// A single message in a chat conversation.
#[derive(Serialize, Deserialize)]
struct ChatMessage {
    /// The role (system, user, assistant).
    role: String,
    /// The content of the message.
    content: String,
}

/// Internal response structure from OpenAI-compatible APIs.
#[derive(Deserialize)]
struct OpenAIResponse {
    /// List of completion choices returned by the model.
    choices: Vec<OpenAIChoice>,
}

/// A single completion choice in the response.
#[derive(Deserialize)]
struct OpenAIChoice {
    /// The message content of the choice.
    message: ChatMessage,
}

impl LLMProvider {
    pub fn execute(prompt: &str, system_prompt: Option<&str>) -> Result<String> {
        let mut api_key = std::env::var("OPENAI_API_KEY").ok();
        if api_key.is_none() {
            api_key = Vault::get_key("openai");
        }

        let mut base_url = std::env::var("OPENAI_BASE_URL")
            .unwrap_or_else(|_| "https://api.openai.com/v1/".to_string());
        let mut model_id =
            std::env::var("OPENAI_MODEL_NAME").unwrap_or_else(|_| "gpt-4o".to_string());

        // Fallback to Gemini if requested or no OpenAI key
        let mut gemini_key = std::env::var("GEMINI_API_KEY").ok();
        if gemini_key.is_none() {
            gemini_key = Vault::get_key("gemini");
        }

        if api_key.is_none() && gemini_key.is_some() {
            api_key = gemini_key;
            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/".to_string();
            model_id = "gemini-2.0-flash".to_string();
        }

        let key = api_key.context("Neither OPENAI_API_KEY nor GEMINI_API_KEY is set")?;

        let mut messages = Vec::new();
        if let Some(sys) = system_prompt {
            if !sys.is_empty() {
                messages.push(ChatMessage {
                    role: "system".to_string(),
                    content: sys.to_string(),
                });
            }
        }
        messages.push(ChatMessage {
            role: "user".to_string(),
            content: prompt.to_string(),
        });

        let client = reqwest::blocking::Client::new();
        let resp = client
            .post(format!("{}chat/completions", base_url))
            .header("Authorization", format!("Bearer {}", key))
            .json(&OpenAIRequest {
                model: model_id,
                messages,
            })
            .send()?;

        if !resp.status().is_success() {
            let status = resp.status();
            let err_text = resp.text()?;
            return Err(anyhow::anyhow!("API Error ({}): {}", status, err_text));
        }

        let data: OpenAIResponse = resp.json()?;
        data.choices
            .first()
            .map(|c| c.message.content.clone())
            .context("No completion choices returned from API")
    }
}
