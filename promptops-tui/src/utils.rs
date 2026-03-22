use glob::glob;
use std::fs;
use std::path::PathBuf;

pub struct InjectionConfig;

impl InjectionConfig {
    pub const MAX_FILES: usize = 100;
    pub const MAX_CHARS: usize = 500000;
    pub const TRUNCATION_MARKER: &'static str = "\n... [TRUNCATED due to length limit] ...";
}

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
    if files.len() > InjectionConfig::MAX_FILES {
        files.truncate(InjectionConfig::MAX_FILES);
    }

    let mut contents = Vec::new();
    let mut total_chars = 0;

    for f_path in &files {
        if total_chars >= InjectionConfig::MAX_CHARS {
            break;
        }

        if let Ok(content) = fs::read_to_string(f_path) {
            let content = content.trim();
            let mut file_text = if files.len() > 1 {
                format!("--- File: {} ---\n{}", f_path.display(), content)
            } else {
                content.to_string()
            };

            if total_chars + file_text.len() > InjectionConfig::MAX_CHARS {
                let remaining = InjectionConfig::MAX_CHARS - total_chars;
                if remaining > 50 {
                    file_text.truncate(remaining);
                    file_text.push_str(InjectionConfig::TRUNCATION_MARKER);
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

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::tempdir;

    #[test]
    fn test_resolve_file_injection_no_prefix() {
        assert_eq!(resolve_file_injection("normal"), "normal");
    }

    #[test]
    fn test_resolve_file_injection_single_file() {
        let dir = tempdir().unwrap();
        let file_path = dir.path().join("test.txt");
        let mut file = fs::File::create(&file_path).unwrap();
        writeln!(file, "hello").unwrap();

        let val = format!("@{}", file_path.to_str().unwrap());
        assert_eq!(resolve_file_injection(&val), "hello");
    }

    #[test]
    fn test_resolve_file_injection_file_limit() {
        let dir = tempdir().unwrap();
        for i in 0..110 {
            let file_path = dir.path().join(format!("file_{:03}.txt", i));
            let mut file = fs::File::create(&file_path).unwrap();
            writeln!(file, "content").unwrap();
        }

        let pattern = dir.path().join("*.txt");
        let val = format!("@{}", pattern.to_str().unwrap());
        let result = resolve_file_injection(&val);
        
        // Should have 100 headers
        let count = result.matches("--- File:").count();
        assert_eq!(count, InjectionConfig::MAX_FILES);
    }

    #[test]
    fn test_resolve_file_injection_char_limit() {
        let dir = tempdir().unwrap();
        let large_content = "A".repeat(300000);
        
        let p1 = dir.path().join("large1.txt");
        let mut f1 = fs::File::create(&p1).unwrap();
        f1.write_all(large_content.as_bytes()).unwrap();

        let p2 = dir.path().join("large2.txt");
        let mut f2 = fs::File::create(&p2).unwrap();
        f2.write_all(large_content.as_bytes()).unwrap();

        let pattern = dir.path().join("large*.txt");
        let val = format!("@{}", pattern.to_str().unwrap());
        let result = resolve_file_injection(&val);
        
        assert!(result.len() <= InjectionConfig::MAX_CHARS + 1000);
        assert!(result.contains("[TRUNCATED due to length limit]"));
    }
}
