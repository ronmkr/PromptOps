use crate::models::{Prompt, PromptMetadata};
use anyhow::{Context, Result};
use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;
use walkdir::WalkDir;

#[derive(Clone)]
pub struct TemplateEngine {
    pub prompts_dir: String,
}

impl TemplateEngine {
    pub fn new(prompts_dir: &str) -> Self {
        Self {
            prompts_dir: prompts_dir.to_string(),
        }
    }

    /// Parses a prompt file to extract metadata and the raw TOML content.
    fn parse_metadata(&self, path: &Path) -> Result<(PromptMetadata, toml::Value)> {
        let prompts_path = Path::new(&self.prompts_dir);
        let rel_path = path.strip_prefix(prompts_path).unwrap_or(path);
        let category = rel_path
            .parent()
            .and_then(|p| p.to_str())
            .filter(|s| !s.is_empty())
            .map(|s| s.to_string());

        let filename = path.file_stem().and_then(|s| s.to_str()).unwrap_or("");
        let mut name = filename.to_string();
        let mut version_id = None;

        if name.contains('.') {
            let parts: Vec<&str> = filename.split('.').collect();
            if let Some(n) = parts.first() {
                name = n.to_string();
            }
            if let Some(v) = parts.get(1) {
                version_id = Some(v.to_string());
            }
        }

        let content = fs::read_to_string(path)?;
        let data = toml::from_str::<toml::Value>(&content)?;

        let metadata = PromptMetadata {
            name: name.clone(),
            display_name: if let Some(ref vid) = version_id {
                format!("{}:{}", name, vid)
            } else {
                name.clone()
            },
            description: data
                .get("description")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            args_description: data
                .get("args_description")
                .and_then(|v| v.as_str())
                .unwrap_or("Input Data")
                .to_string(),
            version: data
                .get("version")
                .and_then(|v| v.as_str())
                .unwrap_or("1.0.0")
                .to_string(),
            last_updated: data
                .get("last_updated")
                .and_then(|v| v.as_str())
                .unwrap_or("")
                .to_string(),
            tags: data
                .get("tags")
                .and_then(|v| v.as_array())
                .map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(|s| s.to_string()))
                        .collect()
                })
                .unwrap_or_default(),
            sensitive: data.get("sensitive").and_then(|v| v.as_bool()).unwrap_or(false),
            version_id,
            path: path.to_str().unwrap_or("").to_string(),
            category,
        };
        Ok((metadata, data))
    }

    /// Loads a full prompt from a specific file path.
    fn load_prompt_from_path(&self, path: &Path) -> Result<Prompt> {
        let (metadata, data) = self.parse_metadata(path)?;

        let prompt_text = data
            .get("prompt")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_string();
        let system_prompt = data
            .get("system_prompt")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_string();
        let user_prompt = data
            .get("user_prompt")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_string();

        let mut raw_data = HashMap::new();
        if let Some(table) = data.as_table() {
            for (k, v) in table {
                let json_val = serde_json::to_value(v)?;
                raw_data.insert(k.clone(), json_val);
            }
        }

        Ok(Prompt {
            metadata,
            prompt: prompt_text,
            system_prompt,
            user_prompt,
            raw_data,
        })
    }

    /// Retrieves metadata for all available prompt templates.
    pub fn get_all_prompts(&self) -> Vec<PromptMetadata> {
        let mut all_prompts = Vec::new();
        let prompts_path = Path::new(&self.prompts_dir);

        if !prompts_path.exists() {
            return all_prompts;
        }

        for entry in WalkDir::new(prompts_path)
            .into_iter()
            .filter_map(|e| e.ok())
            .filter(|e| e.path().extension().is_some_and(|ext| ext == "toml"))
        {
            if let Ok((metadata, _)) = self.parse_metadata(entry.path()) {
                all_prompts.push(metadata);
            }
        }

        all_prompts
    }

    /// Loads all available prompts in a single pass.
    pub fn load_all_prompts(&self) -> Result<Vec<Prompt>> {
        let mut prompts = Vec::new();
        let prompts_path = Path::new(&self.prompts_dir);

        if !prompts_path.exists() {
            return Ok(prompts);
        }

        for entry in WalkDir::new(prompts_path)
            .into_iter()
            .filter_map(|e| e.ok())
            .filter(|e| e.path().extension().is_some_and(|ext| ext == "toml"))
        {
            if let Ok(prompt) = self.load_prompt_from_path(entry.path()) {
                prompts.push(prompt);
            }
        }

        Ok(prompts)
    }

    /// Loads a prompt by name and optional version ID.
    pub fn load_prompt(&self, name: &str, version_id: Option<&str>) -> Result<Prompt> {
        let prompts_path = Path::new(&self.prompts_dir);
        if !prompts_path.exists() {
            return Err(anyhow::anyhow!("Prompts directory not found"));
        }

        // Optimized lookup: try to find the file directly if it's a simple name
        // but since they are in categories, we might still need to walk or use a cache.
        // For now, let's keep get_all_prompts() but it's only called once per CLI command.
        let all_prompts = self.get_all_prompts();
        let metadata = all_prompts
            .into_iter()
            .find(|p| p.name == name && p.version_id.as_deref() == version_id)
            .context(format!("Prompt '{}' not found", name))?;

        self.load_prompt_from_path(Path::new(&metadata.path))
    }

    pub fn discover_variables(text: &str) -> HashSet<String> {
        let mut variables = HashSet::new();
        let re = match Regex::new(r"\{\{\s*([^{}]+?)\s*\}\}") {
            Ok(r) => r,
            Err(_) => return variables,
        };

        fn find_vars(content: &str, re: &Regex, variables: &mut HashSet<String>) {
            for cap in re.captures_iter(content) {
                if let Some(m) = cap.get(1) {
                    let var = m.as_str().trim();
                    if let Some(inner) = var.strip_prefix("$(").and_then(|s| s.strip_suffix(')')) {
                        find_vars(inner, re, variables);
                    } else if !var.starts_with("env.") {
                        variables.insert(var.to_string());
                    }
                }
            }
            let remaining = re.replace_all(content, "V");
            if remaining != content {
                find_vars(&remaining, re, variables);
            }
        }

        find_vars(text, &re, &mut variables);
        variables
    }

    pub fn hydrate(template: &str, variables: &HashMap<String, String>, mask: bool) -> String {
        let mut text = template.to_string();

        let vars = if mask {
            let mut masked = HashMap::new();
            for (k, v) in variables {
                masked.insert(k.clone(), Self::mask_pii(v));
            }
            masked
        } else {
            variables.clone()
        };

        // 1. Resolve conditionals
        text = Self::handle_conditionals(&text, &vars);
        text = Self::handle_existence_conditionals(&text, &vars);

        // 2. Protect and resolve shell blocks
        text = Self::resolve_shell_and_env(&text, &vars);

        // 3. Standard variable substitution
        for (key, val) in &vars {
            let pattern1 = format!("{{{{{}}}}}", key);
            let pattern2 = format!("{{{{ {} }}}}", key);
            text = text.replace(&pattern1, val);
            text = text.replace(&pattern2, val);
        }

        text.trim().to_string()
    }

    /// Masks PII (emails and phone numbers) in the given text.
    fn mask_pii(text: &str) -> String {
        let email_re = match Regex::new(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}") {
            Ok(r) => r,
            Err(_) => return text.to_string(),
        };
        let phone_re = match Regex::new(r"\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}") {
            Ok(r) => r,
            Err(_) => return text.to_string(),
        };
        
        let result = email_re.replace_all(text, "[EMAIL]").to_string();
        phone_re.replace_all(&result, "[PHONE]").to_string()
    }

    /// Handles basic equality conditionals in templates: <if key="value">content</if>
    fn handle_conditionals(text: &str, variables: &HashMap<String, String>) -> String {
        let cond_pattern = match Regex::new(r#"(?s)<if\s+(\w+)\s*=\s*"([^"]+)"\s*>(.*?)</if>"#) {
            Ok(r) => r,
            Err(_) => return text.to_string(),
        };
        let mut result = text.to_string();

        loop {
            let capture = if let Some(cap) = cond_pattern.captures(&result) {
                let m0 = cap.get(0).map(|m| m.range());
                let m1 = cap.get(1).map(|m| m.as_str());
                let m2 = cap.get(2).map(|m| m.as_str());
                let m3 = cap.get(3).map(|m| m.as_str());
                
                if let (Some(range), Some(key), Some(expected), Some(content)) = (m0, m1, m2, m3) {
                    let actual = variables
                        .get(key)
                        .map(|v| v.trim().to_lowercase())
                        .unwrap_or_default();

                    let replacement = if actual == expected.to_lowercase() { content.to_string() } else { String::new() };
                    Some((range, replacement))
                } else {
                    None
                }
            } else {
                None
            };

            if let Some((range, replacement)) = capture {
                result.replace_range(range, &replacement);
            } else {
                break;
            }
        }
        result
    }

    /// Handles existence conditionals in templates: <if key>content</if>
    fn handle_existence_conditionals(text: &str, variables: &HashMap<String, String>) -> String {
        let exist_pattern = match Regex::new(r#"(?s)<if\s+(\w+)\s*>(.*?)</if>"#) {
            Ok(r) => r,
            Err(_) => return text.to_string(),
        };
        let mut result = text.to_string();

        loop {
            let capture = if let Some(cap) = exist_pattern.captures(&result) {
                let m0 = cap.get(0).map(|m| m.range());
                let m1 = cap.get(1).map(|m| m.as_str());
                let m2 = cap.get(2).map(|m| m.as_str());
                
                if let (Some(range), Some(key), Some(content)) = (m0, m1, m2) {
                    let replacement = if variables.get(key).is_some_and(|v| !v.is_empty()) {
                        content.to_string()
                    } else {
                        String::new()
                    };
                    Some((range, replacement))
                } else {
                    None
                }
            } else {
                None
            };

            if let Some((range, replacement)) = capture {
                result.replace_range(range, &replacement);
            } else {
                break;
            }
        }
        result
    }

    /// Resolves shell blocks {{$(cmd)}} and environment variables {{env.VAR}}.
    #[allow(clippy::arithmetic_side_effects)]
    fn resolve_shell_and_env(text: &str, variables: &HashMap<String, String>) -> String {
        let mut result = text.to_string();
        let shell_ranges = Self::find_shell_ranges(&result);

        let mut offset: isize = 0;
        let mut token_map = HashMap::new();

        for (i, (start, end)) in shell_ranges.into_iter().enumerate() {
            let token = format!("__PB_SHELL_{}__", i);
            let s = (start as isize + offset) as usize;
            let e = (end as isize + offset) as usize;
            
            // Safe range access
            if let Some(content_raw) = result.get(s..e) {
                if content_raw.len() > 4 {
                    let shell_content = content_raw[2..content_raw.len() - 2].to_string();
                    token_map.insert(token.clone(), shell_content);
                    result.replace_range(s..e, &token);
                    offset += (token.len() as isize) - (end as isize - start as isize);
                }
            }
        }

        let std_re = match Regex::new(r"(\\)?\{\{\s*([^{}]+?)\s*\}\}") {
            Ok(r) => r,
            Err(_) => return result,
        };
        let mut hydrated = result.clone();
        let mut std_offset: isize = 0;

        for cap in std_re.captures_iter(&result) {
            let full_match = match cap.get(0) {
                Some(m) => m,
                None => continue,
            };
            let escape = cap.get(1).is_some();
            let content = cap.get(2).map(|m| m.as_str().trim()).unwrap_or("");

            let replacement = if escape {
                format!("{{{{{}}}}}", content)
            } else if let Some(env_var) = content.strip_prefix("env.") {
                env::var(env_var).unwrap_or_else(|_| format!("[Env var {} not found]", env_var))
            } else {
                variables
                    .get(content)
                    .cloned()
                    .unwrap_or_else(|| full_match.as_str().to_string())
            };

            let s = (full_match.start() as isize + std_offset) as usize;
            let e = (full_match.end() as isize + std_offset) as usize;
            hydrated.replace_range(s..e, &replacement);
            std_offset += (replacement.len() as isize) - (full_match.as_str().len() as isize);
        }

        let var_re = match Regex::new(r"\{\{\s*(.*?)\s*\}\}") {
            Ok(r) => r,
            Err(_) => return hydrated,
        };
        for (token, shell_content) in token_map {
            if shell_content.len() < 3 { continue; }
            let inner_cmd_template = &shell_content[2..shell_content.len() - 1].trim();
            let mut safe_cmd = inner_cmd_template.to_string();

            while let Some(cap) = var_re.captures(&safe_cmd.clone()) {
                let m0 = match cap.get(0) { Some(m) => m, None => break };
                let v_name = cap.get(1).map(|m| m.as_str().trim()).unwrap_or("");
                let val = if let Some(stripped) = v_name.strip_prefix("env.") {
                    env::var(stripped).unwrap_or_default()
                } else {
                    variables.get(v_name).cloned().unwrap_or_default()
                };
                
                #[allow(deprecated)]
                let quoted = shlex::try_quote(&val)
                    .unwrap_or_else(|_| shlex::quote(&val))
                    .to_string();
                
                safe_cmd.replace_range(m0.range(), &quoted);
            }

            let output = match Command::new("sh").arg("-c").arg(&safe_cmd).output() {
                Ok(out) => {
                    if out.status.success() {
                        String::from_utf8_lossy(&out.stdout).trim().to_string()
                    } else {
                        let err = String::from_utf8_lossy(&out.stderr).trim().to_string();
                        format!("[Error: {}]", if err.is_empty() { "Command failed" } else { &err })
                    }
                }
                Err(e) => format!("[Error: {}]", e),
            };
            hydrated = hydrated.replace(&token, &output);
        }

        hydrated
    }

    /// Finds all shell blocks {{$(cmd)}} in the text, handling nested brackets.
    #[allow(clippy::arithmetic_side_effects)]
    fn find_shell_ranges(text: &str) -> Vec<(usize, usize)> {
        let mut ranges = Vec::new();
        let mut stack = 0;
        let mut start = 0;
        let bytes = text.as_bytes();

        for i in 0..bytes.len() {
            if i + 1 < bytes.len() && bytes.get(i..i+2) == Some(b"{{") {
                if i > 0 && bytes.get(i-1) == Some(&b'\\') {
                    continue;
                }
                if i + 3 < bytes.len() && bytes.get(i..i+4) == Some(b"{{$(") {
                    if stack == 0 {
                        start = i;
                    }
                    stack += 1;
                } else if stack > 0 {
                    stack += 1;
                }
            } else if i + 1 < bytes.len() && bytes.get(i..i+2) == Some(b"}}") && stack > 0 {
                stack -= 1;
                if stack == 0 {
                    ranges.push((start, i + 2));
                }
            }
        }
        ranges
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_discover_variables() {
        let text = "Hello {{name}}, welcome to {{project}}! {{$(echo {{sub}})}}";
        let vars = TemplateEngine::discover_variables(text);
        assert!(vars.contains("name"));
        assert!(vars.contains("project"));
        assert!(vars.contains("sub"));
        assert_eq!(vars.len(), 3);
    }

    #[test]
    fn test_hydrate_basic() {
        let mut vars = HashMap::new();
        vars.insert("name".to_string(), "Alice".to_string());
        let template = "Hello {{name}}!";
        let result = TemplateEngine::hydrate(template, &vars, false);
        assert_eq!(result, "Hello Alice!");
    }

    #[test]
    fn test_mask_pii() {
        let text = "Contact me at test@example.com or 123-456-7890";
        let masked = TemplateEngine::mask_pii(text);
        assert!(masked.contains("[EMAIL]"));
        assert!(masked.contains("[PHONE]"));
        assert!(!masked.contains("test@example.com"));
    }

    #[test]
    fn test_hydrate_conditionals() {
        let mut vars = HashMap::new();
        vars.insert("lang".to_string(), "rust".to_string());
        let template = "<if lang=\"rust\">Rust is great!</if><if lang=\"py\">Python is ok.</if>";
        let result = TemplateEngine::hydrate(template, &vars, false);
        assert_eq!(result, "Rust is great!");
    }

    #[test]
    fn test_hydrate_shell() {
        let vars = HashMap::new();
        let template = "OS: {{$(echo Rust)}}";
        let result = TemplateEngine::hydrate(template, &vars, false);
        assert_eq!(result, "OS: Rust");
    }

    #[test]
    fn test_hydrate_nested() {
        let mut vars = HashMap::new();
        vars.insert("name".to_string(), "Alice".to_string());
        let template = "Result: {{$(echo Hello {{name}})}}";
        let result = TemplateEngine::hydrate(template, &vars, false);
        assert_eq!(result, "Result: Hello Alice");
    }
}
