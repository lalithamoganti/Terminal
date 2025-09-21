# Advanced Python Terminal

A fully functioning command terminal that mimics the behavior of a real system terminal, built with Python backend and featuring both CLI and web-based interfaces.

## Features

### Core Functionality
- **Full-fledged file and directory operations**: `ls`, `cd`, `pwd`, `mkdir`, `rm`, `cp`, `mv`, `cat`, `echo`
- **System monitoring tools**: `ps`, `top`, `df`, `free`, `whoami`, `date`, `uptime`
- **Error handling** for invalid commands with proper exit codes
- **Command history** with arrow key navigation
- **Auto-completion** for commands and file paths
- **Command aliases** (e.g., `ll` = `ls -la`, `..` = `cd ..`)

### Advanced Features
- **AI-driven natural language interpretation**: Type `ai <query>` to convert natural language to terminal commands
- **Clean and responsive interfaces**: Both CLI and web-based interfaces
- **Cross-platform compatibility**: Works on Windows, macOS, and Linux
- **Colored output** for better readability
- **Session management** for web interface

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Set up AI features**:
   - Get an OpenAI API key from [OpenAI](https://platform.openai.com/)
   - Set the environment variable:
     ```bash
     # Windows
     set OPENAI_API_KEY=your_api_key_here
     
     # macOS/Linux
     export OPENAI_API_KEY=your_api_key_here
     ```

## Usage

### Command Line Interface (CLI)

Run the terminal with:
```bash
python terminal.py
```

**Features:**
- Type commands directly
- Use arrow keys for command history
- Tab completion for commands
- Type `help` for available commands
- Type `ai <query>` for natural language commands

**Example AI commands:**
- `ai create a new folder called test and move file1.txt into it`
- `ai show me all running processes`
- `ai find all files larger than 100MB`

### Web Interface

Run the web server with:
```bash
python web_terminal.py
```

Then open your browser and go to: `http://localhost:5000`

**Features:**
- Modern web-based terminal interface
- Real-time command execution
- Command history with click-to-use
- Responsive design
- Session management

## Available Commands

### File Operations
- `ls`, `ll`, `la` - List directory contents
- `cd` - Change directory
- `pwd` - Print working directory
- `mkdir` - Create directory
- `rm` - Remove files/directories
- `rmdir` - Remove empty directories
- `cp` - Copy files/directories
- `mv` - Move/rename files/directories
- `cat` - Display file contents
- `echo` - Echo arguments

### System Information
- `ps` - Show running processes
- `top` - Show top processes by CPU usage
- `df` - Show disk space usage
- `free` - Show memory usage
- `whoami` - Show current user
- `date` - Show current date/time
- `uptime` - Show system uptime

### Terminal Commands
- `clear` - Clear screen
- `history` - Show command history
- `help` - Show help information
- `exit`, `quit` - Exit terminal

### AI Commands
- `ai <query>` - Convert natural language to terminal commands

## Architecture

### Backend (`terminal.py`)
- **TerminalBackend class**: Core terminal functionality
- **Command processing**: Parses and executes commands
- **Built-in commands**: Implements common terminal commands
- **System integration**: Uses `psutil` for system monitoring
- **AI integration**: Uses OpenAI API for natural language processing

### Web Interface (`web_terminal.py`)
- **Flask web server**: Handles HTTP requests
- **Session management**: Maintains terminal state per user
- **RESTful API**: `/execute` endpoint for command execution
- **Real-time updates**: Returns command results via JSON

### Frontend (`templates/terminal.html`)
- **Modern web interface**: Clean, responsive design
- **JavaScript integration**: Handles user input and display
- **Command history**: Arrow key navigation and click-to-use
- **Auto-completion**: Basic command completion support

## Technical Details

### Dependencies
- **psutil**: System and process monitoring
- **colorama**: Cross-platform colored terminal output
- **prompt-toolkit**: Advanced CLI features (history, completion)
- **openai**: AI-powered natural language processing
- **flask**: Web framework for web interface

### Error Handling
- Comprehensive error handling for all commands
- Proper exit codes for command success/failure
- User-friendly error messages
- Graceful handling of permission errors and file not found

### Security Considerations
- Input validation for all commands
- Safe command execution with timeouts
- Session-based isolation for web interface
- No shell injection vulnerabilities

## Examples

### Basic File Operations
```bash
$ ls -la
$ mkdir test_folder
$ cd test_folder
$ echo "Hello World" > hello.txt
$ cat hello.txt
$ cd ..
$ rm -rf test_folder
```

### System Monitoring
```bash
$ ps
$ top
$ df -h
$ free -h
$ uptime
```

### AI-Powered Commands
```bash
$ ai create a backup of all my documents
$ ai show me the largest files in this directory
$ ai find all Python files and show their sizes
```

## Contributing

This terminal is designed to be extensible. You can:

1. **Add new commands**: Extend the `builtin_commands` dictionary
2. **Improve AI integration**: Enhance the natural language processing
3. **Add new interfaces**: Create additional frontend interfaces
4. **Enhance features**: Add more system monitoring capabilities

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

1. **Permission errors**: Make sure you have appropriate permissions for file operations
2. **AI commands not working**: Ensure `OPENAI_API_KEY` environment variable is set
3. **Web interface not loading**: Check if port 5000 is available
4. **Command not found**: Use `help` to see available commands

### Performance Notes

- The terminal is optimized for efficiency
- Large directory listings may take a moment
- AI commands require internet connection
- Web interface maintains session state in memory

## Future Enhancements

- [ ] SSH support for remote connections
- [ ] Plugin system for custom commands
- [ ] Advanced auto-completion with context awareness
- [ ] Terminal themes and customization
- [ ] Multi-user support for web interface
- [ ] Command scripting and automation
- [ ] Integration with version control systems

