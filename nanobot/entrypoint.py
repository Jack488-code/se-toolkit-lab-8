#!/usr/bin/env python3
import json, os
def main():
    config_path = "/app/nanobot/config.json"
    workspace_path = "/app/nanobot/workspace"
    resolved_path = "/tmp/config.resolved.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    if "providers" not in config:
        config["providers"] = {"custom": {}}
    if "custom" not in config["providers"]:
        config["providers"]["custom"] = {}
    if "agents" not in config:
        config["agents"] = {"defaults": {}}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    if "gateway" not in config:
        config["gateway"] = {}
    if "tools" not in config:
        config["tools"] = {"mcpServers": {}}
    if "mcpServers" not in config["tools"]:
        config["tools"]["mcpServers"] = {}
    if "lms" not in config["tools"]["mcpServers"]:
        config["tools"]["mcpServers"]["lms"] = {"command": "python", "args": ["-m", "mcp_lms", "http://backend:8000"], "env": {}}
    if "env" not in config["tools"]["mcpServers"]["lms"]:
        config["tools"]["mcpServers"]["lms"]["env"] = {}
    if os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = os.environ["LLM_API_KEY"]
    if os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = os.environ["LLM_API_BASE_URL"]
    if os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = os.environ["LLM_API_MODEL"]
    if os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = os.environ["NANOBOT_GATEWAY_CONTAINER_ADDRESS"]
    if os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(os.environ["NANOBOT_GATEWAY_CONTAINER_PORT"])
    if os.environ.get("NANOBOT_LMS_BACKEND_URL"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = os.environ["NANOBOT_LMS_BACKEND_URL"]
    if os.environ.get("NANOBOT_LMS_API_KEY"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = os.environ["NANOBOT_LMS_API_KEY"]
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Resolved config written to {resolved_path}")
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", workspace_path])
if __name__ == "__main__":
    main()
