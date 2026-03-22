use ratatui::{
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span, Text},
    widgets::{Block, Borders, List, ListItem, Paragraph, Wrap, Clear, Padding},
    Frame,
};
use crate::model::{AppState, Focus};

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
    
    let main_chunks = Layout::default()
        .direction(Direction::Horizontal)
        .constraints([
            Constraint::Percentage(25), // Categories
            Constraint::Percentage(35), // Prompts
            Constraint::Percentage(40), // Details
        ])
        .split(outer_layout[1]);

    render_categories(f, state, main_chunks[0]);
    render_prompts(f, state, main_chunks[1]);
    render_details(f, state, main_chunks[2]);
    render_footer(f, state, outer_layout[2]);

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

fn render_header(f: &mut Frame, state: &AppState, area: Rect) {
    let focus_style = if state.focus == Focus::Search {
        Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD)
    } else {
        Style::default().fg(Color::DarkGray)
    };

    let title = if state.search_query.is_empty() && state.focus != Focus::Search {
        " PromptOps Explorer "
    } else {
        " Search Prompts "
    };

    let search_content = if state.search_query.is_empty() && state.focus != Focus::Search {
        " Press [/] to search all prompts... ".to_string()
    } else {
        format!(" > {}█", state.search_query)
    };

    let header = Paragraph::new(search_content)
        .block(Block::default()
            .borders(Borders::ALL)
            .title(title)
            .border_style(focus_style));
    
    f.render_widget(header, area);
}

fn render_footer(f: &mut Frame, state: &AppState, area: Rect) {
    if let Some(msg) = &state.status_message {
        let style = Style::default().bg(Color::Green).fg(Color::Black).add_modifier(Modifier::BOLD);
        f.render_widget(Paragraph::new(format!(" {} ", msg)).style(style), area);
    } else {
        let help = match state.focus {
            Focus::Categories => " [j/k/↑/↓] Navigate | [^u/^d] Scroll | [Tab/l/→] Select Prompts | [/] Search | [q] Quit ",
            Focus::Prompts => " [j/k/↑/↓] Navigate | [^u/^d] Scroll | [Enter] Select | [v] Preview | [h/←] Categories | [/] Search ",
            Focus::VersionSelection => " [j/k/↑/↓] Change Version | [Enter] Use | [Esc] Back ",
            Focus::Search => " [Type] Search | [Enter] Confirm | [Esc] Cancel ",
            Focus::InputModal => " [Type] Input | [Enter] Next/Copy | [Alt+Enter] New Line | [Esc] Cancel ",
            Focus::ConfirmationModal => " [y] Confirm | [n/Esc] Cancel ",
        };
        f.render_widget(Paragraph::new(help).style(Style::default().fg(Color::DarkGray)), area);
    }
}

fn render_confirmation_modal(f: &mut Frame, state: &AppState) {
    if let Some(modal) = &state.confirmation_modal {
        let area = centered_rect(60, 30, f.size());
        f.render_widget(Clear, area);

        let block = Block::default()
            .borders(Borders::ALL)
            .title(modal.title.as_str())
            .border_style(Style::default().fg(Color::Red))
            .padding(Padding::uniform(1));

        let text = vec![
            Line::from(vec![
                Span::styled("⚠️  ACTION REQUIRED", Style::default().fg(Color::Red).add_modifier(Modifier::BOLD)),
            ]),
            Line::from(""),
            Line::from(modal.message.as_str()),
            Line::from(""),
            Line::from(vec![
                Span::styled(" [y] ", Style::default().fg(Color::Green).add_modifier(Modifier::BOLD)),
                Span::raw("Confirm"),
                Span::raw("  "),
                Span::styled(" [n] ", Style::default().fg(Color::Red).add_modifier(Modifier::BOLD)),
                Span::raw("Cancel"),
            ]),
        ];

        f.render_widget(Paragraph::new(text).block(block).wrap(Wrap { trim: true }), area);
    }
}

fn render_categories(f: &mut Frame, state: &AppState, area: Rect) {
    let focus_style = if state.focus == Focus::Categories {
        Style::default().fg(Color::Yellow)
    } else {
        Style::default().fg(Color::DarkGray)
    };

    let items: Vec<ListItem> = state.categories
        .iter()
        .enumerate()
        .map(|(i, (name, count))| {
            let style = if i == state.selected_category_index {
                Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD)
            } else {
                Style::default()
            };
            let content = format!("{:<18} [{:>2}]", name, count);
            ListItem::new(content).style(style)
        })
        .collect();

    let list = List::new(items)
        .block(Block::default()
            .borders(Borders::ALL)
            .title(" Domains ")
            .border_style(focus_style)
            .padding(Padding::horizontal(1)))
        .highlight_style(Style::default().bg(Color::Rgb(40, 40, 40)));

    f.render_widget(list, area);
}

fn render_prompts(f: &mut Frame, state: &AppState, area: Rect) {
    let focus_style = if state.focus == Focus::Prompts || state.focus == Focus::VersionSelection {
        Style::default().fg(Color::Yellow)
    } else {
        Style::default().fg(Color::DarkGray)
    };

    let items: Vec<ListItem> = state.filter_groups
        .iter()
        .enumerate()
        .map(|(i, g)| {
            let style = if i == state.selected_prompt_index {
                Style::default().fg(Color::Green).add_modifier(Modifier::BOLD)
            } else {
                Style::default()
            };
            
            let v_count = g.versions.len();
            let label = if v_count > 1 {
                format!("• {} ({} versions)", g.name, v_count)
            } else {
                format!("• {}", g.name)
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
        .block(Block::default()
            .borders(Borders::ALL)
            .title(title)
            .border_style(focus_style)
            .padding(Padding::horizontal(1)))
        .highlight_style(Style::default().bg(Color::Rgb(40, 40, 40)));

    f.render_widget(list, area);
}

fn render_details(f: &mut Frame, state: &AppState, area: Rect) {
    let group = state.filter_groups.get(state.selected_prompt_index);
    let block = Block::default()
        .borders(Borders::ALL)
        .title(" Details ")
        .padding(Padding::uniform(1));

    if let Some(g) = group {
        let p = &g.versions[g.selected_version_index];
        if state.show_preview {
            render_preview(f, p, block, area, state);
        } else {
            render_metadata(f, p, block, area, state);
        }
    } else {
        f.render_widget(Paragraph::new(" No prompt selected ").block(block), area);
    }
}

fn render_metadata(f: &mut Frame, p: &crate::model::Prompt, block: Block, area: Rect, state: &AppState) {
    let mut text = Vec::new();
    
    let display_name = if let Some(v_id) = &p.version_id {
        format!("{}:{}", p.name, v_id)
    } else {
        p.name.clone()
    };

    text.push(Line::from(vec![
        Span::styled("Name:    ", Style::default().fg(Color::DarkGray)),
        Span::styled(display_name, Style::default().add_modifier(Modifier::BOLD).fg(Color::White)),
    ]));
    text.push(Line::from(vec![
        Span::styled("Version: ", Style::default().fg(Color::DarkGray)),
        Span::raw(&p.version),
    ]));
    text.push(Line::from(vec![
        Span::styled("Updated: ", Style::default().fg(Color::DarkGray)),
        Span::raw(&p.last_updated),
    ]));

    for (key, value) in &p.metadata {
        if key == "prompt" || key == "name" || key == "version_id" { continue; }
        let val_str = match value {
            toml::Value::String(s) => s.clone(),
            _ => value.to_string(),
        };
        text.push(Line::from(vec![
            Span::styled(format!("{:<8} ", format!("{}:", key)), Style::default().fg(Color::DarkGray)),
            Span::raw(val_str),
        ]));
    }

    text.push(Line::from(""));
    text.push(Line::from(Span::styled("Description:", Style::default().add_modifier(Modifier::BOLD))));
    text.push(Line::from(p.description.as_str()));
    text.push(Line::from(""));
    text.push(Line::from(vec![
        Span::styled("Input:   ", Style::default().fg(Color::DarkGray)),
        Span::styled(&p.args_description, Style::default().fg(Color::Cyan)),
    ]));
    
    let tags_spans: Vec<Span> = p.tags.iter().map(|t| Span::styled(format!(" #{} ", t), Style::default().bg(Color::Rgb(50, 50, 50)).fg(Color::Gray))).collect();
    text.push(Line::from(""));
    text.push(Line::from(tags_spans));

    text.push(Line::from(""));
    text.push(Line::from(vec![
        Span::styled(" [v] ", Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD)),
        Span::raw("Show Preview Content"),
    ]));
    text.push(Line::from(vec![
        Span::styled(" [Enter] ", Style::default().fg(Color::Green).add_modifier(Modifier::BOLD)),
        Span::raw("Hydrate & Copy"),
    ]));
    
    let paragraph = Paragraph::new(text)
        .block(block)
        .wrap(Wrap { trim: true })
        .scroll((state.details_scroll, 0));
    f.render_widget(paragraph, area);
}

fn render_preview(f: &mut Frame, p: &crate::model::Prompt, block: Block, area: Rect, state: &AppState) {
    let mut spans = Vec::new();
    let content = &p.prompt;
    
    let mut last_idx = 0;
    let re = regex::Regex::new(r"\{\{\s*(\w+)\s*\}\}").unwrap();
    for cap in re.find_iter(content) {
        spans.push(Span::raw(&content[last_idx..cap.start()]));
        spans.push(Span::styled(
            &content[cap.start()..cap.end()],
            Style::default().fg(Color::Magenta).add_modifier(Modifier::BOLD)
        ));
        last_idx = cap.end();
    }
    spans.push(Span::raw(&content[last_idx..]));

    let paragraph = Paragraph::new(Text::from(Line::from(spans)))
        .block(block.title(" Preview Content (v to hide) "))
        .wrap(Wrap { trim: true })
        .scroll((state.details_scroll, 0));
    f.render_widget(paragraph, area);
}

fn render_version_modal(f: &mut Frame, state: &AppState) {
    let group = &state.filter_groups[state.selected_prompt_index];
    let area = centered_rect(60, 40, f.size());
    f.render_widget(Clear, area);

    let block = Block::default()
        .borders(Borders::ALL)
        .title(format!(" Choose Version for: {} ", group.name))
        .border_style(Style::default().fg(Color::Yellow))
        .padding(Padding::uniform(1));

    let items: Vec<ListItem> = group.versions
        .iter()
        .enumerate()
        .map(|(i, v)| {
            let style = if i == group.selected_version_index {
                Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD)
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
    
    f.render_widget(list, area);
}

fn render_modal(f: &mut Frame, state: &AppState) {
    if let Some(modal) = &state.input_modal {
        let area = centered_rect(80, 50, f.size());
        f.render_widget(Clear, area);

        let var_name = &modal.variables[modal.current_var_index];
        let progress = format!("Step {} of {}", modal.current_var_index + 1, modal.variables.len());
        
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
                Span::styled(label, Style::default().fg(Color::Cyan).add_modifier(Modifier::BOLD)),
            ]),
            Line::from(""),
        ];

        if let Some(error) = &modal.error_message {
            text.push(Line::from(vec![
                Span::styled(" Error: ", Style::default().fg(Color::Red).add_modifier(Modifier::BOLD)),
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
                last.spans.push(Span::styled("█", Style::default().fg(Color::Yellow)));
            }
        }

        text.push(Line::from(""));
        text.push(Line::from(Span::styled(" [Enter] Next/Copy | [Alt+Enter] New Line | [Esc] Cancel ", Style::default().fg(Color::DarkGray))));

        f.render_widget(Paragraph::new(text).block(block).wrap(Wrap { trim: false }), area);
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
