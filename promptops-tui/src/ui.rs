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

    if state.focus == Focus::InputModal {
        render_modal(f, state);
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
            Focus::Categories => " [j/k/↑/↓] Navigate | [Tab/l/→] Select Prompts | [/] Search | [q] Quit ",
            Focus::Prompts => " [j/k/↑/↓] Navigate | [Enter] Use | [v] Preview | [h/←] Categories | [/] Search ",
            Focus::Search => " [Type] Search | [Enter] Confirm | [Esc] Cancel ",
            Focus::InputModal => " [Type] Input | [Enter] Next/Copy | [Esc] Cancel ",
        };
        f.render_widget(Paragraph::new(help).style(Style::default().fg(Color::DarkGray)), area);
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
    let focus_style = if state.focus == Focus::Prompts {
        Style::default().fg(Color::Yellow)
    } else {
        Style::default().fg(Color::DarkGray)
    };

    let items: Vec<ListItem> = state.filter_prompts
        .iter()
        .enumerate()
        .map(|(i, p)| {
            let style = if i == state.selected_prompt_index {
                Style::default().fg(Color::Green).add_modifier(Modifier::BOLD)
            } else {
                Style::default()
            };
            ListItem::new(format!("• {}", p.name)).style(style)
        })
        .collect();

    let title = if !state.search_query.is_empty() {
        format!(" Results ({}) ", state.filter_prompts.len())
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
    let prompt = state.filter_prompts.get(state.selected_prompt_index);
    let block = Block::default()
        .borders(Borders::ALL)
        .title(" Details ")
        .padding(Padding::uniform(1));
    
    if let Some(p) = prompt {
        if state.show_preview {
            render_preview(f, p, block, area);
        } else {
            render_metadata(f, p, block, area);
        }
    } else {
        f.render_widget(Paragraph::new(" No prompt selected ").block(block), area);
    }
}

fn render_metadata(f: &mut Frame, p: &crate::model::Prompt, block: Block, area: Rect) {
    let mut text = Vec::new();
    text.push(Line::from(vec![
        Span::styled("Name:    ", Style::default().fg(Color::DarkGray)),
        Span::styled(&p.name, Style::default().add_modifier(Modifier::BOLD).fg(Color::White)),
    ]));
    text.push(Line::from(vec![
        Span::styled("Version: ", Style::default().fg(Color::DarkGray)),
        Span::raw(&p.version),
    ]));
    text.push(Line::from(vec![
        Span::styled("Updated: ", Style::default().fg(Color::DarkGray)),
        Span::raw(&p.last_updated),
    ]));
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
        .wrap(Wrap { trim: true });
    f.render_widget(paragraph, area);
}

fn render_preview(f: &mut Frame, p: &crate::model::Prompt, block: Block, area: Rect) {
    let mut spans = Vec::new();
    let content = &p.prompt;
    
    // Simple "syntax highlighting" for variables
    let mut last_idx = 0;
    let re = regex::Regex::new(r"\{\{\s*(\w+)\s*\}\}").unwrap();
    for cap in re.find_iter(content) {
        // Add text before the variable
        spans.push(Span::raw(&content[last_idx..cap.start()]));
        // Add the variable itself with styling
        spans.push(Span::styled(
            &content[cap.start()..cap.end()],
            Style::default().fg(Color::Magenta).add_modifier(Modifier::BOLD)
        ));
        last_idx = cap.end();
    }
    spans.push(Span::raw(&content[last_idx..]));

    let paragraph = Paragraph::new(Text::from(Line::from(spans)))
        .block(block.title(" Preview Content (v to hide) "))
        .wrap(Wrap { trim: true });
    f.render_widget(paragraph, area);
}

fn render_modal(f: &mut Frame, state: &AppState) {
    if let Some(modal) = &state.input_modal {
        let area = centered_rect(80, 50, f.size()); // Increased size for multiline
        f.render_widget(Clear, area);

        let var_name = &modal.variables[modal.current_var_index];
        let progress = format!("Step {} of {}", modal.current_var_index + 1, modal.variables.len());
        
        // Use user-friendly label
        let label = if var_name == "args" {
            &modal.args_description
        } else {
            var_name
        };

        let block = Block::default()
            .borders(Borders::ALL)
            .title(format!(" Hydrating: {} ", modal.prompt_name))
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

        // Split input buffer by newlines to show multiline input
        for line in modal.input_buffer.lines() {
            text.push(Line::from(vec![
                Span::styled(" > ", Style::default().fg(Color::Yellow)),
                Span::raw(line),
            ]));
        }
        
        // If empty or ends with newline, show the cursor line
        if modal.input_buffer.is_empty() || modal.input_buffer.ends_with('\n') {
            text.push(Line::from(vec![
                Span::styled(" > ", Style::default().fg(Color::Yellow)),
                Span::styled("█", Style::default().fg(Color::Yellow)),
            ]));
        } else {
            // Add a trailing cursor to the last line? (Simplified for now)
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
