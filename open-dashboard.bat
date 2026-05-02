@echo off
REM MBA Job Dashboard Launcher
REM This script opens the dashboard in your default browser

echo.
echo ========================================
echo   MBA Job Dashboard Launcher
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Check if jobs.json exists
if not exist "%SCRIPT_DIR%dashboard\data\jobs.json" (
    echo [!] jobs.json not found. Running scraper first...
    echo.
    cd /d "%SCRIPT_DIR%scraper"
    python main.py
    if errorlevel 1 (
        echo [ERROR] Scraper failed. Make sure Python is installed.
        echo Run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo [+] Opening dashboard in your browser...
echo.

REM Open the dashboard in default browser
start "" "%SCRIPT_DIR%dashboard\index.html"

echo [✓] Dashboard opened! Check your browser.
echo.
echo To refresh jobs, run: scraper\main.py
echo.
pause
