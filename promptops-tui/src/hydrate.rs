use regex::Regex;
use std::collections::HashMap;

pub fn hydrate_prompt(template: &str, variables: &HashMap<String, String>) -> String {
    // Pattern: (\\)?\{\{\s*(\w+)\s*\}\}
    // group 1: optional backslash
    // group 2: variable name
    let re = Regex::new(r"(\\)?\{\{\s*(\w+)\s*\}\}").unwrap();

    re.replace_all(template, |caps: &regex::Captures| {
        let escaped = caps.get(1).is_some();
        let var_name = caps.get(2).unwrap().as_str();

        if escaped {
            // If it was escaped with \, return the literal {{var}}
            format!("{{{{{}}}}}", var_name)
        } else {
            // Otherwise, replace with variable value or leave as is if missing
            variables
                .get(var_name)
                .cloned()
                .unwrap_or_else(|| caps.get(0).unwrap().as_str().to_string())
        }
    })
    .to_string()
}

pub fn get_variables(template: &str) -> Vec<String> {
    let re = Regex::new(r"\{\{\s*(\w+)\s*\}\}").unwrap();
    let mut vars: Vec<String> = re
        .captures_iter(template)
        .map(|cap| cap.get(1).unwrap().as_str().to_string())
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
    fn test_get_variables_unique() {
        let template = "{{a}} {{b}} {{a}}";
        let vars = get_variables(template);
        assert_eq!(vars, vec!["a", "b"]);
    }
}
