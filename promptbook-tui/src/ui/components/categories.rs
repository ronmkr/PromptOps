use crate::model::{AppState, Focus};
use ratatui::{
    layout::{Margin, Rect},
    style::{Color, Modifier, Style},
    widgets::{
        Block, Borders, List, ListItem, Padding, Scrollbar, ScrollbarOrientation, ScrollbarState,
    },
    Frame,
};

pub fn render_categories(f: &mut Frame, state: &mut AppState, area: Rect) {
    let is_modal = matches!(
        state.focus,
        Focus::InputModal | Focus::VersionSelection | Focus::ConfirmationModal
    );
    let is_focused = state.focus == Focus::Categories && !is_modal;
    let focus_style = if is_modal {
        Style::default().fg(Color::Rgb(50, 50, 50))
    } else if is_focused {
        Style::default().fg(Color::Yellow)
    } else {
        Style::default().fg(Color::DarkGray)
    };

    let items: Vec<ListItem> = state
        .categories
        .iter()
        .enumerate()
        .map(|(i, (name, count))| {
            let style = if i == state.selected_category_index {
                if is_modal {
                    Style::default().fg(Color::Rgb(60, 60, 60))
                } else if is_focused {
                    Style::default()
                        .fg(Color::Yellow)
                        .add_modifier(Modifier::BOLD)
                } else {
                    Style::default().fg(Color::DarkGray)
                }
            } else {
                if is_modal {
                    Style::default().fg(Color::Rgb(40, 40, 40))
                } else {
                    Style::default()
                }
            };
            let content = format!("{:<18} [{:>2}] ", name, count);
            ListItem::new(content).style(style)
        })
        .collect();

    let list = List::new(items)
        .block(
            Block::default()
                .borders(Borders::ALL)
                .title(" Domains ")
                .border_style(focus_style)
                .padding(Padding::horizontal(1)),
        )
        .highlight_style(if is_modal {
            Style::default()
        } else {
            Style::default().bg(Color::Rgb(40, 40, 40))
        });

    f.render_stateful_widget(list, area, &mut state.category_list_state);

    let scrollbar = Scrollbar::new(ScrollbarOrientation::VerticalRight)
        .begin_symbol(Some("↑"))
        .end_symbol(Some("↓"));
    let mut scrollbar_state =
        ScrollbarState::new(state.categories.len()).position(state.selected_category_index);

    f.render_stateful_widget(
        scrollbar,
        area.inner(&Margin {
            vertical: 1,
            horizontal: 0,
        }),
        &mut scrollbar_state,
    );
}
