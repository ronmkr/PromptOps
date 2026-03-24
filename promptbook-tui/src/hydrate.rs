use regex::Regex;
use std::collections::HashMap;
use std::env;
use std::process::Command;

pub fn hydrate_prompt(template: &str, variables: &HashMap<String, String>) -> String {
    // 0. Handle Conditional Blocks: <if key="value">...</if>
    // Pattern: <if\s+(\w+)\s*=\s*\"([^\"]+)\"\s*>(.*?)</if>
    // s flag (dot_matches_new_line) is enabled by (?s)
    let cond_re = Regex::new(r#"(?s)<if\s+(\w+)\s*=\s*"([^"]+)"\s*>(.*?)</if>"#).unwrap();
    let mut template = template.to_string();

    template = cond_re
        .replace_all(&template, |caps: &regex::Captures| {
            let key = caps.get(1).unwrap().as_str();
            let expected_val = caps.get(2).unwrap().as_str().trim().to_lowercase();
            let content = caps.get(3).unwrap().as_str();

            let actual_val = variables
                .get(key)
                .map(|v| v.trim().to_lowercase())
                .unwrap_or_default();

            if actual_val == expected_val {
                content.to_string()
            } else {
                "".to_string()
            }
        })
        .to_string();

    // 1. Handle Variable Substitutions
    // Pattern updated: (\\)?\{\{\s*(.*?)\s*\}\}
    let re = Regex::new(r"(\\)?\{\{\s*(.*?)\s*\}\}").unwrap();

    re.replace_all(&template, |caps: &regex::Captures| {
        let escaped = caps.get(1).is_some();
        let content = caps.get(2).unwrap().as_str().trim();

        if escaped {
            format!("{{{{{}}}}}", content)
        } else if let Some(inner) = content.strip_prefix("$(").and_then(|s| s.strip_suffix(')')) {
            let cmd_str = inner.trim();
            match execute_shell(cmd_str) {
                Ok(output) => output,
                Err(e) => format!("[Error executing command: {}] -> {}", cmd_str, e),
            }
        } else if let Some(env_var) = content.strip_prefix("env.") {
            let env_var = env_var.trim();
            env::var(env_var).unwrap_or_else(|_| format!("[Env var {} not found]", env_var))
        } else {
            variables
                .get(content)
                .cloned()
                .unwrap_or_else(|| caps.get(0).unwrap().as_str().to_string())
        }
    })
    .to_string()
}

fn execute_shell(cmd: &str) -> Result<String, String> {
    let output = if cfg!(target_os = "windows") {
        Command::new("cmd").args(["/C", cmd]).output()
    } else {
        Command::new("sh").args(["-c", cmd]).output()
    };

    match output {
        Ok(out) => {
            if out.status.success() {
                Ok(String::from_utf8_lossy(&out.stdout).trim().to_string())
            } else {
                Err(String::from_utf8_lossy(&out.stderr).trim().to_string())
            }
        }
        Err(e) => Err(e.to_string()),
    }
}

pub fn get_variables(template: &str) -> Vec<String> {
    let re = Regex::new(r"\{\{\s*(.*?)\s*\}\}").unwrap();
    let mut vars: Vec<String> = re
        .captures_iter(template)
        .map(|cap| cap.get(1).unwrap().as_str().trim().to_string())
        .collect();
    vars.sort();
    vars.dedup();
    vars
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hydration_basic() {
        let template = "Hello {{ name }}, usage: \\{{literal}}";
        let mut vars = HashMap::new();
        vars.insert("name".to_string(), "Alice".to_string());

        let result = hydrate_prompt(template, &vars);
        assert_eq!(result, "Hello Alice, usage: {{literal}}");
    }

    #[test]
    fn test_hydration_missing_vars() {
        let template = "Hello {{ name }}, {{ missing }}";
        let mut vars = HashMap::new();
        vars.insert("name".to_string(), "Alice".to_string());

        let result = hydrate_prompt(template, &vars);
        assert_eq!(result, "Hello Alice, {{ missing }}");
    }

    #[test]
    fn test_hydration_conditionals() {
        let template = "Start <if lang=\"java\">JAVA</if><if lang=\"kotlin\">KOTLIN</if> End";
        let mut vars = HashMap::new();
        vars.insert("lang".to_string(), "java".to_string());

        let result = hydrate_prompt(template, &vars);
        assert_eq!(result, "Start JAVA End");
    }

    #[test]
    fn test_hydration_dynamic() {
        let template = "OS: {{ env.TERM }}, Shell: {{ $(echo hello) }}";
        let vars = HashMap::new();
        env::set_var("TERM", "xterm");

        let result = hydrate_prompt(template, &vars);
        assert_eq!(result, "OS: xterm, Shell: hello");
    }

    #[test]
    fn test_hydration_shell_error() {
        let template = "{{ $(nonexistent_command_123) }}";
        let vars = HashMap::new();

        let result = hydrate_prompt(template, &vars);
        assert!(result.contains("Error executing command"));
    }
}
