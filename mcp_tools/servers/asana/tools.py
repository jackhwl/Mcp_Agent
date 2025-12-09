from fastmcp import FastMCP, Context
from typing import Dict, Any, List, Optional
import logging
import os

logger = logging.getLogger(__name__)

def format_custom_fields(custom_fields: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Format custom fields into a readable dictionary.
    
    Args:
        custom_fields: List of custom field objects from Asana API
        
    Returns:
        Dictionary with field names as keys and formatted values as values
    """
    formatted_fields = {}
    
    for field in custom_fields:
        field_name = field.get('name', 'Unknown Field')
        
        # Get the appropriate value based on field type
        if field.get('display_value'):
            field_value = field.get('display_value')
        elif field.get('text_value'):
            field_value = field.get('text_value')
        elif field.get('number_value') is not None:
            field_value = str(field.get('number_value'))
        elif field.get('enum_value') and field.get('enum_value', {}).get('name'):
            field_value = field.get('enum_value', {}).get('name')
        else:
            field_value = 'No value set'
            
        formatted_fields[field_name] = field_value
    
    return formatted_fields

def register_asana_tools(mcp: FastMCP, asana_service):
    """Register all Asana-related MCP tools with the FastMCP server."""
    
    @mcp.tool()
    async def asana_healthcheck(ctx: Context) -> Dict[str, Any]:
        """
        Healthcheck tool to verify Asana configuration and Bearer token credentials.
        Provides guidance on updating credentials if needed.
        """
        try:
            await ctx.info("Running Asana MCP Server healthcheck...")
            
            # Get environment variables and service configuration
            current_auth_token = asana_service.auth_token
            env_auth_token = os.getenv("ASANA_AUTH_TOKEN", "Not set")
            
            # Determine configuration status
            config_status = "healthy"
            warnings = []
            instructions = []
            
            if not current_auth_token or current_auth_token == "Not set":
                config_status = "missing_auth_token"
                warnings.append("❌ No Asana auth token configured")
                instructions.extend([
                    "1. Generate a Personal Access Token from your Asana account settings",
                    "2. Go to Asana > My Profile Settings > Apps > Manage Developer Apps",
                    "3. Create a Personal Access Token",
                    "4. Set the ASANA_AUTH_TOKEN environment variable",
                    "5. Update VSCode/Cursor settings with your auth token",
                    "6. Restart VSCode/Cursor to apply changes"
                ])
            
            if current_auth_token:
                if len(current_auth_token) < 20:
                    warnings.append("⚠️ Auth token seems unusually short - verify it's correct")
            
            # Build response data
            healthcheck_data = {
                'status': config_status,
                'overall_health': 'healthy' if config_status == 'healthy' else 'needs_attention',
                'warnings': warnings,
                'setup_instructions': instructions,
                'service_info': {
                    'base_url': asana_service.base_url,
                    'credentials_status': {
                        'auth_token_set': bool(current_auth_token and current_auth_token != "Not set"),
                        'auth_token_length': len(current_auth_token) if current_auth_token else 0
                    }
                },
                'environment_variables': {
                    'ASANA_BASE_URL': os.getenv("ASANA_BASE_URL", "Using default"),
                    'ASANA_AUTH_TOKEN': "Set" if env_auth_token != "Not set" else "Not set"
                },
                'next_steps': {
                    'vscode_settings_path': {
                        'windows': os.path.expanduser("~") + "\\AppData\\Roaming\\Code\\User\\settings.json",
                        'mac_linux': os.path.expanduser("~") + "/.config/Code/User/settings.json"
                    },
                    'configuration_keys': {
                        'auth_token': "mcp.servers.asana-mcp-server.env.ASANA_AUTH_TOKEN"
                    }
                }
            }
            
            # Provide contextual logging
            await ctx.info(f"Healthcheck completed - Base URL: {asana_service.base_url}")
            
            if config_status == "healthy":
                await ctx.info("✅ Configuration looks good! Credentials are set and ready to use.")
            else:
                await ctx.info("⚠️ Configuration needs attention - please check credentials")
            
            return healthcheck_data
            
        except Exception as e:
            error_msg = f"Healthcheck failed: {str(e)}"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return {
                'status': 'error',
                'overall_health': 'error',
                'message': error_msg,
                'instructions': [
                    "1. Check that the Asana MCP server is properly installed",
                    "2. Verify the virtual environment is activated",
                    "3. Ensure all dependencies are installed"
                ]
            }

    @mcp.tool()
    async def get_asana_workspaces(ctx: Context = None) -> Dict[str, Any]:
        """
        Get all accessible Asana workspaces.
        
        Perfect for: Workspace discovery, exploring available workspaces
        Example: get_asana_workspaces()
        
        Returns: List of workspaces with basic information
        """
        try:
            if ctx:
                await ctx.info("Fetching Asana workspaces...")
            
            result = asana_service.get_workspaces()
            
            if ctx:
                if result['status'] == 'success':
                    await ctx.info(f"✅ Retrieved {len(result.get('workspaces', []))} workspaces")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch workspaces: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'workspaces': []
            }

    @mcp.tool()
    async def get_asana_projects(
        workspace_gid: str,
        limit: int = 20,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get projects from a specific Asana workspace.
        
        Perfect for: Project discovery, exploring workspace projects
        Example: get_asana_projects("1234567890", limit=10)
        
        Args:
            workspace_gid: The GID of the workspace (required)
            limit: Maximum number of projects to return (default: 20)
        
        Returns: List of projects with detailed information
        """
        try:
            if ctx:
                await ctx.info(f"Fetching projects from workspace {workspace_gid}...")
            
            result = asana_service.get_projects(workspace_gid, limit)
            
            if ctx:
                if result['status'] == 'success':
                    await ctx.info(f"✅ Retrieved {len(result.get('projects', []))} projects")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch projects: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'projects': []
            }

    @mcp.tool()
    async def get_asana_project_details(
        project_gid: str,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific Asana project including custom fields.
        
        Perfect for: Understanding project configuration, finding available custom fields
        Example: get_asana_project_details("1234567890")
        
        Args:
            project_gid: The GID of the project (required)
        
        Returns: Detailed project information including custom fields configuration
        """
        try:
            if ctx:
                await ctx.info(f"Fetching details for project {project_gid}...")
            
            result = asana_service.get_project_details(project_gid)
            
            if ctx:
                if result['status'] == 'success':
                    project_name = result.get('project', {}).get('name', 'Unknown')
                    custom_fields = result.get('project', {}).get('custom_fields', [])
                    if custom_fields:
                        await ctx.info(f"✅ Retrieved details for project: {project_name} (with {len(custom_fields)} custom fields)")
                    else:
                        await ctx.info(f"✅ Retrieved details for project: {project_name} (no custom fields)")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch project details: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'project': {}
            }

    @mcp.tool()
    async def get_asana_tasks(
        project_gid: Optional[str] = None,
        assignee: Optional[str] = None,
        limit: int = 50,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get tasks from Asana with optional filtering, including custom fields.
        
        Perfect for: Task management, reviewing assignments, project tracking, checking custom fields like IS Status and IS Stakeholders
        Example: get_asana_tasks(project_gid="1234567890") or get_asana_tasks(assignee="me")
        
        Args:
            project_gid: Optional project GID to filter tasks
            assignee: Optional assignee to filter tasks (can be 'me' or user GID)
            limit: Maximum number of tasks to return (default: 50)
        
        Returns: List of tasks with detailed information including custom fields
        """
        try:
            if ctx:
                filters = []
                if project_gid:
                    filters.append(f"project {project_gid}")
                if assignee:
                    filters.append(f"assignee {assignee}")
                filter_desc = f" with filters: {', '.join(filters)}" if filters else ""
                await ctx.info(f"Fetching tasks{filter_desc}...")
            
            result = asana_service.get_tasks(project_gid, assignee, limit)
            
            if ctx:
                if result['status'] == 'success':
                    tasks_with_custom_fields = 0
                    for task in result.get('tasks', []):
                        if task.get('custom_fields'):
                            tasks_with_custom_fields += 1
                    await ctx.info(f"✅ Retrieved {len(result.get('tasks', []))} tasks ({tasks_with_custom_fields} with custom fields)")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            # Format custom fields for all tasks if they exist
            if result.get('status') == 'success':
                for task in result.get('tasks', []):
                    if task.get('custom_fields'):
                        task['formatted_custom_fields'] = format_custom_fields(task['custom_fields'])
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch tasks: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'tasks': []
            }

    @mcp.tool()
    async def get_asana_task_details(
        task_gid: str,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific Asana task including custom fields.
        
        Perfect for: Task analysis, understanding task relationships, getting full context, checking custom fields like IS Status and IS Stakeholders
        Example: get_asana_task_details("1234567890")
        
        Args:
            task_gid: The GID of the task (required)
        
        Returns: Detailed task information including subtasks, dependencies, custom fields, etc.
        """
        try:
            if ctx:
                await ctx.info(f"Fetching details for task {task_gid}...")
            
            result = asana_service.get_task_details(task_gid)
            
            if ctx:
                if result['status'] == 'success':
                    task_name = result.get('task', {}).get('name', 'Unknown')
                    custom_fields = result.get('task', {}).get('custom_fields', [])
                    if custom_fields:
                        await ctx.info(f"✅ Retrieved details for task: {task_name} (with {len(custom_fields)} custom fields)")
                    else:
                        await ctx.info(f"✅ Retrieved details for task: {task_name} (no custom fields)")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            # If custom fields exist, format them for easier reading
            if result.get('status') == 'success' and result.get('task', {}).get('custom_fields'):
                formatted_fields = format_custom_fields(result['task']['custom_fields'])
                result['task']['formatted_custom_fields'] = formatted_fields
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch task details: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'task': {}
            }

    @mcp.tool()
    async def create_asana_task(
        name: str,
        project_gid: Optional[str] = None,
        assignee: Optional[str] = None,
        notes: Optional[str] = None,
        due_on: Optional[str] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Create a new task in Asana.
        
        Perfect for: Task creation, project management, assigning work
        Example: create_asana_task("Review PR", project_gid="1234567890", assignee="me", due_on="2024-12-31")
        
        Args:
            name: The name of the task (required)
            project_gid: Optional project GID to add the task to
            assignee: Optional assignee (can be 'me' or user GID)
            notes: Optional task description/notes
            due_on: Optional due date in YYYY-MM-DD format
        
        Returns: Created task information
        """
        try:
            if ctx:
                await ctx.info(f"Creating task: {name}...")
            
            result = asana_service.create_task(name, project_gid, assignee, notes, due_on)
            
            if ctx:
                if result['status'] == 'success':
                    task_gid = result.get('task', {}).get('gid', 'Unknown')
                    await ctx.info(f"✅ Created task with GID: {task_gid}")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to create task: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'task': {}
            }

    @mcp.tool()
    async def update_asana_task(
        task_gid: str,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        completed: Optional[bool] = None,
        due_on: Optional[str] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Update an existing task in Asana.
        
        Perfect for: Task updates, marking completion, changing due dates
        Example: update_asana_task("1234567890", completed=True) or update_asana_task("1234567890", name="Updated task name")
        
        Args:
            task_gid: The GID of the task to update (required)
            name: Optional new name for the task
            notes: Optional new notes/description
            completed: Optional completion status (True/False)
            due_on: Optional new due date in YYYY-MM-DD format
        
        Returns: Updated task information
        """
        try:
            if ctx:
                await ctx.info(f"Updating task {task_gid}...")
            
            # Build update dictionary
            updates = {}
            if name is not None:
                updates['name'] = name
            if notes is not None:
                updates['notes'] = notes
            if completed is not None:
                updates['completed'] = completed
            if due_on is not None:
                updates['due_on'] = due_on
            
            result = asana_service.update_task(task_gid, **updates)
            
            if ctx:
                if result['status'] == 'success':
                    await ctx.info(f"✅ Successfully updated task")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to update task: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'task': {}
            }

    @mcp.tool()
    async def search_asana_tasks(
        workspace_gid: str,
        text: str,
        limit: int = 20,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Search for tasks in Asana using text query.
        
        Perfect for: Finding specific tasks, searching across projects
        Example: search_asana_tasks("1234567890", "bug fix", limit=10)
        
        Args:
            workspace_gid: The workspace to search in (required)
            text: Text to search for (required)
            limit: Maximum number of results to return (default: 20)
        
        Returns: Search results with task information
        """
        try:
            if ctx:
                await ctx.info(f"Searching for tasks containing: {text}")
            
            result = asana_service.search_tasks(workspace_gid, text, limit)
            
            if ctx:
                if result['status'] == 'success':
                    await ctx.info(f"✅ Found {len(result.get('tasks', []))} tasks")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to search tasks: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'tasks': []
            }

    @mcp.tool()
    async def get_asana_user_info(ctx: Context = None) -> Dict[str, Any]:
        """
        Get information about the authenticated Asana user.
        
        Perfect for: User verification, getting user GID for assignments
        Example: get_asana_user_info()
        
        Returns: User information including name, email, and GID
        """
        try:
            if ctx:
                await ctx.info("Fetching user information...")
            
            result = asana_service.get_user_info()
            
            if ctx:
                if result['status'] == 'success':
                    user_name = result.get('user', {}).get('name', 'Unknown')
                    await ctx.info(f"✅ Retrieved user info for: {user_name}")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch user info: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'user': {}
            }

    @mcp.tool()
    async def get_asana_portfolios(
        workspace_gid: str,
        limit: int = 20,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get portfolios from a specific Asana workspace.
        
        Perfect for: Portfolio discovery, exploring workspace portfolios, high-level project organization
        Example: get_asana_portfolios("1234567890", limit=10)
        
        Args:
            workspace_gid: The GID of the workspace (required)
            limit: Maximum number of portfolios to return (default: 20)
        
        Returns: List of portfolios with detailed information
        """
        try:
            if ctx:
                await ctx.info(f"Fetching portfolios from workspace {workspace_gid}...")
            
            result = asana_service.get_portfolios(workspace_gid, limit)
            
            if ctx:
                if result['status'] == 'success':
                    await ctx.info(f"✅ Retrieved {len(result.get('portfolios', []))} portfolios")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch portfolios: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'portfolios': []
            }

    @mcp.tool()
    async def get_asana_portfolio_details(
        portfolio_gid: str,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific Asana portfolio including custom fields.
        
        Perfect for: Understanding portfolio configuration, finding available custom fields, portfolio status tracking
        Example: get_asana_portfolio_details("1234567890")
        
        Args:
            portfolio_gid: The GID of the portfolio (required)
        
        Returns: Detailed portfolio information including custom fields configuration
        """
        try:
            if ctx:
                await ctx.info(f"Fetching details for portfolio {portfolio_gid}...")
            
            result = asana_service.get_portfolio_details(portfolio_gid)
            
            if ctx:
                if result['status'] == 'success':
                    portfolio_name = result.get('portfolio', {}).get('name', 'Unknown')
                    custom_fields = result.get('portfolio', {}).get('custom_fields', [])
                    if custom_fields:
                        await ctx.info(f"✅ Retrieved details for portfolio: {portfolio_name} (with {len(custom_fields)} custom fields)")
                    else:
                        await ctx.info(f"✅ Retrieved details for portfolio: {portfolio_name} (no custom fields)")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            # If custom fields exist, format them for easier reading
            if result.get('status') == 'success' and result.get('portfolio', {}).get('custom_fields'):
                formatted_fields = format_custom_fields(result['portfolio']['custom_fields'])
                result['portfolio']['formatted_custom_fields'] = formatted_fields
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch portfolio details: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'portfolio': {}
            }

    @mcp.tool()
    async def get_asana_portfolio_items(
        portfolio_gid: str,
        limit: int = 50,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get items (projects) contained within a specific Asana portfolio.
        
        Perfect for: Portfolio project tracking, understanding portfolio composition, project status overview
        Example: get_asana_portfolio_items("1234567890", limit=25)
        
        Args:
            portfolio_gid: The GID of the portfolio (required)
            limit: Maximum number of items to return (default: 50)
        
        Returns: List of projects/items contained in the portfolio with detailed information
        """
        try:
            if ctx:
                await ctx.info(f"Fetching items from portfolio {portfolio_gid}...")
            
            result = asana_service.get_portfolio_items(portfolio_gid, limit)
            
            if ctx:
                if result['status'] == 'success':
                    items_with_custom_fields = 0
                    for item in result.get('items', []):
                        if item.get('custom_fields'):
                            items_with_custom_fields += 1
                    await ctx.info(f"✅ Retrieved {len(result.get('items', []))} items ({items_with_custom_fields} with custom fields)")
                else:
                    await ctx.error(f"❌ {result['message']}")
            
            # Format custom fields for all items if they exist
            if result.get('status') == 'success':
                for item in result.get('items', []):
                    if item.get('custom_fields'):
                        item['formatted_custom_fields'] = format_custom_fields(item['custom_fields'])
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to fetch portfolio items: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'items': []
            }
