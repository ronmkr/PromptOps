use crate::model::{AppState, Focus};
use ratatui::{
    layout::{Constraint, Direction, Layout, Margin, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{
        Block, Borders, Clear, List, ListItem, ListState, Padding, Paragraph, Scrollbar,
        ScrollbarOrientation, ScrollbarState, Wrap,
    },
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
    render_footer(f, state, outer_layout[2]);

    // If modal is open, we can optionally draw a dimming layer here
    // but usually it's better to handle it inside the panes or by drawing a semi-transparent box.
    // However, Ratatui doesn't support alpha transparency well in all terminals.
    // We will handle it by dimming the foreground colors in the panes.

    if state.focus == Focus::VersionSelection {
        render_version_modal(f, state);
    }

    if state.focus == Focus::InputModal {
        render_modal(f, state);
    }

    if state.focus == Focus::ConfirmationModal {
        render_confirmation_modal(f, state);
    }
}

fn is_modal_open(state: &AppState) -> bool {
    matches!(
        state.focus,
        Focus::InputModal | Focus::VersionSelection | Focus::ConfirmationModal
    )
}

fn render_header(f: &mut Frame, state: &mut AppState, area: Rect) {
    let is_modal = is_modal_open(state);
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

fn render_footer(f: &mut Frame, state: &mut AppState, area: Rect) {
    if let Some(msg) = &state.status_message {
        let style = Style::default()
            .bg(Color::Green)
            .fg(Color::Black)
            .add_modifier(Modifier::BOLD);
        f.render_widget(Paragraph::new(format!(" {} ", msg)).style(style), area);
    } else {
        let help = match state.focus {
            Focus::Categories => " [j/k/↑/↓] Navigate | [h/l/←/→/Tab] Panes | [^u/^d] Scroll Details | [/] Search | [q] Quit ",
            Focus::Prompts => " [j/k/↑/↓] Navigate | [h/l/←/→/Tab] Panes | [Enter] Select | [v] Preview | [^u/^d] Scroll Details ",
            Focus::Details => " [j/k/↑/↓] Scroll | [h/l/←/→/Tab] Panes | [Enter] Use | [v] Preview ",
            Focus::VersionSelection => " [j/k/↑/↓] Version | [Enter] Use | [Esc] Back ",
            Focus::Search => " [Type] Search | [Enter] Confirm | [Esc] Cancel ",
            Focus::InputModal => " [Type] Input | [Enter] Next/Copy | [Alt+Enter] New Line | [Esc] Cancel ",
            Focus::ConfirmationModal => " [y] Confirm | [n/Esc] Cancel ",
        };
        let style = if is_modal_open(state) {
            Style::default().fg(Color::Rgb(50, 50, 50))
        } else {
            Style::default().fg(Color::DarkGray)
        };
        f.render_widget(Paragraph::new(help).style(style), area);
    }
}

fn render_confirmation_modal(f: &mut Frame, state: &mut AppState) {
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

fn render_categories(f: &mut Frame, state: &mut AppState, area: Rect) {
    let is_modal = is_modal_open(state);
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
                    Style::default().fg(Color::DarkGray) // Whisper, don't shout
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

fn render_prompts(f: &mut Frame, state: &mut AppState, area: Rect) {
    let is_modal = is_modal_open(state);
    let is_focused =
        (state.focus == Focus::Prompts || state.focus == Focus::VersionSelection) && !is_modal;
    let focus_style = if is_modal {
        Style::default().fg(Color::Rgb(50, 50, 50))
    } else if is_focused {
        Style::default().fg(Color::Yellow)
    } else {
        Style::default().fg(Color::DarkGray)
    };

    let items: Vec<ListItem> = state
        .filter_groups
        .iter()
        .enumerate()
        .map(|(i, g)| {
            let style = if i == state.selected_prompt_index {
                if is_modal {
                    Style::default().fg(Color::Rgb(60, 60, 60))
                } else if is_focused {
                    Style::default()
                        .fg(Color::Green)
                        .add_modifier(Modifier::BOLD)
                } else {
                    Style::default().fg(Color::DarkGray) // Whisper, don't shout
                }
            } else {
                if is_modal {
                    Style::default().fg(Color::Rgb(40, 40, 40))
                } else {
                    Style::default()
                }
            };

            let v_count = g.versions.len();
            let label = if v_count > 1 {
                format!("• {} ({} versions) ", g.name, v_count)
            } else {
                format!("• {} ", g.name)
            };

            ListItem::new(label).style(style)
        })
        .collect();

    let title = if !state.search_query.is_empty() {
        format!(" Results ({}) ", state.filter_groups.len())
    } else {
        " Prompts ".to_string()
    };

    let list = List::new(items)
        .block(
            Block::default()
                .borders(Borders::ALL)
                .title(title)
                .border_style(focus_style)
                .padding(Padding::horizontal(1)),
        )
        .highlight_style(if is_modal {
            Style::default()
        } else {
            Style::default().bg(Color::Rgb(40, 40, 40))
        });

    f.render_stateful_widget(list, area, &mut state.prompt_list_state);

    let scrollbar = Scrollbar::new(ScrollbarOrientation::VerticalRight)
        .begin_symbol(Some("↑"))
        .end_symbol(Some("↓"));
    let mut scrollbar_state =
        ScrollbarState::new(state.filter_groups.len()).position(state.selected_prompt_index);

    f.render_stateful_widget(
        scrollbar,
        area.inner(&Margin {
            vertical: 1,
            horizontal: 0,
        }),
        &mut scrollbar_state,
    );
}

fn render_details(f: &mut Frame, state: &mut AppState, area: Rect) {
    let is_modal = is_modal_open(state);
    let is_focused = state.focus == Focus::Details && !is_modal;
    let focus_style = if is_modal {
        Style::default().fg(Color::Rgb(50, 50, 50))
    } else if is_focused {
        Style::default().fg(Color::Yellow)
    } else {
        Style::default().fg(Color::DarkGray)
    };

    let block = Block::default()
        .borders(Borders::ALL)
        .title(" Details ")
        .border_style(focus_style)
        .padding(Padding::uniform(1));

    if let Some(g) = state.filter_groups.get(state.selected_prompt_index) {
        let p = g.versions[g.selected_version_index].clone();
        if state.show_preview {
            render_preview(f, &p, block, area, state);
        } else {
            render_metadata(f, &p, block, area, state);
        }
    } else {
        f.render_widget(Paragraph::new(" No prompt selected ").block(block), area);
    }
}

fn render_metadata(
    f: &mut Frame,
    p: &crate::model::Prompt,
    block: Block,
    area: Rect,
    state: &mut AppState,
) {
    let is_modal = is_modal_open(state);
    let is_focused = state.focus == Focus::Details && !is_modal;

    let label_style = if is_modal {
        Style::default().fg(Color::Rgb(50, 50, 50))
    } else if is_focused {
        Style::default().fg(Color::DarkGray)
    } else {
        Style::default().fg(Color::Rgb(60, 60, 60))
    };

    let value_style = if is_modal {
        Style::default().fg(Color::Rgb(80, 80, 80))
    } else if is_focused {
        Style::default().fg(Color::White)
    } else {
        Style::default().fg(Color::Rgb(120, 120, 120))
    };

    let bold_value_style = if is_modal {
        Style::default().fg(Color::Rgb(100, 100, 100))
    } else if is_focused {
        Style::default()
            .add_modifier(Modifier::BOLD)
            .fg(Color::White)
    } else {
        Style::default().fg(Color::Rgb(150, 150, 150))
    };

    let cyan_style = if is_modal {
        Style::default().fg(Color::Rgb(60, 80, 80))
    } else if is_focused {
        Style::default().fg(Color::Cyan)
    } else {
        Style::default().fg(Color::Rgb(0, 120, 120))
    };

    let desc_style = if is_modal {
        Style::default().fg(Color::Rgb(70, 70, 70))
    } else if is_focused {
        Style::default()
    } else {
        Style::default().fg(Color::Rgb(100, 100, 100))
    };

    let mut text = Vec::new();

    let display_name = if let Some(v_id) = &p.version_id {
        format!("{}:{}", p.name, v_id)
    } else {
        p.name.clone()
    };

    text.push(Line::from(vec![
        Span::styled("Name:      ", label_style),
        Span::styled(display_name, bold_value_style),
    ]));
    text.push(Line::from(vec![
        Span::styled("Version:   ", label_style),
        Span::styled(&p.version, value_style),
    ]));
    text.push(Line::from(vec![
        Span::styled("Updated:   ", label_style),
        Span::styled(&p.last_updated, value_style),
    ]));

    for (key, value) in &p.metadata {
        if key == "prompt" || key == "name" || key == "version_id" {
            continue;
        }
        let val_str = match value {
            toml::Value::String(s) => s.clone(),
            _ => value.to_string(),
        };
        let label = format!("{}:", key);
        text.push(Line::from(vec![
            Span::styled(format!("{:<11}", label), label_style),
            Span::styled(val_str, value_style),
        ]));
    }

    text.push(Line::from(""));
    text.push(Line::from(Span::styled(
        "Description:",
        if is_modal {
            label_style.add_modifier(Modifier::BOLD)
        } else {
            Style::default().add_modifier(Modifier::BOLD)
        },
    )));
    text.push(Line::from(Span::styled(p.description.as_str(), desc_style)));
    text.push(Line::from(""));
    text.push(Line::from(vec![
        Span::styled("Input:     ", label_style),
        Span::styled(&p.args_description, cyan_style),
    ]));

    let tags_spans: Vec<Span> = p
        .tags
        .iter()
        .map(|t| {
            let style = if is_modal {
                Style::default()
                    .bg(Color::Rgb(30, 30, 30))
                    .fg(Color::Rgb(60, 60, 60))
            } else {
                Style::default().bg(Color::Rgb(50, 50, 50)).fg(Color::Gray)
            };
            Span::styled(format!(" #{} ", t), style)
        })
        .collect();
    text.push(Line::from(""));
    text.push(Line::from(tags_spans));

    text.push(Line::from(""));
    let key_instr_style = if is_modal {
        Style::default().fg(Color::Rgb(40, 40, 40))
    } else {
        Style::default()
            .fg(Color::Rgb(100, 100, 100))
            .add_modifier(Modifier::BOLD)
    };
    let label_instr_style = if is_modal {
        Style::default().fg(Color::Rgb(30, 30, 30))
    } else {
        Style::default().fg(Color::Rgb(80, 80, 80))
    };

    text.push(Line::from(vec![
        Span::styled(" [v] ", key_instr_style),
        Span::styled("Show Preview Content", label_instr_style),
    ]));
    text.push(Line::from(vec![
        Span::styled(" [Enter] ", key_instr_style),
        Span::styled("Hydrate & Copy", label_instr_style),
    ]));

    let line_count = text.len();
    let paragraph = Paragraph::new(text)
        .block(block)
        .wrap(Wrap { trim: true })
        .scroll((state.details_scroll, 0));
    f.render_widget(paragraph, area);

    // Render scrollbar for Details
    let scrollbar = Scrollbar::new(ScrollbarOrientation::VerticalRight)
        .begin_symbol(Some("↑"))
        .end_symbol(Some("↓"));
    let mut scrollbar_state =
        ScrollbarState::new(line_count).position(state.details_scroll as usize);

    f.render_stateful_widget(
        scrollbar,
        area.inner(&Margin {
            vertical: 1,
            horizontal: 0,
        }),
        &mut scrollbar_state,
    );
}

fn render_preview(
    f: &mut Frame,
    p: &crate::model::Prompt,
    block: Block,
    area: Rect,
    state: &mut AppState,
) {
    let is_modal = is_modal_open(state);
    let is_focused = state.focus == Focus::Details && !is_modal;
    let content = &p.prompt;

    let normal_style = if is_modal {
        Style::default().fg(Color::Rgb(60, 60, 60))
    } else if is_focused {
        Style::default()
    } else {
        Style::default().fg(Color::Rgb(100, 100, 100))
    };
    let var_style = if is_modal {
        Style::default().fg(Color::Rgb(80, 40, 80))
    } else if is_focused {
        Style::default()
            .fg(Color::Magenta)
            .add_modifier(Modifier::BOLD)
    } else {
        Style::default().fg(Color::Rgb(120, 60, 120))
    };

    let re = regex::Regex::new(r"\{\{\s*(.+?)\s*\}\}").unwrap();
    let mut lines = Vec::new();

    for line_content in content.lines() {
        let mut spans = Vec::new();
        let mut last_idx = 0;
        for cap in re.find_iter(line_content) {
            if cap.start() > last_idx {
                spans.push(Span::styled(
                    &line_content[last_idx..cap.start()],
                    normal_style,
                ));
            }
            spans.push(Span::styled(
                &line_content[cap.start()..cap.end()],
                var_style,
            ));
            last_idx = cap.end();
        }
        if last_idx < line_content.len() {
            spans.push(Span::styled(&line_content[last_idx..], normal_style));
        }
        lines.push(Line::from(spans));
    }

    let line_count = lines.len();
    let paragraph = Paragraph::new(lines)
        .block(block.title(" Preview Content (v to hide) "))
        .wrap(Wrap { trim: false })
        .scroll((state.details_scroll, 0));
    f.render_widget(paragraph, area);

    // Render scrollbar for Preview
    let scrollbar = Scrollbar::new(ScrollbarOrientation::VerticalRight)
        .begin_symbol(Some("↑"))
        .end_symbol(Some("↓"));
    let mut scrollbar_state =
        ScrollbarState::new(line_count).position(state.details_scroll as usize);

    f.render_stateful_widget(
        scrollbar,
        area.inner(&Margin {
            vertical: 1,
            horizontal: 0,
        }),
        &mut scrollbar_state,
    );
}

fn render_version_modal(f: &mut Frame, state: &mut AppState) {
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

fn render_modal(f: &mut Frame, state: &mut AppState) {
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

fn centered_rect(percent_x: u16, percent_y: u16, r: Rect) -> Rect {
    let popup_layout = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Percentage((100 - percent_y) / 2),
            Constraint::Percentage(percent_y),
            Constraint::Percentage((100 - percent_y) / 2),
        ])
        .split(r);

    Layout::default()
        .direction(Direction::Horizontal)
        .constraints([
            Constraint::Percentage((100 - percent_x) / 2),
            Constraint::Percentage(percent_x),
            Constraint::Percentage((100 - percent_x) / 2),
        ])
        .split(popup_layout[1])[1]
}
