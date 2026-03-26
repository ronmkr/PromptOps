use crate::model::{Action, AppState, ConfirmationModal, Focus, InputModal, Prompt};
use crate::{clipboard, hydrate};
use std::collections::HashMap;

pub fn start_hydration(app: &mut AppState, prompt: Prompt) {
    let mut vars = hydrate::get_variables(&prompt.prompt);
    vars.extend(hydrate::get_variables(&prompt.system_prompt));
    vars.extend(hydrate::get_variables(&prompt.user_prompt));
    vars.sort();
    vars.dedup();

    if vars.is_empty() {
        let content = if !prompt.system_prompt.is_empty() || !prompt.user_prompt.is_empty() {
            let mut parts = Vec::new();
            if !prompt.system_prompt.is_empty() {
                parts.push(format!("--- SYSTEM ---\n{}", prompt.system_prompt));
            }
            if !prompt.user_prompt.is_empty() {
                parts.push(format!("--- USER ---\n{}", prompt.user_prompt));
            }
            parts.join("\n\n")
        } else {
            prompt.prompt.clone()
        };

        if prompt.sensitive {
            app.confirmation_modal = Some(ConfirmationModal {
                title: " Security Confirmation ".to_string(),
                message: format!(
                    "⚠️  SECURITY WARNING: '{}' is sensitive. Copy?",
                    prompt.name
                ),
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
