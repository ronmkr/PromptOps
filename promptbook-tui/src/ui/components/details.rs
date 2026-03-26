use crate::model::{AppState, Focus, Prompt};
use ratatui::{
    layout::{Margin, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{
        Block, Borders, Padding, Paragraph, Scrollbar, ScrollbarOrientation, ScrollbarState, Wrap,
    },
    Frame,
};

pub fn render_details(f: &mut Frame, state: &mut AppState, area: Rect) {
    let is_modal = matches!(
        state.focus,
        Focus::InputModal | Focus::VersionSelection | Focus::ConfirmationModal
    );
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
        if let Some(p) = g.versions.get(g.selected_version_index).cloned() {
            if state.show_preview {
                render_preview(f, &p, block, area, state);
            } else {
                render_metadata(f, &p, block, area, state);
            }
        } else {
            f.render_widget(Paragraph::new(" No version selected ").block(block), area);
        }
    } else {
        f.render_widget(Paragraph::new(" No prompt selected ").block(block), area);
    }
}

fn render_metadata(f: &mut Frame, p: &Prompt, block: Block, area: Rect, state: &mut AppState) {
    let is_modal = matches!(
        state.focus,
        Focus::InputModal | Focus::VersionSelection | Focus::ConfirmationModal
    );
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

    let display_name = if let Some(v_id) = &p.metadata.version_id {
        format!("{}:{}", p.metadata.name, v_id)
    } else {
        p.metadata.name.clone()
    };

    text.push(Line::from(vec![
        Span::styled("Name:      ", label_style),
        Span::styled(display_name, bold_value_style),
    ]));
    text.push(Line::from(vec![
        Span::styled("Version:   ", label_style),
        Span::styled(&p.metadata.version, value_style),
    ]));
    text.push(Line::from(vec![
        Span::styled("Updated:   ", label_style),
        Span::styled(&p.metadata.last_updated, value_style),
    ]));

    for (key, value) in &p.raw_data {
        if key == "prompt"
            || key == "name"
            || key == "version_id"
            || key == "system_prompt"
            || key == "user_prompt"
            || key == "description"
            || key == "args_description"
            || key == "version"
            || key == "last_updated"
            || key == "tags"
            || key == "sensitive"
        {
            continue;
        }
        let val_str = match value {
            serde_json::Value::String(s) => s.clone(),
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
    text.push(Line::from(Span::styled(
        p.metadata.description.as_str(),
        desc_style,
    )));
    text.push(Line::from(""));
    text.push(Line::from(vec![
        Span::styled("Input:     ", label_style),
        Span::styled(&p.metadata.args_description, cyan_style),
    ]));

    let tags_spans: Vec<Span> = p
        .metadata
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

use once_cell::sync::Lazy;

static RE_VARS: Lazy<regex::Regex> = Lazy::new(|| {
    #[allow(clippy::expect_used)]
    regex::Regex::new(r"\{\{\s*(.+?)\s*\}\}").expect("Invalid regex for prompt variables")
});

fn render_preview(f: &mut Frame, p: &Prompt, block: Block, area: Rect, state: &mut AppState) {
    let is_modal = matches!(
        state.focus,
        Focus::InputModal | Focus::VersionSelection | Focus::ConfirmationModal
    );
    let is_focused = state.focus == Focus::Details && !is_modal;

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
    let section_header_style = if is_focused {
        Style::default()
            .fg(Color::Yellow)
            .add_modifier(Modifier::BOLD)
    } else {
        Style::default().fg(Color::Rgb(150, 150, 50))
    };

    let mut lines = Vec::new();

    if !p.system_prompt.is_empty() || !p.user_prompt.is_empty() {
        if !p.system_prompt.is_empty() {
            lines.push(Line::from(vec![Span::styled(
                "--- SYSTEM ---",
                section_header_style,
            )]));
            for line_content in p.system_prompt.lines() {
                let mut spans = Vec::new();
                let mut last_idx = 0;
                for cap in RE_VARS.find_iter(line_content) {
                    let cap: regex::Match = cap;
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
            lines.push(Line::from(""));
        }

        if !p.user_prompt.is_empty() {
            lines.push(Line::from(vec![Span::styled(
                "--- USER ---",
                section_header_style,
            )]));
            for line_content in p.user_prompt.lines() {
                let mut spans = Vec::new();
                let mut last_idx = 0;
                for cap in RE_VARS.find_iter(line_content) {
                    let cap: regex::Match = cap;
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
            lines.push(Line::from(""));
        }

        if !p.prompt.is_empty() {
            lines.push(Line::from(vec![Span::styled(
                "--- LEGACY PROMPT ---",
                section_header_style,
            )]));
            for line_content in p.prompt.lines() {
                let mut spans = Vec::new();
                let mut last_idx = 0;
                for cap in RE_VARS.find_iter(line_content) {
                    let cap: regex::Match = cap;
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
            lines.push(Line::from(""));
        }
    } else {
        for line_content in p.prompt.lines() {
            let mut spans = Vec::new();
            let mut last_idx = 0;
            for cap in RE_VARS.find_iter(line_content) {
                let cap: regex::Match = cap;
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
