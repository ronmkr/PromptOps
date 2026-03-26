pub mod components;
pub mod layout;

use crate::model::{AppState, Focus};
use components::*;
use ratatui::{
    layout::{Constraint, Direction, Layout},
    Frame,
};

pub fn render(f: &mut Frame, state: &mut AppState) {
    let outer_layout = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3), // Header / Search
            Constraint::Min(0),    // Main content
            Constraint::Length(1), // Footer / Status
        ])
        .split(f.size());

    if let Some(header_area) = outer_layout.first() {
        render_header(f, state, *header_area);
    }

    let width = f.size().width;
    let main_content_area = outer_layout.get(1).cloned().unwrap_or(f.size());
    let footer_area = outer_layout.get(2).cloned().unwrap_or(f.size());

    if width >= 120 {
        // --- 3-Pane Layout (Large Screens) ---
        let main_constraints = if state.show_preview {
            [
                Constraint::Percentage(20),
                Constraint::Percentage(20),
                Constraint::Percentage(60),
            ]
        } else {
            [
                Constraint::Percentage(20),
                Constraint::Percentage(30),
                Constraint::Percentage(50),
            ]
        };

        let main_chunks = Layout::default()
            .direction(Direction::Horizontal)
            .constraints(main_constraints)
            .split(main_content_area);

        if let Some(area) = main_chunks.first() { render_categories(f, state, *area); }
        if let Some(area) = main_chunks.get(1) { render_prompts(f, state, *area); }
        if let Some(area) = main_chunks.get(2) { render_details(f, state, *area); }
    } else if width >= 80 {
        // --- 2-Pane Layout (Medium Screens) ---
        if state.focus == Focus::Categories {
            let main_chunks = Layout::default()
                .direction(Direction::Horizontal)
                .constraints([Constraint::Percentage(30), Constraint::Percentage(70)])
                .split(main_content_area);

            if let Some(area) = main_chunks.first() { render_categories(f, state, *area); }
            if let Some(area) = main_chunks.get(1) { render_prompts(f, state, *area); }
        } else {
            let main_chunks = Layout::default()
                .direction(Direction::Horizontal)
                .constraints([Constraint::Percentage(35), Constraint::Percentage(65)])
                .split(main_content_area);

            if let Some(area) = main_chunks.first() { render_prompts(f, state, *area); }
            if let Some(area) = main_chunks.get(1) { render_details(f, state, *area); }
        }
    } else {
        // --- 1-Pane Layout (Small Screens) ---
        match state.focus {
            Focus::Categories => render_categories(f, state, main_content_area),
            Focus::Prompts | Focus::VersionSelection | Focus::Search => {
                render_prompts(f, state, main_content_area)
            }
            _ => render_details(f, state, main_content_area),
        }
    }

    render_footer(f, state, footer_area);

    if state.focus == Focus::VersionSelection {
        render_version_modal(f, state);
    }

    if state.focus == Focus::InputModal {
        render_input_modal(f, state);
    }

    if state.focus == Focus::ConfirmationModal {
        render_confirmation_modal(f, state);
    }
}
