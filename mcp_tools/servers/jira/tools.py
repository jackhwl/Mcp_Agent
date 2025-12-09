from fastmcp import FastMCP, Context
from typing import Dict, Any, Optional
import logging
import os
import requests
import json



logger = logging.getLogger(__name__)

def _format_single_sprint_report(report_data: Dict[str, Any]) -> str:
    """Format a single sprint report into a readable string format."""
    if not report_data:
        return "No sprint data available."
    
    output = []
    
    # Sprint Name
    output.append(f"# 📊 Sprint Report: {report_data.get('sprint_name', 'Unknown Sprint')}")
    output.append("")
    
    # Story Points Breakdown by Status (excluding 0 SP stories)
    sp_breakdown = report_data.get('story_points_breakdown', {})
    output.append("## 🎯 Story Points Breakdown by Status")
    output.append("*(Excludes 0 story point items)*")
    output.append("")
    
    if sp_breakdown.get('total', 0) > 0:
        output.append(f"- **Total Story Points:** {sp_breakdown.get('total', 0)}")
        output.append(f"- **Done:** {sp_breakdown.get('done', 0)} ({round(sp_breakdown.get('done', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
        output.append(f"- **In Progress:** {sp_breakdown.get('in_progress', 0)} ({round(sp_breakdown.get('in_progress', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
        output.append(f"- **In Review:** {sp_breakdown.get('in_review', 0)} ({round(sp_breakdown.get('in_review', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
        output.append(f"- **In QA:** {sp_breakdown.get('in_qa', 0)} ({round(sp_breakdown.get('in_qa', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
        output.append(f"- **To Do:** {sp_breakdown.get('to_do', 0)} ({round(sp_breakdown.get('to_do', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
    else:
        output.append("No story points found in this sprint.")
    output.append("")
    
    # Aging of tickets as per status
    aging = report_data.get('aging_of_tickets', {})
    output.append("## ⏰ Aging of Tickets by Status")
    output.append("")
    
    for status, age_buckets in aging.items():
        output.append(f"**{status}:**")
        for age_bucket, count in age_buckets.items():
            output.append(f"- {age_bucket}: {count} tickets")
        output.append("")
    
    # Incomplete High Priority Tickets
    high_priority = report_data.get('incomplete_high_priority_tickets', [])
    output.append("## 🚨 Incomplete High Priority Tickets")
    output.append("")
    
    if high_priority:
        output.append("**⚠️ ATTENTION REQUIRED:**")
        for ticket in high_priority:
            sp_text = f" ({ticket.get('story_points', 0)} SP)" if ticket.get('story_points', 0) > 0 else ""
            output.append(f"- **{ticket.get('key', '')}** - {ticket.get('summary', '')}")
            output.append(f"  - Priority: {ticket.get('priority', 'Unknown')}")
            output.append(f"  - Status: {ticket.get('status', 'Unknown')}")
            output.append(f"  - Assignee: {ticket.get('assignee', 'Unassigned')}{sp_text}")
            output.append("")
    else:
        output.append("✅ No incomplete high priority tickets.")
        output.append("")
    
    # Sprint Health Indicators
    health = report_data.get('sprint_health_indicators', {})
    output.append("## 📈 Sprint Health Indicators")
    output.append("")
    
    output.append(f"- **Completion Rate:** {health.get('completion_rate', 0)}%")
    output.append(f"- **Work in Progress Rate:** {health.get('work_in_progress_rate', 0)}%")
    output.append(f"- **High Priority Incomplete:** {health.get('high_priority_incomplete_count', 0)} items")
    output.append(f"- **Unassigned Work:** {health.get('unassigned_work_count', 0)} items")
    output.append(f"- **Bug Rate:** {health.get('bug_rate', 0)}%")
    output.append("")
    
    # Recommendations
    recommendations = report_data.get('recommendations', [])
    output.append("## 💡 Recommendations")
    output.append("")
    
    for rec in recommendations:
        output.append(f"- {rec}")
    output.append("")
    
    # Sprint Success Summary
    success = report_data.get('sprint_success_summary', {})
    output.append("## 🎯 Sprint Success Summary")
    output.append("")
    
    output.append(f"- **Success Level:** {success.get('success_level', 'Unknown')}")
    output.append(f"- **Completion Rate:** {success.get('completion_rate', 0)}%")
    output.append(f"- **Total Tickets:** {success.get('total_tickets', 0)}")
    output.append(f"- **Story Points Delivered:** {success.get('story_points_delivered', 0)}")
    output.append("")
    
    # Key Achievements
    achievements = report_data.get('key_achievements', [])
    output.append("## 🏆 Key Achievements")
    output.append("")
    
    if achievements:
        for achievement in achievements:
            output.append(f"- {achievement}")
    else:
        output.append("- No specific achievements highlighted for this sprint.")
    output.append("")
    
    # Tech Categorization %
    tech_cat = report_data.get('tech_categorization', {})
    output.append("## 🔧 Tech Categorization")
    output.append("")
    
    for category, data in tech_cat.items():
        count = data.get('count', 0)
        percentage = data.get('percentage', 0)
        output.append(f"- **{category}:** {count} tickets ({percentage}%)")
    output.append("")
    
    # Bugs vs Story & Task count
    bug_breakdown = report_data.get('bugs_vs_story_task_count', {})
    output.append("## 🐛 Work Type Distribution")
    output.append("")
    
    output.append(f"- **Bugs:** {bug_breakdown.get('bugs', 0)} ({bug_breakdown.get('bug_percentage', 0)}%)")
    output.append(f"- **Stories:** {bug_breakdown.get('stories', 0)}")
    output.append(f"- **Tasks:** {bug_breakdown.get('tasks', 0)}")
    output.append("")
    
    # Production Bugs
    prod_bugs = report_data.get('production_bugs', [])
    output.append("## 🚨 Production Bugs")
    output.append("")
    
    if prod_bugs:
        output.append("**High Priority Production Issues:**")
        for bug in prod_bugs:
            output.append(f"- **{bug.get('key', '')}** - {bug.get('summary', '')}")
            output.append(f"  - Priority: {bug.get('priority', 'Unknown')}")
            output.append(f"  - Status: {bug.get('status', 'Unknown')}")
            output.append(f"  - Assignee: {bug.get('assignee', 'Unassigned')}")
            output.append("")
    else:
        output.append("✅ No high priority production bugs identified.")
        output.append("")
    
    return "\n".join(output)

def register_jira_tools(mcp: FastMCP, jira_service):

    @mcp.tool()
    async def review_ticket_against_template(ticket_key: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Review a JIRA ticket against the template, instructions, and best practices in template.md.
        Args:
            ticket_key: The JIRA ticket number (e.g., 'MS-TECH-123')
        Returns:
            Structured feedback with findings, suggestions, and compliance status.
        """
        try:
            if ctx:
                await ctx.info(f"Reviewing ticket {ticket_key} against template and best practices...")
            result = jira_service.review_ticket_against_template(ticket_key)
            if ctx:
                if result.get('compliant'):
                    await ctx.info(f"✅ Ticket {ticket_key} is compliant with template best practices.")
                else:
                    await ctx.info(f"⚠️ Ticket {ticket_key} has issues: {result.get('feedback')}")
            return result
        except Exception as e:
            error_msg = f"Error reviewing ticket {ticket_key}: {str(e)}"
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'ticket_key': ticket_key
            }

    @mcp.tool()
    async def review_active_sprint_tickets(board_id: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Review all tickets in the active sprint for a given board against template best practices.
        
        Perfect for: Sprint quality assurance, automated sprint reviews, team quality checks
        Example: review_active_sprint_tickets("3411")
        
        Args:
            board_id: The JIRA board ID to get the active sprint from
            
        Returns:
            Sprint details, individual ticket review results, and summary of pass/fail rates
        """
        try:
            if ctx:
                await ctx.info(f"Starting active sprint review for board {board_id}...")
            
            result = jira_service.review_active_sprint_tickets(board_id)
            
            if result.get('status') == 'success':
                sprint_info = result.get('sprint_info', {})
                summary = result.get('summary', {})
                
                sprint_name = sprint_info.get('name', 'Unknown Sprint')
                total_tickets = summary.get('total_tickets', 0)
                passed_count = summary.get('passed_validation', 0)
                failed_count = summary.get('failed_validation', 0)
                error_count = summary.get('review_errors', 0)
                pass_rate = summary.get('pass_rate', 0)
                
                if ctx:
                    await ctx.info(f"✅ Completed sprint review for: {sprint_name}")
                    await ctx.info(f"📊 Results: {passed_count}/{total_tickets} tickets passed ({pass_rate}% pass rate)")
                    
                    if failed_count > 0:
                        await ctx.info(f"⚠️ {failed_count} tickets need improvement")
                        
                        # Show some examples of failed tickets
                        failed_tickets = result.get('failed_tickets', [])
                        if failed_tickets:
                            example_failures = failed_tickets[:3]  # Show first 3
                            await ctx.info(f"❌ Examples of tickets needing work:")
                            for ticket in example_failures:
                                await ctx.info(f"   • {ticket['key']}: {ticket['summary'][:50]}... ({ticket['issues_count']} issues)")
                    
                    if error_count > 0:
                        await ctx.info(f"🚨 {error_count} tickets had review errors")
                    
                    if passed_count > 0:
                        await ctx.info(f"✅ {passed_count} tickets are compliant with best practices")
                
            else:
                if ctx:
                    error_msg = result.get('message', 'Unknown error')
                    if 'No active sprint' in error_msg:
                        await ctx.error(f"📅 No active sprint found for board {board_id}")
                    elif 'not found' in error_msg.lower():
                        await ctx.error(f"🔍 Board {board_id} not found - check the board ID")
                    elif 'access denied' in error_msg.lower():
                        await ctx.error(f"🚫 Access denied to board {board_id} - check permissions")
                    else:
                        await ctx.error(f"❌ Sprint review failed: {error_msg}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error during sprint review for board {board_id}: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'board_id': board_id
            }

    @mcp.tool()
    async def get_pull_request_details(ticket_key: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get pull request details from a JIRA ticket and add comments for open PRs.
        
        Perfect for: Checking PR status, tracking code review progress, automated PR notifications
        Example: get_pull_request_details("MS-TECH-123")
        
        Args:
            ticket_key: The JIRA ticket key (e.g., 'MS-TECH-123')
            
        Returns:
            Pull request count, state, and details. Automatically adds comments for open PRs.
        """
        try:
            if ctx:
                await ctx.info(f"Fetching pull request details for ticket {ticket_key}...")
            
            result = jira_service.get_pull_request_details(ticket_key)
            
            if ctx:
                if result.get('status') == 'success':
                    pr_count = result.get('pull_request_count', 0)
                    pr_state = result.get('pull_request_state', 'UNKNOWN')
                    open_count = result.get('open_count', 0)
                    
                    if pr_count == 0:
                        await ctx.info(f"📝 No pull requests found for ticket {ticket_key}")
                    else:
                        await ctx.info(f"🔄 Found {pr_count} pull request(s) with state: {pr_state}")
                        
                        if open_count > 0:
                            await ctx.info(f"⚠️ {open_count} pull request(s) are still open and need review")
                            if result.get('comment_added'):
                                await ctx.info("💬 Added comment to ticket about open pull requests")
                        else:
                            await ctx.info("✅ All pull requests have been merged or declined")
                else:
                    await ctx.error(f"Failed to get pull request details: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error getting pull request details for {ticket_key}: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'ticket_key': ticket_key
            }
    """Register all Jira-related MCP tools with the FastMCP server."""
    
    @mcp.tool()
    async def healthcheck(ctx: Context) -> Dict[str, Any]:
        """
        Healthcheck tool to verify configuration and auth token.
        Provides guidance on updating the token if needed.
        """
        try:
            await ctx.info("Running JIRA MCP Server healthcheck...")
            
            # Get environment variables and service configuration
            current_token = jira_service.auth_token
            env_token = os.getenv("JIRA_AUTH_TOKEN", "Not set")
            is_default_token = current_token == "your-secure-auth-token"
            
            # Determine configuration status
            config_status = "healthy"
            warnings = []
            instructions = []
            
            if is_default_token:
                config_status = "needs_configuration"
                warnings.append("🚨 Using default placeholder token - authentication will fail")
                instructions.extend([
                    "1. Open VSCode/Cursor settings (Ctrl+Shift+P → 'Open User Settings (JSON)')",
                    "2. Find the 'mcp.servers.my-mcp-server.env.JIRA_AUTH_TOKEN' setting", 
                    "3. Replace 'your-secure-auth-token' with your actual JIRA API token",
                    "4. Restart VSCode/Cursor to apply changes",
                    "5. Run healthcheck again to verify"
                ])
            elif not current_token or current_token == "Not set":
                config_status = "missing_token"
                warnings.append("❌ No authentication token configured")
                instructions.extend([
                    "1. Get your JIRA API token from your JIRA account settings",
                    "2. Open VSCode/Cursor settings (Ctrl+Shift+P → 'Open User Settings (JSON)')",
                    "3. Add or update: \"mcp.servers.my-mcp-server.env.JIRA_AUTH_TOKEN\": \"your-actual-token\"",
                    "4. Restart VSCode/Cursor to apply changes"
                ])
            else:
                # Token is set and not default - likely configured correctly
                if len(current_token) < 20:
                    warnings.append("⚠️ Token seems unusually short - verify it's correct")
                
            # Build response data
            healthcheck_data = {
                'status': config_status,
                'overall_health': 'healthy' if config_status == 'healthy' else 'needs_attention',
                'warnings': warnings,
                'setup_instructions': instructions,
                'service_info': {
                    'base_url': jira_service.base_url,
                    'auth_token_status': {
                        'is_set': bool(current_token and current_token != "Not set"),
                        'is_default_placeholder': is_default_token,
                        'token_length': len(current_token) if current_token else 0,
                        'token_preview': current_token[:10] + '...' if current_token and len(current_token) > 10 else current_token
                    },
                    'has_auth_header': bool(jira_service.headers.get('Authorization')),
                    'auth_header_preview': jira_service.headers.get('Authorization', '')[:25] + '...' if jira_service.headers.get('Authorization') else 'Not set'
                },
                'environment_variables': {
                    'JIRA_BASE_URL': os.getenv("JIRA_BASE_URL", "Using default"),
                    'JIRA_AUTH_TOKEN': "Set" if env_token != "Not set" else "Not set",
                    'token_source': "Environment variable" if env_token != "Not set" else "Default fallback"
                },
                'next_steps': {
                    'vscode_settings_path': {
                        'windows': os.path.expanduser("~") + "\\AppData\\Roaming\\Code\\User\\settings.json",
                        'mac_linux': os.path.expanduser("~") + "/.config/Code/User/settings.json"
                    },
                    'configuration_key': "mcp.servers.my-mcp-server.env.JIRA_AUTH_TOKEN",
                    'get_jira_token_url': f"{jira_service.base_url}/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens"
                }
            }
            
            # Provide contextual logging
            await ctx.info(f"Healthcheck completed - Base URL: {jira_service.base_url}")
            
            if config_status == "healthy":
                await ctx.info("✅ Configuration looks good! Token is set and ready to use.")
            elif config_status == "needs_configuration":
                await ctx.info("⚠️ Default placeholder token detected - please update with your actual JIRA token")
            else:
                await ctx.info("❌ Token configuration needs attention")
            
            # Log instructions if any
            if instructions:
                await ctx.info("📋 Setup instructions available in response")
            
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
                    "1. Check that the JIRA MCP server is properly installed",
                    "2. Verify the virtual environment is activated",
                    "3. Ensure all dependencies are installed"
                ]
            }
    
    @mcp.tool()
    async def test_connection(ctx: Context) -> Dict[str, Any]:
        """
        Test the JIRA connection and authentication by making a simple API call.
        Use this after updating your auth token to verify it works.
        """
        try:
            await ctx.info("Testing JIRA connection and authentication...")
            
            # Try to get current user info - this is a lightweight test
            url = f"{jira_service.base_url}/rest/api/2/myself"
            
            response = requests.get(url, headers=jira_service.headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                await ctx.info("✅ Connection successful! Authentication working properly.")
                
                return {
                    'status': 'success',
                    'connection_status': 'authenticated',
                    'message': 'Successfully connected to JIRA and authenticated',
                    'user_info': {
                        'username': user_data.get('name', 'Unknown'),
                        'display_name': user_data.get('displayName', 'Unknown'),
                        'email': user_data.get('emailAddress', 'Unknown'),
                        'active': user_data.get('active', False)
                    },
                    'server_info': {
                        'base_url': jira_service.base_url,
                        'response_time_ms': response.elapsed.total_seconds() * 1000
                    }
                }
            elif response.status_code == 401:
                await ctx.error("❌ Authentication failed - invalid token")
                return {
                    'status': 'auth_failed',
                    'connection_status': 'unauthorized',
                    'message': 'Authentication failed - please check your JIRA_AUTH_TOKEN',
                    'suggestions': [
                        "1. Verify your token is correct and not expired",
                        "2. Check if the token has the required permissions",
                        "3. Generate a new token from JIRA if needed",
                        "4. Run healthcheck for configuration guidance"
                    ],
                    'server_response': {
                        'status_code': response.status_code,
                        'error': response.text[:200] if response.text else 'No error details'
                    }
                }
            elif response.status_code == 403:
                await ctx.error("❌ Access forbidden - insufficient permissions")
                return {
                    'status': 'access_denied',
                    'connection_status': 'forbidden',
                    'message': 'Access denied - token may lack required permissions',
                    'suggestions': [
                        "1. Check if your JIRA account has the necessary permissions",
                        "2. Verify the token scope includes required access",
                        "3. Contact your JIRA administrator if needed"
                    ],
                    'server_response': {
                        'status_code': response.status_code,
                        'error': response.text[:200] if response.text else 'No error details'
                    }
                }
            else:
                await ctx.error(f"❌ Connection failed with status {response.status_code}")
                return {
                    'status': 'connection_failed',
                    'connection_status': 'error',
                    'message': f'JIRA server returned status {response.status_code}',
                    'suggestions': [
                        "1. Check if the JIRA server URL is correct",
                        "2. Verify the server is accessible from your network",
                        "3. Try again in a few moments (server might be temporarily down)"
                    ],
                    'server_response': {
                        'status_code': response.status_code,
                        'error': response.text[:200] if response.text else 'No error details'
                    }
                }
                
        except requests.exceptions.Timeout:
            error_msg = "Connection timeout - JIRA server took too long to respond"
            await ctx.error(f"❌ {error_msg}")
            return {
                'status': 'timeout',
                'connection_status': 'timeout',
                'message': error_msg,
                'suggestions': [
                    "1. Check your internet connection",
                    "2. Verify the JIRA server URL is correct",
                    "3. Try again in a few moments"
                ]
            }
        except requests.exceptions.ConnectionError:
            error_msg = "Could not connect to JIRA server - check URL and network"
            await ctx.error(f"❌ {error_msg}")
            return {
                'status': 'connection_error',
                'connection_status': 'unreachable',
                'message': error_msg,
                'suggestions': [
                    "1. Verify the JIRA_BASE_URL is correct",
                    "2. Check your internet connection",
                    "3. Confirm the server is accessible from your location"
                ]
            }
        except Exception as e:
            error_msg = f"Unexpected error during connection test: {str(e)}"
            logger.error(error_msg)
            await ctx.error(f"❌ {error_msg}")
            return {
                'status': 'error',
                'connection_status': 'error',
                'message': error_msg,
                'suggestions': [
                    "1. Run healthcheck to verify configuration",
                    "2. Check server logs for more details",
                    "3. Try restarting the MCP server"
                ]
            }
    
    @mcp.tool()
    async def get_ticket_details(ticket_key: str, ctx: Context) -> Dict[str, Any]:
        """Fetch details for a specific Jira ticket."""
        try:
            await ctx.info(f"Fetching details for ticket: {ticket_key}")
            ticketdetails = jira_service.get_ticket_details(ticket_key)
            ctx.info(f"Ticket details fetched successfully - {ticketdetails}")
            return ticketdetails
        except Exception as e:
            await ctx.error(f"Error fetching ticket details: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    @mcp.tool()
    async def create_review_task(parent_key: str, title: str, description: str, ctx: Context) -> Dict[str, Any]:
        """Create a review task under a parent Jira ticket."""
        try:
            await ctx.info(f"Creating review task under parent ticket: {parent_key}")
            
            # Get parent ticket details
            parent_details = jira_service.get_ticket_details(parent_key)
            
            # Create review task
            review_data = {
                'title': title,
                'description': description
            }
            
            result = jira_service.create_review_task(parent_details, review_data)
            
            if result['status'] == 'success':
                await ctx.info(f"Successfully created review task: {result['task_key']}")
            else:
                await ctx.error(f"Failed to create review task: {result['message']}")
                
            return result
        except Exception as e:
            await ctx.error(f"Error creating review task: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    @mcp.tool()
    async def get_my_active_work(ctx: Context = None) -> Dict[str, Any]:
        """
        Get all issues currently assigned to me that are not closed.
        
        Perfect for: Daily standup updates, personal work tracking
        Returns: Open issues assigned to the current user, ordered by priority then update time
        """
        jql = "assignee = currentUser() AND status not in ('Closed', 'Done', 'Resolved') ORDER BY priority DESC, updated DESC"
        try:
            if ctx:
                await ctx.info("Fetching your active work items...")
            
            result = jira_service.search_jira_issues(jql, 25)
            
            if result.get('status') == 'error':
                if ctx:
                    await ctx.error(f"Jira API error: {result.get('message', 'Unknown error')}")
                return {
                    'status': 'error',
                    'message': f"Failed to fetch active work: {result.get('message', 'Unknown error')}",
                    'jql_used': jql
                }
            
            if ctx:
                issue_count = result.get('results', {}).get('total', 0)
                await ctx.info(f"Found {issue_count} active work items")
            
            return result
            
        except Exception as e:
            error_msg = f"Unexpected error in get_my_active_work: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'jql_used': jql
            }

    @mcp.tool()
    async def get_sprint_burndown(project_key: str = "MS-TECH", ctx: Context = None) -> Dict[str, Any]:
        """
        Get current sprint progress - issues by status breakdown.
        
        Perfect for: Sprint reviews, daily standups, progress tracking
        Example: get_sprint_burndown("MS-TECH")
        Returns: Count of issues in each status for current sprint planning
        """
        jql = f"project = {project_key} AND sprint in openSprints() ORDER BY status, priority DESC"
        try:
            if ctx:
                await ctx.info(f"Fetching sprint burndown for {project_key}...")
            return jira_service.search_jira_issues(jql, 100)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_high_priority_blockers(project_key: str = "MS-TECH", ctx: Context = None) -> Dict[str, Any]:
        """
        Get critical and high priority issues that are blocking progress.
        
        Perfect for: Executive reports, escalation tracking, risk management
        Example: get_high_priority_blockers("MS-TECH")
        Returns: High/Critical priority open issues, ordered by priority
        """
        jql = f"project = {project_key} AND priority in ('Highest', 'Critical', 'High') AND status not in ('Closed', 'Done', 'Resolved') ORDER BY priority DESC, created ASC"
        try:
            if ctx:
                await ctx.info(f"Fetching high priority blockers for {project_key}...")
            return jira_service.search_jira_issues(jql, 50)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_weekly_delivery_report(project_key: str = "MS-TECH", ctx: Context = None) -> Dict[str, Any]:
        """
        Get issues completed in the last 7 days for delivery reporting.
        
        Perfect for: Weekly status reports, delivery metrics, team velocity
        Example: get_weekly_delivery_report("MS-TECH")
        Returns: Issues closed/resolved in the past week
        """
        jql = f"project = {project_key} AND status in ('Closed', 'Done', 'Resolved') AND resolved >= -7d ORDER BY resolved DESC"
        try:
            if ctx:
                await ctx.info(f"Fetching weekly delivery report for {project_key}...")
            return jira_service.search_jira_issues(jql, 100)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_bug_health_report(project_key: str = "MS-TECH", ctx: Context = None) -> Dict[str, Any]:
        """
        Get all open bugs for quality health assessment.
        
        Perfect for: Quality reviews, bug triage meetings, release readiness
        Example: get_bug_health_report("MS-TECH")
        Returns: All open bugs ordered by priority and age
        """
        jql = f"project = {project_key} AND issuetype = Bug AND status not in ('Closed', 'Done', 'Resolved') ORDER BY priority DESC, created ASC"
        try:
            if ctx:
                await ctx.info(f"Fetching bug health report for {project_key}...")
            return jira_service.search_jira_issues(jql, 100)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_unassigned_work(project_key: str = "MS-TECH", ctx: Context = None) -> Dict[str, Any]:
        """
        Get unassigned issues that need resource allocation.
        
        Perfect for: Resource planning, backlog grooming, sprint planning
        Example: get_unassigned_work("MS-TECH")
        Returns: Open issues without assignees, ordered by priority
        """
        jql = f"project = {project_key} AND assignee is EMPTY AND status not in ('Closed', 'Done', 'Resolved') ORDER BY priority DESC, created ASC"
        try:
            if ctx:
                await ctx.info(f"Fetching unassigned work for {project_key}...")
            return jira_service.search_jira_issues(jql, 50)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_overdue_items(project_key: str = "MS-TECH", ctx: Context = None) -> Dict[str, Any]:
        """
        Get issues past their due dates that need immediate attention.
        
        Perfect for: Risk management, escalation reports, timeline recovery
        Example: get_overdue_items("MS-TECH")
        Returns: Open issues with due dates in the past
        """
        jql = f"project = {project_key} AND duedate < now() AND status not in ('Closed', 'Done', 'Resolved') ORDER BY duedate ASC"
        try:
            if ctx:
                await ctx.info(f"Fetching overdue items for {project_key}...")
            return jira_service.search_jira_issues(jql, 50)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_team_workload(assignee_name: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get workload overview for a specific team member.
        
        Perfect for: Resource management, 1:1s, capacity planning
        Example: get_team_workload("john.doe")
        Returns: All open issues assigned to the specified person
        """
        jql = f"assignee = '{assignee_name}' AND status not in ('Closed', 'Done', 'Resolved') ORDER BY priority DESC, updated DESC"
        try:
            if ctx:
                await ctx.info(f"Fetching workload for {assignee_name}...")
            return jira_service.search_jira_issues(jql, 50)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_recent_activity(project_key: str = "MS-TECH", days: int = 3, ctx: Context = None) -> Dict[str, Any]:
        """
        Get recent activity across the project for pulse checking.
        
        Perfect for: Daily standups, pulse checks, activity monitoring
        Example: get_recent_activity("MS-TECH", 3)
        Returns: Issues updated in the last N days
        """
        jql = f"project = {project_key} AND updated >= -{days}d ORDER BY updated DESC"
        try:
            if ctx:
                await ctx.info(f"Fetching recent activity for {project_key} (last {days} days)...")
            return jira_service.search_jira_issues(jql, 100)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_feature_progress(feature_label: str, project_key: Optional[str] = None, ctx: Context = None) -> Dict[str, Any]:
        """
        Track progress on a specific feature or epic by label.
        
        Perfect for: Feature status updates, milestone tracking, stakeholder reports
        Example: get_feature_progress("login-redesign", "MS-TECH") or get_feature_progress("login-redesign") for all projects
        Returns: All issues tagged with the specified feature label
        """
        base_jql = f"labels = '{feature_label}'"
        
        if project_key:
            jql = f"project = {project_key} AND {base_jql} ORDER BY status, priority DESC"
            info_msg = f"Fetching progress for feature '{feature_label}' in {project_key}..."
        else:
            jql = f"{base_jql} ORDER BY status, priority DESC"
            info_msg = f"Fetching progress for feature '{feature_label}' in all projects..."
        
        try:
            if ctx:
                await ctx.info(info_msg)
            return jira_service.search_jira_issues(jql, 100)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_release_readiness(fix_version: str, project_key: str = "MS-TECH", ctx: Context = None) -> Dict[str, Any]:
        """
        Get release readiness status for a specific version.
        
        Perfect for: Release planning, go/no-go decisions, release notes
        Example: get_release_readiness("v2.1.0", "MS-TECH")
        Returns: All issues scheduled for the specified release version
        """
        jql = f"project = {project_key} AND fixVersion = '{fix_version}' ORDER BY status, priority DESC"
        try:
            if ctx:
                await ctx.info(f"Fetching release readiness for {fix_version} in {project_key}...")
            return jira_service.search_jira_issues(jql, 200)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def search_jira_custom(jql_query: str, max_results: int = 50, ctx: Context = None) -> Dict[str, Any]:
        """
        Execute custom JQL queries for advanced use cases.
        
        Perfect for: Custom reports, ad-hoc analysis, power user queries
        Example: search_jira_custom("project = MS-TECH AND component = 'Frontend'")
        Returns: Results matching the custom JQL query
        """
        try:
            if ctx:
                await ctx.info(f"Executing custom JQL: {jql_query}")
            return jira_service.search_jira_issues(jql_query, max_results)
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @mcp.tool()
    async def get_user_projects(username: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get all project keys where a user has assigned open issues.
        
        Perfect for: Project discovery, access verification, user onboarding
        Example: get_user_projects("john.doe") or get_user_projects("currentUser()")
        Returns: List of unique project keys where the user has open assigned issues
        """
        # Use currentUser() if no specific username provided or if user wants their own projects
        if username.lower() in ['me', 'current', 'myself']:
            jql = "assignee = currentUser() AND status not in ('Closed', 'Done', 'Resolved') ORDER BY project ASC"
            info_msg = "Fetching your active project assignments..."
        else:
            jql = f"assignee = '{username}' AND status not in ('Closed', 'Done', 'Resolved') ORDER BY project ASC"
            info_msg = f"Fetching active project assignments for {username}..."
        
        try:
            if ctx:
                await ctx.info(info_msg)
            
            # Get all open issues for the user (we need a higher limit to capture all projects)
            result = jira_service.search_jira_issues(jql, 1000)
            
            if result.get('status') == 'error':
                if ctx:
                    await ctx.error(f"Jira API error: {result.get('message', 'Unknown error')}")
                return {
                    'status': 'error',
                    'message': f"Failed to fetch projects for user: {result.get('message', 'Unknown error')}",
                    'username': username,
                    'jql_used': jql
                }
            
            # Extract unique project keys from the issues
            issues = result.get('results', {}).get('issues', [])
            project_info = {}
            
            for issue in issues:
                # Try to extract project info from the issue key (format: PROJECT-123)
                issue_key = issue.get('key', '')
                if '-' in issue_key:
                    project_key = issue_key.split('-')[0]
                    if project_key not in project_info:
                        project_info[project_key] = {
                            'project_key': project_key,
                            'open_issue_count': 0,
                            'sample_issues': []
                        }
                    
                    project_info[project_key]['open_issue_count'] += 1
                    
                    # Add up to 3 sample issues per project
                    if len(project_info[project_key]['sample_issues']) < 3:
                        project_info[project_key]['sample_issues'].append({
                            'key': issue_key,
                            'summary': issue.get('summary', 'No summary')[:50] + '...' if len(issue.get('summary', '')) > 50 else issue.get('summary', 'No summary'),
                            'status': issue.get('status', 'Unknown'),
                            'priority': issue.get('priority', 'Unknown')
                        })
            
            projects_list = list(project_info.values())
            projects_list.sort(key=lambda x: x['open_issue_count'], reverse=True)
            
            if ctx:
                project_count = len(projects_list)
                total_issues = sum(p['open_issue_count'] for p in projects_list)
                await ctx.info(f"Found {project_count} projects with {total_issues} total open assigned issues")
            
            return {
                'status': 'success',
                'username': username,
                'total_projects': len(projects_list),
                'total_open_assigned_issues': sum(p['open_issue_count'] for p in projects_list),
                'projects': projects_list,
                'project_keys_only': [p['project_key'] for p in projects_list],
                'jql_used': jql
            }
            
        except Exception as e:
            error_msg = f"Unexpected error in get_user_projects: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'username': username,
                'jql_used': jql
            }

    @mcp.tool()
    async def create_user_story(
        project_id: str,
        summary: str,
        description: str = "",
        as_an: str = "",
        when: str = "",
        want_to: str = "",
        so_i_can: str = "",
        so_that: str = "",
        acceptance_criteria: str = "",
        priority_id: str = "6",
        issue_type_id: str = "21",
        theme_id: Optional[str] = None,
        team_id: Optional[str] = None,
        assignee: Optional[str] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Create a user story with custom fields for product management.
        
        Perfect for: Creating well-structured user stories with acceptance criteria
        Example: create_user_story(
            project_id="12345",
            summary="User login functionality",
            description="Implement secure user authentication",
            as_an="registered user",
            when="I visit the login page",
            want_to="securely access my account",
            so_i_can="view my personal dashboard",
            so_that="I can manage my profile and settings",
            acceptance_criteria="- User can enter username/password\\n- System validates credentials\\n- User is redirected to dashboard"
        )
        
        Args:
            project_id: Jira project ID (required)
            summary: Story title/summary (required)
            description: Detailed description
            as_an: "As a..." part of user story format
            when: "When..." part of user story format
            want_to: "I want to..." part of user story format
            so_i_can: "So I can..." part of user story format
            so_that: "So that..." part of user story format
            acceptance_criteria: Acceptance criteria for the story
            priority_id: Priority ID (default: "3" for Medium)
            issue_type_id: Issue type ID (default: "10001" for Story)
            theme_id: Theme ID for theme/squad custom field
            team_id: Team ID for theme/squad custom field
            assignee: Username to assign the story to
        
        Returns: Created story details including key and ID
        """
        try:
            if ctx:
                await ctx.info(f"Creating user story: {summary}")
            
            story_data = {
                'project_id': project_id,
                'summary': summary,
                'description': description,
                'as_an': as_an,
                'when': when,
                'want_to': want_to,
                'so_i_can': so_i_can,
                'so_that': so_that,
                'acceptance_criteria': acceptance_criteria,
                'priority_id': priority_id,
                'issue_type_id': issue_type_id,
                'theme_id': theme_id,
                'team_id': team_id,
                'assignee': assignee
            }
            
            result = jira_service.create_user_story(story_data)
            
            if result.get('status') == 'success':
                if ctx:
                    await ctx.info(f"Successfully created user story: {result.get('story_key')}")
            else:
                if ctx:
                    await ctx.error(f"Failed to create user story: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error creating user story: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }

    @mcp.tool()
    async def update_ticket(
        ticket_key: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        priority_id: Optional[str] = None,
        status_id: Optional[str] = None,
        labels: Optional[list] = None,
        add_labels: Optional[list] = None,
        remove_labels: Optional[list] = None,
        comment: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        as_an: Optional[str] = None,
        when: Optional[str] = None,
        want_to: Optional[str] = None,
        so_i_can: Optional[str] = None,
        so_that: Optional[str] = None,
        acceptance_criteria: Optional[str] = None,
        theme_id: Optional[str] = None,
        team_id: Optional[str] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Update an existing Jira ticket with new values for various fields, including user story format fields.
        
        Perfect for: Enhancing poorly written tickets with rich details, updating ticket status, reassigning work, adding structured user story information
        Example: update_ticket(
            ticket_key="MS-TECH-123",
            summary="Enhanced: User login functionality with security improvements",
            description="Comprehensive user authentication system with enhanced security features",
            as_an="registered user",
            when="I visit the login page",
            want_to="securely access my account with multi-factor authentication",
            so_i_can="safely manage my personal information",
            so_that="my data remains protected from unauthorized access",
            acceptance_criteria="- User can enter username/password\\n- System validates credentials\\n- MFA is enforced\\n- User is redirected to dashboard\\n- Failed attempts are logged",
            assignee="john.doe",
            priority_id="2",
            add_labels=["security", "user-experience"]
        )
        
        Args:
            ticket_key: Jira ticket key (e.g., "MS-TECH-123") (required)
            summary: New summary/title for the ticket
            description: New description for the ticket
            assignee: Username to assign the ticket to (use "" to unassign)
            priority_id: Priority ID (1=Highest, 2=High, 3=Medium, 4=Low, 5=Lowest)
            status_id: Status ID to transition the ticket to
            labels: Complete list of labels to set (replaces existing labels)
            add_labels: List of labels to add to existing labels
            remove_labels: List of labels to remove from existing labels
            comment: Comment to add to the ticket
            custom_fields: Dictionary of custom field IDs and their values
            as_an: "As a..." part of user story format
            when: "When..." part of user story format
            want_to: "I want to..." part of user story format
            so_i_can: "So I can..." part of user story format
            so_that: "So that..." part of user story format
            acceptance_criteria: Detailed acceptance criteria for the story
            theme_id: Theme ID for theme/squad custom field
            team_id: Team ID for theme/squad custom field
        
        Returns: Updated ticket details and operation status
        """
        try:
            if ctx:
                await ctx.info(f"Updating ticket: {ticket_key}")
            
            update_data = {
                'ticket_key': ticket_key,
                'summary': summary,
                'description': description,
                'assignee': assignee,
                'priority_id': priority_id,
                'status_id': status_id,
                'labels': labels,
                'add_labels': add_labels,
                'remove_labels': remove_labels,
                'comment': comment,
                'custom_fields': custom_fields or {},
                'as_an': as_an,
                'when': when,
                'want_to': want_to,
                'so_i_can': so_i_can,
                'so_that': so_that,
                'acceptance_criteria': acceptance_criteria,
                'theme_id': theme_id,
                'team_id': team_id
            }
            
            result = jira_service.update_ticket(update_data)
            
            if result.get('status') == 'success':
                if ctx:
                    await ctx.info(f"Successfully updated ticket: {ticket_key}")
            else:
                if ctx:
                    await ctx.error(f"Failed to update ticket: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error updating ticket: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'ticket_key': ticket_key
            }

    @mcp.tool()
    async def enhance_ticket_details(
        ticket_key: str,
        enhanced_summary: Optional[str] = None,
        enhanced_description: Optional[str] = None,
        user_persona: Optional[str] = None,
        user_scenario: Optional[str] = None,
        user_goal: Optional[str] = None,
        business_value: Optional[str] = None,
        outcome_benefit: Optional[str] = None,
        detailed_acceptance_criteria: Optional[str] = None,
        add_priority: Optional[str] = None,
        add_labels: Optional[list] = None,
        assign_to: Optional[str] = None,
        add_comment: Optional[str] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Enhance a poorly written ticket with rich, structured details using user story format.
        
        Perfect for: Converting basic tickets into well-structured user stories with clear acceptance criteria
        Example: enhance_ticket_details(
            ticket_key="MS-TECH-123",
            enhanced_summary="User Authentication: Secure Login with Multi-Factor Authentication",
            enhanced_description="Implement comprehensive user authentication system with enhanced security features and user experience improvements",
            user_persona="registered user accessing the application",
            user_scenario="I am logging into the application from my browser",
            user_goal="securely authenticate and access my personal dashboard",
            business_value="protect user data and maintain system security compliance",
            outcome_benefit="users can confidently access their accounts knowing their data is secure",
            detailed_acceptance_criteria='''
        GIVEN a registered user with valid credentials
        WHEN they attempt to log in
        THEN they should be able to authenticate successfully
        
        Acceptance Criteria:
        - User can enter username and password on login form
        - System validates credentials against secure database
        - Multi-factor authentication is enforced for all users
        - Failed login attempts are logged and rate-limited
        - Successful login redirects to personalized dashboard
        - Session management follows security best practices
        - Password reset functionality is available
        - Account lockout after multiple failed attempts
            ''',
            add_priority="2",
            add_labels=["security", "user-experience", "authentication"],
            assign_to="security.team.lead"
        )
        
        Args:
            ticket_key: Jira ticket key to enhance (required)
            enhanced_summary: Improved, descriptive summary
            enhanced_description: Detailed description of the requirement
            user_persona: "As a..." - who is the user (e.g., "registered customer", "admin user")
            user_scenario: "When..." - what triggers this need (e.g., "I visit the login page")
            user_goal: "I want to..." - what the user wants to achieve
            business_value: "So I can..." - immediate user benefit
            outcome_benefit: "So that..." - broader business/user outcome
            detailed_acceptance_criteria: Comprehensive acceptance criteria with test scenarios
            add_priority: Priority level (1=Highest, 2=High, 3=Medium, 4=Low, 5=Lowest)
            add_labels: Labels to add for categorization and filtering
            assign_to: Username to assign the enhanced ticket to
            add_comment: Comment explaining the enhancement
        
        Returns: Enhanced ticket details and summary of improvements made
        """
        try:
            if ctx:
                await ctx.info(f"Enhancing ticket details for: {ticket_key}")
            
            # First get the current ticket to see what we're working with
            current_ticket = jira_service.get_ticket_details(ticket_key)
            
            # Prepare the enhancement comment
            enhancement_comment = add_comment or f"Ticket enhanced with structured user story format and detailed acceptance criteria. Original summary: '{current_ticket.get('summary', 'N/A')}'"
            
            # Build the update data
            update_data = {
                'ticket_key': ticket_key,
                'summary': enhanced_summary,
                'description': enhanced_description,
                'as_an': user_persona,
                'when': user_scenario,
                'want_to': user_goal,
                'so_i_can': business_value,
                'so_that': outcome_benefit,
                'acceptance_criteria': detailed_acceptance_criteria,
                'priority_id': add_priority,
                'add_labels': add_labels,
                'assignee': assign_to,
                'comment': enhancement_comment
            }
            
            # Remove None values to avoid unnecessary updates
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            result = jira_service.update_ticket(update_data)
            
            if result.get('status') == 'success':
                if ctx:
                    await ctx.info(f"Successfully enhanced ticket: {ticket_key}")
                
                # Add summary of enhancements made
                enhancements_made = []
                if enhanced_summary:
                    enhancements_made.append("✅ Enhanced summary")
                if enhanced_description:
                    enhancements_made.append("✅ Added detailed description")
                if user_persona:
                    enhancements_made.append("✅ Added user persona ('As a...')")
                if user_scenario:
                    enhancements_made.append("✅ Added user scenario ('When...')")
                if user_goal:
                    enhancements_made.append("✅ Added user goal ('I want to...')")
                if business_value:
                    enhancements_made.append("✅ Added business value ('So I can...')")
                if outcome_benefit:
                    enhancements_made.append("✅ Added outcome benefit ('So that...')")
                if detailed_acceptance_criteria:
                    enhancements_made.append("✅ Added detailed acceptance criteria")
                if add_priority:
                    enhancements_made.append("✅ Updated priority")
                if add_labels:
                    enhancements_made.append(f"✅ Added labels: {', '.join(add_labels)}")
                if assign_to:
                    enhancements_made.append(f"✅ Assigned to: {assign_to}")
                
                result['enhancement_summary'] = {
                    'original_ticket': {
                        'summary': current_ticket.get('summary', 'N/A'),
                        'description': current_ticket.get('description', 'N/A')[:100] + '...' if current_ticket.get('description') and len(current_ticket.get('description', '')) > 100 else current_ticket.get('description', 'N/A')
                    },
                    'enhancements_made': enhancements_made,
                    'total_enhancements': len(enhancements_made)
                }
            else:
                if ctx:
                    await ctx.error(f"Failed to enhance ticket: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error enhancing ticket details: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'ticket_key': ticket_key
            }

    @mcp.tool()
    async def get_projects(search_term: str = "", max_results: int = 50, ctx: Context = None) -> Dict[str, Any]:
        """
        Get all accessible Jira projects with their IDs and basic information.
        
        Perfect for: Discovering project IDs before creating user stories, exploring available projects
        Example: get_projects() or get_projects("tech") to search for projects containing "tech"
        
        Args:
            search_term: Optional search term to filter projects by name or key
            max_results: Maximum number of projects to return (default: 50)
        
        Returns: List of projects with IDs, keys, names, and descriptions
        """
        try:
            if ctx:
                if search_term:
                    await ctx.info(f"Searching for projects matching: {search_term}")
                else:
                    await ctx.info("Fetching all accessible projects...")
            
            result = jira_service.get_projects(search_term, max_results)
            
            if result.get('status') == 'success':
                project_count = result.get('results', {}).get('total', 0)
                if ctx:
                    if result.get('filtered'):
                        await ctx.info(f"Found {project_count} projects matching '{search_term}'")
                    else:
                        await ctx.info(f"Found {project_count} accessible projects")
            else:
                if ctx:
                    error_type = result.get('error_type', 'unknown')
                    if error_type == 'timeout':
                        await ctx.error("Request timed out - try again or check your connection")
                    elif error_type == 'connection_error':
                        await ctx.error("Connection failed - check network and JIRA server status")
                    elif error_type == 'http_error':
                        await ctx.error(f"HTTP error {result.get('status_code', 'unknown')} - check permissions")
                    else:
                        await ctx.error(f"Failed to fetch projects: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error fetching projects: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }

    @mcp.tool()
    async def get_project_details(project_id: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get comprehensive details for a specific Jira project by ID or key.
        
        Perfect for: Getting project configuration, available issue types, components, versions, and team roles
        Example: get_project_details("12345") or get_project_details("MS-TECH")
        
        Args:
            project_id: Project ID (numeric) or project key (e.g., "MS-TECH", "12345")
        
        Returns: Detailed project information including components, versions, issue types, roles, and permissions
        """
        try:
            if ctx:
                await ctx.info(f"Fetching detailed information for project: {project_id}")
            
            result = jira_service.get_project_by_id(project_id)
            
            if result.get('status') == 'success':
                project_info = result.get('project', {})
                project_name = project_info.get('name', 'Unknown')
                project_key = project_info.get('key', 'Unknown')
                
                if ctx:
                    await ctx.info(f"✅ Found project: {project_name} ({project_key})")
                    
                    # Provide helpful summary
                    components_count = len(project_info.get('components', []))
                    versions_count = len(project_info.get('versions', []))
                    issue_types_count = len(project_info.get('issue_types', []))
                    
                    await ctx.info(f"📊 Project has {components_count} components, {versions_count} versions, {issue_types_count} issue types")
            else:
                if ctx:
                    error_type = result.get('error_type', 'unknown')
                    if error_type == 'project_not_found':
                        await ctx.error(f"❌ Project not found: {project_id} - check the ID/key is correct")
                    elif error_type == 'access_denied':
                        await ctx.error(f"🚫 Access denied to project: {project_id} - check your permissions")
                    elif error_type == 'timeout':
                        await ctx.error("⏱️ Request timed out - try again or check your connection")
                    elif error_type == 'connection_error':
                        await ctx.error("🔌 Connection failed - check network and JIRA server status")
                    elif error_type == 'http_error':
                        status_code = result.get('status_code', 'unknown')
                        await ctx.error(f"🌐 HTTP error {status_code} - check server status and permissions")
                    else:
                        await ctx.error(f"❌ Failed to fetch project details: {result.get('message')}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error fetching project details for {project_id}: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'project_identifier': project_id
            }

    @mcp.resource("jira://ticket/{ticket_key}")
    async def get_ticket_resource(ticket_key: str, ctx: Context = None) -> Dict[str, Any]:
        """Resource endpoint for fetching Jira ticket details."""
        try:
            if ctx:
                await ctx.info(f"Fetching ticket resource: {ticket_key}")
            return jira_service.get_ticket_details(ticket_key)
        except Exception as e:
            if ctx:
                await ctx.error(f"Error fetching ticket resource: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    @mcp.tool()
    async def get_project_creation_info(project_id: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Get essential project information needed for creating user stories and issues.
        
        Perfect for: Finding issue type IDs, priority IDs, and other metadata needed for create_user_story
        Example: get_project_creation_info("MS-TECH") or get_project_creation_info("12345")
        
        Args:
            project_id: Project ID (numeric) or project key (e.g., "MS-TECH", "12345")
        
        Returns: Streamlined project info focused on creation parameters (issue types, priorities, components)
        """
        try:
            if ctx:
                await ctx.info(f"Fetching creation info for project: {project_id}")
            
            result = jira_service.get_project_by_id(project_id)
            
            if result.get('status') == 'success':
                project_info = result.get('project', {})
                project_name = project_info.get('name', 'Unknown')
                project_key = project_info.get('key', 'Unknown')
                
                # Extract issue types with IDs
                issue_types = []
                story_types = []
                for issue_type in project_info.get('issue_types', []):
                    issue_type_info = {
                        'id': issue_type.get('id'),
                        'name': issue_type.get('name'),
                        'description': issue_type.get('description', 'No description'),
                        'is_subtask': issue_type.get('subtask', False)
                    }
                    issue_types.append(issue_type_info)
                    
                    # Identify story-like types
                    name_lower = issue_type.get('name', '').lower()
                    if any(keyword in name_lower for keyword in ['story', 'feature', 'epic', 'task']):
                        story_types.append(issue_type_info)
                
                # Extract components with IDs
                components = []
                for comp in project_info.get('components', []):
                    component_info = {
                        'id': comp.get('id'),
                        'name': comp.get('name'),
                        'description': comp.get('description', 'No description'),
                        'lead': comp.get('lead', 'Unknown')
                    }
                    components.append(component_info)
                
                # Extract active versions
                active_versions = []
                for version in project_info.get('versions', []):
                    if not version.get('archived', False):
                        version_info = {
                            'id': version.get('id'),
                            'name': version.get('name'),
                            'description': version.get('description', 'No description'),
                            'released': version.get('released', False),
                            'release_date': version.get('release_date'),
                            'start_date': version.get('start_date')
                        }
                        active_versions.append(version_info)
                
                creation_info = {
                    'project': {
                        'id': project_info.get('id'),
                        'key': project_key,
                        'name': project_name,
                        'description': project_info.get('description', 'No description'),
                        'lead': project_info.get('lead', {}),
                        'project_type': project_info.get('project_type', 'Unknown')
                    },
                    'issue_types': {
                        'all': issue_types,
                        'story_types': story_types,
                        'subtask_available': any(it.get('is_subtask') for it in issue_types),
                        'recommended_story_id': story_types[0].get('id') if story_types else (issue_types[0].get('id') if issue_types else None),
                        'recommended_story_name': story_types[0].get('name') if story_types else (issue_types[0].get('name') if issue_types else None)
                    },
                    'components': components,
                    'active_versions': active_versions,
                    'creation_tips': {
                        'use_project_id': project_info.get('id'),
                        'suggested_issue_type_id': story_types[0].get('id') if story_types else (issue_types[0].get('id') if issue_types else "21"),
                        'default_priority_id': "6",  # Medium priority - this is typically universal
                        'priority_options': {
                            '1': 'Highest',
                            '2': 'High', 
                            '3': 'Medium',
                            '4': 'Low',
                            '5': 'Lowest',
                            '6': 'Medium (Default)'
                        }
                    }
                }
                
                if ctx:
                    await ctx.info(f"✅ Found creation info for: {project_name} ({project_key})")
                    await ctx.info(f"🎯 Recommended story type: {creation_info['issue_types']['recommended_story_name']} (ID: {creation_info['issue_types']['recommended_story_id']})")
                    await ctx.info(f"📝 Use project ID: {project_info.get('id')} for create_user_story")
                
                return {
                    'status': 'success',
                    'creation_info': creation_info,
                    'project_identifier': project_id
                }
            else:
                if ctx:
                    error_type = result.get('error_type', 'unknown')
                    if error_type == 'project_not_found':
                        await ctx.error(f"❌ Project not found: {project_id}")
                    elif error_type == 'access_denied':
                        await ctx.error(f"🚫 Access denied to project: {project_id}")
                    else:
                        await ctx.error(f"❌ Failed to fetch project info: {result.get('message')}")
                
                return result
            
        except Exception as e:
            error_msg = f"Error fetching project creation info for {project_id}: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg,
                'project_identifier': project_id
            }

    
    @mcp.tool()
    async def create_bug_ticket(ctx: Context, project_key: str, summary: str, description: str, severity: str,
                         steps_to_reproduce: str , expected_result: str , actual_result: str, 
                         detected_in: str , detected_by: str, priority: str = "3-Medium") -> Dict[str, Any]:
        """Create a new bug ticket in Jira.
        Perfect for: Reporting bugs with detailed reproduction steps and expected/actual results
        Example: create_bug_ticket(
            project_key="SALMU",
            summary="Login page crashes on invalid input",
            description="The login page crashes when entering invalid characters in the username field.",
            severity="High",
            steps_to_reproduce="1. Go to login page\\n2. Enter invalid characters in username field\\n3. Click login",
            expected_result="User should see an error message without crashing",
            actual_result="Page crashes with a 500 error",
            detected_in="UAT",
            detected_by="Manual testing"
        )
        """
        try:
            await ctx.info(f"Creating bug ticket in project: {project_key}")
        
            # Create bug ticket
            result = jira_service.create_bug_ticket(
                project_key=project_key,
                summary=summary,
                description=description,
                priority=priority,
                severity=severity,
                steps_to_reproduce=steps_to_reproduce,
                expected_result=expected_result,
                actual_result=actual_result,
                detected_by=detected_by,
                detected_in=detected_in
            )
        
            if result['status'] == 'success':
                await ctx.info(f"Successfully created bug ticket: {result['ticket_key']}")
            else:
                await ctx.error(f"Failed to create bug ticket: {result['message']}")
            
            return result
        except Exception as e:
            await ctx.error(f"Error creating bug ticket: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    @mcp.tool()
    async def get_current_sprint_status(
        board_id: str,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Get the status of the current (active) sprint for a specific board.
        
        Perfect for: Daily standups, current sprint progress tracking, real-time sprint monitoring
        Example: get_current_sprint_status("691")
        
        Args:
            board_id: The JIRA board ID to get current sprint status for
            
        Returns:
            Current sprint status including:
            - Sprint Name and Details
            - Story Points Breakdown by Status
            - Sprint Health Indicators
            - Recommendations
            - Key Achievements
            - Current Sprint Progress
        """
        try:
            result = jira_service.get_current_sprint_status(board_id)
            
            if result.get('status') == 'success':
                await ctx.info(f"✅ Retrieved current sprint status for board {board_id}")
            else:
                await ctx.error(f"❌ Failed to get current sprint status: {result.get('message')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting current sprint status: {str(e)}")
            await ctx.error(f"Error getting current sprint status: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    @mcp.tool()
    async def generate_sprint_report(
        board_id: Optional[str] = None,
        sprint_id: Optional[str] = None,
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive sprint reports with delivery, flow, and quality metrics.
        
        Perfect for: Sprint retrospectives, team performance analysis, stakeholder reporting, continuous improvement
        Example: generate_sprint_report(board_id="3411", start_date="2024-01-01", end_date="2024-03-31")
        Example: generate_sprint_report(sprint_id="56085")
        
        Args:
            board_id: The JIRA board ID to analyze sprints for (optional if sprint_id provided)
            sprint_id: The specific sprint ID to analyze (optional)
            start_date: Start date in YYYY-MM-DD format (optional, defaults to all sprints)
            end_date: End date in YYYY-MM-DD format (optional, defaults to all sprints)
            
        Returns:
            Comprehensive sprint metrics including:
            - Sprint Name
            - Story Points Breakdown by Status (excludes 0 SP stories)
            - Aging of tickets as per status
            - Incomplete High priority tickets flagged
            - Sprint Health Indicators
            - Recommendations
            - Sprint Success Summary
            - Key Achievement
            - Tech Categorization %
            - Bugs v/s Story & Task count
            - Production Bugs
        """
        try:
            if sprint_id:
                if ctx:
                    await ctx.info(f"Generating focused sprint report for specific sprint {sprint_id}")
            else:
                date_range = f"from {start_date or 'beginning'} to {end_date or 'present'}"
                if ctx:
                    await ctx.info(f"Generating focused sprint reports for board {board_id} {date_range}")
            
            result = jira_service.generate_sprint_report(board_id, sprint_id, start_date, end_date)
            
            if result['status'] == 'success':
                if sprint_id:
                    # Single sprint report - format the output
                    sprint_report = result.get('sprint_report', {})
                    formatted_report = _format_single_sprint_report(sprint_report)
                    
                    if ctx:
                        sprint_name = sprint_report.get('sprint_name', sprint_id)
                        completion_rate = sprint_report.get('sprint_success_summary', {}).get('completion_rate', 0)
                        await ctx.info(f"✅ Sprint report completed for {sprint_name}: {completion_rate}% completion rate")
                    
                    return {
                        'status': 'success',
                        'sprint_id': sprint_id,
                        'report_type': 'single_sprint',
                        'formatted_report': formatted_report,
                        'raw_data': sprint_report
                    }
                else:
                    # Board-level report
                    sprints_count = result.get('date_range', {}).get('sprints_analyzed', 0)
                    
                    if ctx:
                        await ctx.info(f"✅ Sprint reports completed: {sprints_count} sprints analyzed")
                    
                    return result
                
            else:
                if ctx:
                    await ctx.error(f"❌ Sprint report generation failed: {result.get('message', 'Unknown error')}")
                return result
                
        except Exception as e:
            error_msg = f"Error during sprint report generation: {str(e)}"
            logger.error(error_msg)
            if ctx:
                await ctx.error(error_msg)
            return {
                'status': 'error', 
                'message': error_msg,
                'board_id': board_id,
                'sprint_id': sprint_id
            }
    
    def _format_single_sprint_report(self, report_data: Dict[str, Any]) -> str:
        """Format a single sprint report into a readable string format."""
        if not report_data:
            return "No sprint data available."
        
        output = []
        
        # Sprint Name
        output.append(f"# 📊 Sprint Report: {report_data.get('sprint_name', 'Unknown Sprint')}")
        output.append("")
        
        # Story Points Breakdown by Status (excluding 0 SP stories)
        sp_breakdown = report_data.get('story_points_breakdown', {})
        output.append("## 🎯 Story Points Breakdown by Status")
        output.append("*(Excludes 0 story point items)*")
        output.append("")
        
        if sp_breakdown.get('total', 0) > 0:
            output.append(f"- **Total Story Points:** {sp_breakdown.get('total', 0)}")
            output.append(f"- **Done:** {sp_breakdown.get('done', 0)} ({round(sp_breakdown.get('done', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
            output.append(f"- **In Progress:** {sp_breakdown.get('in_progress', 0)} ({round(sp_breakdown.get('in_progress', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
            output.append(f"- **In Review:** {sp_breakdown.get('in_review', 0)} ({round(sp_breakdown.get('in_review', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
            output.append(f"- **In QA:** {sp_breakdown.get('in_qa', 0)} ({round(sp_breakdown.get('in_qa', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
            output.append(f"- **To Do:** {sp_breakdown.get('to_do', 0)} ({round(sp_breakdown.get('to_do', 0) / sp_breakdown.get('total', 1) * 100, 1)}%)")
        else:
            output.append("No story points found in this sprint.")
        output.append("")
        
        # Aging of tickets as per status
        aging = report_data.get('aging_of_tickets', {})
        output.append("## ⏰ Aging of Tickets by Status")
        output.append("")
        
        for status, age_buckets in aging.items():
            output.append(f"**{status}:**")
            for age_bucket, count in age_buckets.items():
                output.append(f"- {age_bucket}: {count} tickets")
            output.append("")
        
        # Incomplete High Priority Tickets
        high_priority = report_data.get('incomplete_high_priority_tickets', [])
        output.append("## 🚨 Incomplete High Priority Tickets")
        output.append("")
        
        if high_priority:
            output.append("**⚠️ ATTENTION REQUIRED:**")
            for ticket in high_priority:
                sp_text = f" ({ticket.get('story_points', 0)} SP)" if ticket.get('story_points', 0) > 0 else ""
                output.append(f"- **{ticket.get('key', '')}** - {ticket.get('summary', '')}")
                output.append(f"  - Priority: {ticket.get('priority', 'Unknown')}")
                output.append(f"  - Status: {ticket.get('status', 'Unknown')}")
                output.append(f"  - Assignee: {ticket.get('assignee', 'Unassigned')}{sp_text}")
                output.append("")
        else:
            output.append("✅ No incomplete high priority tickets.")
            output.append("")
        
        # Sprint Health Indicators
        health = report_data.get('sprint_health_indicators', {})
        output.append("## 📈 Sprint Health Indicators")
        output.append("")
        
        output.append(f"- **Completion Rate:** {health.get('completion_rate', 0)}%")
        output.append(f"- **Work in Progress Rate:** {health.get('work_in_progress_rate', 0)}%")
        output.append(f"- **High Priority Incomplete:** {health.get('high_priority_incomplete_count', 0)} items")
        output.append(f"- **Unassigned Work:** {health.get('unassigned_work_count', 0)} items")
        output.append(f"- **Bug Rate:** {health.get('bug_rate', 0)}%")
        output.append("")
        
        # Recommendations
        recommendations = report_data.get('recommendations', [])
        output.append("## 💡 Recommendations")
        output.append("")
        
        for rec in recommendations:
            output.append(f"- {rec}")
        output.append("")
        
        # Sprint Success Summary
        success = report_data.get('sprint_success_summary', {})
        output.append("## 🎯 Sprint Success Summary")
        output.append("")
        
        output.append(f"- **Success Level:** {success.get('success_level', 'Unknown')}")
        output.append(f"- **Completion Rate:** {success.get('completion_rate', 0)}%")
        output.append(f"- **Total Tickets:** {success.get('total_tickets', 0)}")
        output.append(f"- **Story Points Delivered:** {success.get('story_points_delivered', 0)}")
        output.append("")
        
        # Key Achievements
        achievements = report_data.get('key_achievements', [])
        output.append("## 🏆 Key Achievements")
        output.append("")
        
        if achievements:
            for achievement in achievements:
                output.append(f"- {achievement}")
        else:
            output.append("- No specific achievements highlighted for this sprint.")
        output.append("")
        
        # Tech Categorization %
        tech_cat = report_data.get('tech_categorization', {})
        output.append("## 🔧 Tech Categorization")
        output.append("")
        
        for category, data in tech_cat.items():
            count = data.get('count', 0)
            percentage = data.get('percentage', 0)
            output.append(f"- **{category}:** {count} tickets ({percentage}%)")
        output.append("")
        
        # Bugs vs Story & Task count
        bug_breakdown = report_data.get('bugs_vs_story_task_count', {})
        output.append("## 🐛 Work Type Distribution")
        output.append("")
        
        output.append(f"- **Bugs:** {bug_breakdown.get('bugs', 0)} ({bug_breakdown.get('bug_percentage', 0)}%)")
        output.append(f"- **Stories:** {bug_breakdown.get('stories', 0)}")
        output.append(f"- **Tasks:** {bug_breakdown.get('tasks', 0)}")
        output.append("")
        
        # Production Bugs
        prod_bugs = report_data.get('production_bugs', [])
        output.append("## 🚨 Production Bugs")
        output.append("")
        
        if prod_bugs:
            output.append("**High Priority Production Issues:**")
            for bug in prod_bugs:
                output.append(f"- **{bug.get('key', '')}** - {bug.get('summary', '')}")
                output.append(f"  - Priority: {bug.get('priority', 'Unknown')}")
                output.append(f"  - Status: {bug.get('status', 'Unknown')}")
                output.append(f"  - Assignee: {bug.get('assignee', 'Unassigned')}")
                output.append("")
        else:
            output.append("✅ No high priority production bugs identified.")
            output.append("")
        
        return "\n".join(output)
    