use promptbook_core::TemplateEngine;
use std::collections::HashMap;

pub fn get_variables(text: &str) -> Vec<String> {
    TemplateEngine::discover_variables(text)
        .into_iter()
        .collect()
}
pub fn hydrate_prompt(template: &str, variables: &HashMap<String, String>, mask: bool) -> String {
    TemplateEngine::hydrate(template, variables, mask)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hydration_basic() {
        let mut vars = HashMap::new();
        vars.insert("args".to_string(), "world".to_string());
        let result = hydrate_prompt("hello {{args}}", &vars, false);
        assert_eq!(result, "hello world");
    }

    #[test]
    fn test_hydration_missing_vars() {
        let vars = HashMap::new();
        let result = hydrate_prompt("hello {{missing}}", &vars, false);
        // Should keep the tag if not provided
        assert_eq!(result, "hello {{missing}}");
    }

    #[test]
    fn test_hydration_dynamic() {
        let vars = HashMap::new();
        let result = hydrate_prompt("val: {{$(echo 123)}}", &vars, false);
        assert_eq!(result, "val: 123");
    }

    #[test]
    fn test_hydration_conditionals() {
        let mut vars = HashMap::new();
        vars.insert("os".to_string(), "macos".to_string());
        let template = "<if os=\"macos\">Apple</if><if os=\"linux\">Penguin</if>";
        let result = hydrate_prompt(template, &vars, false);
        assert_eq!(result, "Apple");
    }

    #[test]
    fn test_hydration_shell_error() {
        let vars = HashMap::new();
        // The TemplateEngine::hydrate method calls resolve_shell_and_env
        // which returns [Error: ...] if command fails
        let result = hydrate_prompt("{{$(nonexistentcommand)}}", &vars, false);
        assert!(result.contains("[Error:"));
    }
}

