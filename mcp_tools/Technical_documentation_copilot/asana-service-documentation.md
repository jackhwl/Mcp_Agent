# Asana MCP Server Documentation

## Overview

The Asana MCP Server provides comprehensive integration with Asana's API through the Model Context Protocol (MCP). It follows the same architectural pattern as the Confluence and Jira MCP servers, offering a consistent interface for task management, project tracking, and workspace operations.

## Features

### Core Capabilities
- **Workspace Management**: List and explore accessible workspaces
- **Project Operations**: Retrieve projects and their details
- **Portfolio Management**: Retrieve portfolios, their details, and contained projects
- **Task Management**: Create, read, update, and search tasks
- **User Information**: Get authenticated user details
- **Search Functionality**: Find tasks across workspaces

### Tool Functions

#### Administrative Tools
- `asana_healthcheck()` - Verify configuration and connectivity
- `get_asana_user_info()` - Get current user information

#### Workspace & Project Tools
- `get_asana_workspaces()` - List all accessible workspaces
- `get_asana_projects(workspace_gid, limit=20)` - Get projects from a workspace
- `get_asana_project_details(project_gid)` - Get detailed project information including custom fields

#### Portfolio Management Tools
- `get_asana_portfolios(workspace_gid, limit=20)` - Get portfolios from a workspace
- `get_asana_portfolio_details(portfolio_gid)` - Get detailed portfolio information including custom fields
- `get_asana_portfolio_items(portfolio_gid, limit=50)` - Get projects/items contained within a portfolio

#### Task Management Tools
- `get_asana_tasks(project_gid=None, assignee=None, limit=50)` - Retrieve tasks with filtering
- `get_asana_task_details(task_gid)` - Get detailed task information
- `create_asana_task(name, project_gid=None, assignee=None, notes=None, due_on=None)` - Create new tasks
- `update_asana_task(task_gid, name=None, notes=None, completed=None, due_on=None)` - Update existing tasks
- `search_asana_tasks(workspace_gid, text, limit=20)` - Search for tasks by text

## Configuration

### Environment Variables
- `ASANA_AUTH_TOKEN` - Personal Access Token from Asana (required)
- `ASANA_BASE_URL` - API base URL (default: https://app.asana.com/api/1.0)

### Setting up Authentication

1. **Generate Personal Access Token**:
   - Go to Asana > My Profile Settings > Apps
   - Click "Manage Developer Apps"
   - Create a new Personal Access Token
   - Copy the token securely

2. **Configure in VS Code/Cursor**:
   ```json
   {
     "mcp": {
       "servers": {
         "asana-mcp-server": {
           "env": {
             "ASANA_AUTH_TOKEN": "your_personal_access_token_here"
           }
         }
       }
     }
   }
   ```

## Architecture

The Asana MCP Server follows the established pattern:

```
asana_server.py          # Main server entry point
asana/
├── __init__.py         # Package initialization and exports
├── service.py          # Core Asana API service class
└── tools.py           # MCP tool registration and implementations
```

### Key Components

- **AsanaService**: Handles all API interactions with proper authentication and error handling
- **register_asana_tools()**: Registers all tools with the FastMCP server
- **Tool Functions**: Individual MCP tools that wrap service methods with context handling

## Usage Examples

### Getting Started
```python
# Check server health
result = await asana_healthcheck()

# Get user information
user_info = await get_asana_user_info()

# List workspaces
workspaces = await get_asana_workspaces()
```

### Task Management
```python
# Get my tasks
my_tasks = await get_asana_tasks(assignee="me")

# Create a new task
new_task = await create_asana_task(
    name="Review PR #123",
    project_gid="1234567890",
    assignee="me",
    due_on="2024-12-31"
)

# Mark task as complete
await update_asana_task(task_gid="1234567890", completed=True)
```

### Project Exploration
```python
# Get projects from a workspace
projects = await get_asana_projects(workspace_gid="1234567890")

# Get detailed project information
project_details = await get_asana_project_details(project_gid="1234567890")

# Get tasks from a specific project
project_tasks = await get_asana_tasks(project_gid="1234567890")

# Search for tasks
search_results = await search_asana_tasks(
    workspace_gid="1234567890",
    text="bug fix"
)
```

### Portfolio Management
```python
# Get portfolios from a workspace
portfolios = await get_asana_portfolios(workspace_gid="1234567890")

# Get detailed portfolio information
portfolio_details = await get_asana_portfolio_details(portfolio_gid="1234567890")

# Get projects contained in a portfolio
portfolio_projects = await get_asana_portfolio_items(portfolio_gid="1234567890")
```

## Error Handling

The server implements comprehensive error handling:
- Authentication errors provide guidance on token setup
- API errors include specific troubleshooting suggestions
- Network issues are handled gracefully with informative messages
- All operations return structured responses with status indicators

## Integration with Other MCP Servers

The Asana MCP Server integrates seamlessly with other MCP servers in the library:
- **Jira Integration**: Create Jira tickets from Asana tasks
- **Confluence Integration**: Reference documentation in task descriptions
- **Bitbucket Integration**: Link code reviews to project tasks

## Security Considerations

- Personal Access Tokens are handled securely through environment variables
- API requests use HTTPS for secure communication
- No sensitive data is logged or exposed in error messages
- Token validation provides clear feedback without exposing token contents
