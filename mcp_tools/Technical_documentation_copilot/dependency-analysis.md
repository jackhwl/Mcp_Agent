# Dependency Analysis - MCP ProCode System

## 📋 Overview

This document provides a comprehensive analysis of all dependencies, their purposes, interconnections, and impact on the MCP ProCode system. Understanding these dependencies is crucial for maintenance, updates, and troubleshooting.

## 🔗 Core System Dependencies

### Python Runtime Requirements
- **Python Version**: 3.8+ required
- **Virtual Environment**: Strongly recommended for isolation
- **Platform Support**: Windows, macOS, Linux

### Primary Dependencies

#### 1. `requests` (HTTP Client)
**Version**: Latest stable  
**Purpose**: Core HTTP communication for all Atlassian APIs  
**Usage**:
- JIRA REST API calls
- Bitbucket Server API integration
- Confluence API communication

**Critical Features**:
- Session management and connection pooling
- Authentication handling (Basic, Bearer)
- SSL/TLS certificate management
- Request/response serialization

**Service Integration**:
```python
# JIRA Service
response = requests.get(url, headers=self.headers)

# Bitbucket Service  
self.session = requests.Session()

# Confluence Service (via atlassian library)
# Used indirectly through atlassian SDK
```

#### 2. `mcp` (Multi-Context Protocol)
**Purpose**: Core MCP server functionality  
**Features**:
- Tool registration and management
- Request/response handling
- Protocol compliance
- Error handling standards

**Implementation Pattern**:
```python
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    Tool,
    TextContent,
)
```

## 🌐 Service-Specific Dependencies

### Confluence Service Dependencies

#### 1. `langchain-community`
**Purpose**: Document loading and processing  
**Key Component**: `ConfluenceLoader`  
**Features**:
- Automated page content extraction
- Metadata preservation
- Bulk document processing
- Authentication integration

**Critical Implementation**:
```python
from langchain_community.document_loaders import ConfluenceLoader

loader = ConfluenceLoader(
    url=self.base_url,
    username=self.username,
    api_key=self.api_key,
    include_attachments=True
)
```

**Impact**: Core functionality for page retrieval and markdown conversion

#### 2. `html2text`
**Purpose**: HTML to Markdown conversion  
**Features**:
- Clean markdown output
- Table preservation
- Link handling
- Image references

**Configuration**:
```python
self.converter = html2text.HTML2Text()
self.converter.ignore_links = False
self.converter.bypass_tables = False
self.converter.ignore_images = False
self.converter.body_width = 0
self.converter.single_line_break = True
```

#### 3. `atlassian`
**Purpose**: Native Confluence SDK integration  
**Features**:
- Direct API access
- Authentication handling
- Enterprise features
- Session management

**Patching for SSL**:
```python
# Custom SSL handling for corporate environments
original_init = Confluence.__init__
def custom_init(self, *args, **kwargs):
    self._session = UnsafeSession()
    original_init(self, *args, **kwargs)
```

#### 4. `beautifulsoup4`
**Purpose**: HTML parsing and processing  
**Features**:
- Robust HTML parsing
- Multiple parser support (lxml, html5lib, html.parser)
- Content extraction
- Error handling

**Parser Priority**:
```python
# Priority order: lxml > html5lib > html.parser
try:
    soup = BeautifulSoup(markup, 'lxml')
except:
    try:
        soup = BeautifulSoup(markup, 'html5lib')
    except:
        soup = BeautifulSoup(markup, 'html.parser')
```

#### 5. `markdown`
**Purpose**: Markdown to HTML conversion for page creation  
**Features**:
- Markdown parsing
- HTML generation
- Extension support
- Confluence storage format compatibility

### Universal Dependencies

#### 1. `urllib3`
**Purpose**: Low-level HTTP client (dependency of requests)  
**Configuration**:
```python
# Disable SSL warnings for corporate environments
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
```

#### 2. `logging` (Built-in)
**Purpose**: Comprehensive logging across all services  
**Configuration**:
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 📊 Dependency Tree Analysis

### Direct Dependencies
```
mcp-procode/
├── requests
├── mcp
├── langchain-community
├── html2text
├── atlassian
├── beautifulsoup4
└── markdown
```

### Transitive Dependencies
```
requests → urllib3, certifi, charset-normalizer, idna
langchain-community → langchain-core, pydantic, PyYAML
atlassian → requests, six
beautifulsoup4 → (optional: lxml, html5lib)
```

### Optional Parser Dependencies
```
lxml (recommended)
├── libxml2
├── libxslt
└── C compiler dependencies

html5lib (fallback)
├── webencodings
└── six
```

## ⚠️ Critical Dependency Relationships

### 1. SSL/Certificate Handling Chain
```
requests → urllib3 → OpenSSL/TLS
         ↓
atlassian → requests (patched)
         ↓
ConfluenceLoader → atlassian
```

**Risk**: Corporate SSL certificate issues can cascade through entire Confluence service

### 2. HTML Processing Pipeline
```
ConfluenceLoader → Raw HTML
         ↓
BeautifulSoup → Parsed HTML
         ↓
html2text → Markdown
```

**Risk**: Parser failures can break markdown conversion

### 3. Authentication Flow
```
Environment Variables → Service Configuration
                     ↓
requests/atlassian → API Authentication
                     ↓
All Tool Operations
```

**Risk**: Authentication failures affect all service operations

## 🔧 Version Management Strategy

### Pinned Dependencies (Critical)
```python
# requirements.txt
requests>=2.31.0,<3.0.0
mcp>=1.0.0,<2.0.0
langchain-community>=0.0.29,<1.0.0
```

### Flexible Dependencies (Stable)
```python
html2text>=2020.1.16
atlassian-python-api>=3.41.0
beautifulsoup4>=4.12.0
markdown>=3.4.0
```

### Parser Dependencies (Optional)
```python
lxml>=4.9.0  # Recommended for performance
html5lib>=1.1  # Fallback parser
```

## 🚨 Risk Assessment

### High Risk Dependencies

#### 1. `langchain-community`
**Risk Level**: HIGH  
**Reason**: Rapidly evolving, breaking changes common  
**Mitigation**: Pin to tested version, comprehensive testing

#### 2. `atlassian`
**Risk Level**: MEDIUM-HIGH  
**Reason**: Corporate dependency, SSL patching required  
**Mitigation**: Custom session handling, extensive SSL testing

#### 3. `lxml`
**Risk Level**: MEDIUM  
**Reason**: Native dependencies, compilation requirements  
**Mitigation**: Fallback parser strategy implemented

### Low Risk Dependencies

#### 1. `requests`
**Risk Level**: LOW  
**Reason**: Mature, stable API, wide compatibility  

#### 2. `html2text`
**Risk Level**: LOW  
**Reason**: Simple, focused functionality, minimal changes

#### 3. `beautifulsoup4`
**Risk Level**: LOW  
**Reason**: Mature parsing library, stable API

## 🔄 Update Strategy

### Critical Path Updates
1. **Security Updates**: Immediate for requests, urllib3
2. **LangChain Updates**: Careful testing required
3. **Parser Updates**: Test across all parser options

### Testing Protocol
```bash
# 1. Virtual environment testing
python -m venv test_env
pip install -r requirements.txt

# 2. Service health checks
python -c "from servers.confluence.service import ConfluenceService; print(ConfluenceService().get_spaces(limit=1))"

# 3. Integration testing
# Test each MCP tool individually

# 4. Performance testing
# Monitor response times and memory usage
```

### Rollback Strategy
```bash
# Maintain known good versions
pip freeze > requirements-working.txt

# Rollback procedure
pip uninstall -r requirements.txt -y
pip install -r requirements-working.txt
```

## 🛠️ Development Dependencies

### Optional Development Tools
```python
pytest>=7.0.0          # Testing framework
black>=23.0.0           # Code formatting
flake8>=6.0.0          # Linting
mypy>=1.0.0            # Type checking
requests-mock>=1.10.0   # API mocking for tests
```

### Documentation Dependencies
```python
sphinx>=6.0.0          # Documentation generation
sphinx-rtd-theme>=1.0.0 # Documentation theme
```

## 📈 Performance Impact Analysis

### Memory Usage by Service
- **Base MCP Server**: ~10MB
- **Confluence Service**: ~25MB (with LangChain)
- **JIRA Service**: ~15MB  
- **Bitbucket Service**: ~15MB

### CPU Impact
- **HTML Parsing**: High CPU during document processing
- **SSL Handshakes**: Moderate CPU for HTTPS connections
- **JSON Processing**: Low CPU impact

### Network Dependencies
- **Persistent Connections**: Via requests session management
- **Connection Pooling**: Configured for optimal performance
- **SSL Overhead**: Significant in corporate environments

## 🔍 Monitoring & Health Checks

### Dependency Health Monitoring
```python
def check_dependency_health():
    """Monitor critical dependency status"""
    checks = {
        'requests': test_http_capability(),
        'langchain': test_document_loading(),
        'parsers': test_html_parsing(),
        'ssl': test_ssl_connectivity()
    }
    return checks
```

### Performance Monitoring
```python
def monitor_dependency_performance():
    """Track dependency performance metrics"""
    metrics = {
        'request_latency': measure_http_latency(),
        'parsing_speed': measure_html_parsing(),
        'memory_usage': get_memory_usage(),
        'connection_pool': get_pool_status()
    }
    return metrics
```

This dependency analysis provides a comprehensive understanding of the MCP ProCode system's dependency structure, risks, and management strategies for reliable operation. 