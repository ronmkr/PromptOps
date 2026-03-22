mod clipboard;
mod events;
mod hydrate;
mod loader;
mod model;
mod ui;
mod utils;

use crate::model::{AppState, Focus};
use anyhow::Result;
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{backend::CrosstermBackend, Terminal};
use std::{io, path::Path, time::Duration};

fn main() -> Result<()> {
    // 1. Setup terminal
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    // 2. Load data
    let mut prompts_path = Path::new("commands/prompts").to_path_buf();
    if !prompts_path.exists() {
        prompts_path = Path::new("../commands/prompts").to_path_buf();
    }

    if !prompts_path.exists() {
        disable_raw_mode()?;
        execute!(
            terminal.backend_mut(),
            LeaveAlternateScreen,
            DisableMouseCapture
        )?;
        terminal.show_cursor()?;
        println!("Error: Could not find 'commands/prompts' directory.");
        return Ok(());
    }

    let prompts = loader::load_prompts(&prompts_path)?;
    let mut app = AppState::new(prompts);

    // 3. Main loop
    let res = run_app(&mut terminal, &mut app);

    // 4. Restore terminal
    disable_raw_mode()?;
    execute!(
        terminal.backend_mut(),
        LeaveAlternateScreen,
        DisableMouseCapture
    )?;
    terminal.show_cursor()?;

    if let Err(err) = res {
        println!("{:?}", err);
    }

    Ok(())
}

fn run_app<B: ratatui::backend::Backend>(
    terminal: &mut Terminal<B>,
    app: &mut AppState,
) -> io::Result<()> {
    loop {
        terminal.draw(|f| ui::render(f, app))?;

        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                match app.focus {
                    Focus::InputModal => events::handle_modal_input(app, key),
                    Focus::Search => events::handle_search_input(app, key.code),
                    Focus::VersionSelection => events::handle_version_selection(app, key.code),
                    Focus::ConfirmationModal => events::handle_confirmation_modal(app, key.code),
                    _ => events::handle_navigation_input(app, key),
                }
            }
        }

        app.check_status_timeout();

        if app.should_quit {
            return Ok(());
        }
    }
}
