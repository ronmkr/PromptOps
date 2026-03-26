use super::prompt::{ConfirmationModal, InputModal, Prompt, PromptGroup};
use ratatui::widgets::ListState;
use std::collections::HashMap;
use std::time::Instant;

#[derive(Debug, Clone, PartialEq)]
pub enum Focus {
    Categories,
    Prompts,
    Details,
    VersionSelection,
    InputModal,
    Search,
    ConfirmationModal,
}

pub struct AppState {
    pub all_prompts: Vec<Prompt>,
    pub groups: Vec<PromptGroup>,
    pub categories: Vec<(String, usize)>, // (Category Name, Count)
    pub selected_category_index: usize,
    pub selected_prompt_index: usize,
    pub filter_groups: Vec<PromptGroup>,
    pub focus: Focus,
    pub last_focus: Focus,
    pub should_quit: bool,
    pub input_modal: Option<InputModal>,
    pub confirmation_modal: Option<ConfirmationModal>,
    pub status_message: Option<String>,
    pub status_timeout: Option<Instant>,
    pub search_query: String,
    pub show_preview: bool,
    pub details_scroll: u16,
    pub category_list_state: ListState,
    pub prompt_list_state: ListState,
}

impl AppState {
    pub fn new(prompts: Vec<Prompt>) -> Self {
        // Group prompts by name
        let mut group_map: HashMap<String, Vec<Prompt>> = HashMap::new();
        for p in prompts.iter() {
            group_map.entry(p.name.clone()).or_default().push(p.clone());
        }

        let mut groups: Vec<PromptGroup> = group_map
            .into_iter()
            .map(|(name, mut versions)| {
                // Sort: None (default) first, then by ID
                versions.sort_by(|a, b| {
                    (
                        a.version_id.is_some(),
                        a.version_id.as_ref().unwrap_or(&String::new()),
                    )
                        .cmp(&(
                            b.version_id.is_some(),
                            b.version_id.as_ref().unwrap_or(&String::new()),
                        ))
                });
                PromptGroup {
                    name,
                    versions,
                    selected_version_index: 0,
                }
            })
            .collect();
        groups.sort_by(|a, b| a.name.cmp(&b.name));

        let mut counts: HashMap<String, usize> = HashMap::new();
        for g in &groups {
            let mut tags = std::collections::HashSet::new();
            for v in &g.versions {
                for t in &v.tags {
                    tags.insert(t.clone());
                }
            }
            for tag in tags {
                *counts.entry(tag).or_insert(0) += 1;
            }
        }

        let mut categories: Vec<(String, usize)> = counts.into_iter().collect();
        categories.sort_by(|a, b| a.0.cmp(&b.0));

        let mut app = Self {
            all_prompts: prompts,
            groups,
            categories,
            selected_category_index: 0,
            selected_prompt_index: 0,
            filter_groups: Vec::new(),
            focus: Focus::Categories,
            last_focus: Focus::Categories,
            should_quit: false,
            input_modal: None,
            confirmation_modal: None,
            status_message: None,
            status_timeout: None,
            search_query: String::new(),
            show_preview: false,
            details_scroll: 0,
            category_list_state: ListState::default().with_selected(Some(0)),
            prompt_list_state: ListState::default().with_selected(Some(0)),
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
            self.filter_groups = self
                .groups
                .iter()
                .filter(|g| {
                    g.name.to_lowercase().contains(&query)
                        || g.versions.iter().any(|v| {
                            v.description.to_lowercase().contains(&query)
                                || v.tags.iter().any(|t| t.to_lowercase().contains(&query))
                        })
                })
                .cloned()
                .collect();
        } else if self.categories.is_empty() {
            self.filter_groups = Vec::new();
        } else {
            let category = &self.categories[self.selected_category_index].0;
            self.filter_groups = self
                .groups
                .iter()
                .filter(|g| g.versions.iter().any(|v| v.tags.contains(category)))
                .cloned()
                .collect();
        }

        if self.selected_prompt_index >= self.filter_groups.len() {
            self.selected_prompt_index = 0;
        }
        self.category_list_state
            .select(Some(self.selected_category_index));
        self.prompt_list_state
            .select(Some(self.selected_prompt_index));
        self.details_scroll = 0;
    }

    pub fn next(&mut self) {
        match self.focus {
            Focus::Categories => {
                if !self.categories.is_empty() {
                    self.selected_category_index =
                        (self.selected_category_index + 1) % self.categories.len();
                    self.category_list_state
                        .select(Some(self.selected_category_index));
                    self.update_filter();
                }
            }
            Focus::Prompts => {
                if !self.filter_groups.is_empty() {
                    self.selected_prompt_index =
                        (self.selected_prompt_index + 1) % self.filter_groups.len();
                    self.prompt_list_state
                        .select(Some(self.selected_prompt_index));
                    self.details_scroll = 0;
                }
            }
            Focus::VersionSelection => {
                let group = &mut self.filter_groups[self.selected_prompt_index];
                group.selected_version_index =
                    (group.selected_version_index + 1) % group.versions.len();
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
                    self.category_list_state
                        .select(Some(self.selected_category_index));
                    self.update_filter();
                }
            }
            Focus::Prompts => {
                if !self.filter_groups.is_empty() {
                    if self.selected_prompt_index == 0 {
                        self.selected_prompt_index = self.filter_groups.len() - 1;
                    } else {
                        self.selected_prompt_index -= 1;
                    }
                    self.prompt_list_state
                        .select(Some(self.selected_prompt_index));
                    self.details_scroll = 0;
                }
            }
            Focus::VersionSelection => {
                let group = &mut self.filter_groups[self.selected_prompt_index];
                if group.selected_version_index == 0 {
                    group.selected_version_index = group.versions.len() - 1;
                } else {
                    group.selected_version_index -= 1;
                }
            }
            _ => {}
        }
    }
}
