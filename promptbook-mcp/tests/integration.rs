use std::process::{Command, Stdio};
use std::io::{Write, BufReader, BufRead};
use serde_json::{json, Value};

#[test]
fn test_server_initialize_and_tools() {
    // 1. Build the server first to ensure we have a fresh binary
    let build_status = Command::new("cargo")
        .args(["build", "-p", "promptbook-mcp"])
        .status()
        .expect("Failed to build server");
    assert!(build_status.success());

    // 2. Spawn the server
    let mut child = Command::new("../target/debug/promptbook-mcp")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit())
        .spawn()
        .expect("Failed to spawn server");

    let mut stdin = child.stdin.take().expect("Failed to open stdin");
    let stdout = child.stdout.take().expect("Failed to open stdout");
    let mut reader = BufReader::new(stdout);

    // 3. Send initialize request
    let init_req = json!({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "1.0.0",
            "capabilities": {},
            "clientInfo": { "name": "test-client", "version": "1.0.0" }
        }
    });

    let mut req_str = init_req.to_string();
    req_str.push('\n');
    stdin.write_all(req_str.as_bytes()).expect("Failed to write to stdin");
    stdin.flush().expect("Failed to flush stdin");

    // 4. Read initialize response
    let mut line = String::new();
    reader.read_line(&mut line).expect("Failed to read from stdout");
    let resp: Value = serde_json::from_str(&line).expect("Failed to parse response");
    assert_eq!(resp["id"], 1);

    // 5. Send initialized notification (Required by MCP protocol)
    let initialized_notification = json!({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {}
    });
    let mut notification_str = initialized_notification.to_string();
    notification_str.push('\n');
    stdin.write_all(notification_str.as_bytes()).expect("Failed to write notification");
    stdin.flush().expect("Failed to flush notification");

    // 6. Send list_tools request
    let list_req = json!({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    });
    let mut list_req_str = list_req.to_string();
    list_req_str.push('\n');
    stdin.write_all(list_req_str.as_bytes()).expect("Failed to write to stdin");
    stdin.flush().expect("Failed to flush stdin");

    let mut line2 = String::new();
    reader.read_line(&mut line2).expect("Failed to read from stdout");
    let resp2: Value = serde_json::from_str(&line2).expect("Failed to parse response");
    
    assert_eq!(resp2["id"], 2);
    assert!(!resp2["result"]["tools"].as_array().expect("tools should be an array").is_empty());

    // 7. Cleanup
    child.kill().expect("Failed to kill server");
}
