use anyhow::Result;
use promptbook_core::{Prompt, TemplateEngine};

pub fn load_prompts(prompts_dir: &str) -> Result<Vec<Prompt>> {
    let engine = TemplateEngine::new(prompts_dir);
    engine.load_all_prompts()
}
