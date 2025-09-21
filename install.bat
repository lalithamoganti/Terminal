@echo off
echo Installing Advanced Python Terminal
echo ==================================
echo.

echo Installing Python dependencies...
py -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error installing dependencies. Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.
echo To run the terminal:
echo   - Double-click run_terminal.bat
echo   - Or run: py terminal.py (for CLI)
echo   - Or run: py web_terminal.py (for web interface)
echo.
echo For AI features, set your OpenAI API key:
echo   set OPENAI_API_KEY=your_api_key_here
echo.
pause


