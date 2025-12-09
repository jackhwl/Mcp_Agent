from fastmcp import FastMCP
import logging

# Import the refactored TestRail components
from testrail import TestRailService, register_testrail_tools

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create a server instance
mcp = FastMCP("TestRail MCP Server")

# Initialize TestRail service
testrail_service = TestRailService()

# Register all TestRail tools
register_testrail_tools(mcp, testrail_service)

if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport