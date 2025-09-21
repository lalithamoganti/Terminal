# Advanced Python Terminal - Complete Setup Guide

## 📋 Prerequisites

Before running the project, ensure you have:
- Python 3.7 or higher installed
- Internet connection (for installing dependencies and AI features)
- Windows, macOS, or Linux operating system

## 🚀 Step-by-Step Setup

### Step 1: Verify Python Installation

**Windows:**
```cmd
py --version
```
You should see something like: `Python 3.13.0`

**macOS/Linux:**
```bash
python3 --version
```
You should see something like: `Python 3.9.0` or higher

### Step 2: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project folder:
```bash
cd C:\Users\_MSI_\codemint
```

### Step 3: Install Dependencies

**Option A: Automatic Installation (Windows)**
```cmd
install.bat
```

**Option B: Manual Installation**
```bash
# Windows
py -m pip install -r requirements.txt

# macOS/Linux
python3 -m pip install -r requirements.txt
```

**Expected Output:**
```
Collecting psutil==5.9.6
  Downloading psutil-5.9.6-cp39-cp39-win_amd64.whl (245 kB)
Collecting colorama==0.4.6
  Downloading colorama-0.4.6-py2.py3-none-any.whl (16 kB)
...
Successfully installed psutil-5.9.6 colorama-0.4.6 prompt-toolkit-3.0.43 openai-1.3.0 flask-3.0.0
```

### Step 4: (Optional) Set up AI Features

To enable AI-powered natural language commands:

1. Get an OpenAI API key from [https://platform.openai.com/](https://platform.openai.com/)
2. Set the environment variable:

**Windows:**
```cmd
set OPENAI_API_KEY=your_api_key_here
```

**macOS/Linux:**
```bash
export OPENAI_API_KEY=your_api_key_here
```

## 🎮 Running the Terminal

### Method 1: Easy Launcher (Windows)

Double-click `run_terminal.bat` and choose your preferred interface:
- Option 1: CLI Terminal
- Option 2: Web Terminal  
- Option 3: Demo Mode

### Method 2: Command Line

**CLI Terminal:**
```bash
# Windows
py terminal.py

# macOS/Linux
python3 terminal.py
```

**Web Terminal:**
```bash
# Windows
py web_terminal.py

# macOS/Linux
python3 web_terminal.py
```

**Demo Mode:**
```bash
# Windows
py demo.py

# macOS/Linux
python3 demo.py
```

### Method 3: Using the Launcher Script

```bash
# CLI Terminal
py run_terminal.py --mode cli

# Web Terminal
py run_terminal.py --mode web --port 5000

# Demo Mode
py run_terminal.py --mode demo
```

## 🌐 Web Interface Access

When you run the web terminal:
1. Open your web browser
2. Go to: `http://localhost:5000`
3. You'll see a modern terminal interface
4. Start typing commands!

## 📱 Interface Options

### CLI Terminal Features
- **Command History**: Use ↑/↓ arrow keys
- **Auto-completion**: Press Tab for suggestions
- **Colored Output**: Different colors for different types of output
- **AI Commands**: Type `ai <query>` for natural language commands

### Web Terminal Features
- **Modern Interface**: Clean, responsive design
- **Command History**: Click on history items to reuse
- **Real-time Updates**: Instant command execution
- **Mobile Friendly**: Works on phones and tablets

## 🧪 Testing the Installation

### Quick Test Commands

1. **Basic File Operations:**
   ```bash
   ls
   pwd
   mkdir test_folder
   cd test_folder
   echo "Hello World" > hello.txt
   cat hello.txt
   cd ..
   rm -rf test_folder
   ```

2. **System Information:**
   ```bash
   whoami
   date
   uptime
   ps
   df -h
   ```

3. **AI Commands (if API key is set):**
   ```bash
   ai create a new folder called demo
   ai show me all running processes
   ai find the largest files in this directory
   ```

### Demo Mode
Run the demo to see all features in action:
```bash
py demo.py
```

## 🔧 Troubleshooting

### Common Issues and Solutions

**1. "Python was not found"**
- **Windows**: Use `py` instead of `python`
- **macOS/Linux**: Install Python from [python.org](https://python.org)

**2. "Module not found" errors**
```bash
# Reinstall dependencies
py -m pip install -r requirements.txt --force-reinstall
```

**3. "Permission denied" errors**
- Run terminal as administrator (Windows)
- Use `sudo` for system commands (macOS/Linux)

**4. Web interface not loading**
- Check if port 5000 is available
- Try a different port: `py run_terminal.py --mode web --port 8080`

**5. AI commands not working**
- Verify your OpenAI API key is set correctly
- Check your internet connection
- Ensure you have credits in your OpenAI account

### Port Conflicts

If port 5000 is busy, use a different port:
```bash
py run_terminal.py --mode web --port 8080
```
Then access: `http://localhost:8080`

## 📊 Performance Tips

1. **First Run**: May take a moment to load dependencies
2. **Large Directories**: `ls` on large directories may take a few seconds
3. **AI Commands**: Require internet connection and may take 2-3 seconds
4. **Memory Usage**: Typically uses < 50MB RAM

## 🎯 Quick Start Checklist

- [ ] Python installed and working
- [ ] Dependencies installed successfully
- [ ] Project files in correct directory
- [ ] Terminal starts without errors
- [ ] Basic commands work (`ls`, `pwd`, `whoami`)
- [ ] Web interface accessible (if using web mode)
- [ ] AI features working (optional)

## 🆘 Getting Help

If you encounter issues:

1. **Check the README.md** for detailed documentation
2. **Run the demo** to see expected behavior
3. **Check error messages** for specific issues
4. **Verify Python version** (3.7+ required)
5. **Reinstall dependencies** if needed

## 🎉 Success!

Once everything is working, you'll have:
- A fully functional command terminal
- Both CLI and web interfaces
- AI-powered natural language commands
- Complete file and system operations
- Modern, responsive design

Enjoy your new Advanced Python Terminal! 🐍


