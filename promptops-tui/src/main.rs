mod model;
mod loader;
mod ui;
mod hydrate;
mod clipboard;

use anyhow::Result;
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{backend::CrosstermBackend, Terminal};
use std::{io, path::Path, time::Duration, collections::HashMap};
use crate::model::{AppState, Focus, InputModal, Prompt};

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
        // Fallback for running from inside promptops-tui directory
        prompts_path = Path::new("../commands/prompts").to_path_buf();
    }
    
    if !prompts_path.exists() {
        // Restore terminal before exiting with error
        disable_raw_mode()?;
        execute!(terminal.backend_mut(), LeaveAlternateScreen, DisableMouseCapture)?;
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

use crossterm::event::{KeyEvent, KeyModifiers};

fn run_app<B: ratatui::backend::Backend>(
    terminal: &mut Terminal<B>,
    app: &mut AppState,
) -> io::Result<()> {
    loop {
        terminal.draw(|f| ui::render(f, app))?;

        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                match app.focus {
                    Focus::InputModal => handle_modal_input(app, key),
                    Focus::Search => handle_search_input(app, key.code),
                    Focus::VersionSelection => handle_version_selection(app, key.code),
                    _ => handle_navigation_input(app, key.code),
                }
            }
        }
        
        app.check_status_timeout();

        if app.should_quit {
            return Ok(());
        }
    }
}

fn handle_navigation_input(app: &mut AppState, code: KeyCode) {
    match code {
        KeyCode::Char('q') => app.should_quit = true,
        KeyCode::Down | KeyCode::Char('j') => app.next(),
        KeyCode::Up | KeyCode::Char('k') => app.previous(),
        KeyCode::Right | KeyCode::Tab | KeyCode::Char('l') => {
            app.focus = Focus::Prompts;
        }
        KeyCode::Left | KeyCode::Char('h') => {
            app.focus = Focus::Categories;
        }
        KeyCode::Char('/') => {
            app.last_focus = app.focus.clone();
            app.focus = Focus::Search;
        }
        KeyCode::Char('v') => {
            app.show_preview = !app.show_preview;
        }
        KeyCode::Enter => {
            if let Some(group) = app.filter_groups.get(app.selected_prompt_index) {
                if group.versions.len() > 1 {
                    app.focus = Focus::VersionSelection;
                } else {
                    start_hydration(app, group.versions[0].clone());
                }
            }
        }
        _ => {}
    }
}

fn handle_version_selection(app: &mut AppState, code: KeyCode) {
    match code {
        KeyCode::Esc => {
            app.focus = Focus::Prompts;
        }
        KeyCode::Enter => {
            let group = app.filter_groups[app.selected_prompt_index].clone();
            let version = group.versions[group.selected_version_index].clone();
            start_hydration(app, version);
        }
        KeyCode::Down | KeyCode::Char('j') => app.next(),
        KeyCode::Up | KeyCode::Char('k') => app.previous(),
        _ => {}
    }
}

fn start_hydration(app: &mut AppState, prompt: Prompt) {
    let vars = hydrate::get_variables(&prompt.prompt);
    if vars.is_empty() {
        let content = prompt.prompt.clone();
        let _ = clipboard::copy_to_clipboard(&content);
        app.set_status(format!("Success: '{}' copied!", prompt.name), 3);
        app.focus = Focus::Prompts;
    } else {
        app.input_modal = Some(InputModal {
            prompt_name: prompt.name.clone(),
            version_id: prompt.version_id.clone(),
            variables: vars,
            current_var_index: 0,
            values: HashMap::new(),
            input_buffer: String::new(),
            args_description: prompt.args_description.clone(),
        });
        app.focus = Focus::InputModal;
    }
}

fn handle_search_input(app: &mut AppState, code: KeyCode) {
    match code {
        KeyCode::Esc => {
            app.search_query.clear();
            app.update_filter();
            app.focus = app.last_focus.clone();
        }
        KeyCode::Enter => {
            app.focus = Focus::Prompts;
        }
        KeyCode::Char(c) => {
            app.search_query.push(c);
            app.update_filter();
        }
        KeyCode::Backspace => {
            app.search_query.pop();
            app.update_filter();
        }
        _ => {}
    }
}

use glob::glob;
use std::fs;

fn resolve_file_injection(val: &str) -> String {
    if !val.starts_with('@') {
        return val.to_string();
    }

    let pattern = &val[1..];
    let mut contents = Vec::new();
    let mut files = Vec::<std::path::PathBuf>::new();

    if let Ok(entries) = glob(pattern) {
        for entry in entries.filter_map(Result::ok) {
            if entry.is_file() {
                files.push(entry);
            }
        }
    }

    if files.is_empty() {
        return val.to_string();
    }

    files.sort();

    for f_path in &files {
        if let Ok(content) = fs::read_to_string(f_path) {
            let content = content.trim();
            if files.len() > 1 {
                contents.push(format!("--- File: {} ---\n{}", f_path.display(), content));
            } else {
                contents.push(content.to_string());
            }
        }
    }

    if contents.is_empty() {
        val.to_string()
    } else {
        contents.join("\n\n")
    }
}

fn handle_modal_input(app: &mut AppState, event: KeyEvent) {
    if let Some(modal) = &mut app.input_modal {
        match event.code {
            KeyCode::Esc => {
                app.input_modal = None;
                app.focus = Focus::Prompts;
            }
            KeyCode::Enter => {
                // Alt+Enter or Ctrl+Enter for newline
                if event.modifiers.contains(KeyModifiers::ALT) || event.modifiers.contains(KeyModifiers::CONTROL) {
                    modal.input_buffer.push('\n');
                } else {
                    // Resolve file injection if needed
                    let resolved_val = resolve_file_injection(&modal.input_buffer);
                    
                    let var_name = modal.variables[modal.current_var_index].clone();
                    modal.values.insert(var_name, resolved_val);
                    modal.input_buffer.clear();
                    
                    if modal.current_var_index + 1 < modal.variables.len() {
                        modal.current_var_index += 1;
                    } else {
                        if let Some(prompt) = app.all_prompts.iter().find(|p| {
                            p.name == modal.prompt_name && p.version_id == modal.version_id
                        }) {
                            let hydrated = hydrate::hydrate_prompt(&prompt.prompt, &modal.values);
                            let _ = clipboard::copy_to_clipboard(&hydrated);
                            app.set_status(format!("Success: '{}' copied!", prompt.name), 4);
                        }
                        app.input_modal = None;
                        app.focus = Focus::Prompts;
                    }
                }
            }
            KeyCode::Char(c) => {
                modal.input_buffer.push(c);
            }
            KeyCode::Backspace => {
                modal.input_buffer.pop();
            }
            _ => {}
        }
    }
}
