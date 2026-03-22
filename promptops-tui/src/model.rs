use serde::Deserialize;
use std::collections::HashMap;
use std::time::Instant;

#[derive(Debug, Clone, Deserialize)]
pub struct Prompt {
    #[serde(default)]
    pub name: String,
    pub description: String,
    pub args_description: String,
    pub version: String,
    pub last_updated: String,
    pub tags: Vec<String>,
    pub prompt: String,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Focus {
    Categories,
    Prompts,
    InputModal,
    Search,
}

pub struct InputModal {
    pub prompt_name: String,
    pub variables: Vec<String>,
    pub current_var_index: usize,
    pub values: HashMap<String, String>,
    pub input_buffer: String,
    pub args_description: String,
}

pub struct AppState {
    pub all_prompts: Vec<Prompt>,
    pub categories: Vec<(String, usize)>, // (Category Name, Count)
    pub selected_category_index: usize,
    pub selected_prompt_index: usize,
    pub filter_prompts: Vec<Prompt>,
    pub focus: Focus,
    pub last_focus: Focus,
    pub should_quit: bool,
    pub input_modal: Option<InputModal>,
    pub status_message: Option<String>,
    pub status_timeout: Option<Instant>,
    pub search_query: String,
    pub show_preview: bool,
}

impl AppState {
    pub fn new(prompts: Vec<Prompt>) -> Self {
        let mut counts: HashMap<String, usize> = HashMap::new();
        for p in &prompts {
            for tag in &p.tags {
                *counts.entry(tag.clone()).or_insert(0) += 1;
            }
        }
        
        let mut categories: Vec<(String, usize)> = counts.into_iter().collect();
        categories.sort_by(|a, b| a.0.cmp(&b.0));
        
        let mut app = Self {
            all_prompts: prompts,
            categories,
            selected_category_index: 0,
            selected_prompt_index: 0,
            filter_prompts: Vec::new(),
            focus: Focus::Categories,
            last_focus: Focus::Categories,
            should_quit: false,
            input_modal: None,
            status_message: None,
            status_timeout: None,
            search_query: String::new(),
            show_preview: false,
        };
        app.update_filter();
        app
    }

    pub fn set_status(&mut self, message: String, secs: u64) {
        self.status_message = Some(message);
        self.status_timeout = Some(Instant::now() + std::time::Duration::from_secs(secs));
    }

    pub fn check_status_timeout(&mut self) {
        if let Some(timeout) = self.status_timeout {
            if Instant::now() > timeout {
                self.status_message = None;
                self.status_timeout = None;
            }
        }
    }

    pub fn update_filter(&mut self) {
        if !self.search_query.is_empty() {
            let query = self.search_query.to_lowercase();
            self.filter_prompts = self.all_prompts
                .iter()
                .filter(|p| {
                    p.name.to_lowercase().contains(&query) || 
                    p.description.to_lowercase().contains(&query) ||
                    p.tags.iter().any(|t| t.to_lowercase().contains(&query))
                })
                .cloned()
                .collect();
        } else if self.categories.is_empty() {
            self.filter_prompts = Vec::new();
        } else {
            let category = &self.categories[self.selected_category_index].0;
            self.filter_prompts = self.all_prompts
                .iter()
                .filter(|p| p.tags.contains(category))
                .cloned()
                .collect();
        }
        
        if self.selected_prompt_index >= self.filter_prompts.len() {
            self.selected_prompt_index = 0;
        }
    }

    pub fn next(&mut self) {
        match self.focus {
            Focus::Categories => {
                if !self.categories.is_empty() {
                    self.selected_category_index = (self.selected_category_index + 1) % self.categories.len();
                    self.update_filter();
                }
            }
            Focus::Prompts => {
                if !self.filter_prompts.is_empty() {
                    self.selected_prompt_index = (self.selected_prompt_index + 1) % self.filter_prompts.len();
                }
            }
            _ => {}
        }
    }

    pub fn previous(&mut self) {
        match self.focus {
            Focus::Categories => {
                if !self.categories.is_empty() {
                    if self.selected_category_index == 0 {
                        self.selected_category_index = self.categories.len() - 1;
                    } else {
                        self.selected_category_index -= 1;
                    }
                    self.update_filter();
                }
            }
            Focus::Prompts => {
                if !self.filter_prompts.is_empty() {
                    if self.selected_prompt_index == 0 {
                        self.selected_prompt_index = self.filter_prompts.len() - 1;
                    } else {
                        self.selected_prompt_index -= 1;
                    }
                }
            }
            _ => {}
        }
    }
}
