use crate::model::Prompt;
use anyhow::Result;
use std::fs;
use std::path::Path;
use walkdir::WalkDir;

pub fn load_prompts<P: AsRef<Path>>(prompts_dir: P) -> Result<Vec<Prompt>> {
    let mut prompts = Vec::new();
    let prompts_dir = prompts_dir.as_ref();

    for entry in WalkDir::new(prompts_dir)
        .min_depth(1)
        .max_depth(2)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.path().extension().is_some_and(|ext| ext == "toml"))
    {
        let path = entry.path();
        let rel_path = path.strip_prefix(prompts_dir).unwrap();
        let parts: Vec<_> = rel_path.components().collect();

        let (name, version_id) = if parts.len() == 1 {
            // Flat file: commands/prompts/name.toml
            (
                path.file_stem().unwrap().to_string_lossy().to_string(),
                None,
            )
        } else {
            // Grouped file: commands/prompts/name/v1.toml
            (
                parts[0].as_os_str().to_string_lossy().to_string(),
                Some(path.file_stem().unwrap().to_string_lossy().to_string()),
            )
        };

        let content = fs::read_to_string(path)?;
        let mut prompt: Prompt = match toml::from_str(&content) {
            Ok(p) => p,
            Err(_) => continue, // Skip invalid TOML
        };

        prompt.name = name;
        prompt.version_id = version_id;
        prompts.push(prompt);
    }

    Ok(prompts)
}
