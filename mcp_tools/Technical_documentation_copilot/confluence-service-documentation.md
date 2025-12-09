# Confluence Service Documentation

## 📋 Module Overview

**File**: `servers/confluence/service.py`  
**Purpose**: Core service layer for Confluence API integration  
**Dependencies**: `requests`, `html2text`, `atlassian`, `beautifulsoup4`, `langchain-community`  
**Lines of Code**: 530 lines  

## 🏗️ Architecture

### Class Structure
```python
class ConfluenceService:
    """Service class for interacting with Confluence API."""
```

### Key Dependencies & Integrations
- **LangChain Community**: `ConfluenceLoader` for document processing
- **HTML2Text**: Markdown conversion capabilities
- **Atlassian SDK**: Native Confluence API integration
- **BeautifulSoup**: HTML parsing and processing
- **Requests**: HTTP client for API communication

## 🔧 Configuration & Initialization

### Environment Variables
```python
CONFLUENCE_BASE_URL = "https://wlwiki.wenlin.net/"
CONFLUENCE_USERNAME = "user@domain.com"
CONFLUENCE_API_KEY = "api-key-string"
```

### SSL & Security Configuration
The service includes sophisticated SSL handling:
- **SSL Verification Bypass**: For corporate environments
- **Custom Session Patching**: Patches `Confluence` class for unsafe SSL
- **Warning Suppression**: Manages SSL-related warnings
- **Parser Optimization**: Forces `lxml` parser for consistency

### Initialization Process
1. **Credential Validation**: Checks for required environment variables
2. **HTML2Text Setup**: Configures markdown conversion settings
3. **SSL Configuration**: Applies security patches
4. **Authentication Setup**: Creates HTTP Basic Auth tuple

## 🚀 Core Methods

### 1. Document Retrieval & Conversion

#### `get_pages_as_markdown(page_ids, space_key)`
**Purpose**: Fetch Confluence pages and convert to markdown  
**Input**: 
- `page_ids`: List of specific page IDs
- `space_key`: Space identifier for bulk retrieval

**Process Flow**:
1. **Credential Validation**: Ensures authentication is available
2. **Loader Configuration**: Sets up `ConfluenceLoader` with parameters
3. **Parser Testing**: Validates HTML parser availability (lxml → html5lib → html.parser)
4. **Document Loading**: Executes document retrieval via LangChain
5. **Markdown Conversion**: Processes HTML content to markdown format
6. **Metadata Extraction**: Extracts title, URL, author, creation date, page ID

**Return Structure**:
```python
{
    'status': 'success',
    'message': 'Successfully retrieved X pages',
    'pages': [
        {
            'page_number': 1,
            'title': 'Page Title',
            'url': 'https://confluence.../page',
            'author': 'John Doe',
            'created': '2024-01-01',
            'page_id': '12345',
            'markdown_content': '# Content...',
            'metadata': {...}
        }
    ],
    'total_pages': 5,
    'search_criteria': {...}
}
```

### 2. Search Operations

#### `search_pages(query, space_key, limit)`
**Purpose**: Execute CQL (Confluence Query Language) searches  
**Input**:
- `query`: CQL search string
- `space_key`: Optional space filter
- `limit`: Maximum results (default: 25)

**API Endpoint**: `/rest/api/content/search`  
**Authentication**: HTTP Basic Auth  

**Search Features**:
- **CQL Support**: Full Confluence Query Language capabilities
- **Space Filtering**: Optional space-specific searches
- **Result Limiting**: Configurable result pagination
- **Rich Metadata**: Includes content type, status, version info

### 3. Space Management

#### `get_spaces(limit)`
**Purpose**: Retrieve available Confluence spaces  
**API Endpoint**: `/rest/api/space`  
**Features**:
- **Pagination Support**: Configurable result limits
- **Space Types**: Personal, team, and global spaces
- **Metadata Extraction**: Key, name, type, permissions

### 4. Page Operations

#### `get_page_by_title(title, space_key)`
**Purpose**: Retrieve specific page by title and space  
**Unique Features**:
- **Exact Title Matching**: Finds pages by exact title
- **Space-Scoped Search**: Requires space context
- **Content Expansion**: Includes body content and metadata

#### `create_page(title, content, space_key, parent_page_id, labels)`
**Purpose**: Create new Confluence pages with full feature support  
**Advanced Features**:
- **Markdown Support**: Converts markdown to Confluence storage format
- **Hierarchical Structure**: Optional parent page assignment
- **Label Management**: Automatic label application
- **Error Recovery**: Handles creation conflicts and validation errors

**Content Processing**:
1. **Markdown Detection**: Identifies markdown content patterns
2. **HTML Conversion**: Uses `markdown` library for conversion
3. **Storage Format**: Converts to Confluence's storage format
4. **Validation**: Ensures content meets Confluence requirements

## 🔍 Technical Implementation Details

### HTML Parser Management
The service implements sophisticated parser fallback logic:

```python
def _patch_beautifulsoup_parser(self):
    """Patch BeautifulSoup to use a working parser without repeated warnings."""
    # Priority: lxml → html5lib → html.parser
    # Includes testing and fallback mechanisms
```

### SSL Certificate Handling
Corporate environment support with SSL bypass:

```python
def _patch_confluence_loader_ssl(self):
    """Patch the ConfluenceLoader to disable SSL verification."""
    # Creates custom session with SSL verification disabled
    # Patches Confluence class initialization
```

### Error Handling Strategy
- **Graceful Degradation**: Continues operation when possible
- **Comprehensive Logging**: Detailed error information
- **User-Friendly Messages**: Clear error descriptions
- **Exception Propagation**: Maintains error context

## 🔗 Integration Points

### LangChain Integration
- **Document Loaders**: Leverages LangChain's `ConfluenceLoader`
- **Content Processing**: Automatic text extraction and formatting
- **Metadata Handling**: Preserves document metadata and structure

### HTML Processing Pipeline
1. **Content Retrieval**: Raw HTML from Confluence API
2. **Parser Selection**: Optimal parser based on availability
3. **Markdown Conversion**: Clean, readable markdown output
4. **Content Validation**: Ensures proper formatting

### Authentication Flow
```python
# HTTP Basic Authentication
auth = (username, api_key)
headers = {'Authorization': f'Basic {base64_encoded_credentials}'}
```

## 📊 Performance Considerations

### Optimization Strategies
- **Session Reuse**: Persistent HTTP connections
- **Parser Caching**: Avoid repeated parser selection
- **Content Streaming**: Efficient handling of large documents
- **Connection Pooling**: Manages concurrent requests

### Resource Management
- **Memory Efficiency**: Streams large documents
- **Connection Limits**: Respects Confluence API rate limits
- **Timeout Handling**: Prevents hanging requests
- **Cleanup Procedures**: Proper resource disposal

## 🛠️ Error Scenarios & Recovery

### Common Error Types
1. **Authentication Failures**: Invalid credentials or expired tokens
2. **Network Issues**: Connection timeouts or SSL problems
3. **API Limitations**: Rate limits or service unavailability
4. **Content Errors**: Invalid markup or encoding issues

### Recovery Mechanisms
- **Automatic Retry**: Transient error recovery
- **Fallback Parsing**: Multiple parser options
- **Graceful Degradation**: Partial operation capabilities
- **Error Reporting**: Detailed diagnostic information

## 🔄 Workflow Integration

### Typical Usage Patterns
1. **Documentation Discovery**: Search and retrieve relevant pages
2. **Content Analysis**: Convert to markdown for processing
3. **Knowledge Management**: Organize and structure information
4. **Automated Publishing**: Create and update documentation

### Cross-Service Integration
- **JIRA Linking**: Connect documentation to tickets
- **Bitbucket Integration**: Link to code repositories
- **Version Control**: Track documentation changes

This service provides a robust, scalable foundation for Confluence integration with comprehensive error handling, flexible authentication, and powerful content processing capabilities. 