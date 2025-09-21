# Running Advanced Python Terminal in VS Code

## 🚀 Quick Start for VS Code Users

### Step 1: Open Project in VS Code

1. **Open VS Code**
2. **Open Folder**: `File` → `Open Folder` → Select `C:\Users\_MSI_\codemint`
3. **Or use Command Palette**: `Ctrl+Shift+P` → `File: Open Folder`

### Step 2: Open VS Code Terminal

**Method 1: Built-in Terminal**
- Press `Ctrl + `` (backtick) to open integrated terminal
- Or go to `Terminal` → `New Terminal`

**Method 2: Command Palette**
- Press `Ctrl+Shift+P`
- Type `Terminal: Create New Terminal`

### Step 3: Install Dependencies

In the VS Code terminal, run:
```bash
py -m pip install -r requirements.txt
```

### Step 4: Run the Terminal

Choose one of these options:

## 🎯 Running Options

### Option 1: CLI Terminal
```bash
py terminal.py
```

### Option 2: Web Terminal
```bash
py web_terminal.py
```
Then open browser to: `http://localhost:5000`

### Option 3: Demo Mode
```bash
py demo.py
```

### Option 4: Using Launcher Script
```bash
py run_terminal.py --mode cli
py run_terminal.py --mode web
py run_terminal.py --mode demo
```

## 🔧 VS Code Configuration

### Create VS Code Tasks (Optional)

Create `.vscode/tasks.json` for easy running:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run CLI Terminal",
            "type": "shell",
            "command": "py",
            "args": ["terminal.py"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            }
        },
        {
            "label": "Run Web Terminal",
            "type": "shell",
            "command": "py",
            "args": ["web_terminal.py"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            }
        },
        {
            "label": "Run Demo",
            "type": "shell",
            "command": "py",
            "args": ["demo.py"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            }
        }
    ]
}
```

### Create VS Code Launch Configuration

Create `.vscode/launch.json` for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug CLI Terminal",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/terminal.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Debug Web Terminal",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/web_terminal.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Debug Demo",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/demo.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

## 🎮 VS Code Shortcuts

### Running Commands
- **Run Current File**: `F5` (if launch.json is configured)
- **Run in Terminal**: `Ctrl+F5`
- **Stop Running**: `Ctrl+C` in terminal

### Terminal Shortcuts
- **New Terminal**: `Ctrl+Shift+`` (backtick)
- **Split Terminal**: `Ctrl+Shift+5`
- **Switch Between Terminals**: `Ctrl+PageUp/PageDown`

## 🔍 Debugging in VS Code

### Set Breakpoints
1. Click in the left margin next to line numbers
2. Red dots will appear indicating breakpoints
3. Press `F5` to start debugging

### Debug Features
- **Step Over**: `F10`
- **Step Into**: `F11`
- **Step Out**: `Shift+F11`
- **Continue**: `F5`
- **Stop**: `Shift+F5`

## 📁 Project Structure in VS Code

```
📁 codemint/
├── 📄 terminal.py          # Main CLI terminal
├── 📄 web_terminal.py      # Web interface
├── 📄 run_terminal.py      # Launcher script
├── 📄 demo.py             # Demo script
├── 📄 requirements.txt    # Dependencies
├── 📁 templates/
│   └── 📄 terminal.html   # Web interface frontend
├── 📁 .vscode/            # VS Code configuration
│   ├── 📄 tasks.json      # Custom tasks
│   └── 📄 launch.json     # Debug configurations
└── 📄 README.md           # Documentation
```

## 🚨 Common VS Code Issues

### Issue 1: Python Not Found
**Solution**: Install Python extension and set interpreter
1. Install "Python" extension
2. Press `Ctrl+Shift+P`
3. Type "Python: Select Interpreter"
4. Choose your Python installation

### Issue 2: Terminal Not Working
**Solution**: Check terminal settings
1. Go to `File` → `Preferences` → `Settings`
2. Search for "terminal.integrated.shell.windows"
3. Set to: `"terminal.integrated.shell.windows": "powershell.exe"`

### Issue 3: Dependencies Not Found
**Solution**: Install in correct environment
```bash
# Check Python version
py --version

# Install dependencies
py -m pip install -r requirements.txt

# Verify installation
py -c "import psutil, colorama, flask; print('All dependencies installed!')"
```

## 🎯 Quick Commands for VS Code

### Essential Commands
```bash
# Install dependencies
py -m pip install -r requirements.txt

# Run CLI terminal
py terminal.py

# Run web terminal
py web_terminal.py

# Run demo
py demo.py

# Check if everything works
py -c "from terminal import TerminalBackend; print('Success!')"
```

### Testing Commands
```bash
# Test basic functionality
py -c "from terminal import TerminalBackend; t = TerminalBackend(); print(t.execute_command('whoami'))"

# Test web server
py -c "from web_terminal import app; print('Web server ready!')"
```

## 🔧 VS Code Extensions (Recommended)

Install these extensions for better experience:

1. **Python** - Microsoft
2. **Python Debugger** - Microsoft
3. **Python Docstring Generator** - Nils Werner
4. **Python Indent** - Kevin Rose
5. **Python Type Hint** - njqdev

## 🎉 Success Checklist

- [ ] Project opened in VS Code
- [ ] Dependencies installed successfully
- [ ] Terminal opens without errors
- [ ] Basic commands work (`ls`, `pwd`, `whoami`)
- [ ] Web interface accessible (if using web mode)
- [ ] Debugging works (if configured)

## 🆘 Getting Help

If you encounter issues:

1. **Check VS Code Output**: `View` → `Output` → Select "Python"
2. **Check Terminal**: Look for error messages in integrated terminal
3. **Restart VS Code**: Sometimes helps with extension issues
4. **Reinstall Dependencies**: `py -m pip install -r requirements.txt --force-reinstall`

## 🚀 Pro Tips

1. **Use Multiple Terminals**: Split terminal for running different components
2. **Set Up Debugging**: Use launch.json for easy debugging
3. **Use Tasks**: Create custom tasks for common operations
4. **Install Extensions**: Python extensions make development easier
5. **Use IntelliSense**: VS Code provides great code completion

Enjoy coding with your Advanced Python Terminal in VS Code! 🐍✨


