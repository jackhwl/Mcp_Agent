# Bitbucket Service Documentation

## 📋 Module Overview

**File**: `servers/bitbucket/service.py`  
**Purpose**: Core service layer for Bitbucket API integration  
**Dependencies**: `requests`  
**Lines of Code**: 428 lines  
**Authentication**: Bearer/Basic Token (Flexible)  

## 🏗️ Architecture

### Class Structure
```python
class BitbucketService:
    """Service class for interacting with Bitbucket Server API."""
```

### Configuration
```python
BITBUCKET_BASE_URL = "http://wlstash.wenlin.net"
BITBUCKET_AUTH_TOKEN = "auth-token-string"
```

## 🔧 Authentication & Session Management

### Flexible Authentication
```python
# Support both Bearer token and basic auth
if ':' in self.auth_token:  # Basic auth format
    auth_header = f"Basic {self.auth_token}"
else:  # Bearer token format
    auth_header = f"Bearer {self.auth_token}"
```

### Session Configuration
```python
self.session = requests.Session()
self.session.cookies.set('BITBUCKETSESSIONID', 'session_id')
```

### Protocol Management
- **HTTP/HTTPS Flexibility**: Dynamic protocol switching based on endpoint requirements
- **Session Persistence**: Maintains session state across requests
- **Cookie Management**: Handles Bitbucket session cookies

## 🚀 Core Operations

### 1. Pull Request Management

#### `parse_pr_link(pr_link)`
**Purpose**: Extract workspace, repository, and PR ID from URLs  
**Supported Patterns**:
- `/projects/{workspace}/repos/{repo}/pull-requests/{id}`
- `/projects/{workspace}/repos/{repo}/pull-request/{id}` (legacy)

**URL Processing**:
1. **Cleanup**: Removes `/overview` suffix if present
2. **Pattern Matching**: Supports multiple URL formats
3. **Extraction**: Returns workspace, repo_slug, pr_id tuple
4. **Validation**: Comprehensive error handling for malformed URLs

#### `fetch_pr_details(workspace, repo_slug, pr_id)`
**Purpose**: Retrieve comprehensive PR information including diff  
**API Endpoints**:
- **PR Details**: `/rest/api/1.0/projects/{workspace}/repos/{repo}/pull-requests/{pr_id}`
- **Diff Content**: `/rest/api/1.0/projects/{workspace}/repos/{repo}/pull-requests/{pr_id}.diff`

**Protocol Strategy**:
- **HTTP for PR Details**: Uses HTTP base URL for API calls
- **Header Management**: Different headers for JSON vs plain text responses
- **Content Types**: Handles both JSON (PR data) and plain text (diff)

**Data Mapping**:
```python
def _map_pr_data(self, pr_data):
    """Map complex Bitbucket PR data to simplified format"""
    # Extracts essential PR information
    # Handles nested JSON structures
    # Provides safe field access
```

#### `add_comment(workspace, repo_slug, pr_id, comment_data)`
**Purpose**: Add comments to pull requests  
**API Endpoint**: `/rest/api/1.0/projects/{workspace}/repos/{repo}/pull-requests/{pr_id}/comments`  
**Method**: POST  

**Comment Features**:
- **Rich Text Support**: Handles formatted comments
- **Thread Management**: Supports comment threading
- **User Attribution**: Automatic user attribution based on authentication

### 2. Repository Operations

#### `get_repository_info(workspace, repo_slug)`
**Purpose**: Retrieve repository metadata and configuration  
**API Endpoint**: `/rest/api/1.0/projects/{workspace}/repos/{repo}`  
**Method**: GET  

**Repository Information**:
- **Basic Metadata**: Name, description, visibility
- **Clone URLs**: HTTP and SSH clone endpoints
- **Project Context**: Parent project information
- **Configuration**: Repository settings and permissions

#### `get_branches(workspace, repo_slug, filter_text)`
**Purpose**: List repository branches with optional filtering  
**API Endpoint**: `/rest/api/1.0/projects/{workspace}/repos/{repo}/branches`  
**Method**: GET  

**Branch Features**:
- **Filter Support**: Text-based branch name filtering
- **Metadata**: Branch information including latest commit
- **Pagination**: Handles large branch lists
- **Active Branches**: Identifies active development branches

#### `get_file_content(workspace, repo_slug, path, ref)`
**Purpose**: Retrieve file content from repository  
**Features**:
- **Path Navigation**: Support for nested file paths
- **Reference Support**: Specific commit, branch, or tag references
- **Content Types**: Handles various file types and encodings
- **Large File Handling**: Efficient processing of large files

### 3. Code Review & Analysis

#### `get_reviewed_prs(workspaces, repo_slugs, username, state, limit)`
**Purpose**: Find PRs reviewed by specific users across repositories  
**API Query Parameters**:
```python
params = {
    'limit': limit,
    'state': state,           # ALL, OPEN, MERGED, DECLINED
    'role.1': 'REVIEWER',
    'username.1': username
}
```

**Multi-Repository Support**:
- **Batch Processing**: Queries multiple repositories simultaneously
- **Result Aggregation**: Combines results across workspaces/repos
- **User Filtering**: Filters by reviewer participation
- **State Management**: Supports various PR states

#### `get_pr_activities(workspace, repo_slug, pr_id)`
**Purpose**: Retrieve PR activity timeline and comments  
**Activity Types**:
- **Comments**: Review comments and discussions
- **Approvals**: Approval/rejection events
- **Updates**: PR updates and changes
- **Commits**: Associated commit activity

### 4. Advanced Features

#### `create_pull_request(workspace, repo_slug, source_branch, target_branch, title, description, reviewers)`
**Purpose**: Create new pull requests programmatically  
**API Endpoint**: `/rest/api/1.0/projects/{workspace}/repos/{repo}/pull-requests`  
**Method**: POST  

**PR Creation Features**:
- **Branch Validation**: Ensures source and target branches exist
- **Reviewer Assignment**: Automatic reviewer assignment
- **Template Support**: Description templates and formatting
- **Validation**: Pre-creation validation checks

#### `get_commit_details(workspace, repo_slug, commit_id)`
**Purpose**: Retrieve detailed commit information  
**Commit Details**:
- **Metadata**: Author, date, message
- **Changes**: File changes and statistics
- **Parents**: Parent commit relationships
- **Diff Information**: Detailed change information

#### `parse_jira_id(title)`
**Purpose**: Extract JIRA ticket IDs from PR titles  
**Pattern Recognition**:
- **Standard Format**: PROJECT-123
- **Case Insensitive**: Handles various cases
- **Multiple Patterns**: Supports different JIRA key formats
- **Validation**: Ensures valid JIRA key structure

## 🔍 Technical Implementation Details

### URL Management
```python
def _get_base_url(self, use_https: bool = True) -> str:
    """Get the appropriate base URL based on the required scheme."""
    # Dynamic protocol switching
    # Maintains compatibility with different endpoints
```

### Error Handling Strategy
```python
try:
    response = self.session.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"Error: {str(e)}")
    return None
```

### Session Management
- **Persistent Sessions**: Maintains session state
- **Cookie Handling**: Automatic cookie management
- **Connection Pooling**: Efficient connection reuse
- **Timeout Management**: Configurable request timeouts

## 📊 Integration Patterns

### JIRA Integration
```python
def parse_jira_id(self, title: str) -> Optional[str]:
    """Extract JIRA ticket ID from PR title"""
    # Regex pattern matching for JIRA keys
    # Supports PROJECT-123 format
    # Case-insensitive matching
```

### Cross-Service Workflows
1. **PR Review Process**:
   - PR created → Extract JIRA ID → Link to ticket
   - Comments added → Update JIRA ticket
   - PR merged → Close review task

2. **Documentation Updates**:
   - Code changes → Identify affected documentation
   - Auto-generate Confluence updates
   - Link PR to documentation pages

### Data Mapping Strategy
The service includes sophisticated data mapping for complex Bitbucket responses:

```python
def _map_pr_data(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
    """Map Bitbucket PR data to simplified format"""
    # Handles nested JSON structures
    # Provides safe field access
    # Standardizes response format
```

## 🛠️ API Endpoint Coverage

### Core Bitbucket Server REST API v1.0 Endpoints
| Endpoint | Method | Purpose | Implementation |
|----------|--------|---------|----------------|
| `/rest/api/1.0/projects/{workspace}/repos/{repo}/pull-requests/{id}` | GET | Get PR details | `fetch_pr_details()` |
| `/rest/api/1.0/projects/{workspace}/repos/{repo}/pull-requests/{id}.diff` | GET | Get PR diff | `fetch_pr_details()` |
| `/rest/api/1.0/projects/{workspace}/repos/{repo}/pull-requests` | GET/POST | List/Create PRs | `get_reviewed_prs()`, `create_pull_request()` |
| `/rest/api/1.0/projects/{workspace}/repos/{repo}` | GET | Get repo info | `get_repository_info()` |
| `/rest/api/1.0/projects/{workspace}/repos/{repo}/branches` | GET | List branches | `get_branches()` |
| `/rest/api/1.0/projects/{workspace}/repos/{repo}/commits/{id}` | GET | Get commit | `get_commit_details()` |

### Protocol Considerations
- **HTTP vs HTTPS**: Dynamic switching based on endpoint requirements
- **Content Types**: Handles JSON and plain text responses
- **Authentication**: Flexible token-based authentication
- **Session Management**: Persistent session handling

## 🔄 Workflow Examples

### Code Review Automation
1. **PR Detection** → Monitor for new PRs
2. **JIRA Extraction** → Parse ticket ID from title
3. **Review Assignment** → Auto-assign reviewers
4. **Status Tracking** → Monitor review progress
5. **Completion Actions** → Update tickets, merge branches

### Repository Management
1. **Branch Discovery** → List active branches
2. **Commit Analysis** → Analyze commit patterns
3. **File Monitoring** → Track file changes
4. **Merge Management** → Handle merge conflicts

### Integration Workflows
1. **Cross-Service Linking** → Connect PRs to JIRA tickets
2. **Documentation Updates** → Link code changes to docs
3. **Automated Testing** → Trigger CI/CD pipelines
4. **Notification Management** → Send status updates

## 🔧 Configuration & Customization

### Environment Variables
```bash
BITBUCKET_BASE_URL=http://wlstash.wenlin.net
BITBUCKET_AUTH_TOKEN=your-auth-token
```

### Session Configuration
```python
# Custom session settings
self.session.cookies.set('BITBUCKETSESSIONID', 'session_id')
self.session.timeout = 30  # Request timeout
```

### Authentication Flexibility
The service supports multiple authentication methods:
- **Bearer Tokens**: Standard OAuth-style tokens
- **Basic Authentication**: Username:password base64 encoded
- **Session Cookies**: Persistent session management

### URL Pattern Configuration
Supports multiple Bitbucket URL patterns for compatibility:
- **Standard**: `/projects/{workspace}/repos/{repo}/pull-requests/{id}`
- **Legacy**: `/projects/{workspace}/repos/{repo}/pull-request/{id}`
- **Custom**: Configurable URL patterns for different Bitbucket versions

This service provides comprehensive Bitbucket Server integration with support for pull request workflows, repository management, and cross-service automation capabilities. 