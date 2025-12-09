#!/usr/bin/env python3
"""
Bitbucket MCP Server

A Model Context Protocol (MCP) server for interacting with Bitbucket repositories,
pull requests, and other version control operations.

This server provides tools for:
- Retrieving pull request details and diffs
- Adding comments to pull requests
- Managing repository information
- Working with branches and commits
- Repository permissions and file operations
- Creating pull requests

Environment Variables:
- BITBUCKET_BASE_URL: Bitbucket server URL (default: http://wlstash.wenlin.net)
- BITBUCKET_AUTH_TOKEN: Authentication token for Bitbucket API
"""

import logging
import sys
from pathlib import Path

# Add the parent directory to Python path to allow imports
sys.path.append(str(Path(__file__).parent.parent))

from fastmcp import FastMCP
from bitbucket import register_bitbucket_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP("Bitbucket MCP Server")

# Register all Bitbucket tools
register_bitbucket_tools(mcp)

if __name__ == "__main__":
    logger.info("Starting Bitbucket MCP Server...")
    mcp.run() 