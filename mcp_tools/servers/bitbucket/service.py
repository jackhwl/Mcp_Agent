import requests
from typing import Dict, Any, Optional, List, Tuple
import os
import logging
import re
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class BitbucketService:
    def __init__(self):
        self.base_url = os.getenv("BITBUCKET_BASE_URL", "http://wlstash.wenlin.net")
        self.auth_token = os.getenv("BITBUCKET_AUTH_TOKEN")
        self.session = requests.Session()
        
        # Support both Bearer token and basic auth
        if self.auth_token:
            auth_header = f"Bearer {self.auth_token}"
            if ':' in self.auth_token:  # Basic auth format
                auth_header = f"Basic {self.auth_token}"
        else:
            auth_header = None
            
        self.headers = {
            'Accept': 'application/json;charset=UTF-8',
            'Content-Type': 'application/json'
        }
        
        if auth_header:
            self.headers['Authorization'] = auth_header
            
        # Add default cookie
        self.session.cookies.set('BITBUCKETSESSIONID', 'C72A9EC0F7491AD5AACFE7E9CF5AD96E')
        
    def _get_base_url(self, use_https: bool = True) -> str:
        """Get the appropriate base URL based on the required scheme."""
        if use_https and not self.base_url.startswith('https://'):
            return self.base_url.replace('http://', 'https://')
        elif not use_https and not self.base_url.startswith('http://'):
            return self.base_url.replace('https://', 'http://')
        return self.base_url
        
    def parse_pr_link(self, pr_link: str) -> Optional[Tuple[str, str, str]]:
        """
        Parse PR link to extract workspace, repository slug and PR ID.
        
        Args:
            pr_link: Full PR URL (e.g., https://wlstash.wenlin.net/projects/INGN/repos/ingn_api/pull-requests/866/overview)
        
        Returns:
            Tuple containing (workspace, repo_slug, pr_id) or None if parsing fails
        """
        try:
            # Remove /overview from the end if present
            pr_link = pr_link.replace('/overview', '')
            
            # Support both old and new URL patterns
            patterns = [
                r'/projects/([^/]+)/repos/([^/]+)/pull-requests/(\d+)',
                r'/projects/([^/]+)/repos/([^/]+)/pull-request/(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, pr_link)
                if match:
                    workspace = match.group(1)
                    repo_slug = match.group(2)
                    pr_id = match.group(3)
                    
                    logger.info(f"Parsed PR link - Workspace: {workspace}, Repo: {repo_slug}, PR ID: {pr_id}")
                    return workspace, repo_slug, pr_id
            # Sanitize the URL by extracting only the path portion for logging
            sanitized_link = re.sub(r'https?://[^/]+', '[HOSTNAME_REDACTED]', pr_link)
            logger.error(f"Invalid PR link format: {sanitized_link}")
            return None
            
        except Exception as e:
            logger.error(f"Error parsing PR link: {str(e)}")
            return None
            
    def fetch_pr_details(self, workspace: str, repo_slug: str, pr_id: str) -> Optional[Dict]:
        """
        Fetch PR details including title and diff from Bitbucket API.
        Uses HTTP scheme as required by the API for this endpoint.
        """
        try:
            # Use HTTP base URL
            base_url = self._get_base_url(use_https=False)
            
            # Construct URLs
            pr_url = f"{base_url}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/pull-requests/{pr_id}"
            diff_url = f"{pr_url}.diff"

            # Use different headers for PR details (JSON) and diff (plain text)
            json_headers = {
                'Content-Type': 'application/json',
                'Authorization': self.headers['Authorization']
            }
            
            # Fetch PR details
            logger.info(f"Fetching PR details from: {pr_url}")
            pr_response = self.session.get(pr_url, headers=json_headers)
            pr_response.raise_for_status()
            pr_data = pr_response.json()

            # Fetch diff (using simpler headers as it's plain text)
            logger.info(f"Fetching diff from: {diff_url}")
            diff_response = self.session.get(diff_url, headers={'Authorization': self.headers['Authorization']})
            diff_response.raise_for_status()
            
            logger.info(f"Successfully fetched PR details and diff")
            
            # Map the PR data to a simpler format
            mapped_data = self._map_pr_data(pr_data)
            
            return {
                'pr_data': mapped_data,
                'diff_content': diff_response.text
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching PR details: {str(e)}")
            return None

    def add_comment(self, workspace: str, repo_slug: str, pr_id: str, 
                   comment_data: Dict[str, Any]) -> Optional[Dict]:
        """Add a comment to a pull request."""
        try:
            url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/pull-requests/{pr_id}/comments"
            
            response = self.session.post(url, headers=self.headers, json=comment_data)
            response.raise_for_status()
            
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error adding comment: {str(e)}")
            return None

    def get_reviewed_prs(self, workspaces: List[str], repo_slugs: List[str], 
                        username: str, state: str = "ALL", limit: int = 25) -> Dict[str, Dict[str, List[Dict]]]:
        """Get PRs reviewed by a specific user across repositories."""
        try:
            results = {}
            for workspace in workspaces:
                results[workspace] = {}
                for repo_slug in repo_slugs:
                    url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/pull-requests"
                    params = {
                        'limit': limit,
                        'state': state,
                        'role.1': 'REVIEWER',
                        'username.1': username
                    }
                    
                    response = self.session.get(url, headers=self.headers, params=params)
                    response.raise_for_status()
                    
                    results[workspace][repo_slug] = response.json()['values']
            
            return results

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching reviewed PRs: {str(e)}")
            return {}

    def get_repository_info(self, workspace: str, repo_slug: str) -> Optional[Dict]:
        """Get repository information."""
        try:
            url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}"
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching repository info: {str(e)}")
            return None

    def get_branches(self, workspace: str, repo_slug: str, filter_text: Optional[str] = None) -> Optional[List[Dict]]:
        """Get repository branches, optionally filtered by name."""
        try:
            url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/branches"
            params = {}
            if filter_text:
                params['filterText'] = filter_text
            
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()['values']
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching branches: {str(e)}")
            return None

    def get_commit_details(self, workspace: str, repo_slug: str, commit_id: str) -> Optional[Dict]:
        """Get details of a specific commit."""
        try:
            url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/commits/{commit_id}"
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching commit details: {str(e)}")
            return None

    def get_pr_activities(self, workspace: str, repo_slug: str, pr_id: str) -> Optional[List[Dict]]:
        """Get activities/comments for a pull request."""
        try:
            url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/pull-requests/{pr_id}/activities"
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()['values']
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching PR activities: {str(e)}")
            return None

    def get_repo_permissions(self, workspace: str, repo_slug: str) -> Optional[Dict]:
        """Get permissions for a repository."""
        try:
            url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/permissions/users"
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching repository permissions: {str(e)}")
            return None

    def get_file_content(self, workspace: str, repo_slug: str, path: str, ref: Optional[str] = None) -> Optional[Dict]:
        """Get content of a specific file."""
        try:
            url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/browse/{path}"
            params = {}
            if ref:
                params['at'] = ref
            
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching file content: {str(e)}")
            return None

    def create_pull_request(self, workspace: str, repo_slug: str, 
                          source_branch: str, target_branch: str,
                          title: str, description: Optional[str] = None,
                          reviewers: Optional[List[str]] = None) -> Optional[Dict]:
        """Create a new pull request."""
        try:
            url = f"{self._get_base_url()}/rest/api/1.0/projects/{workspace}/repos/{repo_slug}/pull-requests"
            
            pr_data = {
                "title": title,
                "description": description or "",
                "fromRef": {
                    "id": f"refs/heads/{source_branch}",
                    "repository": {
                        "slug": repo_slug,
                        "project": {
                            "key": workspace
                        }
                    }
                },
                "toRef": {
                    "id": f"refs/heads/{target_branch}",
                    "repository": {
                        "slug": repo_slug,
                        "project": {
                            "key": workspace
                        }
                    }
                }
            }
            
            if reviewers:
                pr_data["reviewers"] = [{"user": {"name": reviewer}} for reviewer in reviewers]
            
            response = self.session.post(url, headers=self.headers, json=pr_data)
            response.raise_for_status()
            
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating pull request: {str(e)}")
            return None

    def _map_pr_data(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map Bitbucket PR data to a simplified format."""
        try:
            # Extract basic PR information
            mapped = {
                'id': pr_data.get('id'),
                'title': pr_data.get('title'),
                'description': pr_data.get('description', ''),
                'state': pr_data.get('state'),
                'open': pr_data.get('open', False),
                'closed': pr_data.get('closed', False),
                'created_date': pr_data.get('createdDate'),
                'updated_date': pr_data.get('updatedDate'),
                'version': pr_data.get('version'),
                'locked': pr_data.get('locked', False)
            }

            # Extract author information
            author = pr_data.get('author', {})
            if author:
                user = author.get('user', {})
                mapped['author'] = {
                    'username': user.get('name'),
                    'display_name': user.get('displayName'),
                    'email': user.get('emailAddress'),
                    'role': author.get('role', 'AUTHOR'),
                    'approved': author.get('approved', False),
                    'status': author.get('status', 'UNAPPROVED')
                }

            # Extract reviewers information
            reviewers = pr_data.get('reviewers', [])
            mapped['reviewers'] = []
            for reviewer in reviewers:
                user = reviewer.get('user', {})
                mapped['reviewers'].append({
                    'username': user.get('name'),
                    'display_name': user.get('displayName'),
                    'email': user.get('emailAddress'),
                    'role': reviewer.get('role', 'REVIEWER'),
                    'approved': reviewer.get('approved', False),
                    'status': reviewer.get('status', 'UNAPPROVED'),
                    'last_reviewed_commit': reviewer.get('lastReviewedCommit')
                })

            # Extract participants information
            participants = pr_data.get('participants', [])
            mapped['participants'] = []
            for participant in participants:
                user = participant.get('user', {})
                mapped['participants'].append({
                    'username': user.get('name'),
                    'display_name': user.get('displayName'),
                    'email': user.get('emailAddress'),
                    'role': participant.get('role', 'PARTICIPANT'),
                    'approved': participant.get('approved', False),
                    'status': participant.get('status', 'UNAPPROVED')
                })

            # Extract source branch information
            from_ref = pr_data.get('fromRef', {})
            if from_ref:
                repo = from_ref.get('repository', {})
                project = repo.get('project', {})
                mapped['source_branch'] = {
                    'name': from_ref.get('displayId'),
                    'id': from_ref.get('id'),
                    'latest_commit': from_ref.get('latestCommit'),
                    'repository': {
                        'slug': repo.get('slug'),
                        'name': repo.get('name'),
                        'project_key': project.get('key'),
                        'project_name': project.get('name')
                    }
                }

            # Extract target branch information
            to_ref = pr_data.get('toRef', {})
            if to_ref:
                repo = to_ref.get('repository', {})
                project = repo.get('project', {})
                mapped['target_branch'] = {
                    'name': to_ref.get('displayId'),
                    'id': to_ref.get('id'),
                    'latest_commit': to_ref.get('latestCommit'),
                    'repository': {
                        'slug': repo.get('slug'),
                        'name': repo.get('name'),
                        'project_key': project.get('key'),
                        'project_name': project.get('name')
                    }
                }

            # Extract links
            links = pr_data.get('links', {})
            if links:
                self_links = links.get('self', [])
                mapped['links'] = {
                    'self': [link.get('href') for link in self_links] if self_links else [],
                    'web_url': self_links[0].get('href') if self_links else None
                }

            # Extract properties (custom fields)
            properties = pr_data.get('properties', {})
            mapped['properties'] = properties

            # Extract JIRA issue ID if present in title
            jira_id = self.parse_jira_id(mapped.get('title', ''))
            if jira_id:
                mapped['jira_issue_id'] = jira_id

            return mapped

        except Exception as e:
            logger.error(f"Error mapping PR data: {str(e)}")
            # Return original data if mapping fails
            return pr_data

    def parse_jira_id(self, title: str) -> Optional[str]:
        """
        Parse JIRA issue ID from PR title.
        
        Args:
            title: PR title that may contain JIRA issue ID
            
        Returns:
            JIRA issue ID if found, None otherwise
        """
        try:
            # Common patterns for JIRA issue IDs
            patterns = [
                r'([A-Z]+-\d+)',  # Standard format: PROJECT-123
                r'\[([A-Z]+-\d+)\]',  # Bracketed format: [PROJECT-123]
                r'\(([A-Z]+-\d+)\)',  # Parentheses format: (PROJECT-123)
            ]
            
            for pattern in patterns:
                match = re.search(pattern, title)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing JIRA ID from title: {str(e)}")
            return None 