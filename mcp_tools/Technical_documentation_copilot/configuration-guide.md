# MCP ProCode Configuration Guide

## 📋 Overview

This guide provides comprehensive instructions for configuring and setting up the MCP ProCode system for Atlassian service integration. The system supports JIRA, Bitbucket, and Confluence through a unified Multi-Context Protocol (MCP) interface.

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**: Required for all MCP servers
- **VSCode**: With MCP extension support
- **Atlassian Access**: Valid credentials for target services
- **Virtual Environment**: Recommended for dependency isolation

### Installation Steps
```bash
# 1. Clone and setup
git clone <repository-url>
cd mcp-procode

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

## 🔧 Configuration Architecture

### Configuration File: `configure_mcp.py`

The central configuration script handles:
- **Cross-platform compatibility**: Windows, macOS, Linux support
- **VSCode integration**: Automatic settings.json updates
- **Environment management**: Secure credential handling
- **Path resolution**: Absolute path detection for reliability

### Configuration Flow
```python
# 1. Detect system paths
venv_python = detect_virtual_environment()
server_paths = resolve_server_scripts()

# 2. Load existing VSCode settings
settings = load_vscode_settings()

# 3. Update MCP configuration
settings["mcp"]["servers"] = configure_mcp_servers()

# 4. Save updated settings
save_vscode_settings(settings)
```

## 🏗️ Service Configuration

### 1. JIRA Configuration

#### Environment Variables
```bash
# Required
JIRA_BASE_URL=https://wljira.wenlin.net
JIRA_AUTH_TOKEN=your-bearer-token

# Optional
JIRA_REQUEST_TIMEOUT=30
JIRA_MAX_RETRIES=3
```

#### VSCode Settings
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
      }
    }
  }
}
```

#### Authentication Setup
1. **Generate API Token**:
   - Login to JIRA → Profile → Personal Access Tokens
   - Create new token with appropriate scopes
   - Copy token for configuration

2. **Token Verification**:
   ```bash
   curl -H "Authorization: Bearer your-token" \
        "https://wljira.wenlin.net/rest/api/2/myself"
   ```

### 2. Bitbucket Configuration

#### Environment Variables
```bash
# Required
BITBUCKET_BASE_URL=http://wlstash.wenlin.net
BITBUCKET_AUTH_TOKEN=your-auth-token

# Optional
BITBUCKET_SESSION_TIMEOUT=300
BITBUCKET_MAX_CONNECTIONS=10
```

#### Authentication Options

##### Option A: Bearer Token
```bash
BITBUCKET_AUTH_TOKEN=your-bearer-token
```

##### Option B: Basic Authentication
```bash
# Format: username:password (base64 encoded)
BITBUCKET_AUTH_TOKEN=username:password
```

#### VSCode Settings
```json
{
  "mcp": {
    "servers": {
      "bitbucket-mcp-server": {
        "type": "stdio",
        "command": "/path/to/.venv/Scripts/python.exe",
        "args": ["/path/to/servers/bitbucket_server.py"],
        "env": {
          "BITBUCKET_AUTH_TOKEN": "your-secure-auth-token",
          "BITBUCKET_BASE_URL": "http://wlstash.wenlin.net"
        }
      }
    }
  }
}
```

### 3. Confluence Configuration

#### Environment Variables
```bash
# Required
CONFLUENCE_BASE_URL=https://wlwiki.wenlin.net/
CONFLUENCE_USERNAME=your-username@domain.com
CONFLUENCE_API_KEY=your-api-key

# Optional
CONFLUENCE_SSL_VERIFY=false
CONFLUENCE_REQUEST_TIMEOUT=60
```

#### Authentication Setup
1. **Find Username**:
   - **Atlassian Cloud**: Usually your email address
   - **Server/Data Center**: Your username or email

2. **Generate API Key**:
   - **Cloud**: Atlassian Account Settings → Security → API tokens
   - **Server**: User Profile → Personal Access Tokens

3. **Verification**:
   ```bash
   curl -u "username:api-key" \
        "https://wlwiki.wenlin.net/rest/api/user/current"
   ```

#### VSCode Settings
```json
{
  "mcp": {
    "servers": {
      "confluence-mcp-server": {
        "type": "stdio",
        "command": "/path/to/.venv/Scripts/python.exe",
        "args": ["/path/to/servers/confluence_server.py"],
        "env": {
          "CONFLUENCE_USERNAME": "your-confluence-username",
          "CONFLUENCE_API_KEY": "your-confluence-api-key",
          "CONFLUENCE_BASE_URL": "https://wlwiki.wenlin.net/"
        }
      }
    }
  }
}
```

## 🔐 Security Configuration

### Credential Management

#### Environment File (.env)
```bash
# Create .env file in project root
# Add to .gitignore for security

# JIRA Configuration
JIRA_BASE_URL=https://wljira.wenlin.net
JIRA_AUTH_TOKEN=your-jira-token

# Bitbucket Configuration
BITBUCKET_BASE_URL=http://wlstash.wenlin.net
BITBUCKET_AUTH_TOKEN=your-bitbucket-token

# Confluence Configuration
CONFLUENCE_BASE_URL=https://wlwiki.wenlin.net/
CONFLUENCE_USERNAME=your-username
CONFLUENCE_API_KEY=your-confluence-key
```

#### Loading Environment Variables
```python
# Option 1: python-dotenv
from dotenv import load_dotenv
load_dotenv()

# Option 2: Manual export (Linux/macOS)
export JIRA_AUTH_TOKEN="your-token"

# Option 3: PowerShell (Windows)
$env:JIRA_AUTH_TOKEN="your-token"
```

### SSL/TLS Configuration

#### Corporate Environments
```python
# Disable SSL verification for corporate networks
import os
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

# Custom certificate bundle
os.environ['REQUESTS_CA_BUNDLE'] = '/path/to/corporate-ca.pem'
```

#### Certificate Handling
```python
# In service configuration
verify_ssl = os.getenv('CONFLUENCE_SSL_VERIFY', 'true').lower() == 'true'
session.verify = verify_ssl
```

## 🛠️ Advanced Configuration

### Custom Field Mapping (JIRA)

#### wenlin-Specific Fields
```python
custom_fields = {
    'asAn': 'customfield_25354',
    'when': 'customfield_26560', 
    'wantTo': 'customfield_25355',
    'soICan': 'customfield_26559',
    'soThat': 'customfield_25356',
    'acceptanceCriteria': 'customfield_10253',
    'themeSquad': 'customfield_34040'
}
```

#### Customization for Other Organizations
```python
# Update in servers/jira/service.py
def create_user_story(self, story_data):
    custom_fields = {
        'asAn': 'your_custom_field_id',
        'wantTo': 'your_custom_field_id',
        # ... add your custom fields
    }
```

### Issue Type Configuration
```python
# Update default issue type IDs in JIRA service
DEFAULT_STORY_TYPE = "10001"    # Your story type ID
DEFAULT_SUBTASK_TYPE = "10002"  # Your subtask type ID
DEFAULT_PRIORITY = "10003"      # Your default priority ID
```

### Workspace Configuration (Bitbucket)

#### Multiple Workspaces
```python
# Configure multiple workspaces for batch operations
DEFAULT_WORKSPACES = [
    "WORKSPACE1",
    "WORKSPACE2", 
    "WORKSPACE3"
]

DEFAULT_REPOSITORIES = [
    "repo1",
    "repo2",
    "repo3"
]
```

## 📊 Monitoring & Logging

### Logging Configuration
```python
# Configure logging level
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp-procode.log'),
        logging.StreamHandler()
    ]
)
```

### Health Check Configuration
```python
# Configure health check endpoints
HEALTH_CHECK_TIMEOUT = 10
HEALTH_CHECK_RETRY_COUNT = 3
HEALTH_CHECK_INTERVAL = 300  # 5 minutes
```

### Performance Monitoring
```python
# Request timeout configuration
REQUEST_TIMEOUTS = {
    'jira': 30,
    'confluence': 60,
    'bitbucket': 45
}

# Connection pool settings
CONNECTION_POOL_SIZE = 10
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.3
```

## 🔄 Troubleshooting

### Common Issues

#### 1. Authentication Failures
**Symptoms**: 401/403 errors, "Invalid credentials"
**Solutions**:
- Verify token/credentials are correct
- Check token permissions and scopes
- Ensure URLs are correct (trailing slashes, protocols)
- Test with curl/Postman first

#### 2. SSL Certificate Errors
**Symptoms**: SSL verification failures, certificate errors
**Solutions**:
```python
# Temporary: Disable SSL verification
CONFLUENCE_SSL_VERIFY=false

# Permanent: Add corporate certificate
export REQUESTS_CA_BUNDLE=/path/to/cert.pem
```

#### 3. Network Connectivity
**Symptoms**: Connection timeouts, network unreachable
**Solutions**:
- Check firewall settings
- Verify VPN connections
- Test network connectivity to services
- Configure proxy settings if needed

#### 4. Parser Warnings (Confluence)
**Symptoms**: BeautifulSoup parser warnings
**Solutions**:
```bash
# Install lxml parser
pip install lxml

# Or use html5lib as fallback
pip install html5lib
```

### Diagnostic Commands

#### Test JIRA Connection
```bash
python -c "
from servers.jira.service import JiraService
service = JiraService()
print('JIRA Health:', service.health_check())
"
```

#### Test Confluence Connection
```bash
python -c "
from servers.confluence.service import ConfluenceService
service = ConfluenceService()
print('Confluence Health:', service.get_spaces(limit=1))
"
```

#### Test Bitbucket Connection
```bash
python -c "
from servers.bitbucket.service import BitbucketService
service = BitbucketService()
print('Bitbucket Health:', service.get_repository_info('WORKSPACE', 'repo'))
"
```

### Log Analysis
```bash
# Check recent errors
tail -f mcp-procode.log | grep ERROR

# Filter by service
grep "confluence" mcp-procode.log | tail -20

# Monitor performance
grep "Response time" mcp-procode.log
```

## 📈 Performance Optimization

### Connection Pooling
```python
# Configure session with connection pooling
session = requests.Session()
adapter = HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20,
    max_retries=3
)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### Caching Configuration
```python
# Enable response caching for read operations
from requests_cache import CachedSession

session = CachedSession(
    cache_name='mcp_cache',
    expire_after=300,  # 5 minutes
    allowable_methods=['GET'],
    allowable_codes=[200]
)
```

### Rate Limiting
```python
# Implement rate limiting for API calls
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)  # 100 calls per minute
def api_call():
    # Your API call here
    pass
```

This configuration guide provides comprehensive setup instructions for all MCP ProCode services with security, performance, and troubleshooting considerations. 