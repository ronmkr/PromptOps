use anyhow::{Context, Result};
use colored::*;
use promptbook_core::{
    colors, copy_to_clipboard, get_prompts_dir, LLMProvider, SessionManager, TemplateEngine, Vault,
};
use std::collections::HashMap;
use std::io::{self, Read};

pub fn list_prompts(tag: Option<String>) -> Result<()> {
    let prompts_dir = get_prompts_dir();
    let engine = TemplateEngine::new(&prompts_dir.to_string_lossy());
    let mut prompts = engine.get_all_prompts();

    if let Some(t) = tag {
        let t_lower = t.to_lowercase();
        prompts.retain(|p| p.tags.iter().any(|tag| tag.to_lowercase() == t_lower));
    }

    if prompts.is_empty() {
        println!("No prompts found.");
        return Ok(());
    }

    // Group by category
    let mut grouped: HashMap<String, Vec<_>> = HashMap::new();
    for p in prompts {
        let cat = p.category.clone().unwrap_or_else(|| "General".to_string());
        grouped.entry(cat).or_default().push(p);
    }

    let mut categories: Vec<_> = grouped.keys().cloned().collect();
    categories.sort();

    println!(
        "\n{} promptbook Template Overview{}",
        colors::BOLD,
        colors::RESET
    );
    println!("================================================================================\n");

    for cat in categories {
        let items_in_cat = grouped.get(&cat).cloned().unwrap_or_default();
        println!("📂 {} ({} prompts)", cat.bold(), items_in_cat.len());
        println!(
            "--------------------------------------------------------------------------------"
        );
        let mut items = items_in_cat;
        items.sort_by(|a, b| a.name.cmp(&b.name));
        for p in items {
            println!("  {:30} | {}", p.name.cyan(), p.description);
        }
        println!();
    }

    Ok(())
}

pub fn search_prompts(term: String, tag: Option<String>) -> Result<()> {
    let prompts_dir = get_prompts_dir();
    let engine = TemplateEngine::new(&prompts_dir.to_string_lossy());
    let prompts = engine.get_all_prompts();
    let term_lower = term.to_lowercase();

    let mut results = Vec::new();
    for p in prompts {
        if p.name.to_lowercase().contains(&term_lower)
            || p.description.to_lowercase().contains(&term_lower)
            || p.tags
                .iter()
                .any(|t| t.to_lowercase().contains(&term_lower))
        {
            if let Some(ref t) = tag {
                if !p
                    .tags
                    .iter()
                    .any(|tag| tag.to_lowercase() == t.to_lowercase())
                {
                    continue;
                }
            }
            results.push(p);
        }
    }

    if results.is_empty() {
        println!("No prompts found matching '{}'.", term);
    } else {
        // Just use list logic for simplicity
        let mut grouped: HashMap<String, Vec<_>> = HashMap::new();
        for p in results {
            let name = p.name.clone();
            grouped.entry(name).or_default().push(p);
        }
        // Simplified display for search
        for (name, versions) in grouped {
            println!(
                "  {} ({} versions) - {}",
                name.cyan().bold(),
                versions.len(),
                versions.first().map(|v| v.description.as_str()).unwrap_or("")
            );
        }
    }

    Ok(())
}

pub fn use_prompt(
    name: String,
    version: Option<String>,
    profile: Option<String>,
    no_copy: bool,
    auto_confirm: bool,
    mask: bool,
    provided_vars: HashMap<String, String>,
) -> Result<()> {
    let prompts_dir = get_prompts_dir();
    let engine = TemplateEngine::new(&prompts_dir.to_string_lossy());
    let prompt_data = engine.load_prompt(&name, version.as_deref())?;

    let mut vars = provided_vars;

    // Load from profile
    if let Some(p_name) = profile {
        let session = SessionManager::new(&promptbook_core::StoragePaths::profiles_file().to_string_lossy());
        if let Some(p_vars) = session.load_profile(&p_name) {
            for (k, v) in p_vars {
                vars.entry(k).or_insert(v);
            }
        }
    }

    // Collect missing variables interactively
    let mut all_vars = TemplateEngine::discover_variables(&prompt_data.prompt);
    all_vars.extend(TemplateEngine::discover_variables(
        &prompt_data.system_prompt,
    ));
    all_vars.extend(TemplateEngine::discover_variables(&prompt_data.user_prompt));

    let mut final_vars = vars;

    // Check for piped data
    if !atty::is(atty::Stream::Stdin) {
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer)?;
        if !buffer.trim().is_empty() {
            final_vars
                .entry("args".to_string())
                .or_insert(buffer.trim().to_string());
        }
    }

    for var in all_vars {
        if let std::collections::hash_map::Entry::Vacant(e) = final_vars.entry(var.clone()) {
            let label = if var == "args" {
                &prompt_data.metadata.args_description
            } else {
                &var
            };
            let val = inquire::Text::new(&format!("Enter {}: ", label.bold().cyan())).prompt()?;
            e.insert(val);
        }
    }

    let h_legacy = TemplateEngine::hydrate(&prompt_data.prompt, &final_vars, mask);
    let h_system = TemplateEngine::hydrate(&prompt_data.system_prompt, &final_vars, mask);
    let h_user = TemplateEngine::hydrate(&prompt_data.user_prompt, &final_vars, mask);

    let (output, copy_text) = if !h_system.is_empty() || !h_user.is_empty() {
        let out = format!(
            "{}{}--- SYSTEM ---{}\n{}\n\n{}{}--- USER ---{}\n{}",
            colors::BOLD,
            colors::MAGENTA,
            colors::RESET,
            h_system,
            colors::BOLD,
            colors::CYAN,
            colors::RESET,
            h_user
        );
        let copy = format!("--- SYSTEM ---\n{}\n\n--- USER ---\n{}", h_system, h_user);
        (out, copy)
    } else {
        (h_legacy.clone(), h_legacy)
    };

    if !no_copy {
        let do_copy = if prompt_data.metadata.sensitive && !auto_confirm {
            println!(
                "\n{}⚠️  SECURITY WARNING: This prompt is sensitive.{}",
                colors::YELLOW,
                colors::RESET
            );
            inquire::Confirm::new("Copy to clipboard?")
                .with_default(false)
                .prompt()?
        } else {
            true
        };

        if do_copy {
            copy_to_clipboard(&copy_text)?;
            eprintln!(
                " {}[Done] Prompt copied to clipboard!{}",
                colors::GREEN,
                colors::RESET
            );
        }
    }

    println!("{}", output);
    Ok(())
}

pub fn chain_prompts(
    prompts: Vec<String>,
    initial_args: Option<String>,
    profile: Option<String>,
) -> Result<()> {
    let prompts_dir = get_prompts_dir();
    let engine = TemplateEngine::new(&prompts_dir.to_string_lossy());
    let mut current_input = initial_args;

    println!(
        "\n{}{}⛓️ Starting Prompt Chain ({}) steps{}\n----------------------------------------------------------------------",
        colors::BOLD,
        colors::CYAN,
        prompts.len(),
        colors::RESET
    );

    for (i, name) in prompts.iter().enumerate() {
        println!(
            "\n{}Step {}: {}{}{} (Executing...)",
            colors::BOLD,
            i + 1,
            colors::GREEN,
            name,
            colors::RESET
        );

        let prompt_data = engine.load_prompt(name, None)?;
        let mut vars = HashMap::new();

        if let Some(ref input) = current_input {
            vars.insert("args".to_string(), input.clone());
        }

        if let Some(ref p_name) = profile {
            let session = SessionManager::new(
                &promptbook_core::StoragePaths::profiles_file().to_string_lossy(),
            );
            if let Some(p_vars) = session.load_profile(p_name) {
                for (k, v) in p_vars {
                    vars.entry(k).or_insert(v);
                }
            }
        }

        let p_run = if !prompt_data.prompt.is_empty() {
            &prompt_data.prompt
        } else {
            &prompt_data.user_prompt
        };
        let s_run = if !prompt_data.system_prompt.is_empty() {
            Some(prompt_data.system_prompt.as_str())
        } else {
            None
        };

        let hydrated = TemplateEngine::hydrate(p_run, &vars, false);
        let hydrated_sys = s_run.map(|s| TemplateEngine::hydrate(s, &vars, false));

        println!(
            " {}Wait for LLM response...{}",
            colors::YELLOW,
            colors::RESET
        );
        let response = LLMProvider::execute(&hydrated, hydrated_sys.as_deref())?;

        println!(
            " {}[Done] Step {} completed.{}",
            colors::GREEN,
            i + 1,
            colors::RESET
        );
        let excerpt = if response.len() > 100 {
            format!("{}...", &response[..100])
        } else {
            response.clone()
        };
        println!(
            " {}--- Response Excerpt ---{}\n {}",
            colors::BOLD,
            colors::RESET,
            excerpt.replace('\n', " ")
        );

        current_input = Some(response);
    }

    if let Some(final_output) = current_input {
        println!(
            "\n{}{}✅ Chain complete!{}",
            colors::BOLD,
            colors::CYAN,
            colors::RESET
        );
        copy_to_clipboard(&final_output)?;
        println!("Final output copied to clipboard.\n\n{}", final_output);
    }

    Ok(())
}

pub fn manage_profiles(command: String, name: Option<String>, vars: Vec<String>) -> Result<()> {
    let session = SessionManager::new(&promptbook_core::StoragePaths::profiles_file().to_string_lossy());

    match command.as_str() {
        "set" => {
            let n = name.context("Profile name is required")?;
            let mut variables = HashMap::new();
            for v in vars {
                if let Some((k, val)) = v.split_once('=') {
                    variables.insert(k.trim().to_string(), val.trim().to_string());
                }
            }
            session.save_profile(&n, variables.clone())?;
            println!(
                " {}[Done] Profile '{}' saved with {} variables.{}",
                colors::GREEN,
                n,
                variables.len(),
                colors::RESET
            );
        }
        "list" => {
            let profiles = session.list_profiles();
            if profiles.is_empty() {
                println!("No profiles found.");
            } else {
                println!("{}Context Profiles:{}", colors::BOLD, colors::RESET);
                for p in profiles {
                    println!("  - {}", p);
                }
            }
        }
        "delete" => {
            let n = name.context("Profile name is required")?;
            if session.delete_profile(&n) {
                println!(
                    " {}[Done] Profile '{}' deleted.{}",
                    colors::GREEN,
                    n,
                    colors::RESET
                );
            } else {
                println!(
                    " {}Warning: Profile '{}' not found.{}",
                    colors::YELLOW,
                    n,
                    colors::RESET
                );
            }
        }
        _ => println!("Unknown profile command."),
    }
    Ok(())
}

pub fn manage_keys(command: String, provider: Option<String>, key: Option<String>) -> Result<()> {
    match command.as_str() {
        "set" => {
            let p = provider.context("Provider is required")?;
            let k = key.context("Key is required")?;
            Vault::set_key(&p, &k)?;
            println!(
                " {}[Done] API key for '{}' secured in vault.{}",
                colors::GREEN,
                p,
                colors::RESET
            );
        }
        "list" => {
            let keys = Vault::list_keys();
            if keys.is_empty() {
                println!("No keys found in vault.");
            } else {
                println!("{}Providers in Vault:{}", colors::BOLD, colors::RESET);
                for k in keys {
                    println!("  - {}", k);
                }
            }
        }
        "delete" => {
            let p = provider.context("Provider is required")?;
            if Vault::delete_key(&p) {
                println!(
                    " {}[Done] API key for '{}' deleted.{}",
                    colors::GREEN,
                    p,
                    colors::RESET
                );
            } else {
                println!(
                    " {}Warning: Provider '{}' not found.{}",
                    colors::YELLOW,
                    p,
                    colors::RESET
                );
            }
        }
        _ => println!("Unknown keys command."),
    }
    Ok(())
}
