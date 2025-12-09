# JIRA, Bitbucket, Confluence, Asana & TestRail MCP Servers

Comprehensive Model Context Protocol (MCP) servers that provide seamless JIRA, Bitbucket, Confluence, Asana, and TestRail integration for VSCode and Cursor IDEs. Access JIRA tickets, projects, sprints, analytics, Bitbucket pull requests, repositories, code reviews, Confluence documentation, Asana tasks, projects, portfolios, and TestRail test management directly from your development environment.

## 🚀 Quick Start

### **Automated Setup (Recommended)**

Choose your platform and run the one-click setup:

#### Windows (PowerShell)
```powershell
git clone https://wlstash.wenlin.net/scm/ingn/mcp-server-library.git
cd mcp-server-library
.\setup.ps1
```

#### Windows (Batch)
```batch
git clone https://wlstash.wenlin.net/scm/ingn/mcp-server-library.git
cd mcp-server-library
.\setup.bat
```

#### macOS/Linux (Bash)
```bash
git clone https://wlstash.wenlin.net/scm/ingn/mcp-server-library.git
cd mcp-server-library
chmod +x setup.sh
./setup.sh
```

### **What the Setup Does**
- ✅ Verifies Python 3.8+ installation
- ✅ Creates and activates virtual environment
- ✅ Installs all dependencies from `requirements.txt`
- ✅ Configures JIRA, Bitbucket, Confluence, Asana, and TestRail MCP servers in VSCode/Cursor settings
- ✅ Provides clear next steps for authentication

---

## 🛠️ Available Tools

### **JIRA Tools**

#### **Configuration & Health**
- **`healthcheck`** - Verify JIRA setup and configuration status
- **`test_connection`** - Test JIRA authentication and connectivity

#### **Ticket Management**
- **`get_ticket_details`** - Get comprehensive ticket information
- **`create_review_task`** - Create code review tasks
- **`create_user_story`** - Create user stories with Agile templates

#### **Project Analytics**
- **`get_my_active_work`** - View your assigned tickets
- **`get_sprint_burndown`** - Sprint progress and burndown charts
- **`get_high_priority_blockers`** - Find critical blocking issues
- **`get_weekly_delivery_report`** - Weekly delivery metrics
- **`get_bug_health_report`** - Bug statistics and health metrics
- **`get_overdue_items`** - Find overdue tickets

#### **Team Management**
- **`get_unassigned_work`** - Find unassigned project tickets
- **`get_team_workload`** - Analyze team member workloads
- **`get_recent_activity`** - Recent project activity

#### **Release Management**
- **`get_feature_progress`** - Track feature development progress
- **`get_release_readiness`** - Assess release readiness status

#### **Search & Discovery**
- **`search_jira_custom`** - Execute custom JQL queries
- **`get_user_projects`** - List user-accessible projects
- **`get_projects`** - Search and discover projects

### **Bitbucket Tools**

#### **Pull Request Management**
- **`get_pr_details`** - Get comprehensive PR information and diffs
- **`add_pr_comment`** - Add comments to pull requests (general or line-specific)
- **`get_reviewed_prs`** - Get PRs reviewed by a specific user
- **`get_pr_activities`** - Get PR activities and comment history
- **`create_pull_request`** - Create new pull requests

#### **Repository Management**
- **`get_repository_info`** - Get detailed repository information
- **`get_repository_branches`** - List and filter repository branches
- **`get_file_content`** - Get content of specific files
- **`get_repo_permissions`** - Get repository user permissions

#### **Code & Commit Management**
- **`get_commit_details`** - Get detailed commit information
- **`bitbucket_healthcheck`** - Verify Bitbucket connectivity and setup

### **Confluence Tools**

#### **Configuration & Health**
- **`confluence_healthcheck`** - Verify Confluence setup and configuration status

#### **Documentation Retrieval**
- **`get_confluence_pages`** - Fetch pages by IDs or space key, converted to markdown
- **`get_confluence_page_by_title`** - Get specific page by title within a space
- **`get_space_documentation`** - Get comprehensive documentation from a space

#### **Search & Discovery**
- **`search_confluence`** - Search pages using text queries with CQL
- **`get_confluence_spaces`** - List all accessible Confluence spaces

### **Asana Tools**

#### **Configuration & Health**
- **`asana_healthcheck`** - Verify Asana setup and configuration status

#### **Workspace & Project Management**
- **`get_asana_workspaces`** - Get all accessible Asana workspaces
- **`get_asana_projects`** - Get projects from a specific workspace
- **`get_asana_project_details`** - Get detailed project information including custom fields

#### **Task Management**
- **`get_asana_tasks`** - Get tasks with optional filtering by project or assignee
- **`get_asana_task_details`** - Get detailed task information including subtasks and dependencies
- **`create_asana_task`** - Create new tasks with assignments and due dates
- **`update_asana_task`** - Update existing tasks (completion, assignments, due dates)
- **`search_asana_tasks`** - Search for tasks using text queries

#### **Portfolio Management**
- **`get_asana_portfolios`** - Get portfolios from a workspace
- **`get_asana_portfolio_details`** - Get detailed portfolio information
- **`get_asana_portfolio_items`** - Get projects within a specific portfolio

#### **User Management**
- **`get_asana_user_info`** - Get information about the authenticated user

### **TestRail Tools**

#### **Configuration & Health**
- **`testrail_healthcheck`** - Verify TestRail setup and configuration status

#### **Project Management**
- **`get_project`** - Get detailed information about a specific project
- **`get_projects_from_testrail`** - Get all accessible projects with search filtering
- **`add_project`** - Create new TestRail projects with configuration
- **`update_project`** - Update existing project details and settings
- **`delete_project`** - Delete projects when no longer needed

#### **Test Case Management**
- **`get_case`** - Get detailed information about a specific test case
- **`get_cases`** - Get test cases with filtering by project, reference, or search terms
- **`add_case`** - Create new test cases with structured steps and expectations
- **`update_case`** - Update existing test cases with new information
- **`delete_case`** - Delete test cases that are no longer relevant
- **`get_labels`** - Get available labels for categorizing test cases

#### **Section Management**
- **`get_section`** - Get detailed information about a specific section
- **`get_sections`** - Get all sections within a project for organization
- **`add_section`** - Create new sections to organize test cases
- **`update_section`** - Update section names and descriptions
- **`delete_section`** - Delete sections (with soft delete option)
- **`move_section`** - Move sections to different parents or positions

#### **Test Run Management**
- **`get_run`** - Get detailed information about a specific test run
- **`get_runs`** - Get test runs with filtering by project and status
- **`add_run`** - Create new test runs for executing test cases
- **`update_run`** - Update test run configurations and assignments
- **`close_run`** - Close test runs to finalize execution
- **`delete_run`** - Delete test runs when no longer needed

#### **Test Result Management**
- **`get_results`** - Get all results for a specific test case
- **`get_results_for_run`** - Get all results associated with a test run
- **`add_result`** - Add execution results for individual test cases
- **`add_results_for_cases`** - Submit results for multiple test cases in a run

#### **Test Data Management**
- **`get_dataset`** - Get detailed information about a specific dataset
- **`get_datasets`** - Get all datasets available in a project
- **`add_dataset`** - Create new datasets for data-driven testing
- **`update_dataset`** - Update existing dataset information
- **`delete_dataset`** - Delete datasets that are no longer needed

---

## 🔐 Authentication Setup

### **Step 1: Get API Tokens**

#### **JIRA API Token**
1. Go to your JIRA instance
2. Profile → Account Settings → Security
3. Create and manage API tokens → Create API token
4. Save the token securely

#### **Bitbucket Authentication Token**
1. Go to your Bitbucket instance
2. Account Settings → Personal Access Tokens
3. Create new token with appropriate permissions
4. Save the token securely

#### **Confluence Authentication Token**
1. Go to your Confluence instance
2. Account Settings → Personal Access Tokens (or API Tokens)
3. Create new token with appropriate permissions
4. Save both username and API key securely

#### **Asana Personal Access Token**
1. Go to Asana (https://app.asana.com)
2. Profile Settings → Apps → View developer console → Personal Access Token
3. Create new Personal Access Token
4. Copy and save the token securely (you won't see it again)

#### **TestRail API Key**
1. Go to your TestRail instance
2. My Settings → API Keys
3. Generate a new API key or use existing one
4. Save both username and API key securely

### **Step 2: Configure Authentication**

After running the setup script, update your authentication:

1. Open VSCode/Cursor
2. `Ctrl+Shift+P` → "Open User Settings (JSON)"
3. Update the MCP configuration:

```json
{
  "mcp": {
    "servers": {
      "jira-mcp-server": {
        "type": "stdio",
        "command": "/path/to/.venv/Scripts/python.exe",
        "args": ["/path/to/servers/jira_mcp_server.py"],
        "env": {
          "JIRA_AUTH_TOKEN": "your-secure-auth-token",
          "JIRA_BASE_URL": "https://wljira.wenlin.net"
        }
      },
      "bitbucket-mcp-server": {
        "type": "stdio",
        "command": "/path/to/.venv/Scripts/python.exe",
        "args": ["/path/to/servers/bitbucket_server.py"],
        "env": {
          "BITBUCKET_AUTH_TOKEN": "your-bitbucket-token-here",
          "BITBUCKET_BASE_URL": "http://wlstash.wenlin.net"
        }
      },
      "confluence-mcp-server": {
        "type": "stdio",
        "command": "/path/to/.venv/Scripts/python.exe",
        "args": ["/path/to/servers/confluence_server.py"],
        "env": {
          "CONFLUENCE_USERNAME": "your-confluence-username",
          "CONFLUENCE_API_KEY": "your-confluence-api-key",
          "CONFLUENCE_BASE_URL": "https://wlwiki.wenlin.net/"
        }
      },
      "asana-mcp-server": {
        "type": "stdio",
        "command": "/path/to/.venv/Scripts/python.exe",
        "args": ["/path/to/servers/asana_server.py"],
        "env": {
          "ASANA_AUTH_TOKEN": "your-asana-personal-access-token",
          "ASANA_BASE_URL": "https://app.asana.com/api/1.0",
          "ASANA_DISABLE_SSL_VERIFY": "false"
        }
      },
      "testrail-mcp-server": {
        "type": "stdio",
        "command": "/path/to/.venv/Scripts/python.exe",
        "args": ["/path/to/servers/testrail_mcp_server.py"],
        "env": {
          "TESTRAIL_URL": "https://your-testrail-instance.testrail.io",
          "TESTRAIL_USERNAME": "your-testrail-username",
          "TESTRAIL_API_KEY": "your-testrail-api-key"
        }
      }
    }
  }
}
```

### **Step 3: Verify Setup**
1. Restart VSCode/Cursor
2. Run the `healthcheck` tool (JIRA)
3. Run the `test_connection` tool (JIRA)
4. Run the `bitbucket_healthcheck` tool (Bitbucket)
5. Run the `confluence_healthcheck` tool (Confluence)
6. Run the `asana_healthcheck` tool (Asana)
7. Run the `testrail_healthcheck` tool (TestRail)

---

## 📖 Usage Examples

### **Daily Workflow**
```
JIRA:
1. get_my_active_work - See your current tickets
2. get_sprint_burndown - Check sprint progress
3. get_high_priority_blockers - Identify urgent issues

Bitbucket:
1. get_reviewed_prs - Check PRs you need to review
2. get_pr_details - Review specific PR changes
3. add_pr_comment - Provide feedback on code

Confluence:
1. confluence_healthcheck - Verify setup
2. get_confluence_spaces - Discover available spaces
3. search_confluence - Find specific documentation
4. get_confluence_pages - Retrieve documentation content

Asana:
1. asana_healthcheck - Verify setup
2. get_asana_workspaces - View available workspaces
3. get_asana_tasks - See your assigned tasks
4. get_asana_projects - View project status

TestRail:
1. testrail_healthcheck - Verify setup
2. get_projects_from_testrail - View available projects
3. get_cases - See test cases for a project
4. get_runs - Check test execution status
```

### **Code Review Process**
```
JIRA - Create Review Task:
- parent_key: "PROJ-123"
- title: "Code Review: Feature Implementation"
- description: "Review OAuth2 integration changes"

Bitbucket - Review Process:
- get_pr_details: Get PR info and diff
- add_pr_comment: Provide feedback
- get_pr_activities: Check discussion history
```

### **Repository Management**
```
Bitbucket:
- get_repository_info: Get repo details
- get_repository_branches: List all branches
- get_file_content: Review specific files
- create_pull_request: Create new PRs
```

### **Custom Searches**
```
JIRA:
search_jira_custom:
- jql_query: "project = PROJ AND assignee = currentUser() AND status = 'In Progress'"

Bitbucket:
get_reviewed_prs:
- workspaces: ["PROJ"]
- repo_slugs: ["main-repo"]
- username: "your-username"
```

### **Documentation Workflow**
```
Confluence:
1. confluence_healthcheck - Verify setup
2. get_confluence_spaces - Discover available spaces
3. search_confluence - Find specific documentation
4. get_confluence_pages - Retrieve documentation content
```

### **Task Management Workflow**
```
Asana:
1. asana_healthcheck - Verify setup
2. get_asana_workspaces - Discover workspaces
3. get_asana_projects - View project structure
4. get_asana_tasks - Review assigned tasks
5. create_asana_task - Create new work items
6. update_asana_task - Update task status and assignments
```

### **Project & Portfolio Management**
```
Asana:
- get_asana_portfolios: Get high-level portfolio view
- get_asana_portfolio_items: See projects within portfolios
- get_asana_project_details: Get detailed project information
- search_asana_tasks: Find specific tasks across projects
```

### **Test Management Workflow**
```
TestRail:
1. testrail_healthcheck - Verify setup
2. get_projects_from_testrail - Discover test projects
3. get_cases - Review test cases for a project
4. add_run - Create new test execution runs
5. add_results_for_cases - Record test execution results
6. get_runs - Monitor test execution progress
```

### **Quality Assurance Process**
```
TestRail:
- get_cases: Review existing test cases
- add_case: Create new test cases with structured steps
- add_run: Start test execution cycles
- add_result: Record individual test outcomes
- get_results_for_run: Analyze execution results
```
```
Confluence:
- get_space_documentation: Get all docs from a project space
- search_confluence: Find documentation across spaces
- get_confluence_page_by_title: Retrieve specific pages

Asana:
- get_asana_user_info: Get current user information
- search_asana_tasks: Search for tasks by keyword
- get_asana_task_details: Get comprehensive task information

TestRail:
- get_projects_from_testrail: Discover test management projects
- get_cases: Find and review test cases
- add_run: Create test execution cycles
- get_results_for_run: Analyze test execution outcomes
```

---

## ⚙️ Manual Setup (Alternative)

If you prefer manual setup or need to troubleshoot:

### **Prerequisites**
- Python 3.8 or higher
- VSCode or Cursor IDE
- JIRA instance access
- Bitbucket instance access
- Confluence instance access (optional)
- Asana account access (optional)
- TestRail instance access (optional)

### **Manual Installation**
```bash
# 1. Clone repository
git clone https://wlstash.wenlin.net/scm/ingn/mcp-server-library.git
cd mcp-server-library

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure MCP servers
python configure_mcp.py
```

---

## 🔧 Troubleshooting

### **Common Issues**

**"Authentication failed"**
- Verify your API tokens are correct and not expired
- Check VSCode settings JSON syntax
- Run `healthcheck`, `bitbucket_healthcheck`, `confluence_healthcheck`, `asana_healthcheck`, and `testrail_healthcheck` for detailed guidance

**"Python not found"**
- Install Python 3.8+ from https://python.org
- Ensure Python is in your system PATH

**"Setup script fails"**
- Run PowerShell as Administrator (Windows)
- Check internet connection for dependency downloads
- Verify write permissions in project directory

**"Server not found"**
- Check your base URLs are correct
- Verify network connectivity to JIRA/Bitbucket instances
- Ensure firewall/proxy settings allow connections

### **Getting Help**
1. Run `healthcheck` tool for JIRA configuration status
2. Run `bitbucket_healthcheck` tool for Bitbucket configuration status
3. Run `confluence_healthcheck` tool for Confluence configuration status
4. Run `asana_healthcheck` tool for Asana configuration status
5. Run `testrail_healthcheck` tool for TestRail configuration status
6. Run `test_connection` to verify JIRA authentication
7. Check console output for error details

---

## 📁 Project Structure

```
mcp-server-library/
├── servers/
│   ├── jira/
│   │   ├── __init__.py             # JIRA module initialization
│   │   ├── tools.py                # All JIRA tools (19 tools)
│   │   └── service.py              # JIRA API service layer
│   ├── bitbucket/
│   │   ├── __init__.py             # Bitbucket module initialization
│   │   ├── tools.py                # All Bitbucket tools (11 tools)
│   │   └── service.py              # Bitbucket API service layer
│   ├── confluence/
│   │   ├── __init__.py             # Confluence module initialization
│   │   ├── tools.py                # All Confluence tools (6 tools)
│   │   └── service.py              # Confluence API service layer
│   ├── asana/
│   │   ├── __init__.py             # Asana module initialization
│   │   ├── tools.py                # All Asana tools (13 tools)
│   │   └── service.py              # Asana API service layer
│   ├── testrail/
│   │   ├── __init__.py             # TestRail module initialization
│   │   ├── tools.py                # All TestRail tools (33 tools)
│   │   └── service.py              # TestRail API service layer
│   ├── jira_mcp_server.py          # Main JIRA MCP server
│   ├── bitbucket_server.py         # Main Bitbucket MCP server
│   ├── confluence_server.py        # Main Confluence MCP server
│   ├── asana_server.py             # Main Asana MCP server
│   └── testrail_mcp_server.py      # Main TestRail MCP server
├── setup.ps1                       # Windows PowerShell setup
├── setup.bat                       # Windows Batch setup  
├── setup.sh                        # macOS/Linux Bash setup
├── configure_mcp.py                # MCP configuration script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔄 Platform Support

| Platform | Setup Script | Status |
|----------|--------------|--------|
| Windows  | `setup.ps1`  | ✅ Full Support |
| Windows  | `setup.bat`  | ✅ Full Support |
| macOS    | `setup.sh`   | ✅ Full Support |
| Linux    | `setup.sh`   | ✅ Full Support |

---

## 📦 Dependencies

- **fastmcp** - MCP framework
- **requests** - HTTP client for JIRA/Bitbucket APIs
- **python-dotenv** - Environment management
- **langchain-community** - Confluence document loading
- **html2text** - HTML to markdown conversion
- **atlassian-python-api** - Atlassian API client
- **pytest** - Testing framework (dev)
- **black** - Code formatting (dev)
- **flake8** - Code linting (dev)

---

## 🚀 Getting Started Checklist

- [ ] Run platform-specific setup script
- [ ] Generate JIRA API token
- [ ] Generate Bitbucket authentication token
- [ ] Generate Confluence API key (optional)
- [ ] Generate Asana Personal Access Token (optional)
- [ ] Generate TestRail API key (optional)
- [ ] Update tokens in VSCode settings
- [ ] Update usernames and URLs in settings
- [ ] Restart IDE
- [ ] Run `healthcheck` tool (JIRA)
- [ ] Run `bitbucket_healthcheck` tool (Bitbucket)
- [ ] Run `confluence_healthcheck` tool (Confluence)
- [ ] Run `asana_healthcheck` tool (Asana)
- [ ] Run `testrail_healthcheck` tool (TestRail)
- [ ] Run `test_connection` tool (JIRA)
- [ ] Try `get_my_active_work` (JIRA)
- [ ] Try `get_pr_details` with a sample PR URL (Bitbucket)
- [ ] Try `get_confluence_spaces` (Confluence)
- [ ] Try `get_asana_workspaces` (Asana)
- [ ] Try `get_projects_from_testrail` (TestRail)
- [ ] Explore other tools

---

## 📝 Advanced Features

### **Custom JQL Queries (JIRA)**
Use `search_jira_custom` with powerful JQL:
```jql
project = PROJ AND type = Bug AND assignee = currentUser() AND sprint in openSprints()
```

### **Pull Request Automation (Bitbucket)**
Streamline code review workflows:
- **PR Review**: `get_pr_details` + `add_pr_comment` + `get_pr_activities`
- **Repository Management**: `get_repository_info` + `get_repository_branches`
- **Team Coordination**: `get_reviewed_prs` across multiple repos

### **Workflow Integration**
Combine JIRA, Bitbucket, Confluence, Asana, and TestRail tools for powerful workflows:
- **Feature Development**: Create JIRA tasks → Review Bitbucket PRs → Update Asana project status → Execute TestRail test cases
- **Bug Tracking**: Track JIRA bugs → Review related PR fixes → Create Asana follow-up tasks → Run TestRail regression tests
- **Release Management**: JIRA release planning → Bitbucket branch management → Asana milestone tracking → TestRail release testing
- **Documentation**: Confluence documentation → JIRA requirement tickets → Asana task assignments → TestRail test case creation
- **Quality Assurance**: TestRail test planning → JIRA defect tracking → Bitbucket code fixes → Asana project updates

### **Documentation Management**
```
Confluence:
- get_confluence_spaces - Discover documentation areas
- search_confluence - Find specific documentation
- get_space_documentation - Get comprehensive project docs
- get_confluence_pages - Retrieve formatted documentation
```

*For comprehensive documentation with detailed examples, see the full wiki documentation.*
- https://wlwiki.wenlin.net/spaces/AIO/pages/1363580155/MCP+Library#config-tabs--1239742614