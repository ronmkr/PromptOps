use super::actions::start_hydration;
use crate::model::{AppState, Focus};
use crossterm::event::{KeyCode, KeyEvent, KeyModifiers};

pub fn handle_navigation_input(app: &mut AppState, event: KeyEvent) {
    match event.code {
        KeyCode::Char('q') => app.should_quit = true,
        KeyCode::Down | KeyCode::Char('j') => {
            if app.focus == Focus::Details || event.modifiers.contains(KeyModifiers::CONTROL) {
                handle_scroll_input(app, KeyCode::Down);
            } else {
                app.next();
            }
        }
        KeyCode::Up | KeyCode::Char('k') => {
            if app.focus == Focus::Details || event.modifiers.contains(KeyModifiers::CONTROL) {
                handle_scroll_input(app, KeyCode::Up);
            } else {
                app.previous();
            }
        }
        KeyCode::PageDown => handle_scroll_input(app, KeyCode::PageDown),
        KeyCode::PageUp => handle_scroll_input(app, KeyCode::PageUp),
        KeyCode::Char('d') if event.modifiers.contains(KeyModifiers::CONTROL) => {
            handle_scroll_input(app, KeyCode::PageDown)
        }
        KeyCode::Char('u') if event.modifiers.contains(KeyModifiers::CONTROL) => {
            handle_scroll_input(app, KeyCode::PageUp)
        }
        KeyCode::Char('f') if event.modifiers.contains(KeyModifiers::CONTROL) => {
            handle_scroll_input(app, KeyCode::PageDown)
        }
        KeyCode::Char('b') if event.modifiers.contains(KeyModifiers::CONTROL) => {
            handle_scroll_input(app, KeyCode::PageUp)
        }
        KeyCode::Right | KeyCode::Tab | KeyCode::Char('l') => match app.focus {
            Focus::Categories => app.focus = Focus::Prompts,
            Focus::Prompts => app.focus = Focus::Details,
            _ => app.focus = Focus::Categories,
        },
        KeyCode::Left | KeyCode::Char('h') => match app.focus {
            Focus::Details => app.focus = Focus::Prompts,
            Focus::Prompts => app.focus = Focus::Categories,
            _ => app.focus = Focus::Details,
        },
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
