import requests
import os
import logging
import warnings
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings if needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Asana configuration from environment variables
ASANA_BASE_URL = os.getenv("ASANA_BASE_URL", "https://app.asana.com/api/1.0")
ASANA_AUTH_TOKEN = os.getenv("ASANA_AUTH_TOKEN")
ASANA_DISABLE_SSL_VERIFY = os.getenv("ASANA_DISABLE_SSL_VERIFY", "false").lower() == "true"

class AsanaService:
    """Service class for interacting with Asana API."""
    
    def __init__(self):
        self.base_url = ASANA_BASE_URL
        self.auth_token = ASANA_AUTH_TOKEN
        self.ssl_verify = not ASANA_DISABLE_SSL_VERIFY
        
        # Set up authentication headers if auth token is available
        if self.auth_token:
            self.headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }
        else:
            self.headers = {'Content-Type': 'application/json'}
            logger.warning("No Asana auth token provided. Some operations may fail.")
        
        # Configure SSL handling
        self._configure_ssl()
        
        if not self.ssl_verify:
            logger.warning("SSL verification disabled for Asana connections. This is not recommended for production use.")

    def _configure_ssl(self):
        """Configure SSL settings for Asana connections."""
        # Suppress SSL warnings
        warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    def get_workspaces(self) -> Dict[str, Any]:
        """
        Fetch all workspaces accessible to the authenticated user.
        
        Returns:
            Dictionary containing workspace information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured. Please set ASANA_AUTH_TOKEN environment variable.'
                }

            url = f"{self.base_url}/workspaces"
            
            response = requests.get(
                url,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': f'Successfully retrieved {len(data.get("data", []))} workspaces',
                'workspaces': data.get('data', [])
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana workspaces: {str(e)}")
            
            error_message = str(e)
            if "401" in error_message or "unauthorized" in error_message.lower():
                error_message += " - Check your Bearer token is valid and has proper permissions"
            elif "404" in error_message:
                error_message += " - Check that the API endpoint is accessible"
            
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana workspaces: {error_message}',
                'workspaces': []
            }

    def get_projects(self, workspace_gid: str, limit: int = 20) -> Dict[str, Any]:
        """
        Fetch projects from a specific workspace.
        
        Args:
            workspace_gid: The GID of the workspace
            limit: Maximum number of projects to return
            
        Returns:
            Dictionary containing project information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/projects"
            params = {
                'workspace': workspace_gid,
                'limit': limit,
                'opt_fields': 'name,created_at,modified_at,owner,current_status,notes,color,public,archived'
            }
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': f'Successfully retrieved {len(data.get("data", []))} projects',
                'projects': data.get('data', []),
                'workspace_gid': workspace_gid
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana projects: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana projects: {str(e)}',
                'projects': []
            }

    def get_tasks(self, project_gid: str = None, assignee: str = None, limit: int = 50) -> Dict[str, Any]:
        """
        Fetch tasks from Asana including custom fields.
        
        Args:
            project_gid: Optional project GID to filter tasks
            assignee: Optional assignee to filter tasks (can be 'me' or user GID)
            limit: Maximum number of tasks to return
            
        Returns:
            Dictionary containing task information including custom fields
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/tasks"
            params = {
                'limit': limit,
                'opt_fields': 'name,created_at,modified_at,completed,completed_at,due_on,assignee,projects,notes,tags,parent,custom_fields,custom_fields.name,custom_fields.display_value,custom_fields.text_value,custom_fields.number_value,custom_fields.enum_value,custom_fields.enum_value.name'
            }
            
            if project_gid:
                params['project'] = project_gid
            if assignee:
                params['assignee'] = assignee
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': f'Successfully retrieved {len(data.get("data", []))} tasks',
                'tasks': data.get('data', []),
                'project_gid': project_gid,
                'assignee': assignee
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana tasks: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana tasks: {str(e)}',
                'tasks': []
            }

    def get_task_details(self, task_gid: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific task including custom fields.
        
        Args:
            task_gid: The GID of the task
            
        Returns:
            Dictionary containing detailed task information including custom fields
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/tasks/{task_gid}"
            params = {
                'opt_fields': 'name,created_at,modified_at,completed,completed_at,due_on,assignee,projects,notes,tags,parent,subtasks,dependencies,dependents,followers,hearts,num_hearts,permalink_url,custom_fields,custom_fields.name,custom_fields.display_value,custom_fields.text_value,custom_fields.number_value,custom_fields.enum_value,custom_fields.enum_value.name,custom_fields.type'
            }
            
            logger.debug(f"Requesting task details with params: {params}")
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Debug log to see if custom fields are present
            task_data = data.get('data', {})
            if 'custom_fields' in task_data:
                logger.info(f"Found {len(task_data['custom_fields'])} custom fields for task {task_gid}")
                for field in task_data['custom_fields']:
                    logger.info(f"Custom field: {field.get('name', 'Unknown')} = {field.get('display_value', 'No value')}")
            else:
                logger.info(f"No custom_fields key found in task {task_gid}")
                logger.debug(f"Available keys: {list(task_data.keys())}")
            
            return {
                'status': 'success',
                'message': 'Successfully retrieved task details',
                'task': task_data
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana task details: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana task details: {str(e)}',
                'task': {}
            }

    def create_task(self, name: str, project_gid: str = None, assignee: str = None, 
                   notes: str = None, due_on: str = None) -> Dict[str, Any]:
        """
        Create a new task in Asana.
        
        Args:
            name: The name of the task
            project_gid: Optional project GID to add the task to
            assignee: Optional assignee (can be 'me' or user GID)
            notes: Optional task description/notes
            due_on: Optional due date in YYYY-MM-DD format
            
        Returns:
            Dictionary containing the created task information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/tasks"
            
            task_data = {
                'name': name
            }
            
            if project_gid:
                task_data['projects'] = [project_gid]
            if assignee:
                task_data['assignee'] = assignee
            if notes:
                task_data['notes'] = notes
            if due_on:
                task_data['due_on'] = due_on
            
            payload = {'data': task_data}
            
            response = requests.post(
                url,
                json=payload,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': 'Successfully created task',
                'task': data.get('data', {})
            }
            
        except Exception as e:
            logger.error(f"Error creating Asana task: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to create Asana task: {str(e)}',
                'task': {}
            }

    def update_task(self, task_gid: str, **kwargs) -> Dict[str, Any]:
        """
        Update an existing task in Asana.
        
        Args:
            task_gid: The GID of the task to update
            **kwargs: Task fields to update (name, notes, completed, due_on, etc.)
            
        Returns:
            Dictionary containing the updated task information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/tasks/{task_gid}"
            
            # Filter out None values
            task_data = {k: v for k, v in kwargs.items() if v is not None}
            payload = {'data': task_data}
            
            response = requests.put(
                url,
                json=payload,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': 'Successfully updated task',
                'task': data.get('data', {})
            }
            
        except Exception as e:
            logger.error(f"Error updating Asana task: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to update Asana task: {str(e)}',
                'task': {}
            }

    def search_tasks(self, workspace_gid: str, text: str, limit: int = 20) -> Dict[str, Any]:
        """
        Search for tasks using text query.
        
        Args:
            workspace_gid: The workspace to search in
            text: Text to search for
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing search results
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/workspaces/{workspace_gid}/tasks/search"
            params = {
                'text': text,
                'resource_type': 'task',
                'limit': limit,
                'opt_fields': 'name,created_at,modified_at,completed,completed_at,due_on,assignee,projects,notes'
            }
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': f'Successfully found {len(data.get("data", []))} tasks',
                'tasks': data.get('data', []),
                'search_text': text,
                'workspace_gid': workspace_gid
            }
            
        except Exception as e:
            logger.error(f"Error searching Asana tasks: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to search Asana tasks: {str(e)}',
                'tasks': []
            }

    def get_user_info(self) -> Dict[str, Any]:
        """
        Get information about the authenticated user.
        
        Returns:
            Dictionary containing user information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/users/me"
            
            response = requests.get(
                url,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': 'Successfully retrieved user information',
                'user': data.get('data', {})
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana user info: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana user info: {str(e)}',
                'user': {}
            }

    def get_project_details(self, project_gid: str) -> Dict[str, Any]:
        """
        Get detailed information about a project including custom fields.
        
        Args:
            project_gid: The GID of the project
            
        Returns:
            Dictionary containing project information and custom fields
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/projects/{project_gid}"
            params = {
                'opt_fields': 'name,created_at,modified_at,owner,archived,color,notes,public,custom_fields,custom_fields.name,custom_fields.type,custom_fields.enum_options,custom_fields.enum_options.name'
            }
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': 'Successfully retrieved project details',
                'project': data.get('data', {})
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana project details: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana project details: {str(e)}',
                'project': {}
            }

    def get_portfolios(self, workspace_gid: str, limit: int = 20) -> Dict[str, Any]:
        """
        Fetch portfolios from a specific workspace.
        
        Args:
            workspace_gid: The GID of the workspace
            limit: Maximum number of portfolios to return
            
        Returns:
            Dictionary containing portfolio information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/portfolios"
            params = {
                'workspace': workspace_gid,
                'limit': limit,
                'opt_fields': 'name,created_at,modified_at,owner,archived,color,public,due_on,start_on,current_status_update,permalink_url,privacy_setting,default_access_level'
            }
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': f'Successfully retrieved {len(data.get("data", []))} portfolios',
                'portfolios': data.get('data', []),
                'workspace_gid': workspace_gid
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana portfolios: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana portfolios: {str(e)}',
                'portfolios': []
            }

    def get_portfolio_details(self, portfolio_gid: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific portfolio including custom fields.
        
        Args:
            portfolio_gid: The GID of the portfolio
            
        Returns:
            Dictionary containing detailed portfolio information including custom fields
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/portfolios/{portfolio_gid}"
            params = {
                'opt_fields': 'name,created_at,modified_at,created_by,owner,archived,color,public,due_on,start_on,current_status_update,current_status_update.title,current_status_update.resource_subtype,permalink_url,privacy_setting,default_access_level,workspace,workspace.name,members,members.name,custom_fields,custom_fields.name,custom_fields.display_value,custom_fields.text_value,custom_fields.number_value,custom_fields.enum_value,custom_fields.enum_value.name,custom_fields.type,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.name'
            }
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Debug log to see if custom fields are present
            portfolio_data = data.get('data', {})
            if 'custom_fields' in portfolio_data:
                logger.info(f"Found {len(portfolio_data['custom_fields'])} custom fields for portfolio {portfolio_gid}")
                for field in portfolio_data['custom_fields']:
                    logger.info(f"Custom field: {field.get('name', 'Unknown')} = {field.get('display_value', 'No value')}")
            else:
                logger.info(f"No custom_fields key found in portfolio {portfolio_gid}")
                logger.debug(f"Available keys: {list(portfolio_data.keys())}")
            
            return {
                'status': 'success',
                'message': 'Successfully retrieved portfolio details',
                'portfolio': portfolio_data
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana portfolio details: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana portfolio details: {str(e)}',
                'portfolio': {}
            }

    def get_portfolio_items(self, portfolio_gid: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get items (projects) contained within a specific portfolio.
        
        Args:
            portfolio_gid: The GID of the portfolio
            limit: Maximum number of items to return
            
        Returns:
            Dictionary containing portfolio items (projects) information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Asana credentials not configured'
                }

            url = f"{self.base_url}/portfolios/{portfolio_gid}/items"
            params = {
                'limit': limit,
                'opt_fields': 'name,created_at,modified_at,owner,archived,color,public,current_status,current_status.title,current_status.color,due_on,start_on,permalink_url,workspace,workspace.name,team,team.name,custom_fields,custom_fields.name,custom_fields.display_value'
            }
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                verify=self.ssl_verify
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'status': 'success',
                'message': f'Successfully retrieved {len(data.get("data", []))} items from portfolio',
                'items': data.get('data', []),
                'portfolio_gid': portfolio_gid
            }
            
        except Exception as e:
            logger.error(f"Error fetching Asana portfolio items: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch Asana portfolio items: {str(e)}',
                'items': []
            }
