from fastmcp import FastMCP
import logging

# Import the refactored Confluence components
from confluence import ConfluenceService, register_confluence_tools

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create a server instance
mcp = FastMCP("Confluence MCP Server")

# Initialize Confluence service
confluence_service = ConfluenceService()

# Register all Confluence tools
register_confluence_tools(mcp, confluence_service)

if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport 