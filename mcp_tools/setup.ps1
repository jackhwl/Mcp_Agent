# JIRA, Bitbucket & Confluence MCP Servers Setup Script (PowerShell)
# This script automates the setup process for new users cloning the repository

param(
    [switch]$Force,  # Force recreate virtual environment
    [switch]$Help    # Show help
)

# Color functions
function Write-Success { param($Message) Write-Host "[SUCCESS] $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Cyan }

if ($Help) {
    Write-Host "JIRA, Bitbucket, Confluence, Asana & TestRail MCP Servers Setup Script" -ForegroundColor Green
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "    .\setup.ps1 [-Force] [-Help]"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "    -Force    Force recreation of virtual environment"
    Write-Host "    -Help     Show this help message"
    Write-Host ""
    Write-Host "DESCRIPTION:" -ForegroundColor Yellow
    Write-Host "    This script automates the complete setup process:"
    Write-Host "    1. Checks Python installation"
    Write-Host "    2. Creates virtual environment"
    Write-Host "    3. Installs dependencies"
    Write-Host "    4. Configures MCP servers in VSCode"
    Write-Host "    5. Provides next steps for token setup"
    Write-Host ""
    Write-Host "REQUIREMENTS:" -ForegroundColor Yellow
    Write-Host "    - Python 3.8 or higher"
    Write-Host "    - VSCode or Cursor IDE"
    exit 0
}

Write-Host "========================================" -ForegroundColor Blue
Write-Host "   JIRA, Bitbucket, Confluence, Asana & TestRail MCP Servers Setup" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host

# Check execution policy
$executionPolicy = Get-ExecutionPolicy
if ($executionPolicy -eq "Restricted") {
    Write-Warning "PowerShell execution policy is restricted"
    Write-Info "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host "Do you want to continue anyway? (Y/N): " -NoNewline
    $response = Read-Host
    if ($response -ne "Y" -and $response -ne "y") {
        exit 1
    }
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Success "Python found: $pythonVersion"
} catch {
    Write-Error "Python is not installed or not in PATH"
    Write-Host "Please install Python 3.8+ and add it to your PATH"
    Write-Host "Download from: https://python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Read-Host "Press Enter to exit"
    exit 1
}

# Handle virtual environment
if (Test-Path ".venv") {
    if ($Force) {
        Write-Info "Removing existing virtual environment..."
        Remove-Item -Recurse -Force ".venv"
        Write-Success "Existing virtual environment removed"
    } else {
        Write-Success "Virtual environment already exists"
    }
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host
    Write-Info "Creating virtual environment..."
    try {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create virtual environment"
        }
        Write-Success "Virtual environment created"
    } catch {
        Write-Error "Failed to create virtual environment: $_"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment
Write-Host
Write-Info "Activating virtual environment..."
try {
    & ".\.venv\Scripts\Activate.ps1"
    Write-Success "Virtual environment activated"
} catch {
    Write-Warning "Could not activate virtual environment using PowerShell script"
    Write-Info "Trying alternative method..."
    & ".\.venv\Scripts\activate.bat"
}

# Upgrade pip
Write-Host
Write-Info "Upgrading pip..."
try {
    python -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        throw "Pip upgrade failed"
    }
    Write-Success "Pip upgraded successfully"
} catch {
    Write-Warning "Could not upgrade pip: $_"
}

# Install dependencies
Write-Host
if (Test-Path "requirements.txt") {
    Write-Info "Installing requirements from requirements.txt..."
    try {
        pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            throw "Requirements installation failed"
        }
        Write-Success "Requirements installed successfully"
    } catch {
        Write-Error "Failed to install requirements: $_"
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Info "Installing core dependencies..."
    try {
        pip install fastmcp requests python-dotenv
        if ($LASTEXITCODE -ne 0) {
            throw "Core dependencies installation failed"
        }
        Write-Success "Core dependencies installed"
    } catch {
        Write-Error "Failed to install core dependencies: $_"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Run configuration script
Write-Host
Write-Info "Running MCP configuration..."
try {
    python configure_mcp.py
    if ($LASTEXITCODE -ne 0) {
        throw "Configuration script failed"
    }
    Write-Success "MCP configuration completed"
} catch {
    Write-Error "Configuration failed: $_"
    Read-Host "Press Enter to exit"
    exit 1
}

# Success message
Write-Host
Write-Host "========================================" -ForegroundColor Green
Write-Host "   SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host

Write-Success "Virtual environment created and activated"
Write-Success "Dependencies installed"
Write-Success "MCP servers configured in VSCode settings"

Write-Host
Write-Info "Next steps:"
Write-Host "  1. Update your authentication tokens in VSCode settings:"
Write-Host "     - JIRA_AUTH_TOKEN (JIRA API token)"
Write-Host "     - BITBUCKET_AUTH_TOKEN (Bitbucket auth token)"
Write-Host "     - CONFLUENCE_USERNAME & CONFLUENCE_API_KEY (Confluence credentials)"
Write-Host "     - ASANA_AUTH_TOKEN (Asana Personal Access Token)"
Write-Host "     - TESTRAIL_URL, TESTRAIL_USERNAME & TESTRAIL_API_KEY (TestRail credentials)"
Write-Host "  2. Restart VSCode/Cursor"
Write-Host "  3. Run the 'healthcheck' tools to verify setup:"
Write-Host "     - healthcheck (JIRA)"
Write-Host "     - bitbucket_healthcheck (Bitbucket)"
Write-Host "     - confluence_healthcheck (Confluence)"
Write-Host "     - asana_healthcheck (Asana)"
Write-Host "     - testrail_healthcheck (TestRail)"
Write-Host "  4. Run the 'test_connection' tool to test JIRA authentication"

Write-Host
Write-Info "To manually activate the virtual environment later:"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  # or if that fails:"
Write-Host "  .\.venv\Scripts\activate.bat"

Write-Host
Write-Info "For help with token setup, check the healthcheck tools output"

Write-Host
Read-Host "Press Enter to exit" 