@echo off
echo Advanced Python Terminal Launcher
echo ================================
echo.
echo Choose interface mode:
echo 1. CLI Terminal
echo 2. Web Terminal
echo 3. Demo Mode
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting CLI Terminal...
    py terminal.py
) else if "%choice%"=="2" (
    echo Starting Web Terminal...
    echo Web interface will be available at: http://localhost:5000
    echo Press Ctrl+C to stop the server
    py web_terminal.py
) else if "%choice%"=="3" (
    echo Running Demo...
    py demo.py
) else (
    echo Invalid choice. Please run the script again.
    pause
)


