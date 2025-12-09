"""
Confluence MCP Server Package

This package provides a comprehensive set of tools for interacting with Confluence
through the Model Context Protocol (MCP). It includes:

- ConfluenceService: Core service for Confluence API interactions
- register_confluence_tools: Function to register all Confluence tools with FastMCP
- Document retrieval and markdown conversion tools
"""

from .service import ConfluenceService
from .tools import register_confluence_tools

__all__ = ['ConfluenceService', 'register_confluence_tools'] 