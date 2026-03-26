use anyhow::Result;
use std::collections::HashMap;
use std::fs;
use std::path::Path;

pub struct SessionManager {
    pub profiles_file: String,
}

impl SessionManager {
    pub fn new(profiles_file: &str) -> Self {
        Self {
            profiles_file: profiles_file.to_string(),
        }
    }

    pub fn get_all_profiles(&self) -> HashMap<String, HashMap<String, String>> {
        let path = Path::new(&self.profiles_file);
        if !path.exists() {
            return HashMap::new();
        }

        fs::read_to_string(path)
            .ok()
            .and_then(|content| serde_json::from_str(&content).ok())
            .unwrap_or_default()
    }

    pub fn save_profile(&self, name: &str, variables: HashMap<String, String>) -> Result<()> {
        let mut profiles = self.get_all_profiles();
        profiles.insert(name.to_string(), variables);

        if let Some(parent) = Path::new(&self.profiles_file).parent() {
            fs::create_dir_all(parent)?;
        }

        let content = serde_json::to_string_pretty(&profiles)?;
        fs::write(&self.profiles_file, content)?;
        Ok(())
    }

    pub fn load_profile(&self, name: &str) -> Option<HashMap<String, String>> {
        self.get_all_profiles().get(name).cloned()
    }

    pub fn delete_profile(&self, name: &str) -> bool {
        let mut profiles = self.get_all_profiles();
        if profiles.remove(name).is_some() {
            if let Ok(content) = serde_json::to_string_pretty(&profiles) {
                return fs::write(&self.profiles_file, content).is_ok();
            }
        }
        false
    }

    pub fn list_profiles(&self) -> Vec<String> {
        let mut names: Vec<String> = self.get_all_profiles().keys().cloned().collect();
        names.sort();
        names
    }
}
