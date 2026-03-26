use crate::model::AppState;
use crate::ui::layout::centered_rect;
use ratatui::{
    layout::Margin,
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{
        Block, Borders, Clear, List, ListItem, ListState, Padding, Paragraph, Scrollbar,
        ScrollbarOrientation, ScrollbarState, Wrap,
    },
    Frame,
};

pub fn render_version_modal(f: &mut Frame, state: &mut AppState) {
    let group = &state.filter_groups[state.selected_prompt_index];
    let area = centered_rect(60, 40, f.size());
    f.render_widget(Clear, area);

    let block = Block::default()
        .borders(Borders::ALL)
        .title(format!(" Choose Version for: {} ", group.name))
        .border_style(Style::default().fg(Color::Yellow))
        .padding(Padding::uniform(1));

    let items: Vec<ListItem> = group
        .versions
        .iter()
        .enumerate()
        .map(|(i, v)| {
            let style = if i == group.selected_version_index {
                Style::default()
                    .fg(Color::Yellow)
                    .add_modifier(Modifier::BOLD)
            } else {
                Style::default()
            };
            let v_id = v.version_id.as_deref().unwrap_or("default");
            ListItem::new(format!(" > {:<10} | {}", v_id, v.description)).style(style)
        })
        .collect();

    let list = List::new(items)
        .block(block)
        .highlight_style(Style::default().bg(Color::Rgb(50, 50, 50)));

    let mut list_state = ListState::default().with_selected(Some(group.selected_version_index));
    f.render_stateful_widget(list, area, &mut list_state);

    let scrollbar = Scrollbar::new(ScrollbarOrientation::VerticalRight)
        .begin_symbol(Some("↑"))
        .end_symbol(Some("↓"));
    let mut scrollbar_state =
        ScrollbarState::new(group.versions.len()).position(group.selected_version_index);

    f.render_stateful_widget(
        scrollbar,
        area.inner(&Margin {
            vertical: 1,
            horizontal: 0,
        }),
        &mut scrollbar_state,
    );
}

pub fn render_input_modal(f: &mut Frame, state: &mut AppState) {
    if let Some(modal) = &state.input_modal {
        let area = centered_rect(80, 50, f.size());
        f.render_widget(Clear, area);

        let var_name = &modal.variables[modal.current_var_index];
        let progress = format!(
            "Step {} of {}",
            modal.current_var_index + 1,
            modal.variables.len()
        );

        let label = if var_name == "args" {
            &modal.args_description
        } else {
            var_name
        };

        let title = if let Some(v_id) = &modal.version_id {
            format!(" Hydrating: {}:{} ", modal.prompt_name, v_id)
        } else {
            format!(" Hydrating: {} ", modal.prompt_name)
        };

        let block = Block::default()
            .borders(Borders::ALL)
            .title(title)
            .border_style(Style::default().fg(Color::Yellow))
            .padding(Padding::uniform(1));

        let mut text = vec![
            Line::from(vec![
                Span::styled(progress, Style::default().fg(Color::DarkGray)),
                Span::raw(" | Required: "),
                Span::styled(
                    label,
                    Style::default()
                        .fg(Color::Cyan)
                        .add_modifier(Modifier::BOLD),
                ),
            ]),
            Line::from(""),
        ];

        if let Some(error) = &modal.error_message {
            text.push(Line::from(vec![
                Span::styled(
                    " Error: ",
                    Style::default().fg(Color::Red).add_modifier(Modifier::BOLD),
                ),
                Span::styled(error, Style::default().fg(Color::Red)),
            ]));
            text.push(Line::from(""));
        }

        for line in modal.input_buffer.lines() {
            text.push(Line::from(vec![
                Span::styled(" > ", Style::default().fg(Color::Yellow)),
                Span::raw(line),
            ]));
        }

        if modal.input_buffer.is_empty() || modal.input_buffer.ends_with('\n') {
            text.push(Line::from(vec![
                Span::styled(" > ", Style::default().fg(Color::Yellow)),
                Span::styled("█", Style::default().fg(Color::Yellow)),
            ]));
        } else {
            if let Some(last) = text.last_mut() {
                last.spans
                    .push(Span::styled("█", Style::default().fg(Color::Yellow)));
            }
        }

        text.push(Line::from(""));
        text.push(Line::from(Span::styled(
            " [Enter] Next/Copy | [Alt+Enter] New Line | [Esc] Cancel ",
            Style::default().fg(Color::DarkGray),
        )));

        f.render_widget(
            Paragraph::new(text).block(block).wrap(Wrap { trim: false }),
            area,
        );
    }
}

pub fn render_confirmation_modal(f: &mut Frame, state: &mut AppState) {
    if let Some(modal) = &state.confirmation_modal {
        let area = centered_rect(60, 30, f.size());
        f.render_widget(Clear, area);

        let block = Block::default()
            .borders(Borders::ALL)
            .title(modal.title.as_str())
            .border_style(Style::default().fg(Color::Red))
            .padding(Padding::uniform(1));

        let text = vec![
            Line::from(vec![Span::styled(
                "⚠️  ACTION REQUIRED",
                Style::default().fg(Color::Red).add_modifier(Modifier::BOLD),
            )]),
            Line::from(""),
            Line::from(modal.message.as_str()),
            Line::from(""),
            Line::from(vec![
                Span::styled(
                    " [y] ",
                    Style::default()
                        .fg(Color::Green)
                        .add_modifier(Modifier::BOLD),
                ),
                Span::raw("Confirm"),
                Span::raw("  "),
                Span::styled(
                    " [n] ",
                    Style::default().fg(Color::Red).add_modifier(Modifier::BOLD),
                ),
                Span::raw("Cancel"),
            ]),
        ];

        f.render_widget(
            Paragraph::new(text).block(block).wrap(Wrap { trim: true }),
            area,
        );
    }
}
