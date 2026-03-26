use std::path::PathBuf;

pub fn get_project_root() -> PathBuf {
    // In a real installed scenario, this might be different,
    // but for development we can look for 'commands' directory.
    let mut curr = std::env::current_dir().unwrap_or_else(|_| PathBuf::from("."));
    while let Some(parent) = curr.parent() {
        if curr.join("commands").exists() && curr.join("Cargo.toml").exists() {
            return curr;
        }
        curr = parent.to_path_buf();
    }
    std::env::current_dir().unwrap_or_else(|_| PathBuf::from("."))
}

pub fn get_user_config_dir() -> PathBuf {
    dirs::home_dir()
        .unwrap_or_else(|| PathBuf::from("."))
        .join(".promptbook")
}

pub fn get_prompts_dir() -> PathBuf {
    get_project_root().join("commands").join("prompts")
}

pub struct StoragePaths;

impl StoragePaths {
    pub fn vault_file() -> PathBuf {
        get_user_config_dir().join("vault.json")
    }
    pub fn profiles_file() -> PathBuf {
        get_user_config_dir().join("profiles.json")
    }
    pub fn log_file() -> PathBuf {
        get_user_config_dir().join("audit.log")
    }
}

pub mod colors {
    pub const CYAN: &str = "\x1b[96m";
    pub const MAGENTA: &str = "\x1b[95m";
    pub const GREEN: &str = "\x1b[92m";
    pub const YELLOW: &str = "\x1b[93m";
    pub const RED: &str = "\x1b[91m";
    pub const BOLD: &str = "\x1b[1m";
    pub const RESET: &str = "\x1b[0m";
}
