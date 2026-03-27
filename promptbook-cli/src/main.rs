mod commands;
mod wizards;

use anyhow::Result;
use clap::{CommandFactory, Parser, Subcommand};
use std::collections::HashMap;

#[derive(Parser)]
#[command(name = "pop")]
#[command(about = "promptbook — AI CLI Prompt Template Library", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// List all available templates
    List {
        /// Filter by category tag
        #[arg(long)]
        tag: Option<String>,
    },
    /// Search templates by name, description, or tags
    Search {
        /// Search term
        term: String,
        /// Filter search by category tag
        #[arg(long)]
        tag: Option<String>,
    },
    /// Interactively run a prompt template
    Use {
        /// Template name (e.g., refactor-suggestions)
        name: String,
        /// Specific version to use (e.g., 1.0.0)
        #[arg(long)]
        version: Option<String>,
        /// Named context profile to use for pre-filling variables
        #[arg(long)]
        profile: Option<String>,
        /// Skip copying output to clipboard
        #[arg(long)]
        no_copy: bool,
        /// Skip sensitive confirmations
        #[arg(short, long)]
        yes: bool,
        /// Mask PII in variables
        #[arg(long)]
        mask: bool,
        /// Arbitrary variable assignments (e.g. --project PB)
        #[arg(trailing_var_arg = true, allow_hyphen_values = true)]
        vars: Vec<String>,
    },
    /// Sequentially execute multiple prompts
    Chain {
        /// List of prompt names to chain
        prompts: Vec<String>,
        /// Initial input for the first prompt (assigned to {{args}})
        #[arg(long)]
        args: Option<String>,
        /// Context profile for the entire chain
        #[arg(long)]
        profile: Option<String>,
    },
    /// Manage named context profiles
    Profile {
        #[command(subcommand)]
        command: ProfileCommands,
    },
    /// Manage secure API keys in the vault
    Keys {
        #[command(subcommand)]
        command: KeysCommands,
    },
    /// List all unique category tags
    Tags,
    /// Setup promptbook (completions, TUI, etc.)
    Init,
    /// Interactive prompt authoring wizard
    Create,
    /// Validate all prompts follow the schema
    Validate,
    /// Synchronize documentation (CATALOG.md)
    SyncDocs,
    /// Synchronize all versions across the project
    SyncVersions {
        /// New version string (e.g., 1.0.0)
        version: String,
    },
    /// Run automated evaluations using golden datasets
    Evaluate {
        /// Specific prompt to evaluate
        #[arg(long)]
        prompt: Option<String>,
    },
    /// Generate shell completion scripts
    Completion {
        /// Shell to generate completion for
        #[arg(value_enum)]
        shell: clap_complete::Shell,
    },
}

#[derive(Subcommand)]
enum ProfileCommands {
    /// Create or update a profile
    Set {
        /// Profile name
        name: String,
        /// Variable assignments (e.g., project=PB lang=py)
        vars: Vec<String>,
    },
    /// List available profiles
    List,
    /// Delete a profile
    Delete {
        /// Profile name to delete
        name: String,
    },
}

#[derive(Subcommand)]
enum KeysCommands {
    /// Set an API key for a provider
    Set {
        /// Provider name (e.g., openai, gemini)
        provider: String,
        /// API Key value
        key: String,
    },
    /// List providers with keys in the vault
    List,
    /// Delete a key from the vault
    Delete {
        /// Provider name to delete
        provider: String,
    },
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::List { tag } => commands::user::list_prompts(tag)?,
        Commands::Search { term, tag } => commands::user::search_prompts(term, tag)?,
        Commands::Use {
            name,
            version,
            profile,
            no_copy,
            yes,
            mask,
            vars,
        } => {
            let mut provided_vars = HashMap::new();
            let mut i = 0;
            while i < vars.len() {
                if let Some(arg) = vars.get(i) {
                    if arg.starts_with("--") {
                        if let Some(value) = vars.get(i + 1) {
                            let key = arg.get(2..).unwrap_or("").to_string();
                            provided_vars.insert(key, value.clone());
                            i += 2;
                            continue;
                        }
                    }
                }
                i += 1;
            }
            commands::user::use_prompt(name, version, profile, no_copy, yes, mask, provided_vars)?;
        }
        Commands::Chain {
            prompts,
            args,
            profile,
        } => commands::user::chain_prompts(prompts, args, profile)?,
        Commands::Profile { command } => match command {
            ProfileCommands::Set { name, vars } => {
                commands::user::manage_profiles("set".to_string(), Some(name), vars)?
            }
            ProfileCommands::List => {
                commands::user::manage_profiles("list".to_string(), None, vec![])?
            }
            ProfileCommands::Delete { name } => {
                commands::user::manage_profiles("delete".to_string(), Some(name), vec![])?
            }
        },
        Commands::Keys { command } => match command {
            KeysCommands::Set { provider, key } => {
                commands::user::manage_keys("set".to_string(), Some(provider), Some(key))?
            }
            KeysCommands::List => commands::user::manage_keys("list".to_string(), None, None)?,
            KeysCommands::Delete { provider } => {
                commands::user::manage_keys("delete".to_string(), Some(provider), None)?
            }
        },
        Commands::Tags => {
            // Re-use core logic via TemplateEngine if needed
            let prompts_dir = promptbook_core::get_prompts_dir();
            let engine = promptbook_core::TemplateEngine::new(&prompts_dir.to_string_lossy());
            let prompts = engine.get_all_prompts();
            let mut tags = std::collections::HashSet::new();
            for p in prompts {
                for t in p.tags {
                    tags.insert(t);
                }
            }
            let mut sorted_tags: Vec<_> = tags.into_iter().collect();
            sorted_tags.sort();
            for t in sorted_tags {
                println!("{}", t);
            }
        }
        Commands::Init => wizards::init_wizard()?,
        Commands::Create => wizards::create_wizard()?,
        Commands::Validate => commands::dev::validate_prompts()?,
        Commands::SyncDocs => commands::dev::sync_docs()?,
        Commands::SyncVersions { version } => commands::dev::sync_versions(version)?,
        Commands::Evaluate { prompt } => commands::dev::run_evaluation(prompt)?,
        Commands::Completion { shell } => {
            let mut cmd = Cli::command();
            clap_complete::generate(shell, &mut cmd, "pop", &mut std::io::stdout());
        }
    }

    Ok(())
}
