use crate::models::PromptMetadata;
use std::collections::HashSet;

pub struct SearchEngine;

impl SearchEngine {
    /// Performs a hybrid search combining fuzzy/substring matching with concept mapping.
    pub fn hybrid_search(
        prompts: &[PromptMetadata],
        query: &str,
        tag_filter: Option<&str>,
    ) -> Vec<PromptMetadata> {
        let query_lower = query.to_lowercase();
        let query_words: HashSet<&str> = query_lower.split_whitespace().collect();
        
        let mut scored_results: Vec<(i32, PromptMetadata)> = prompts
            .iter()
            .filter(|p| {
                // Apply tag filter if present
                if let Some(tag) = tag_filter {
                    if !p.tags.iter().any(|t| t.to_lowercase() == tag.to_lowercase()) {
                        return false;
                    }
                }
                true
            })
            .map(|p| {
                let mut score = 0;
                let name_lower = p.name.to_lowercase();
                let desc_lower = p.description.to_lowercase();
                
                // 1. Exact match in name (highest weight)
                if name_lower == query_lower {
                    score += 100;
                }
                
                // 2. Substring in name
                if name_lower.contains(&query_lower) {
                    score += 50;
                }
                
                // 3. Concept match (Semantic Relevancy)
                for concept in &p.concepts {
                    let concept_lower = concept.to_lowercase();
                    if concept_lower == query_lower {
                        score += 40;
                    } else if concept_lower.contains(&query_lower) {
                        score += 20;
                    }
                }
                
                // 4. Word-based matches in description and tags
                for word in &query_words {
                    if desc_lower.contains(word) {
                        score += 5;
                    }
                    if p.tags.iter().any(|t| t.to_lowercase().contains(word)) {
                        score += 10;
                    }
                }
                
                (score, p.clone())
            })
            .filter(|(score, _)| *score > 0)
            .collect();

        // Sort by score descending
        scored_results.sort_by(|a, b| b.0.cmp(&a.0));
        
        scored_results.into_iter().map(|(_, p)| p).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hybrid_search_scoring() {
        let prompts = vec![
            PromptMetadata {
                name: "rust-helper".to_string(),
                display_name: "rust-helper".to_string(),
                description: "A helper for Rust".to_string(),
                args_description: "args".to_string(),
                version: "1.0.0".to_string(),
                last_updated: "2024-01-01".to_string(),
                tags: vec!["coding".to_string()],
                sensitive: false,
                version_id: None,
                path: "path1".to_string(),
                category: None,
                prompt: None,
                concepts: vec!["memory safety".to_string(), "systems".to_string()],
            },
            PromptMetadata {
                name: "cpp-helper".to_string(),
                display_name: "cpp-helper".to_string(),
                description: "A helper for C++".to_string(),
                args_description: "args".to_string(),
                version: "1.0.0".to_string(),
                last_updated: "2024-01-01".to_string(),
                tags: vec!["coding".to_string()],
                sensitive: false,
                version_id: None,
                path: "path2".to_string(),
                category: None,
                prompt: None,
                concepts: vec!["memory management".to_string()],
            }
        ];

        // Search for "memory safety" should rank rust-helper first
        let results = SearchEngine::hybrid_search(&prompts, "memory safety", None);
        assert_eq!(results[0].name, "rust-helper");

        // Search for "systems" should find rust-helper
        let results = SearchEngine::hybrid_search(&prompts, "systems", None);
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].name, "rust-helper");
    }
}
