use anyhow::Result;
use colored::*;
use promptbook_core::{colors, get_prompts_dir, TemplateEngine};
use serde_json::Value;
use std::fs;
use std::path::Path;

pub fn validate_prompts() -> Result<()> {
    let prompts_dir = get_prompts_dir();
    let engine = TemplateEngine::new(&prompts_dir.to_string_lossy());
    let prompts = engine.get_all_prompts();

    println!("Validating {} prompts...", prompts.len());
    let mut errors = 0;

    // Semantic Checks: Pre-compile regexes outside the loop
    let open_tag = regex::Regex::new(r"\{\{[^}]*($|\{)")?;
    let open_block = regex::Regex::new(r"\{%[^%]*($|\{)")?;

    for p_meta in prompts {
        let p = match engine.load_prompt(&p_meta.name, p_meta.version_id.as_deref()) {
            Ok(p) => p,
            Err(e) => {
                println!("  ❌ {}: Failed to load prompt content: {}", p_meta.name.red(), e);
                errors += 1;
                continue;
            }
        };

        // 1. Metadata Checks
        if p.metadata.description.is_empty() {
            println!("  ❌ {}: Missing description", p.metadata.name.red());
            errors += 1;
        }
        if !p.metadata.description.ends_with('.') {
            println!("  ❌ {}: Description must end with a period", p.metadata.name.red());
            errors += 1;
        }
        if p.metadata.tags.is_empty() {
            println!("  ❌ {}: Missing tags", p.metadata.name.red());
            errors += 1;
        }

        // 2. Semantic Checks: Unclosed Tags
        if open_tag.is_match(&p.prompt) {
            println!("  ❌ {}: Found unclosed {{{{ tag", p.metadata.name.red());
            errors += 1;
        }

        if open_block.is_match(&p.prompt) {
            println!("  ❌ {}: Found unclosed {{% block", p.metadata.name.red());
            errors += 1;
        }

        // 3. Dry-run Hydration
        let vars = TemplateEngine::discover_variables(&p.prompt);
        let mut dummy_vars = std::collections::HashMap::new();
        for v in vars {
            dummy_vars.insert(v, "[placeholder]".to_string());
        }

        let hydrated = TemplateEngine::hydrate(&p.prompt, &dummy_vars, false);
        if hydrated.contains("{{") || hydrated.contains("{%") {
            // This might happen if some variables weren't discovered or provided
            // For dry-run, we want to ensure everything that looks like a variable is handled
            let remaining_vars = TemplateEngine::discover_variables(&hydrated);
            if !remaining_vars.is_empty() {
                println!("  ❌ {}: Dry-run failed, remaining variables: {:?}", p.metadata.name.red(), remaining_vars);
                errors += 1;
            }
        }
    }

    if errors == 0 {
        println!(
            "{}✅ All prompts validated successfully!{}",
            colors::GREEN,
            colors::RESET
        );
    } else {
        println!(
            "{}❌ Found {} errors during validation.{}",
            colors::RED,
            errors,
            colors::RESET
        );
    }

    Ok(())
}

pub fn sync_docs() -> Result<()> {
    let prompts_dir = get_prompts_dir();
    let engine = TemplateEngine::new(&prompts_dir.to_string_lossy());
    let prompts = engine.get_all_prompts();

    println!("Syncing documentation for {} prompts...", prompts.len());

    let mut md = String::from(
        "# Template Catalog\n\n| Category | Prompt | Description |\n|---|---|---|\n",
    );

    let mut sorted_prompts = prompts.clone();
    sorted_prompts.sort_by(|a, b| {
        let cat_a = a.category.as_deref().unwrap_or("");
        let cat_b = b.category.as_deref().unwrap_or("");
        cat_a.cmp(cat_b).then(a.name.cmp(&b.name))
    });

    for p in sorted_prompts {
        let cat = p.category.as_deref().unwrap_or("General");
        md.push_str(&format!(
            "| **{}** | `{}` | {} |\n",
            cat, p.name, p.description
        ));
    }

    fs::write("docs/CATALOG.md", md)?;
    println!(
        "{}✅ Catalog updated: docs/CATALOG.md{}",
        colors::GREEN,
        colors::RESET
    );

    Ok(())
}

pub fn run_evaluation(prompt_name: Option<String>) -> Result<()> {
    let dataset_dir = Path::new("tests/golden_datasets");
    if !dataset_dir.exists() {
        println!("No golden datasets found in tests/golden_datasets/");
        return Ok(());
    }

    let mut dataset_files = Vec::new();
    if let Some(name) = prompt_name {
        let path = dataset_dir.join(format!("{}.json", name));
        if path.exists() {
            dataset_files.push(path);
        } else {
            println!("No golden dataset found for prompt '{}'", name);
            return Ok(());
        }
    } else {
        for entry in fs::read_dir(dataset_dir)? {
            let entry = entry?;
            if entry.path().extension().is_some_and(|ext| ext == "json") {
                dataset_files.push(entry.path());
            }
        }
    }

    if dataset_files.is_empty() {
        println!("No relevant golden datasets found.");
        return Ok(());
    }

    println!(
        "{}📊 Running Golden Test Evaluation{}",
        colors::BOLD,
        colors::RESET
    );
    println!("----------------------------------------------------------------------");

    let mut total_passed = 0;
    let mut total_tests = 0;

    let prompts_dir = get_prompts_dir();
    let engine = TemplateEngine::new(&prompts_dir.to_string_lossy());

    for file in dataset_files {
        let content = fs::read_to_string(&file)?;
        let dataset: Value = serde_json::from_str(&content)?;
        let name = file.file_stem()
            .map(|s| s.to_string_lossy().to_string())
            .unwrap_or_else(|| "unknown".to_string());

        println!("\n{}Prompt: {}{}", colors::BOLD, name.cyan(), colors::RESET);

        let prompt_data = engine.load_prompt(&name, None)?;

        if let Some(test_cases) = dataset.get("test_cases").and_then(|v| v.as_array()) {
            for (i, test_case) in test_cases.iter().enumerate() {
                total_tests += 1;
                print!("  Test Case #{}: ", i + 1);

                let mut vars = std::collections::HashMap::new();
                if let Some(inputs) = test_case.get("inputs").and_then(|v| v.as_object()) {
                    for (k, v) in inputs {
                        vars.insert(k.clone(), v.as_str().unwrap_or_default().to_string());
                    }
                }

                let hydrated = TemplateEngine::hydrate(&prompt_data.prompt, &vars, false);
                let _hydrated_sys = if !prompt_data.system_prompt.is_empty() {
                    Some(TemplateEngine::hydrate(
                        &prompt_data.system_prompt,
                        &vars,
                        false,
                    ))
                } else {
                    None
                };

                if !hydrated.is_empty() {
                    println!("{}", "✅ PASS (Hydration)".green());
                    total_passed += 1;
                } else {
                    println!("{}", "❌ FAIL (Empty)".red());
                }
            }
        }
    }

    println!("\n----------------------------------------------------------------------");
    println!(
        "{}Results: {}/{} Passed{}",
        colors::BOLD,
        total_passed,
        total_tests,
        colors::RESET
    );

    Ok(())
}

#[allow(dead_code)]
pub fn sync_versions(new_version: String) -> Result<()> {
    let new_version = new_version.trim_start_matches('v').to_string();
    println!("Syncing all versions to: {}", new_version);
    let today = chrono::Local::now().format("%Y-%m-%d").to_string();

    // 1. Update Cargo.tomls
    let cargo_tomls = vec![
        "promptbook-core/Cargo.toml",
        "promptbook-cli/Cargo.toml",
        "promptbook-tui/Cargo.toml",
        "promptbook-mcp/Cargo.toml",
    ];

    for path in cargo_tomls {
        if Path::new(path).exists() {
            let content = fs::read_to_string(path)?;
            let mut lines: Vec<String> = content.lines().map(|s| s.to_string()).collect();
            let mut in_package = false;
            let mut updated = false;
            for line in &mut lines {
                if line.trim() == "[package]" {
                    in_package = true;
                } else if line.trim().starts_with('[') {
                    in_package = false;
                }
                if in_package && line.trim().starts_with("version =") {
                    *line = format!("version = \"{}\"", new_version);
                    updated = true;
                    break;
                }
            }
            if updated {
                fs::write(path, lines.join("\n") + "\n")?;
                println!("  ✅ Updated {}", path);
            }
        }
    }

    // 2. Update prompt templates
    let prompts_dir = get_prompts_dir();
    let mut template_count = 0;
    for entry in walkdir::WalkDir::new(prompts_dir) {
        let entry = entry?;
        if entry.path().extension().is_some_and(|ext| ext == "toml") {
            let content = fs::read_to_string(entry.path())?;
            let mut lines: Vec<String> = content.lines().map(|s| s.to_string()).collect();
            let mut updated_version = false;
            let mut updated_date = false;
            for line in &mut lines {
                if line.trim().starts_with("version =") {
                    *line = format!("version = \"{}\"", new_version);
                    updated_version = true;
                }
                if line.trim().starts_with("last_updated =") {
                    *line = format!("last_updated = \"{}\"", today);
                    updated_date = true;
                }
                if updated_version && updated_date {
                    break;
                }
            }
            fs::write(entry.path(), lines.join("\n") + "\n")?;
            template_count += 1;
        }
    }
    println!("  ✅ Updated {} prompt templates", template_count);

    Ok(())
}
