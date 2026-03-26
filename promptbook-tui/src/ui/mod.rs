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

    render_header(f, state, outer_layout[0]);

    let width = f.size().width;

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
            .split(outer_layout[1]);

        render_categories(f, state, main_chunks[0]);
        render_prompts(f, state, main_chunks[1]);
        render_details(f, state, main_chunks[2]);
    } else if width >= 80 {
        // --- 2-Pane Layout (Medium Screens) ---
        if state.focus == Focus::Categories {
            let main_chunks = Layout::default()
                .direction(Direction::Horizontal)
                .constraints([Constraint::Percentage(30), Constraint::Percentage(70)])
                .split(outer_layout[1]);

            render_categories(f, state, main_chunks[0]);
            render_prompts(f, state, main_chunks[1]);
        } else {
            let main_chunks = Layout::default()
                .direction(Direction::Horizontal)
                .constraints([Constraint::Percentage(35), Constraint::Percentage(65)])
                .split(outer_layout[1]);

            render_prompts(f, state, main_chunks[0]);
            render_details(f, state, main_chunks[1]);
        }
    } else {
        // --- 1-Pane Layout (Small Screens) ---
        let area = outer_layout[1];
        match state.focus {
            Focus::Categories => render_categories(f, state, area),
            Focus::Prompts | Focus::VersionSelection | Focus::Search => {
                render_prompts(f, state, area)
            }
            _ => render_details(f, state, area),
        }
    }

    render_footer(f, state, outer_layout[2]);

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
