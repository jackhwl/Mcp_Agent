# JIRA Service Documentation

## 📋 Module Overview

**File**: `servers/jira/service.py`  
**Purpose**: Core service layer for JIRA API integration  
**Dependencies**: `requests`  
**Lines of Code**: 313 lines  
**Authentication**: Bearer Token  

## 🏗️ Architecture

### Class Structure
```python
class JiraService:
    """Service class for interacting with Jira API."""
```

### Configuration
```python
JIRA_BASE_URL = "https://wljira.wenlin.net"
JIRA_AUTH_TOKEN = "bearer-token-string"
```

## 🔧 Authentication & Headers

### Bearer Token Authentication
```python
headers = {
    'Authorization': f'Bearer {self.auth_token}',
    'Content-Type': 'application/json'
}
```

### Security Model
- **Token-Based**: Uses Bearer token for all API calls
- **Environment-Driven**: Credentials loaded from environment variables
- **Header Management**: Consistent authorization headers across requests

## 🚀 Core Operations

### 1. Ticket Management

#### `get_ticket_details(ticket_key)`
**Purpose**: Retrieve comprehensive ticket information  
**API Endpoint**: `/rest/api/2/issue/{ticket_key}`  
**Method**: GET  

**Extracted Fields**:
- **Basic Info**: Key, project ID/key, issue type, summary, description
- **Status Management**: Current status, priority level
- **Assignment**: Assignee information
- **Project Structure**: Components and categorization

**Return Structure**:
```python
{
    'key': 'PROJ-123',
    'project_id': '10001',
    'project_key': 'PROJ',
    'issue_type': 'Story',
    'summary': 'Ticket Summary',
    'description': 'Detailed description...',
    'status': 'In Progress',
    'priority': 'High',
    'assignee': 'john.doe',
    'components': ['Frontend', 'API']
}
```

#### `create_review_task(parent_details, review_data)`
**Purpose**: Create subtasks for code review implementation  
**API Endpoint**: `/rest/api/2/issue`  
**Method**: POST  

**Subtask Creation Process**:
1. **Parent Validation**: Ensures parent ticket exists and is accessible
2. **Project Context**: Inherits project settings from parent
3. **Subtask Configuration**: Sets issue type to subtask (ID: "5")
4. **Content Mapping**: Maps review data to JIRA fields

**Payload Structure**:
```python
{
    "fields": {
        "project": {"id": parent_details['project_id']},
        "parent": {"key": parent_details['key']},
        "summary": "Code Review Implementation Task",
        "description": "Implementation of code review suggestions",
        "issuetype": {"id": "5"}  # Subtask
    }
}
```

### 2. Search & Query Operations

#### `search_jira_issues(query, max_results)`
**Purpose**: Execute JQL (JIRA Query Language) searches  
**API Endpoint**: `/rest/api/2/search`  
**Method**: GET  

**Search Features**:
- **JQL Support**: Full JIRA Query Language capabilities
- **Result Limiting**: Configurable maximum results (default: 50)
- **Field Selection**: Optimized field retrieval for performance
- **Safe Field Access**: Handles missing or null fields gracefully

**Query Parameters**:
```python
params = {
    'jql': query,
    'maxResults': max_results,
    'fields': 'key,summary,status,issuetype,priority,assignee,created,updated'
}
```

**Result Processing**:
- **Total Count**: Number of matching issues
- **Issue Array**: Detailed information for each result
- **Metadata Extraction**: Safe handling of optional fields
- **Error Handling**: Graceful degradation for API failures

### 3. User Story Creation

#### `create_user_story(story_data)`
**Purpose**: Create user stories with custom product management fields  
**API Endpoint**: `/rest/api/2/issue`  
**Method**: POST  

**Custom Field Mapping**:
```python
custom_fields = {
    'asAn': 'customfield_25354',        # User role
    'when': 'customfield_26560',         # Contextual condition
    'wantTo': 'customfield_25355',       # User desire
    'soICan': 'customfield_26559',       # Immediate benefit
    'soThat': 'customfield_25356',       # Business value
    'acceptanceCriteria': 'customfield_10253',  # Definition of done
    'themeSquad': 'customfield_34040'    # Team assignment
}
```

**Story Structure Template**:
- **As An**: User role or persona
- **When**: Contextual condition or trigger
- **Want To**: Specific user desire or need
- **So I Can**: Immediate user benefit
- **So That**: Broader business value
- **Acceptance Criteria**: Definition of done
- **Theme/Squad**: Team or theme assignment

**Payload Building**:
1. **Required Fields**: Issue type, project, summary
2. **Optional Fields**: Description, priority (defaults to Medium)
3. **Custom Fields**: Product management template fields
4. **Validation**: Ensures required project ID is provided

### 4. Project Management

#### `get_projects(search_term, max_results)`
**Purpose**: Retrieve and search JIRA projects  
**Features**:
- **Search Filtering**: Optional search term filtering
- **Result Limiting**: Configurable result pagination
- **Project Metadata**: Comprehensive project information

## 🔍 Technical Implementation Details

### Error Handling Strategy
```python
try:
    response = requests.get(url, headers=self.headers)
    response.raise_for_status()
    return response.json()
except Exception as e:
    logger.error(f"Error message: {str(e)}")
    return {'status': 'error', 'message': str(e)}
```

### Safe Field Access Pattern
```python
# Defensive programming for optional fields
assignee = fields.get('assignee', {}).get('displayName', 'Unassigned') if fields.get('assignee') else 'Unassigned'
status = fields.get('status', {}).get('name', 'Unknown') if fields.get('status') else 'Unknown'
```

### Request Management
- **Header Consistency**: Standardized headers across all requests
- **Response Validation**: HTTP status code checking
- **JSON Processing**: Automatic response parsing
- **Error Propagation**: Maintains error context for debugging

## 📊 Integration Patterns

### Ticket Lifecycle Management
1. **Creation**: User story creation with custom fields
2. **Tracking**: Status and progress monitoring
3. **Subtask Management**: Code review task creation
4. **Completion**: Automatic status updates

### Cross-Service Workflows
- **Bitbucket Integration**: Link PRs to JIRA tickets
- **Confluence Integration**: Connect documentation to tickets
- **Automation**: Trigger actions based on ticket events

### Custom Field Integration
The service supports wenlin's specific JIRA customizations:
- **Product Management Fields**: User story template support
- **Team Assignment**: Squad/theme-based organization
- **Workflow Integration**: Custom workflow state management

## 🛠️ API Endpoint Coverage

### Core JIRA REST API v2 Endpoints
| Endpoint | Method | Purpose | Implementation |
|----------|--------|---------|----------------|
| `/rest/api/2/issue/{key}` | GET | Get ticket details | `get_ticket_details()` |
| `/rest/api/2/issue` | POST | Create issues | `create_review_task()`, `create_user_story()` |
| `/rest/api/2/search` | GET | Search issues | `search_jira_issues()` |
| `/rest/api/2/project` | GET | List projects | `get_projects()` |

### Authentication Handling
- **Bearer Token**: Primary authentication method
- **Environment Configuration**: Secure credential management
- **Request Headers**: Consistent authorization handling

## 🔄 Workflow Examples

### Code Review Workflow
1. **PR Created** → Bitbucket webhook
2. **Parent Ticket Identified** → Extract JIRA key from PR
3. **Review Task Created** → `create_review_task()`
4. **Implementation Tracking** → Subtask status updates

### User Story Creation Workflow
1. **Requirements Gathered** → Product management input
2. **Story Template Applied** → Custom field mapping
3. **Story Created** → `create_user_story()`
4. **Sprint Planning** → Story assignment and estimation

### Search & Discovery Workflow
1. **Query Construction** → JQL query building
2. **Search Execution** → `search_jira_issues()`
3. **Result Processing** → Data extraction and formatting
4. **Action Routing** → Based on search results

## 🔧 Configuration & Customization

### Environment Variables
```bash
JIRA_BASE_URL=https://wljira.wenlin.net
JIRA_AUTH_TOKEN=your-bearer-token
```

### Custom Field Configuration
The service includes pre-configured custom field mappings for wenlin's JIRA instance. These can be updated for different organizations:

```python
# Update custom_fields dictionary in create_user_story()
custom_fields = {
    'asAn': 'your_custom_field_id',
    'wantTo': 'your_custom_field_id',
    # ... other mappings
}
```

### Issue Type Configuration
- **Story**: Default issue type ID "21"
- **Subtask**: Default issue type ID "5"
- **Priority**: Default priority ID "6" (Medium)

These IDs are JIRA instance-specific and may need adjustment for different installations.

This service provides comprehensive JIRA integration with support for custom workflows, product management practices, and enterprise security requirements. 