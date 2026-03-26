use crate::model::{AppState, Focus};
use ratatui::{
    layout::Rect,
    style::{Color, Modifier, Style},
    widgets::Paragraph,
    Frame,
};

pub fn render_footer(f: &mut Frame, state: &mut AppState, area: Rect) {
    if let Some(msg) = &state.status_message {
        let style = Style::default()
            .bg(Color::Green)
            .fg(Color::Black)
            .add_modifier(Modifier::BOLD);
        f.render_widget(Paragraph::new(format!(" {} ", msg)).style(style), area);
    } else {
        let width = f.size().width;
        let help = match state.focus {
            Focus::Categories => {
                if width >= 90 {
                    " [j/k/↑/↓] Navigate | [h/l/←/→/Tab] Panes | [^u/^d] Scroll Details | [/] Search | [q] Quit "
                } else if width >= 60 {
                    " [↑/↓] Nav | [←/→] Panes | [^u/^d] Scroll | [/] Search | [q] Quit "
                } else {
                    " [↑/↓] Nav | [←/→] Panes | [/] Search "
                }
            }
            Focus::Prompts => {
                if width >= 90 {
                    " [j/k/↑/↓] Navigate | [h/l/←/→/Tab] Panes | [Enter] Select | [v] Preview | [^u/^d] Scroll Details "
                } else if width >= 60 {
                    " [↑/↓] Nav | [←/→] Panes | [Enter] Sel | [v] Pre | [^u/^d] Scroll "
                } else {
                    " [↑/↓] Nav | [Enter] Sel | [v] Pre "
                }
            }
            Focus::Details => {
                if width >= 90 {
                    " [j/k/↑/↓] Scroll | [h/l/←/→/Tab] Panes | [Enter] Use | [v] Preview "
                } else if width >= 60 {
                    " [↑/↓] Scroll | [←/→] Panes | [Enter] Use | [v] Pre "
                } else {
                    " [↑/↓] Scroll | [←] Back | [Enter] Use "
                }
            }
            Focus::VersionSelection => " [j/k/↑/↓] Version | [Enter] Use | [Esc] Back ",
            Focus::Search => " [Type] Search | [Enter] Confirm | [Esc] Cancel ",
            Focus::InputModal => {
                if width >= 60 {
                    " [Type] Input | [Enter] Next/Copy | [Alt+Enter] New Line | [Esc] Cancel "
                } else {
                    " [Type] Input | [Enter] Next | [Esc] Cancel "
                }
            }
            Focus::ConfirmationModal => " [y] Confirm | [n/Esc] Cancel ",
        };
        let style = if matches!(
            state.focus,
            Focus::InputModal | Focus::VersionSelection | Focus::ConfirmationModal
        ) {
            Style::default().fg(Color::Rgb(50, 50, 50))
        } else {
            Style::default().fg(Color::DarkGray)
        };
        f.render_widget(Paragraph::new(help).style(style), area);
    }
}
