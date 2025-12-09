"""
Testrail MCP Server Package

This package provides a comprehensive set of tools for interacting with TestRail
through the Model Context Protocol (MCP). It includes:

- TestRailService: Core service for TestRail API interactions
- register_testrail_tools: Function to register all TestRail tools with FastMCP
- Specialized tools for product manager workflows
"""

from .service import TestRailService
from .tools import register_testrail_tools

__all__ = ['TestRailService', 'register_testrail_tools'] 