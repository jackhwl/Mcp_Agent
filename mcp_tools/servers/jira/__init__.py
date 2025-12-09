"""
Jira MCP Server Package

This package provides a comprehensive set of tools for interacting with Jira
through the Model Context Protocol (MCP). It includes:

- JiraService: Core service for Jira API interactions
- register_jira_tools: Function to register all Jira tools with FastMCP
- Specialized tools for product manager workflows
"""

from .service import JiraService
from .tools import register_jira_tools

__all__ = ['JiraService', 'register_jira_tools'] 