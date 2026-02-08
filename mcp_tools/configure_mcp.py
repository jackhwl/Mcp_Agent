import json
import os
from pathlib import Path

# Detect absolute paths
venv_python = str((Path(__file__).parent / ".venv" / "Scripts" / "python.exe").resolve())
jira_server = str((Path(__file__).parent / "servers" / "jira_mcp_server.py").resolve())
bitbucket_server = str((Path(__file__).parent / "servers" / "bitbucket_server.py").resolve())
confluence_server = str((Path(__file__).parent / "servers" / "confluence_server.py").resolve())
asana_server = str((Path(__file__).parent / "servers" / "asana_server.py").resolve())
testrail_server = str((Path(__file__).parent / "servers" / "testrail_mcp_server.py").resolve())

# Path to global VSCode settings (cross-platform)
if os.name == 'nt':  # Windows
    settings_path = Path(os.path.expanduser("~")) / "AppData" / "Roaming" / "Code" / "User" / "settings.json"
else:  # macOS/Linux
    settings_path = Path(os.path.expanduser("~")) / ".config" / "Code" / "User" / "settings.json"

# Ensure the directory exists
settings_path.parent.mkdir(parents=True, exist_ok=True)

# Load existing settings or create empty dict
if settings_path.exists():
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
else:
    settings = {}

# Update only the MCP config, preserving all other settings
settings.setdefault("mcp", {})
settings["mcp"].setdefault("servers", {})

# Configure JIRA MCP Server
settings["mcp"]["servers"]["jira-mcp-server"] = {
    "type": "stdio",
    "command": venv_python,
    "args": [jira_server],
    "env": {
        "JIRA_AUTH_TOKEN": "your-secure-auth-token",
        "JIRA_BASE_URL": "https://wljira.wenlin.net"
    }
}

# Configure Bitbucket MCP Server
settings["mcp"]["servers"]["bitbucket-mcp-server"] = {
    "type": "stdio",
    "command": venv_python,
    "args": [bitbucket_server],
    "env": {
        "BITBUCKET_AUTH_TOKEN": "your-secure-auth-token",
        "BITBUCKET_BASE_URL": "http://wlstash.wenlin.net"
    }
}

# Configure Confluence MCP Server
settings["mcp"]["servers"]["confluence-mcp-server"] = {
    "type": "stdio",
    "command": venv_python,
    "args": [confluence_server],
    "env": {
        "CONFLUENCE_USERNAME": "your-confluence-username",
        "CONFLUENCE_AUTH_TOKEN": "your-secure-auth-token",
        "CONFLUENCE_BASE_URL": "https://wlwiki.wenlin.net/"
    }
}

# Configure Asana MCP Server
settings["mcp"]["servers"]["asana-mcp-server"] = {
    "type": "stdio",
    "command": venv_python,
    "args": [asana_server],
    "env": {
        "ASANA_AUTH_TOKEN": "your-secure-auth-token",
        "ASANA_BASE_URL": "https://app.asana.com/api/1.0",
        "ASANA_DISABLE_SSL_VERIFY": "false"
    }
}

# Configure TestRail MCP Server
settings["mcp"]["servers"]["testrail-mcp-server"] = {
    "type": "stdio",
    "command": venv_python,
    "args": [testrail_server],
    "env": {
        "TESTRAIL_URL": "https://your-testrail-instance.testrail.io",
        "TESTRAIL_USERNAME": "your-testrail-username",
        "TESTRAIL_API_KEY": "your-testrail-api-key"
    }
}

# Save settings back to file
with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(settings, f, indent=4)

print(f"Updated global VSCode settings at: {settings_path}")
print(f"JIRA MCP server configured with:\n  command: {venv_python}\n  args: [{jira_server}]")
print(f"Bitbucket MCP server configured with:\n  command: {venv_python}\n  args: [{bitbucket_server}]")
print(f"Confluence MCP server configured with:\n  command: {venv_python}\n  args: [{confluence_server}]")
print(f"Asana MCP server configured with:\n  command: {venv_python}\n  args: [{asana_server}]")
print(f"TestRail MCP server configured with:\n  command: {venv_python}\n  args: [{testrail_server}]")
print("\nIMPORTANT: Update your authentication tokens in the VSCode settings!")
print("- JIRA_AUTH_TOKEN: Your JIRA API token")
print("- BITBUCKET_AUTH_TOKEN: Your Bitbucket authentication token")
print("- CONFLUENCE_USERNAME & CONFLUENCE_API_KEY: Your Confluence credentials")
print("- ASANA_AUTH_TOKEN: Your Asana Personal Access Token")
print("- TESTRAIL_URL, TESTRAIL_USERNAME & TESTRAIL_API_KEY: Your TestRail credentials")
print("- Adjust BASE_URLs if using different instances")