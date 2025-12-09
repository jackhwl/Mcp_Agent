import logging
from typing import Dict, Any, Optional, List
from fastmcp import FastMCP, Context
from .service import BitbucketService

logger = logging.getLogger(__name__)

def register_bitbucket_tools(mcp: FastMCP) -> None:
    """Register all Bitbucket tools with the MCP server."""
    
    service = BitbucketService()
    
    @mcp.tool()
    async def get_pr_details(pr_link: str, ctx: Context) -> Dict[str, Any]:
        """
        Retrieve detailed information about a Bitbucket pull request.
        
        This tool fetches comprehensive PR details including title, description, 
        author information, reviewers, diff content, and metadata from Bitbucket.
        
        Args:
            pr_link: Full URL to the pull request (e.g., 
                    https://wlstash.wenlin.net/projects/INGN/repos/ingn_api/pull-requests/866/overview)
        
        Returns:
            Dictionary containing:
            - pr_data: Mapped PR information with author, reviewers, participants, branches
            - diff_content: Complete diff content showing code changes
            - error: Error message if operation fails
        """
        try:
            await ctx.info(f"Fetching PR details from: {pr_link}")
            
            parsed = service.parse_pr_link(pr_link)
            if not parsed:
                await ctx.error("Invalid PR link format")
                return {"error": "Invalid PR link format"}
            
            workspace, repo_slug, pr_id = parsed
            result = service.fetch_pr_details(workspace, repo_slug, pr_id)
            
            if result:
                await ctx.info(f"Successfully fetched PR details for {workspace}/{repo_slug} PR #{pr_id}")
                return {
                    "success": True,
                    "pr_data": result['pr_data'],
                    "diff_content": result['diff_content']
                }
            else:
                await ctx.error("Failed to fetch PR details")
                return {"error": "Failed to fetch PR details"}
                
        except Exception as e:
            logger.error(f"Error in get_pr_details: {str(e)}")
            await ctx.error(f"Error retrieving PR details: {str(e)}")
            return {"error": f"Failed to retrieve PR details: {str(e)}"}

    @mcp.tool()
    async def add_pr_comment(pr_link: str, comment_text: str, 
                           line_comment: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
        """
        Add a comment to a Bitbucket pull request.
        
        This tool allows adding general comments to a PR or line-specific comments
        to code changes within the PR diff.
        
        Args:
            pr_link: Full URL to the pull request
            comment_text: The comment content to add
            line_comment: Optional line reference for inline comments (format: "filename:line_number")
        
        Returns:
            Dictionary containing success status and comment details or error message
        """
        try:
            if ctx:
                await ctx.info(f"Adding comment to PR: {pr_link}")
            
            parsed = service.parse_pr_link(pr_link)
            if not parsed:
                if ctx:
                    await ctx.error("Invalid PR link format")
                return {"error": "Invalid PR link format"}
            
            workspace, repo_slug, pr_id = parsed
            
            # Prepare comment data
            comment_data = {
                "text": comment_text
            }
            
            # Add line comment data if specified
            if line_comment:
                try:
                    filename, line_num = line_comment.split(":")
                    comment_data["anchor"] = {
                        "line": int(line_num),
                        "lineType": "ADDED",
                        "fileType": "TO",
                        "path": filename
                    }
                    if ctx:
                        await ctx.info(f"Adding line-specific comment to {filename}:{line_num}")
                except ValueError:
                    if ctx:
                        await ctx.error("Invalid line_comment format. Use 'filename:line_number'")
                    return {"error": "Invalid line_comment format. Use 'filename:line_number'"}
            
            result = service.add_comment(workspace, repo_slug, pr_id, comment_data)
            
            if result:
                if ctx:
                    await ctx.info("Comment added successfully")
                return {
                    "success": True,
                    "comment_id": result.get('id'),
                    "message": "Comment added successfully"
                }
            else:
                if ctx:
                    await ctx.error("Failed to add comment")
                return {"error": "Failed to add comment"}
                
        except Exception as e:
            logger.error(f"Error in add_pr_comment: {str(e)}")
            if ctx:
                await ctx.error(f"Error adding comment: {str(e)}")
            return {"error": f"Failed to add comment: {str(e)}"}

    @mcp.tool()
    async def get_reviewed_prs(workspaces: List[str], repo_slugs: List[str], 
                             username: str, state: str = "ALL", 
                             limit: int = 25, ctx: Context = None) -> Dict[str, Any]:
        """
        Get pull requests reviewed by a specific user across multiple repositories.
        
        This tool fetches PRs where the specified user was assigned as a reviewer,
        allowing filtering by state and limiting the number of results.
        
        Args:
            workspaces: List of Bitbucket project keys/workspaces to search
            repo_slugs: List of repository slugs to search within
            username: Username of the reviewer to filter by
            state: PR state filter ("ALL", "OPEN", "MERGED", "DECLINED")
            limit: Maximum number of PRs to return per repository
        
        Returns:
            Dictionary with workspaces as keys, containing repositories and their PR lists
        """
        try:
            if ctx:
                await ctx.info(f"Fetching PRs reviewed by {username} across {len(workspaces)} workspaces")
            
            results = service.get_reviewed_prs(workspaces, repo_slugs, username, state, limit)
            
            # Count total PRs found
            total_prs = 0
            for workspace_data in results.values():
                for repo_prs in workspace_data.values():
                    total_prs += len(repo_prs)
            
            if ctx:
                await ctx.info(f"Found {total_prs} PRs reviewed by {username}")
            
            return {
                "success": True,
                "total_prs_found": total_prs,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error in get_reviewed_prs: {str(e)}")
            if ctx:
                await ctx.error(f"Error fetching reviewed PRs: {str(e)}")
            return {"error": f"Failed to fetch reviewed PRs: {str(e)}"}

    @mcp.tool()
    async def get_repository_info(workspace: str, repo_slug: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get detailed information about a Bitbucket repository.
        
        This tool fetches repository metadata including name, description, project info,
        clone URLs, and other repository properties.
        
        Args:
            workspace: Bitbucket project key/workspace name
            repo_slug: Repository slug/name
        
        Returns:
            Dictionary containing repository information and metadata
        """
        try:
            if ctx:
                await ctx.info(f"Fetching repository info for {workspace}/{repo_slug}")
            
            result = service.get_repository_info(workspace, repo_slug)
            
            if result:
                if ctx:
                    await ctx.info(f"Successfully fetched repository info")
                return {
                    "success": True,
                    "repository": result
                }
            else:
                if ctx:
                    await ctx.error("Repository not found or access denied")
                return {"error": "Repository not found or access denied"}
                
        except Exception as e:
            logger.error(f"Error in get_repository_info: {str(e)}")
            if ctx:
                await ctx.error(f"Error fetching repository info: {str(e)}")
            return {"error": f"Failed to fetch repository info: {str(e)}"}

    @mcp.tool()
    async def get_repository_branches(workspace: str, repo_slug: str, 
                                    filter_text: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
        """
        Get branches from a Bitbucket repository.
        
        This tool retrieves all branches or filtered branches from a repository,
        including branch names, latest commits, and other branch metadata.
        
        Args:
            workspace: Bitbucket project key/workspace name
            repo_slug: Repository slug/name
            filter_text: Optional text to filter branch names
        
        Returns:
            Dictionary containing list of branches with their details
        """
        try:
            if ctx:
                filter_msg = f" with filter '{filter_text}'" if filter_text else ""
                await ctx.info(f"Fetching branches for {workspace}/{repo_slug}{filter_msg}")
            
            result = service.get_branches(workspace, repo_slug, filter_text)
            
            if result is not None:
                if ctx:
                    await ctx.info(f"Found {len(result)} branches")
                return {
                    "success": True,
                    "branches": result,
                    "count": len(result)
                }
            else:
                if ctx:
                    await ctx.error("Failed to fetch branches or repository not found")
                return {"error": "Failed to fetch branches or repository not found"}
                
        except Exception as e:
            logger.error(f"Error in get_repository_branches: {str(e)}")
            if ctx:
                await ctx.error(f"Error fetching branches: {str(e)}")
            return {"error": f"Failed to fetch branches: {str(e)}"}

    @mcp.tool()
    async def get_commit_details(workspace: str, repo_slug: str, 
                               commit_id: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get detailed information about a specific commit.
        
        This tool fetches commit details including author, message, timestamp,
        file changes, and other commit metadata.
        
        Args:
            workspace: Bitbucket project key/workspace name
            repo_slug: Repository slug/name
            commit_id: Full commit hash or short hash
        
        Returns:
            Dictionary containing commit details and metadata
        """
        try:
            if ctx:
                await ctx.info(f"Fetching commit details for {workspace}/{repo_slug} commit {commit_id}")
            
            result = service.get_commit_details(workspace, repo_slug, commit_id)
            
            if result:
                if ctx:
                    await ctx.info("Successfully fetched commit details")
                return {
                    "success": True,
                    "commit": result
                }
            else:
                if ctx:
                    await ctx.error("Commit not found or access denied")
                return {"error": "Commit not found or access denied"}
                
        except Exception as e:
            logger.error(f"Error in get_commit_details: {str(e)}")
            if ctx:
                await ctx.error(f"Error fetching commit details: {str(e)}")
            return {"error": f"Failed to fetch commit details: {str(e)}"}

    @mcp.tool()
    async def get_pr_activities(pr_link: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get activities and comments for a pull request.
        
        This tool fetches all activities, comments, and events associated with a PR,
        providing a complete history of interactions and changes.
        
        Args:
            pr_link: Full URL to the pull request
        
        Returns:
            Dictionary containing list of activities and comments
        """
        try:
            if ctx:
                await ctx.info(f"Fetching PR activities for: {pr_link}")
            
            parsed = service.parse_pr_link(pr_link)
            if not parsed:
                if ctx:
                    await ctx.error("Invalid PR link format")
                return {"error": "Invalid PR link format"}
            
            workspace, repo_slug, pr_id = parsed
            result = service.get_pr_activities(workspace, repo_slug, pr_id)
            
            if result is not None:
                if ctx:
                    await ctx.info(f"Found {len(result)} activities")
                return {
                    "success": True,
                    "activities": result,
                    "count": len(result)
                }
            else:
                if ctx:
                    await ctx.error("Failed to fetch PR activities")
                return {"error": "Failed to fetch PR activities"}
                
        except Exception as e:
            logger.error(f"Error in get_pr_activities: {str(e)}")
            if ctx:
                await ctx.error(f"Error fetching PR activities: {str(e)}")
            return {"error": f"Failed to fetch PR activities: {str(e)}"}

    @mcp.tool()
    async def get_repo_permissions(workspace: str, repo_slug: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get user permissions for a repository.
        
        This tool retrieves the list of users and their permission levels
        for accessing and modifying the repository.
        
        Args:
            workspace: Bitbucket project key/workspace name
            repo_slug: Repository slug/name
        
        Returns:
            Dictionary containing user permissions and access levels
        """
        try:
            if ctx:
                await ctx.info(f"Fetching repository permissions for {workspace}/{repo_slug}")
            
            result = service.get_repo_permissions(workspace, repo_slug)
            
            if result:
                if ctx:
                    await ctx.info("Successfully fetched repository permissions")
                return {
                    "success": True,
                    "permissions": result
                }
            else:
                if ctx:
                    await ctx.error("Failed to fetch repository permissions")
                return {"error": "Failed to fetch repository permissions"}
                
        except Exception as e:
            logger.error(f"Error in get_repo_permissions: {str(e)}")
            if ctx:
                await ctx.error(f"Error fetching repository permissions: {str(e)}")
            return {"error": f"Failed to fetch repository permissions: {str(e)}"}

    @mcp.tool()
    async def get_file_content(workspace: str, repo_slug: str, file_path: str, 
                             ref: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
        """
        Get content of a specific file from a repository.
        
        This tool retrieves the content of a file at a specific path,
        optionally from a specific branch or commit.
        
        Args:
            workspace: Bitbucket project key/workspace name
            repo_slug: Repository slug/name
            file_path: Path to the file within the repository
            ref: Optional branch name or commit hash (defaults to main branch)
        
        Returns:
            Dictionary containing file content and metadata
        """
        try:
            if ctx:
                ref_msg = f" at ref '{ref}'" if ref else ""
                await ctx.info(f"Fetching file content for {workspace}/{repo_slug}:{file_path}{ref_msg}")
            
            result = service.get_file_content(workspace, repo_slug, file_path, ref)
            
            if result:
                if ctx:
                    await ctx.info("Successfully fetched file content")
                return {
                    "success": True,
                    "file_content": result
                }
            else:
                if ctx:
                    await ctx.error("File not found or access denied")
                return {"error": "File not found or access denied"}
                
        except Exception as e:
            logger.error(f"Error in get_file_content: {str(e)}")
            if ctx:
                await ctx.error(f"Error fetching file content: {str(e)}")
            return {"error": f"Failed to fetch file content: {str(e)}"}

    @mcp.tool()
    async def create_pull_request(workspace: str, repo_slug: str, 
                                source_branch: str, target_branch: str,
                                title: str, description: Optional[str] = None,
                                reviewers: Optional[List[str]] = None, ctx: Context = None) -> Dict[str, Any]:
        """
        Create a new pull request in a Bitbucket repository.
        
        This tool creates a PR from a source branch to a target branch,
        with optional description and reviewer assignments.
        
        Args:
            workspace: Bitbucket project key/workspace name
            repo_slug: Repository slug/name
            source_branch: Name of the source branch (where changes are)
            target_branch: Name of the target branch (where to merge)
            title: Title for the pull request
            description: Optional description/body of the pull request
            reviewers: Optional list of usernames to assign as reviewers
        
        Returns:
            Dictionary containing created PR details or error message
        """
        try:
            if ctx:
                await ctx.info(f"Creating PR: {source_branch} → {target_branch} in {workspace}/{repo_slug}")
            
            result = service.create_pull_request(
                workspace, repo_slug, source_branch, target_branch,
                title, description, reviewers
            )
            
            if result:
                pr_id = result.get('id')
                if ctx:
                    await ctx.info(f"Successfully created PR #{pr_id}")
                return {
                    "success": True,
                    "pr_id": pr_id,
                    "pr_url": result.get('links', {}).get('self', [{}])[0].get('href'),
                    "pr_data": result
                }
            else:
                if ctx:
                    await ctx.error("Failed to create pull request")
                return {"error": "Failed to create pull request"}
                
        except Exception as e:
            logger.error(f"Error in create_pull_request: {str(e)}")
            if ctx:
                await ctx.error(f"Error creating pull request: {str(e)}")
            return {"error": f"Failed to create pull request: {str(e)}"}

    @mcp.tool()
    async def bitbucket_healthcheck(ctx: Context = None) -> Dict[str, Any]:
        """
        Check the health and connectivity of the Bitbucket MCP server.
        
        This tool verifies that the server can connect to Bitbucket APIs,
        authentication is working, and basic functionality is available.
        
        Returns:
            Dictionary containing health status, configuration info, and connection details
        """
        try:
            if ctx:
                await ctx.info("Running Bitbucket MCP Server healthcheck...")
            
            # Check basic configuration
            if not service.auth_token:
                if ctx:
                    await ctx.error("BITBUCKET_AUTH_TOKEN not configured")
                return {
                    "status": "unhealthy",
                    "error": "BITBUCKET_AUTH_TOKEN not configured",
                    "suggestion": "Set the BITBUCKET_AUTH_TOKEN environment variable"
                }
            
            if not service.base_url:
                if ctx:
                    await ctx.error("BITBUCKET_BASE_URL not configured")
                return {
                    "status": "unhealthy",
                    "error": "BITBUCKET_BASE_URL not configured",
                    "suggestion": "Set the BITBUCKET_BASE_URL environment variable"
                }
            
            # Try to make a simple API call to test connectivity
            # Using a basic API endpoint that should always be available
            try:
                test_url = f"{service._get_base_url()}/rest/api/1.0/application-properties"
                response = service.session.get(test_url, headers=service.headers, timeout=10)
                
                if response.status_code == 200:
                    api_status = "connected"
                    api_info = "Successfully connected to Bitbucket API"
                    if ctx:
                        await ctx.info("✅ Successfully connected to Bitbucket API")
                elif response.status_code == 401:
                    api_status = "authentication_failed"
                    api_info = "Authentication failed - check your auth token"
                    if ctx:
                        await ctx.error("❌ Authentication failed - check your auth token")
                else:
                    api_status = "connection_issues"
                    api_info = f"API returned status code: {response.status_code}"
                    if ctx:
                        await ctx.error(f"⚠️ API returned status code: {response.status_code}")
                    
            except Exception as api_error:
                api_status = "connection_failed"
                api_info = f"Failed to connect to API: {str(api_error)}"
                if ctx:
                    await ctx.error(f"❌ Failed to connect to API: {str(api_error)}")
            
            result = {
                "status": "healthy" if api_status == "connected" else "degraded",
                "api_status": api_status,
                "api_info": api_info,
                "configuration": {
                    "base_url": service.base_url,
                    "auth_configured": bool(service.auth_token),
                    "auth_type": "Bearer" if ':' not in service.auth_token else "Basic"
                },
                "tools_available": [
                    "get_pr_details",
                    "add_pr_comment", 
                    "get_reviewed_prs",
                    "get_repository_info",
                    "get_repository_branches",
                    "get_commit_details",
                    "get_pr_activities",
                    "get_repo_permissions",
                    "get_file_content",
                    "create_pull_request"
                ]
            }
            
            if ctx:
                if result["status"] == "healthy":
                    await ctx.info("✅ Bitbucket MCP Server is healthy")
                else:
                    await ctx.info("⚠️ Bitbucket MCP Server has some issues but is functional")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in bitbucket_healthcheck: {str(e)}")
            if ctx:
                await ctx.error(f"❌ Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": f"Health check failed: {str(e)}"
            } 