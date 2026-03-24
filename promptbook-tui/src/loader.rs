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
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.path().extension().is_some_and(|ext| ext == "toml"))
    {
        let path = entry.path();
        let rel_path = path.strip_prefix(prompts_dir).unwrap();
        let parts: Vec<_> = rel_path.components().collect();
        let file_stem = path.file_stem().unwrap().to_string_lossy().to_string();

        let (name, version_id) = match parts.len() {
            1 => (file_stem, None), // commands/prompts/name.toml
            2 => {
                // commands/prompts/category/name.toml
                (file_stem, None)
            }
            _ => {
                // commands/prompts/category/name/version.toml
                let name = parts[parts.len() - 2]
                    .as_os_str()
                    .to_string_lossy()
                    .to_string();
                (name, Some(file_stem))
            }
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
