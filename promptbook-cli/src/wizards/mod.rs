use anyhow::Result;
use inquire::{Select, Text};
use promptbook_core::{colors, get_prompts_dir};
use std::fs;
use chrono::Local;

pub fn create_wizard() -> Result<()> {
    println!("\n{}{}✨ New Prompt Template Wizard{}\n-------------------------------------------------------\n", colors::BOLD, colors::CYAN, colors::RESET);

    let name = Text::new("1. Prompt Name (e.g., my-new-tool): ").prompt()?;
    let prompts_dir = get_prompts_dir();
    
    let categories: Vec<String> = fs::read_dir(&prompts_dir)?
        .filter_map(|e| e.ok())
        .filter(|e| e.path().is_dir())
        .map(|e| e.file_name().to_string_lossy().to_string())
        .collect();

    let mut select_cats = categories.clone();
    select_cats.push("[Create New Category]".to_string());

    let category = Select::new("2. Select Category:", select_cats).prompt()?;
    let final_cat = if category == "[Create New Category]" {
        Text::new("New category name: ").prompt()?
    } else {
        category
    };

    let description = Text::new("3. Description: ").prompt()?;
    let args_desc = Text::new("   Arguments Description: ").with_default("Input Data").prompt()?;
    
    let tags_input = Text::new("4. Tags (comma-separated): ").prompt()?;
    let mut tags: Vec<String> = tags_input.split(',').map(|s| s.trim().to_lowercase()).filter(|s| !s.is_empty()).collect();
    if !tags.contains(&final_cat.to_lowercase()) {
        tags.push(final_cat.to_lowercase());
    }

    let mode = Select::new("5. Prompt Mode:", vec!["Single Prompt (Standard)", "Multi-Message Prompt (System + User)"]).prompt()?;

    let mut toml_content = format!(
        "description      = \"{}\"\nargs_description = \"{}\"\nversion          = \"1.0.0\"\nlast_updated     = \"{}\"\ntags             = {:?}\n",
        description, args_desc, Local::now().format("%Y-%m-%d"), tags
    );

    if mode == "Single Prompt (Standard)" {
        println!("\n5.1 Prompt Instructions (Enter content, then Ctrl+D to finish):");
        let mut content = String::new();
        use std::io::{self, Read};
        io::stdin().read_to_string(&mut content)?;
        toml_content.push_str(&format!("\nprompt           = \"\"\"\n# {}\n{}\n\"\"\"\n", name, content.trim()));
    } else {
        println!("\n5.1 System Prompt (Enter content, then Ctrl+D to finish):");
        let mut system = String::new();
        use std::io::{self, Read};
        io::stdin().read_to_string(&mut system)?;
        
        toml_content.push_str(&format!("\nsystem_prompt    = \"\"\"\n{}\n\"\"\"\n", system.trim()));
        
        println!("\n5.2 User Prompt (Enter content, then Ctrl+D to finish):");
        let mut user = String::new();
        io::stdin().read_to_string(&mut user)?;
        toml_content.push_str(&format!("\nuser_prompt      = \"\"\"\n{}\n\"\"\"\n", user.trim()));
    }

    let dest_dir = prompts_dir.join(&final_cat);
    fs::create_dir_all(&dest_dir)?;
    let filepath = dest_dir.join(format!("{}.toml", name));
    
    fs::write(&filepath, toml_content)?;
    println!("\n{}✓ Created {}{}", colors::GREEN, filepath.display(), colors::RESET);

    Ok(())
}

pub fn init_wizard() -> Result<()> {
    println!("\n{}{}🚀 Promptbook Setup Wizard{}\n-------------------------------------------------------\n", colors::BOLD, colors::CYAN, colors::RESET);
    println!("Checking system requirements...");
    Ok(())
}
