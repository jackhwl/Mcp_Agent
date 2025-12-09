from fastmcp import FastMCP, Context
from typing import Dict, Any, List, Optional
import logging
import os

logger = logging.getLogger(__name__)

def register_confluence_tools(mcp: FastMCP, confluence_service):
    """Register all Confluence-related MCP tools with the FastMCP server."""
    
    @mcp.tool()
    async def confluence_healthcheck(ctx: Context) -> Dict[str, Any]:
        """
        Healthcheck tool to verify Confluence configuration and token credentials.
        Provides guidance on updating credentials if needed.
        """
        try:
            await ctx.info("Running Confluence MCP Server healthcheck...")
            
            # Get environment variables and service configuration
            current_auth_token = confluence_service.auth_token
            env_auth_token = os.getenv("CONFLUENCE_AUTH_TOKEN", "Not set")
            
            # Determine configuration status
            config_status = "healthy"
            warnings = []
            instructions = []
            
            if not current_auth_token or current_auth_token == "Not set":
                config_status = "missing_auth_token"
                warnings.append("❌ No Confluence auth token configured")
                instructions.extend([
                    "1. Generate a Bearer token from your Confluence account settings",
                    "2. Set the CONFLUENCE_AUTH_TOKEN environment variable",
                    "3. Update VSCode/Cursor settings with your auth token",
                    "4. Restart VSCode/Cursor to apply changes"
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
                    'base_url': confluence_service.base_url,
                    'credentials_status': {
                        'auth_token_set': bool(current_auth_token and current_auth_token != "Not set"),
                        'auth_token_length': len(current_auth_token) if current_auth_token else 0
                    }
                },
                'environment_variables': {
                    'CONFLUENCE_BASE_URL': os.getenv("CONFLUENCE_BASE_URL", "Using default"),
                    'CONFLUENCE_AUTH_TOKEN': "Set" if env_auth_token != "Not set" else "Not set"
                },
                'next_steps': {
                    'vscode_settings_path': {
                        'windows': os.path.expanduser("~") + "\\AppData\\Roaming\\Code\\User\\settings.json",
                        'mac_linux': os.path.expanduser("~") + "/.config/Code/User/settings.json"
                    },
                    'configuration_keys': {
                        'auth_token': "mcp.servers.confluence-mcp-server.env.CONFLUENCE_AUTH_TOKEN"
                    }
                }
            }
            
            # Provide contextual logging
            await ctx.info(f"Healthcheck completed - Base URL: {confluence_service.base_url}")
            
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
                    "1. Check that the Confluence MCP server is properly installed",
                    "2. Verify the virtual environment is activated",
                    "3. Ensure all dependencies are installed"
                ]
            }

    @mcp.tool()
    async def get_confluence_pages(
        page_ids: Optional[List[str]] = None,
        space_key: Optional[str] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Fetch Confluence pages by page IDs or space key and convert to markdown.
        
        Perfect for: Getting specific pages by ID or all pages from a space
        Example: get_confluence_pages(page_ids=["123", "456"]) or get_confluence_pages(space_key="TECH")
        
        Args:
            page_ids: List of specific page IDs to fetch
            space_key: Space key to fetch all pages from
        
        Returns: Dictionary containing the requested pages with their markdown content
        """
        try:
            if ctx:
                if page_ids:
                    await ctx.info(f"Fetching Confluence pages by IDs: {page_ids}")
                elif space_key:
                    await ctx.info(f"Fetching all pages from space: {space_key}")
                else:
                    await ctx.info("Fetching Confluence pages (no specific criteria)")
            
            result = confluence_service.get_pages_as_markdown(page_ids=page_ids, space_key=space_key)
            
            if result.get('status') == 'success':
                if ctx:
                    await ctx.info(f"Successfully retrieved {result.get('total_pages', 0)} pages")
            else:
                if ctx:
                    await ctx.error(f"Failed to fetch pages: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error fetching Confluence pages: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }

    @mcp.tool()
    async def search_confluence(
        query: str,
        space_key: Optional[str] = None,
        limit: int = 25,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Search Confluence pages using text queries.
        
        Perfect for: Finding documentation, searching across spaces
        Example: search_confluence("API documentation", space_key="TECH", limit=10)
        
        Args:
            query: Search query string
            space_key: Optional space key to limit search scope
            limit: Maximum number of results to return (default: 25)
        
        Returns: Search results with page information and excerpts
        """
        try:
            if ctx:
                if space_key:
                    await ctx.info(f"Searching Confluence for '{query}' in space '{space_key}'")
                else:
                    await ctx.info(f"Searching Confluence for '{query}' across all spaces")
            
            result = confluence_service.search_pages(query=query, space_key=space_key, limit=limit)
            
            if result.get('status') == 'success':
                if ctx:
                    await ctx.info(f"Found {len(result.get('results', []))} search results")
            else:
                if ctx:
                    await ctx.error(f"Search failed: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error searching Confluence: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }

    @mcp.tool()
    async def get_confluence_spaces(
        limit: int = 50,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get all accessible Confluence spaces.
        
        Perfect for: Space discovery, exploring available documentation areas
        Example: get_confluence_spaces(limit=20)
        
        Args:
            limit: Maximum number of spaces to return (default: 50)
        
        Returns: List of spaces with basic information
        """
        try:
            if ctx:
                await ctx.info("Fetching accessible Confluence spaces...")
            
            result = confluence_service.get_spaces(limit=limit)
            
            if result.get('status') == 'success':
                if ctx:
                    await ctx.info(f"Found {result.get('total_spaces', 0)} accessible spaces")
            else:
                if ctx:
                    await ctx.error(f"Failed to fetch spaces: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error fetching Confluence spaces: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }

    @mcp.tool()
    async def get_confluence_page_by_title(
        title: str,
        space_key: str,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get a specific Confluence page by title within a space.
        
        Perfect for: Retrieving known pages, getting specific documentation
        Example: get_confluence_page_by_title("API Guidelines", "TECH")
        
        Args:
            title: Page title to search for
            space_key: Space key where the page exists
        
        Returns: Page information and markdown content
        """
        try:
            if ctx:
                await ctx.info(f"Fetching page '{title}' from space '{space_key}'")
            
            result = confluence_service.get_page_by_title(title=title, space_key=space_key)
            
            if result.get('status') == 'success':
                if ctx:
                    await ctx.info(f"Successfully retrieved page: {title}")
            else:
                if ctx:
                    await ctx.error(f"Failed to fetch page: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error fetching page by title: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }

    @mcp.tool()
    async def get_space_documentation(
        space_key: str,
        search_terms: Optional[List[str]] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive documentation from a Confluence space.
        
        Perfect for: Getting all pages from a space, bulk documentation retrieval
        Example: get_space_documentation("TECH", search_terms=["API", "guide"])
        
        Args:
            space_key: Space key to get documentation from
            search_terms: Optional list of terms to filter pages by title/content
        
        Returns: Dictionary containing all pages from the space with their markdown content
        """
        try:
            if ctx:
                if search_terms:
                    await ctx.info(f"Getting documentation from space '{space_key}' filtered by: {search_terms}")
                else:
                    await ctx.info(f"Getting all documentation from space '{space_key}'")
            
            # First get all pages from the space
            result = confluence_service.get_pages_as_markdown(space_key=space_key)
            
            if result.get('status') != 'success':
                return result
            
            pages = result.get('pages', [])
            
            # Filter by search terms if provided
            if search_terms:
                filtered_pages = []
                for page in pages:
                    title = page.get('title', '').lower()
                    content = page.get('markdown_content', '').lower()
                    
                    # Check if any search term is found in title or content
                    for term in search_terms:
                        if term.lower() in title or term.lower() in content:
                            filtered_pages.append(page)
                            break
                
                pages = filtered_pages
                
                if ctx:
                    await ctx.info(f"Filtered to {len(pages)} pages matching search terms")
            
            return {
                'status': 'success',
                'message': f'Retrieved {len(pages)} pages from space {space_key}',
                'space_key': space_key,
                'search_terms': search_terms,
                'pages': pages,
                'total_pages': len(pages)
            }
            
        except Exception as e:
            error_msg = f"Error getting space documentation: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            } 