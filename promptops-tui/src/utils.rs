use glob::glob;
use std::fs;
use std::path::PathBuf;

const MAX_FILES_LIMIT: usize = 100;
const MAX_CHARS_LIMIT: usize = 500000;

pub fn resolve_file_injection(val: &str) -> String {
    if !val.starts_with('@') {
        return val.to_string();
    }

    let pattern = &val[1..];
    let mut files = Vec::<PathBuf>::new();

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

    // Limit number of files
    if files.len() > MAX_FILES_LIMIT {
        files.truncate(MAX_FILES_LIMIT);
    }

    let mut contents = Vec::new();
    let mut total_chars = 0;

    for f_path in &files {
        if total_chars >= MAX_CHARS_LIMIT {
            break;
        }

        if let Ok(content) = fs::read_to_string(f_path) {
            let content = content.trim();
            let mut file_text = if files.len() > 1 {
                format!("--- File: {} ---\n{}", f_path.display(), content)
            } else {
                content.to_string()
            };

            if total_chars + file_text.len() > MAX_CHARS_LIMIT {
                let remaining = MAX_CHARS_LIMIT - total_chars;
                if remaining > 50 {
                    file_text.truncate(remaining);
                    file_text.push_str("\n... [TRUNCATED due to length limit] ...");
                    contents.push(file_text);
                }
                break;
            }

            total_chars += file_text.len();
            contents.push(file_text);
        }
    }

    if contents.is_empty() {
        val.to_string()
    } else {
        contents.join("\n\n")
    }
}
