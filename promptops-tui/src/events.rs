use crossterm::event::{KeyCode, KeyEvent, KeyModifiers};
use std::collections::HashMap;
use crate::model::{AppState, Focus, InputModal, Prompt, Action, ConfirmationModal};
use crate::{hydrate, clipboard};

pub fn handle_navigation_input(app: &mut AppState, event: KeyEvent) {
    match event.code {
        KeyCode::Char('q') => app.should_quit = true,
        KeyCode::Down | KeyCode::Char('j') => {
            if event.modifiers.contains(KeyModifiers::CONTROL) {
                handle_scroll_input(app, KeyCode::Down);
            } else {
                app.next();
            }
        }
        KeyCode::Up | KeyCode::Char('k') => {
            if event.modifiers.contains(KeyModifiers::CONTROL) {
                handle_scroll_input(app, KeyCode::Up);
            } else {
                app.previous();
            }
        }
        KeyCode::PageDown => handle_scroll_input(app, KeyCode::PageDown),
        KeyCode::PageUp => handle_scroll_input(app, KeyCode::PageUp),
        KeyCode::Char('d') if event.modifiers.contains(KeyModifiers::CONTROL) => handle_scroll_input(app, KeyCode::PageDown),
        KeyCode::Char('u') if event.modifiers.contains(KeyModifiers::CONTROL) => handle_scroll_input(app, KeyCode::PageUp),
        KeyCode::Char('f') if event.modifiers.contains(KeyModifiers::CONTROL) => handle_scroll_input(app, KeyCode::PageDown),
        KeyCode::Char('b') if event.modifiers.contains(KeyModifiers::CONTROL) => handle_scroll_input(app, KeyCode::PageUp),
        KeyCode::Right | KeyCode::Tab | KeyCode::Char('l') => {
            app.focus = Focus::Prompts;
        }
        KeyCode::Left | KeyCode::Char('h') => {
            app.focus = Focus::Categories;
        }
        KeyCode::Char('/') => {
            app.last_focus = app.focus.clone();
            app.focus = Focus::Search;
        }
        KeyCode::Char('v') => {
            app.show_preview = !app.show_preview;
            app.details_scroll = 0;
        }
        KeyCode::Enter => {
            if let Some(group) = app.filter_groups.get(app.selected_prompt_index) {
                if group.versions.len() > 1 {
                    app.focus = Focus::VersionSelection;
                } else {
                    start_hydration(app, group.versions[0].clone());
                }
            }
        }
        _ => {}
    }
}

pub fn handle_scroll_input(app: &mut AppState, code: KeyCode) {
    match code {
        KeyCode::Down => {
            app.details_scroll = app.details_scroll.saturating_add(1);
        }
        KeyCode::Up => {
            app.details_scroll = app.details_scroll.saturating_sub(1);
        }
        KeyCode::PageDown => {
            app.details_scroll = app.details_scroll.saturating_add(10);
        }
        KeyCode::PageUp => {
            app.details_scroll = app.details_scroll.saturating_sub(10);
        }
        _ => {}
    }
}

pub fn handle_version_selection(app: &mut AppState, code: KeyCode) {
    match code {
        KeyCode::Esc => {
            app.focus = Focus::Prompts;
        }
        KeyCode::Enter => {
            let group = app.filter_groups[app.selected_prompt_index].clone();
            let version = group.versions[group.selected_version_index].clone();
            start_hydration(app, version);
        }
        KeyCode::Down | KeyCode::Char('j') => app.next(),
        KeyCode::Up | KeyCode::Char('k') => app.previous(),
        _ => {}
    }
}

pub fn handle_search_input(app: &mut AppState, code: KeyCode) {
    match code {
        KeyCode::Esc => {
            app.search_query.clear();
            app.update_filter();
            app.focus = app.last_focus.clone();
        }
        KeyCode::Enter => {
            app.focus = Focus::Prompts;
        }
        KeyCode::Char(c) => {
            app.search_query.push(c);
            app.update_filter();
        }
        KeyCode::Backspace => {
            app.search_query.pop();
            app.update_filter();
        }
        _ => {}
    }
}

pub fn handle_modal_input(app: &mut AppState, event: KeyEvent) {
    if let Some(modal) = &mut app.input_modal {
        match event.code {
            KeyCode::Esc => {
                app.input_modal = None;
                app.focus = Focus::Prompts;
            }
            KeyCode::Enter => {
                if event.modifiers.contains(KeyModifiers::ALT) || event.modifiers.contains(KeyModifiers::CONTROL) {
                    modal.input_buffer.push('\n');
                    modal.error_message = None;
                } else {
                    if modal.input_buffer.trim().is_empty() {
                        modal.error_message = Some("Input cannot be empty".to_string());
                        return;
                    }
                    
                    let resolved_val = crate::utils::resolve_file_injection(&modal.input_buffer);
                    let var_name = modal.variables[modal.current_var_index].clone();
                    modal.values.insert(var_name, resolved_val);
                    modal.input_buffer.clear();
                    modal.error_message = None;
                    
                    if modal.current_var_index + 1 < modal.variables.len() {
                        modal.current_var_index += 1;
                    } else {
                        if let Some(prompt) = app.all_prompts.iter().find(|p| {
                            p.name == modal.prompt_name && p.version_id == modal.version_id
                        }) {
                            let hydrated = hydrate::hydrate_prompt(&prompt.prompt, &modal.values);
                            if prompt.sensitive {
                                app.confirmation_modal = Some(ConfirmationModal {
                                    title: " Security Confirmation ".to_string(),
                                    message: format!("⚠️  SECURITY WARNING: '{}' is sensitive. Copy?", prompt.name),
                                    action: Action::CopyPrompt(hydrated),
                                });
                                app.focus = Focus::ConfirmationModal;
                            } else {
                                let _ = clipboard::copy_to_clipboard(&hydrated);
                                app.set_status(format!("Success: '{}' copied!", prompt.name), 4);
                                app.focus = Focus::Prompts;
                            }
                        }
                        app.input_modal = None;
                    }
                }
            }
            KeyCode::Char(c) => {
                modal.input_buffer.push(c);
                modal.error_message = None;
            }
            KeyCode::Backspace => {
                modal.input_buffer.pop();
                modal.error_message = None;
            }
            _ => {}
        }
    }
}

pub fn handle_confirmation_modal(app: &mut AppState, code: KeyCode) {
    match code {
        KeyCode::Enter | KeyCode::Char('y') | KeyCode::Char('Y') => {
            if let Some(modal) = &app.confirmation_modal {
                match &modal.action {
                    Action::CopyPrompt(content) => {
                        let _ = clipboard::copy_to_clipboard(content);
                        app.set_status("Success: Copied to clipboard!".to_string(), 3);
                    }
                }
            }
            app.confirmation_modal = None;
            app.focus = Focus::Prompts;
        }
        KeyCode::Esc | KeyCode::Char('n') | KeyCode::Char('N') => {
            app.confirmation_modal = None;
            app.focus = Focus::Prompts;
            app.set_status("Action cancelled.".to_string(), 2);
        }
        _ => {}
    }
}

fn start_hydration(app: &mut AppState, prompt: Prompt) {
    let vars = hydrate::get_variables(&prompt.prompt);
    if vars.is_empty() {
        let content = prompt.prompt.clone();
        if prompt.sensitive {
            app.confirmation_modal = Some(ConfirmationModal {
                title: " Security Confirmation ".to_string(),
                message: format!("⚠️  SECURITY WARNING: '{}' is sensitive. Copy?", prompt.name),
                action: Action::CopyPrompt(content),
            });
            app.focus = Focus::ConfirmationModal;
        } else {
            let _ = clipboard::copy_to_clipboard(&content);
            app.set_status(format!("Success: '{}' copied!", prompt.name), 3);
            app.focus = Focus::Prompts;
        }
    } else {
        app.input_modal = Some(InputModal {
            prompt_name: prompt.name.clone(),
            version_id: prompt.version_id.clone(),
            variables: vars,
            current_var_index: 0,
            values: HashMap::new(),
            input_buffer: String::new(),
            args_description: prompt.args_description.clone(),
            error_message: None,
        });
        app.focus = Focus::InputModal;
    }
}
