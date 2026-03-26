use crate::model::{Action, AppState, ConfirmationModal, Focus};
use crate::{clipboard, hydrate};
use crossterm::event::{KeyCode, KeyEvent, KeyModifiers};

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
                if event.modifiers.contains(KeyModifiers::ALT)
                    || event.modifiers.contains(KeyModifiers::CONTROL)
                {
                    modal.input_buffer.push('\n');
                    modal.error_message = None;
                } else {
                    if modal.input_buffer.trim().is_empty() {
                        modal.error_message = Some("Input cannot be empty".to_string());
                        return;
                    }

                    let resolved_val = crate::utils::resolve_file_injection(&modal.input_buffer);
                    if let Some(var_name) = modal.variables.get(modal.current_var_index) {
                        modal.values.insert(var_name.clone(), resolved_val);
                    }
                    modal.input_buffer.clear();
                    modal.error_message = None;

                    if modal.current_var_index + 1 < modal.variables.len() {
                        modal.current_var_index += 1;
                    } else {
                        if let Some(prompt) = app.all_prompts.iter().find(|p| {
                            p.metadata.name == modal.prompt_name
                                && p.metadata.version_id == modal.version_id
                        }) {
                            let hydrated_legacy =
                                hydrate::hydrate_prompt(&prompt.prompt, &modal.values, false);
                            let hydrated_system =
                                hydrate::hydrate_prompt(&prompt.system_prompt, &modal.values, false);
                            let hydrated_user =
                                hydrate::hydrate_prompt(&prompt.user_prompt, &modal.values, false);

                            let final_hydrated =
                                if !hydrated_system.is_empty() || !hydrated_user.is_empty() {
                                    let mut parts = Vec::new();
                                    if !hydrated_system.is_empty() {
                                        parts.push(format!("--- SYSTEM ---\n{}", hydrated_system));
                                    }
                                    if !hydrated_user.is_empty() {
                                        parts.push(format!("--- USER ---\n{}", hydrated_user));
                                    }
                                    parts.join("\n\n")
                                } else {
                                    hydrated_legacy
                                };

                            if prompt.metadata.sensitive {
                                app.confirmation_modal = Some(ConfirmationModal {
                                    title: " Security Confirmation ".to_string(),
                                    message: format!(
                                        "⚠️  SECURITY WARNING: '{}' is sensitive. Copy?",
                                        prompt.metadata.name
                                    ),
                                    action: Action::CopyPrompt(final_hydrated),
                                });
                                app.focus = Focus::ConfirmationModal;
                            } else {
                                let _ = clipboard::copy_to_clipboard(&final_hydrated);
                                app.set_status(
                                    format!("Success: '{}' copied!", prompt.metadata.name),
                                    4,
                                );
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
