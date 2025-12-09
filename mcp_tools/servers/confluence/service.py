import requests
import os
import logging
import warnings
from typing import Dict, Any, List, Optional
import html2text
from datetime import datetime, timedelta
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

# Suppress SSL warnings if needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Confluence configuration from environment variables
CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL", "https://wlwiki.wenlin.net/")
CONFLUENCE_AUTH_TOKEN = os.getenv("CONFLUENCE_AUTH_TOKEN")

class ConfluenceService:
    """Service class for interacting with Confluence API."""
    
    def __init__(self):
        self.base_url = CONFLUENCE_BASE_URL
        self.auth_token = CONFLUENCE_AUTH_TOKEN
        
        # Set up authentication headers if auth token is available
        if self.auth_token:
            self.headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }
            self.auth = None  # Not using basic auth
        else:
            self.headers = {'Content-Type': 'application/json'}
            self.auth = None
            logger.warning("No Confluence auth token provided. Some operations may fail.")
        
        # Initialize HTML to markdown converter
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.bypass_tables = False
        self.converter.ignore_images = False
        self.converter.body_width = 0
        self.converter.single_line_break = True
        
        # Configure SSL handling
        self._configure_ssl()

    def _configure_ssl(self):
        """Configure SSL settings for Confluence connections."""
        # Suppress SSL warnings
        warnings.filterwarnings("ignore", message="Unverified HTTPS request")
        
        # Disable SSL verification globally for requests if needed
        os.environ['CURL_CA_BUNDLE'] = ''
        os.environ['REQUESTS_CA_BUNDLE'] = ''
        
        # Patch BeautifulSoup parser selection
        self._patch_beautifulsoup_parser()

    def _patch_beautifulsoup_parser(self):
        """Patch BeautifulSoup to use a working parser without repeated warnings."""
        # Use lxml as the preferred parser since we confirmed it's working
        original_init = BeautifulSoup.__init__
        
        def patched_init(self_bs, markup="", features="lxml", **kwargs):
            # Force lxml parser for consistency
            return original_init(self_bs, markup, features="lxml", **kwargs)
        
        BeautifulSoup.__init__ = patched_init
        logger.info("Patched BeautifulSoup to use lxml parser")

    def get_pages_as_markdown(self, page_ids: List[str] = None, space_key: str = None) -> Dict[str, Any]:
        """
        Fetch Confluence pages and convert them to markdown format using direct API calls.
        
        Args:
            page_ids: List of specific page IDs to fetch
            space_key: Space key to fetch all pages from
            
        Returns:
            Dictionary containing formatted markdown content and metadata
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Confluence credentials not configured. Please set CONFLUENCE_AUTH_TOKEN environment variable.'
                }

            pages_data = []
            
            if page_ids:
                # Fetch specific pages by ID
                for page_id in page_ids:
                    page_result = self._get_page_by_id(page_id)
                    if page_result.get('status') == 'success':
                        pages_data.append(page_result['page'])
                    else:
                        logger.warning(f"Failed to fetch page {page_id}: {page_result.get('message')}")
            
            elif space_key:
                # Fetch all pages from space
                space_pages_result = self._get_all_pages_from_space(space_key)
                if space_pages_result.get('status') == 'success':
                    pages_data = space_pages_result['pages']
                else:
                    return space_pages_result
            
            else:
                return {
                    'status': 'error',
                    'message': 'Either page_ids or space_key must be provided'
                }

            # Convert content to markdown format
            for page in pages_data:
                if 'html_content' in page:
                    page['markdown_content'] = self.converter.handle(page['html_content']).strip()

            return {
                'status': 'success',
                'message': f'Successfully retrieved {len(pages_data)} pages',
                'pages': pages_data,
                'total_pages': len(pages_data),
                'space_key': space_key,
                'page_ids': page_ids
            }
            
        except Exception as e:
            logger.error(f"Error fetching Confluence pages: {str(e)}")
            
            # Provide more specific error information
            error_message = str(e)
            if "401" in error_message or "unauthorized" in error_message.lower():
                error_message += " - Check your Bearer token is valid and has proper permissions"
            elif "404" in error_message:
                error_message += " - Check that the space key or page IDs exist and are accessible"
            
            return {
                'status': 'error',
                'message': f'Failed to fetch Confluence pages: {error_message}',
                'pages': [],
                'total_pages': 0
            }

    def search_pages(self, query: str, space_key: str = None, limit: int = 25) -> Dict[str, Any]:
        """
        Search for Confluence pages using CQL (Confluence Query Language).
        
        Args:
            query: Search query string
            space_key: Optional space key to limit search scope
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing search results
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Confluence credentials not configured'
                }

            # Build search URL
            search_url = f"{self.base_url.rstrip('/')}/rest/api/content/search"
            
            # Build CQL query
            cql_query = f'text ~ "{query}"'
            if space_key:
                cql_query += f' and space = "{space_key}"'
            
            params = {
                'cql': cql_query,
                'limit': limit,
                'expand': 'version,space,body.view,metadata.labels'
            }
            
            response = requests.get(
                search_url,
                params=params,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            
            search_data = response.json()
            
            search_results = []
            for result in search_data.get('results', []):
                search_results.append({
                    'id': result.get('id'),
                    'title': result.get('title'),
                    'type': result.get('type'),
                    'space_key': result.get('space', {}).get('key'),
                    'space_name': result.get('space', {}).get('name'),
                    'url': f"{self.base_url.rstrip('/')}{result.get('_links', {}).get('webui', '')}",
                    'created': result.get('version', {}).get('when'),
                    'creator': result.get('version', {}).get('by', {}).get('displayName'),
                    'excerpt': result.get('excerpt', '')
                })
            
            return {
                'status': 'success',
                'message': f'Found {len(search_results)} results',
                'results': search_results,
                'total_results': search_data.get('totalSize', len(search_results)),
                'query': query,
                'cql_query': cql_query
            }
            
        except Exception as e:
            logger.error(f"Error searching Confluence: {str(e)}")
            return {
                'status': 'error',
                'message': f'Search failed: {str(e)}'
            }

    def get_spaces(self, limit: int = 50) -> Dict[str, Any]:
        """
        Get all accessible Confluence spaces.
        
        Args:
            limit: Maximum number of spaces to return
            
        Returns:
            Dictionary containing space information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Confluence credentials not configured'
                }

            spaces_url = f"{self.base_url.rstrip('/')}/rest/api/space"
            
            params = {
                'limit': limit,
                'expand': 'description.plain,homepage'
            }
            
            response = requests.get(
                spaces_url,
                params=params,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            
            spaces_data = response.json()
            
            spaces = []
            for space in spaces_data.get('results', []):
                spaces.append({
                    'key': space.get('key'),
                    'name': space.get('name'),
                    'type': space.get('type'),
                    'description': space.get('description', {}).get('plain', ''),
                    'homepage_id': space.get('homepage', {}).get('id'),
                    'url': f"{self.base_url.rstrip('/')}{space.get('_links', {}).get('webui', '')}"
                })
            
            return {
                'status': 'success',
                'message': f'Found {len(spaces)} accessible spaces',
                'spaces': spaces,
                'total_spaces': spaces_data.get('size', len(spaces))
            }
            
        except Exception as e:
            logger.error(f"Error fetching spaces: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch spaces: {str(e)}'
            }

    def get_page_by_title(self, title: str, space_key: str) -> Dict[str, Any]:
        """
        Get a specific page by title within a space.
        
        Args:
            title: Page title to search for
            space_key: Space key where the page exists
            
        Returns:
            Dictionary containing page information and content
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Confluence credentials not configured'
                }

            search_url = f"{self.base_url.rstrip('/')}/rest/api/content"
            
            params = {
                'title': title,
                'spaceKey': space_key,
                'expand': 'body.storage,version,space'
            }
            
            response = requests.get(
                search_url,
                params=params,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            
            page_data = response.json()
            
            if not page_data.get('results'):
                return {
                    'status': 'error',
                    'message': f'Page "{title}" not found in space "{space_key}"'
                }
            
            page = page_data['results'][0]
            content_html = page.get('body', {}).get('storage', {}).get('value', '')
            markdown_content = self.converter.handle(content_html)
            
            return {
                'status': 'success',
                'page': {
                    'id': page.get('id'),
                    'title': page.get('title'),
                    'space_key': page.get('space', {}).get('key'),
                    'space_name': page.get('space', {}).get('name'),
                    'type': page.get('type'),
                    'url': f"{self.base_url.rstrip('/')}{page.get('_links', {}).get('webui', '')}",
                    'created': page.get('version', {}).get('when'),
                    'creator': page.get('version', {}).get('by', {}).get('displayName'),
                    'markdown_content': markdown_content.strip(),
                    'html_content': content_html
                }
            }
            
        except Exception as e:
            logger.error(f"Error fetching page by title: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch page: {str(e)}'
            }

    def create_page(self, title: str, content: str, space_key: str, parent_page_id: str = None, labels: List[str] = None) -> Dict[str, Any]:
        """
        Create a new Confluence page.
        
        Args:
            title: Page title
            content: Page content in markdown format
            space_key: Space where the page will be created
            parent_page_id: Optional parent page ID
            labels: Optional list of labels to add to the page
            
        Returns:
            Dictionary containing created page information
        """
        try:
            if not self.auth_token:
                return {
                    'status': 'error',
                    'message': 'Confluence credentials not configured'
                }

            # Convert markdown to HTML for Confluence storage format
            import markdown
            html_content = markdown.markdown(content)
            
            # Prepare page data
            page_data = {
                "type": "page",
                "title": title,
                "space": {
                    "key": space_key
                },
                "body": {
                    "storage": {
                        "value": html_content,
                        "representation": "storage"
                    }
                }
            }
            
            # Add parent page if specified
            if parent_page_id:
                page_data["ancestors"] = [{"id": parent_page_id}]
            
            create_url = f"{self.base_url.rstrip('/')}/rest/api/content"
            
            response = requests.post(
                create_url,
                json=page_data,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            
            created_page = response.json()
            
            # Add labels if specified
            if labels:
                try:
                    self._add_labels_to_page(created_page['id'], labels)
                except Exception as e:
                    logger.warning(f"Page created but failed to add labels: {str(e)}")
            
            return {
                'status': 'success',
                'message': f'Successfully created page "{title}"',
                'page': {
                    'id': created_page.get('id'),
                    'title': created_page.get('title'),
                    'space_key': created_page.get('space', {}).get('key'),
                    'url': f"{self.base_url.rstrip('/')}{created_page.get('_links', {}).get('webui', '')}",
                    'version': created_page.get('version', {}).get('number'),
                    'created': created_page.get('version', {}).get('when')
                }
            }
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_detail = e.response.json().get('message', 'Bad request')
                return {
                    'status': 'error',
                    'message': f'Failed to create page: {error_detail}'
                }
            else:
                return {
                    'status': 'error',
                    'message': f'HTTP error creating page: {e.response.status_code}'
                }
        except Exception as e:
            logger.error(f"Error creating page: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to create page: {str(e)}'
            }

    def _add_labels_to_page(self, page_id: str, labels: List[str]) -> None:
        """
        Add labels to a page.
        
        Args:
            page_id: Page ID to add labels to
            labels: List of label names
        """
        labels_data = [{"prefix": "global", "name": label} for label in labels]
        
        labels_url = f"{self.base_url.rstrip('/')}/rest/api/content/{page_id}/label"
        
        response = requests.post(
            labels_url,
            json=labels_data,
            headers=self.headers,
            verify=False
        )
        response.raise_for_status()

    def _get_page_by_id(self, page_id: str) -> Dict[str, Any]:
        """
        Get a single page by its ID.
        
        Args:
            page_id: The page ID to fetch
            
        Returns:
            Dictionary containing page information
        """
        try:
            page_url = f"{self.base_url.rstrip('/')}/rest/api/content/{page_id}"
            
            params = {
                'expand': 'body.storage,version,space,metadata.labels'
            }
            
            response = requests.get(
                page_url,
                params=params,
                headers=self.headers,
                verify=False
            )
            response.raise_for_status()
            
            page = response.json()
            content_html = page.get('body', {}).get('storage', {}).get('value', '')
            
            return {
                'status': 'success',
                'page': {
                    'id': page.get('id'),
                    'title': page.get('title'),
                    'space_key': page.get('space', {}).get('key'),
                    'space_name': page.get('space', {}).get('name'),
                    'type': page.get('type'),
                    'url': f"{self.base_url.rstrip('/')}{page.get('_links', {}).get('webui', '')}",
                    'created': page.get('version', {}).get('when'),
                    'creator': page.get('version', {}).get('by', {}).get('displayName'),
                    'html_content': content_html,
                    'labels': [label.get('name', '') for label in page.get('metadata', {}).get('labels', {}).get('results', [])]
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to fetch page {page_id}: {str(e)}'
            }

    def _get_all_pages_from_space(self, space_key: str) -> Dict[str, Any]:
        """
        Get all pages from a specific space.
        
        Args:
            space_key: The space key to fetch pages from
            
        Returns:
            Dictionary containing all pages from the space
        """
        try:
            pages = []
            start = 0
            limit = 50
            
            while True:
                content_url = f"{self.base_url.rstrip('/')}/rest/api/content"
                
                params = {
                    'spaceKey': space_key,
                    'type': 'page',
                    'start': start,
                    'limit': limit,
                    'expand': 'body.storage,version,space,metadata.labels'
                }
                
                response = requests.get(
                    content_url,
                    params=params,
                    headers=self.headers,
                    verify=False
                )
                response.raise_for_status()
                
                data = response.json()
                results = data.get('results', [])
                
                for page in results:
                    content_html = page.get('body', {}).get('storage', {}).get('value', '')
                    pages.append({
                        'id': page.get('id'),
                        'title': page.get('title'),
                        'space_key': page.get('space', {}).get('key'),
                        'space_name': page.get('space', {}).get('name'),
                        'type': page.get('type'),
                        'url': f"{self.base_url.rstrip('/')}{page.get('_links', {}).get('webui', '')}",
                        'created': page.get('version', {}).get('when'),
                        'creator': page.get('version', {}).get('by', {}).get('displayName'),
                        'html_content': content_html,
                        'labels': [label.get('name', '') for label in page.get('metadata', {}).get('labels', {}).get('results', [])]
                    })
                
                # Check if we have more pages
                if len(results) < limit:
                    break
                    
                start += limit
            
            return {
                'status': 'success',
                'pages': pages,
                'total_pages': len(pages)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to fetch pages from space {space_key}: {str(e)}',
                'pages': [],
                'total_pages': 0
            } 