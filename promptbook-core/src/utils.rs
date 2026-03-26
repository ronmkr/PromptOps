use crate::config::StoragePaths;
use anyhow::Result;
use chrono::Local;
use std::fs;
use std::io::Write;

pub struct AuditLogger;

impl AuditLogger {
    pub fn log(
        name: &str,
        version_id: Option<&str>,
        variables: &std::collections::HashMap<String, String>,
    ) -> Result<()> {
        let log_file = StoragePaths::log_file();
        if let Some(parent) = log_file.parent() {
            fs::create_dir_all(parent)?;
        }

        let timestamp = Local::now().to_rfc3339();
        let user = whoami::username(); // We might need whoami crate or just env var

        let mut masked_vars = std::collections::HashMap::new();
        for k in variables.keys() {
            masked_vars.insert(k.clone(), "MASKED".to_string());
        }

        let log_entry = serde_json::json!({
            "timestamp": timestamp,
            "user": user,
            "prompt": name,
            "version": version_id,
            "variables": masked_vars,
        });

        let mut file = fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open(log_file)?;

        writeln!(file, "{}", log_entry)?;
        Ok(())
    }
}

pub fn copy_to_clipboard(text: &str) -> Result<()> {
    let mut ctx = arboard::Clipboard::new()?;
    ctx.set_text(text.to_string())?;
    Ok(())
}
