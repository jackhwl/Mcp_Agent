from fastmcp import FastMCP
import logging

# Import the refactored Jira components
from jira import JiraService, register_jira_tools

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create a server instance
mcp = FastMCP("Jira MCP Server")

# Initialize Jira service
jira_service = JiraService()

# Register all Jira tools
register_jira_tools(mcp, jira_service)

if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport