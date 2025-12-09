#!/bin/bash

echo "========================================"
echo "   JIRA, Bitbucket, Confluence, Asana & TestRail MCP Servers Setup"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
print_info() { echo -e "${BLUE}📋 $1${NC}"; }

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed or not in PATH"
        echo "Please install Python 3.8+ and add it to your PATH"
        echo "macOS: brew install python"
        echo "Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
        echo "CentOS/RHEL: sudo yum install python3 python3-venv python3-pip"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_success "Python found: $($PYTHON_CMD --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
echo
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo
echo "📈 Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo
    echo "📦 Installing requirements from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Failed to install requirements"
        exit 1
    fi
    print_success "Requirements installed successfully"
else
    echo
    echo "📦 Installing core dependencies..."
    pip install fastmcp requests
    if [ $? -ne 0 ]; then
        print_error "Failed to install core dependencies"
        exit 1
    fi
    print_success "Core dependencies installed"
fi

# Run configuration script
echo
echo "⚙️  Running MCP configuration..."
python configure_mcp.py
if [ $? -ne 0 ]; then
    print_error "Configuration failed"
    exit 1
fi

echo
echo "========================================"
echo "   🎉 Setup Complete!"
echo "========================================"
echo
print_success "Virtual environment created and activated"
print_success "Dependencies installed"
print_success "MCP servers configured in VSCode settings"
echo
print_info "Next steps:"
echo "  1. Update your authentication tokens in VSCode settings:"
echo "     - JIRA_AUTH_TOKEN (JIRA API token)"
echo "     - BITBUCKET_AUTH_TOKEN (Bitbucket auth token)"
echo "     - CONFLUENCE_USERNAME & CONFLUENCE_API_KEY (Confluence credentials)"
echo "     - ASANA_AUTH_TOKEN (Asana Personal Access Token)"
echo "     - TESTRAIL_URL, TESTRAIL_USERNAME & TESTRAIL_API_KEY (TestRail credentials)"
echo "  2. Restart VSCode/Cursor"
echo "  3. Run the healthcheck tools to verify setup:"
echo "     - healthcheck (JIRA)"
echo "     - bitbucket_healthcheck (Bitbucket)"
echo "     - confluence_healthcheck (Confluence)"
echo "     - asana_healthcheck (Asana)"
echo "     - testrail_healthcheck (TestRail)"
echo "  4. Run the 'test_connection' tool to test JIRA authentication"
echo
print_info "To manually activate the virtual environment later:"
echo "  source .venv/bin/activate"
echo
print_info "For help with token setup, check the healthcheck tools output"
echo 