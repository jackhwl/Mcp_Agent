@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   JIRA, Bitbucket, Confluence, Asana ^& TestRail MCP Servers Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo [SUCCESS] Python found:
python --version

:: Check if virtual environment exists
if exist ".venv" (
    echo [SUCCESS] Virtual environment already exists
) else (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
)

echo.
echo [INFO] Activating virtual environment...

:: Activate virtual environment
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip
    pause
    exit /b 1
)

echo.
if exist "requirements.txt" (
    echo [INFO] Installing requirements from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements
        pause
        exit /b 1
    )
    echo [SUCCESS] Requirements installed successfully
) else (
    echo [INFO] Installing core dependencies...
    pip install fastmcp requests python-dotenv
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Core dependencies installed
)

echo.
echo [INFO] Running MCP configuration...
python configure_mcp.py
if errorlevel 1 (
    echo [ERROR] Failed to configure MCP server
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo [SUCCESS] Virtual environment created and activated
echo [SUCCESS] Dependencies installed
echo [SUCCESS] MCP servers configured in VSCode settings
echo.
echo [INFO] Next steps:
echo   1. Update your authentication tokens in VSCode settings:
echo      - JIRA_AUTH_TOKEN (JIRA API token)
echo      - BITBUCKET_AUTH_TOKEN (Bitbucket auth token)
echo      - CONFLUENCE_USERNAME ^& CONFLUENCE_API_KEY (Confluence credentials)
echo      - ASANA_AUTH_TOKEN (Asana Personal Access Token)
echo      - TESTRAIL_URL, TESTRAIL_USERNAME ^& TESTRAIL_API_KEY (TestRail credentials)
echo   2. Restart VSCode/Cursor
echo   3. Run the healthcheck tools to verify setup:
echo      - healthcheck (JIRA)
echo      - bitbucket_healthcheck (Bitbucket)
echo      - confluence_healthcheck (Confluence)
echo      - asana_healthcheck (Asana)
echo      - testrail_healthcheck (TestRail)
echo   4. Run the 'test_connection' tool to test JIRA authentication
echo.
echo [INFO] To manually activate the virtual environment later:
echo    .venv\Scripts\activate.bat
echo.
echo [INFO] For help with token setup, check the healthcheck tools output
echo.
pause 