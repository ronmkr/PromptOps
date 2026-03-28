#[cfg(test)]
mod tests {
    use crate::events::navigation::handle_navigation_input;
    use crate::model::{AppState, Focus, Prompt};
    use promptbook_core::PromptMetadata;
    use crossterm::event::{KeyCode, KeyEvent, KeyModifiers};
    use std::collections::HashMap;

    fn mock_app() -> AppState {
        let p = Prompt {
            metadata: PromptMetadata {
                name: "test".to_string(),
                display_name: "test".to_string(),
                description: "desc".to_string(),
                args_description: "args".to_string(),
                version: "1.0.0".to_string(),
                last_updated: "2024-01-01".to_string(),
                tags: vec!["tag".to_string()],
                sensitive: false,
                version_id: None,
                path: "".to_string(),
                category: None,
                prompt: Some("hello {{args}}".to_string()),
            },
            prompt: "hello {{args}}".to_string(),
            system_prompt: "".to_string(),
            user_prompt: "".to_string(),
            raw_data: HashMap::new(),
        };
        AppState::new(vec![p])
    }

    #[test]
    fn test_focus_navigation_cycle() {
        let mut app = mock_app();
        assert_eq!(app.focus, Focus::Categories);

        // Right from Categories -> Prompts
        handle_navigation_input(&mut app, KeyEvent::new(KeyCode::Right, KeyModifiers::NONE));
        assert_eq!(app.focus, Focus::Prompts);

        // Right from Prompts -> Details
        handle_navigation_input(&mut app, KeyEvent::new(KeyCode::Right, KeyModifiers::NONE));
        assert_eq!(app.focus, Focus::Details);

        // Right from Details -> Categories (Cycle)
        handle_navigation_input(&mut app, KeyEvent::new(KeyCode::Right, KeyModifiers::NONE));
        assert_eq!(app.focus, Focus::Categories);

        // Tab should also work
        handle_navigation_input(&mut app, KeyEvent::new(KeyCode::Tab, KeyModifiers::NONE));
        assert_eq!(app.focus, Focus::Prompts);
    }

    #[test]
    fn test_details_scrolling() {
        let mut app = mock_app();
        app.focus = Focus::Details;
        app.details_scroll = 0;

        // j should scroll down when Details is focused
        handle_navigation_input(
            &mut app,
            KeyEvent::new(KeyCode::Char('j'), KeyModifiers::NONE),
        );
        assert_eq!(app.details_scroll, 1);

        // k should scroll up
        handle_navigation_input(
            &mut app,
            KeyEvent::new(KeyCode::Char('k'), KeyModifiers::NONE),
        );
        assert_eq!(app.details_scroll, 0);
    }
}
