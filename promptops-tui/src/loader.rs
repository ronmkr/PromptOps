use std::fs;
use std::path::Path;
use anyhow::{Context, Result};
use crate::model::Prompt;
use walkdir::WalkDir;

pub fn load_prompts<P: AsRef<Path>>(path: P) -> Result<Vec<Prompt>> {
    let mut prompts = Vec::new();
    
    for entry in WalkDir::new(path)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.path().extension().map_or(false, |ext| ext == "toml"))
    {
        let content = fs::read_to_string(entry.path())
            .with_context(|| format!("Failed to read prompt file: {:?}", entry.path()))?;
        
        let mut prompt: Prompt = toml::from_str(&content)
            .with_context(|| format!("Failed to parse TOML in: {:?}", entry.path()))?;
        
        // Use filename as prompt name if not explicitly set (though our schema has it in toml usually? wait, our schema DOES NOT have name in toml usually, we derive it from filename in python)
        // Let's check our TOML structure again.
        // Actually, looking at previous reads, it seems we don't have 'name' in the TOML.
        // So I should add it to the struct manually or use an intermediate struct.
        
        prompt.name = entry.path()
            .file_stem()
            .unwrap()
            .to_string_lossy()
            .to_string();
            
        prompts.push(prompt);
    }
    
    Ok(prompts)
}
