from fastmcp import FastMCP
import logging

# Import the refactored Asana components
from asana import AsanaService, register_asana_tools

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create a server instance
mcp = FastMCP("Asana MCP Server")

# Initialize Asana service
asana_service = AsanaService()

# Register all Asana tools
register_asana_tools(mcp, asana_service)

if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport
