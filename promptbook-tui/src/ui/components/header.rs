use crate::model::{AppState, Focus};
use ratatui::{
    layout::Rect,
    style::{Color, Modifier, Style},
    widgets::{Block, Borders, Paragraph},
    Frame,
};

pub fn render_header(f: &mut Frame, state: &mut AppState, area: Rect) {
    let is_modal = matches!(
        state.focus,
        Focus::InputModal | Focus::VersionSelection | Focus::ConfirmationModal
    );
    let focus_style = if is_modal {
        Style::default().fg(Color::Rgb(50, 50, 50)) // Deep dim
    } else if state.focus == Focus::Search {
        Style::default()
            .fg(Color::Yellow)
            .add_modifier(Modifier::BOLD)
    } else {
        Style::default().fg(Color::DarkGray)
    };

    let title = if state.search_query.is_empty() && state.focus != Focus::Search {
        " promptbook Explorer "
    } else {
        " Search Prompts "
    };

    let search_content = if state.search_query.is_empty() && state.focus != Focus::Search {
        " Press [/] to search all prompts... ".to_string()
    } else {
        format!(" > {}█", state.search_query)
    };

    let content_style = if is_modal {
        Style::default().fg(Color::DarkGray)
    } else {
        Style::default()
    };

    let header = Paragraph::new(search_content).style(content_style).block(
        Block::default()
            .borders(Borders::ALL)
            .title(title)
            .border_style(focus_style),
    );

    f.render_widget(header, area);
}
