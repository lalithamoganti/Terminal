#!/usr/bin/env python3
"""
Advanced Command Terminal - Python Backend
A fully functioning command terminal that mimics real system terminal behavior.
"""

import os
import sys
import subprocess
import shutil
import platform
import time
import json
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import psutil
from colorama import init, Fore, Back, Style
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter, PathCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import openai

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class TerminalBackend:
    """Core terminal backend that processes and executes commands."""
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.history = []
        self.session = PromptSession(history=InMemoryHistory())
        self.command_history = []
        self.aliases = {
            'll': 'ls -la',
            'la': 'ls -la',
            '..': 'cd ..',
            '...': 'cd ../..',
            'h': 'history',
            'c': 'clear'
        }
        
        # Initialize OpenAI for AI-driven commands (optional)
        self.openai_client = None
        try:
            # You'll need to set OPENAI_API_KEY environment variable
            if os.getenv('OPENAI_API_KEY'):
                self.openai_client = openai.OpenAI()
        except Exception as e:
            print(f"Warning: OpenAI not available: {e}")
    
    def get_prompt(self) -> str:
        """Generate the terminal prompt with current directory and user info."""
        user = os.getenv('USER', os.getenv('USERNAME', 'user'))
        hostname = platform.node()
        cwd = os.path.basename(self.current_dir) if self.current_dir != '/' else '/'
        
        # Color-coded prompt
        prompt_text = f"{Fore.GREEN}{user}@{hostname}{Fore.RESET}:{Fore.BLUE}{cwd}{Fore.RESET}$ "
        return prompt_text
    
    def parse_command(self, command: str) -> Tuple[str, List[str]]:
        """Parse command string into command and arguments."""
        parts = command.strip().split()
        if not parts:
            return "", []
        
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Handle aliases
        if cmd in self.aliases:
            alias_command = self.aliases[cmd]
            return self.parse_command(alias_command)
        
        return cmd, args
    
    def execute_command(self, command: str) -> Tuple[str, int]:
        """Execute a command and return output and exit code."""
        if not command.strip():
            return "", 0
        
        # Add to history
        self.command_history.append(command)
        self.history.append(command)
        
        cmd, args = self.parse_command(command)
        
        # Built-in commands
        if cmd in self.builtin_commands:
            return self.builtin_commands[cmd](args)
        
        # External commands
        try:
            result = subprocess.run(
                [cmd] + args,
                cwd=self.current_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds", 1
        except FileNotFoundError:
            return f"Command not found: {cmd}", 1
        except Exception as e:
            return f"Error executing command: {str(e)}", 1
    
    @property
    def builtin_commands(self):
        """Dictionary of built-in commands."""
        return {
            'cd': self.cmd_cd,
            'ls': self.cmd_ls,
            'pwd': self.cmd_pwd,
            'mkdir': self.cmd_mkdir,
            'rm': self.cmd_rm,
            'rmdir': self.cmd_rmdir,
            'cp': self.cmd_cp,
            'mv': self.cmd_mv,
            'cat': self.cmd_cat,
            'echo': self.cmd_echo,
            'clear': self.cmd_clear,
            'history': self.cmd_history,
            'ps': self.cmd_ps,
            'top': self.cmd_top,
            'df': self.cmd_df,
            'free': self.cmd_free,
            'whoami': self.cmd_whoami,
            'date': self.cmd_date,
            'uptime': self.cmd_uptime,
            'help': self.cmd_help,
            'exit': self.cmd_exit,
            'quit': self.cmd_exit
        }
    
    def cmd_cd(self, args: List[str]) -> Tuple[str, int]:
        """Change directory command."""
        if not args:
            new_dir = os.path.expanduser("~")
        else:
            new_dir = args[0]
        
        try:
            # Handle special directory references
            if new_dir == "~":
                new_dir = os.path.expanduser("~")
            elif new_dir == "-":
                # Go to previous directory
                if hasattr(self, 'prev_dir'):
                    new_dir = self.prev_dir
                else:
                    return "No previous directory", 1
            
            # Store current directory as previous
            self.prev_dir = self.current_dir
            
            # Change directory
            os.chdir(new_dir)
            self.current_dir = os.getcwd()
            return "", 0
        except FileNotFoundError:
            return f"Directory not found: {new_dir}", 1
        except PermissionError:
            return f"Permission denied: {new_dir}", 1
        except Exception as e:
            return f"Error changing directory: {str(e)}", 1
    
    def cmd_ls(self, args: List[str]) -> Tuple[str, int]:
        """List directory contents."""
        try:
            # Parse arguments
            show_all = '-a' in args or '--all' in args
            long_format = '-l' in args or '--long' in args
            human_readable = '-h' in args or '--human-readable' in args
            
            # Determine target directory
            target_dir = args[-1] if args and not args[-1].startswith('-') else self.current_dir
            
            # Get directory contents
            items = os.listdir(target_dir)
            if not show_all:
                items = [item for item in items if not item.startswith('.')]
            
            items.sort()
            
            if long_format:
                return self._format_long_listing(items, target_dir, human_readable), 0
            else:
                return '\n'.join(items), 0
                
        except FileNotFoundError:
            return f"Directory not found: {target_dir}", 1
        except PermissionError:
            return f"Permission denied: {target_dir}", 1
        except Exception as e:
            return f"Error listing directory: {str(e)}", 1
    
    def _format_long_listing(self, items: List[str], target_dir: str, human_readable: bool) -> str:
        """Format directory listing in long format."""
        lines = []
        total_size = 0
        
        for item in items:
            item_path = os.path.join(target_dir, item)
            try:
                stat = os.stat(item_path)
                size = stat.st_size
                total_size += size
                
                # Format permissions
                mode = stat.st_mode
                permissions = self._format_permissions(mode)
                
                # Format size
                if human_readable:
                    size_str = self._format_size(size)
                else:
                    size_str = str(size)
                
                # Format date
                mtime = time.ctime(stat.st_mtime)
                
                # Determine if it's a directory
                is_dir = os.path.isdir(item_path)
                item_name = item + '/' if is_dir else item
                
                lines.append(f"{permissions} {size_str:>8} {mtime} {item_name}")
                
            except (OSError, IOError):
                lines.append(f"?????????? ????????? {item}")
        
        # Add total line
        if human_readable:
            total_str = self._format_size(total_size)
        else:
            total_str = str(total_size)
        
        result = f"total {total_str}\n" + '\n'.join(lines)
        return result
    
    def _format_permissions(self, mode: int) -> str:
        """Format file permissions."""
        permissions = []
        
        # File type
        if os.path.isdir(mode):
            permissions.append('d')
        else:
            permissions.append('-')
        
        # Owner permissions
        permissions.append('r' if mode & 0o400 else '-')
        permissions.append('w' if mode & 0o200 else '-')
        permissions.append('x' if mode & 0o100 else '-')
        
        # Group permissions
        permissions.append('r' if mode & 0o040 else '-')
        permissions.append('w' if mode & 0o020 else '-')
        permissions.append('x' if mode & 0o010 else '-')
        
        # Other permissions
        permissions.append('r' if mode & 0o004 else '-')
        permissions.append('w' if mode & 0o002 else '-')
        permissions.append('x' if mode & 0o001 else '-')
        
        return ''.join(permissions)
    
    def _format_size(self, size: int) -> str:
        """Format size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}PB"
    
    def cmd_pwd(self, args: List[str]) -> Tuple[str, int]:
        """Print working directory."""
        return self.current_dir, 0
    
    def cmd_mkdir(self, args: List[str]) -> Tuple[str, int]:
        """Create directory."""
        if not args:
            return "mkdir: missing operand", 1
        
        for dir_name in args:
            try:
                os.makedirs(dir_name, exist_ok=True)
            except PermissionError:
                return f"Permission denied: {dir_name}", 1
            except Exception as e:
                return f"Error creating directory {dir_name}: {str(e)}", 1
        
        return "", 0
    
    def cmd_rm(self, args: List[str]) -> Tuple[str, int]:
        """Remove files or directories."""
        if not args:
            return "rm: missing operand", 1
        
        recursive = '-r' in args or '-R' in args or '--recursive' in args
        force = '-f' in args or '--force' in args
        
        # Remove flag arguments
        files = [arg for arg in args if not arg.startswith('-')]
        
        for file_path in files:
            try:
                if os.path.isdir(file_path):
                    if recursive:
                        shutil.rmtree(file_path)
                    else:
                        return f"rm: cannot remove '{file_path}': Is a directory", 1
                else:
                    os.remove(file_path)
            except FileNotFoundError:
                if not force:
                    return f"rm: cannot remove '{file_path}': No such file or directory", 1
            except PermissionError:
                return f"rm: cannot remove '{file_path}': Permission denied", 1
            except Exception as e:
                return f"rm: cannot remove '{file_path}': {str(e)}", 1
        
        return "", 0
    
    def cmd_rmdir(self, args: List[str]) -> Tuple[str, int]:
        """Remove empty directories."""
        if not args:
            return "rmdir: missing operand", 1
        
        for dir_name in args:
            try:
                os.rmdir(dir_name)
            except FileNotFoundError:
                return f"rmdir: failed to remove '{dir_name}': No such file or directory", 1
            except OSError as e:
                return f"rmdir: failed to remove '{dir_name}': {str(e)}", 1
        
        return "", 0
    
    def cmd_cp(self, args: List[str]) -> Tuple[str, int]:
        """Copy files or directories."""
        if len(args) < 2:
            return "cp: missing file operand", 1
        
        recursive = '-r' in args or '-R' in args or '--recursive' in args
        files = [arg for arg in args if not arg.startswith('-')]
        
        if len(files) < 2:
            return "cp: missing destination file operand after 'source'", 1
        
        source = files[0]
        destination = files[1]
        
        try:
            if os.path.isdir(source):
                if recursive:
                    shutil.copytree(source, destination)
                else:
                    return f"cp: -r not specified; omitting directory '{source}'", 1
            else:
                shutil.copy2(source, destination)
        except FileNotFoundError:
            return f"cp: cannot stat '{source}': No such file or directory", 1
        except PermissionError:
            return f"cp: cannot create '{destination}': Permission denied", 1
        except Exception as e:
            return f"cp: {str(e)}", 1
        
        return "", 0
    
    def cmd_mv(self, args: List[str]) -> Tuple[str, int]:
        """Move or rename files or directories."""
        if len(args) < 2:
            return "mv: missing file operand", 1
        
        source = args[0]
        destination = args[1]
        
        try:
            shutil.move(source, destination)
        except FileNotFoundError:
            return f"mv: cannot stat '{source}': No such file or directory", 1
        except PermissionError:
            return f"mv: cannot create '{destination}': Permission denied", 1
        except Exception as e:
            return f"mv: {str(e)}", 1
        
        return "", 0
    
    def cmd_cat(self, args: List[str]) -> Tuple[str, int]:
        """Display file contents."""
        if not args:
            return "cat: missing operand", 1
        
        output = []
        for file_path in args:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    output.append(f.read())
            except FileNotFoundError:
                return f"cat: {file_path}: No such file or directory", 1
            except PermissionError:
                return f"cat: {file_path}: Permission denied", 1
            except Exception as e:
                return f"cat: {file_path}: {str(e)}", 1
        
        return '\n'.join(output), 0
    
    def cmd_echo(self, args: List[str]) -> Tuple[str, int]:
        """Echo arguments."""
        return ' '.join(args), 0
    
    def cmd_clear(self, args: List[str]) -> Tuple[str, int]:
        """Clear the screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        return "", 0
    
    def cmd_history(self, args: List[str]) -> Tuple[str, int]:
        """Show command history."""
        if not self.command_history:
            return "No commands in history", 0
        
        history_output = []
        for i, cmd in enumerate(self.command_history[-20:], 1):  # Show last 20 commands
            history_output.append(f"{i:4d}  {cmd}")
        
        return '\n'.join(history_output), 0
    
    def cmd_ps(self, args: List[str]) -> Tuple[str, int]:
        """Show running processes."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    processes.append(f"{proc_info['pid']:6d} {proc_info['name']:20s} {proc_info['cpu_percent']:6.1f}% {proc_info['memory_percent']:6.1f}%")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            header = "PID    NAME                 CPU%   MEM%"
            return header + '\n' + '\n'.join(processes), 0
        except Exception as e:
            return f"Error getting process list: {str(e)}", 1
    
    def cmd_top(self, args: List[str]) -> Tuple[str, int]:
        """Show top processes by CPU usage."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] is not None:
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            output = ["PID    NAME                 CPU%   MEM%"]
            for proc in processes[:10]:  # Top 10
                output.append(f"{proc['pid']:6d} {proc['name']:20s} {proc['cpu_percent']:6.1f}% {proc['memory_percent']:6.1f}%")
            
            return '\n'.join(output), 0
        except Exception as e:
            return f"Error getting top processes: {str(e)}", 1
    
    def cmd_df(self, args: List[str]) -> Tuple[str, int]:
        """Show disk space usage."""
        try:
            partitions = psutil.disk_partitions()
            output = ["Filesystem     1K-blocks     Used Available Use% Mounted on"]
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total = usage.total // 1024
                    used = usage.used // 1024
                    available = usage.free // 1024
                    percent = (used / total) * 100 if total > 0 else 0
                    
                    output.append(f"{partition.device:15s} {total:8d} {used:8d} {available:8d} {percent:4.1f}% {partition.mountpoint}")
                except PermissionError:
                    continue
            
            return '\n'.join(output), 0
        except Exception as e:
            return f"Error getting disk usage: {str(e)}", 1
    
    def cmd_free(self, args: List[str]) -> Tuple[str, int]:
        """Show memory usage."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            output = [
                "              total        used        free      shared  buff/cache   available",
                f"Mem:        {memory.total:10d} {memory.used:10d} {memory.available:10d} {memory.shared:10d} {memory.buffers + memory.cached:10d} {memory.available:10d}",
                f"Swap:       {swap.total:10d} {swap.used:10d} {swap.free:10d} {0:10d} {0:10d} {swap.free:10d}"
            ]
            
            return '\n'.join(output), 0
        except Exception as e:
            return f"Error getting memory info: {str(e)}", 1
    
    def cmd_whoami(self, args: List[str]) -> Tuple[str, int]:
        """Show current user."""
        return os.getenv('USER', os.getenv('USERNAME', 'unknown')), 0
    
    def cmd_date(self, args: List[str]) -> Tuple[str, int]:
        """Show current date and time."""
        return time.strftime("%a %b %d %H:%M:%S %Z %Y"), 0
    
    def cmd_uptime(self, args: List[str]) -> Tuple[str, int]:
        """Show system uptime."""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            return f"up {days} days, {hours} hours, {minutes} minutes", 0
        except Exception as e:
            return f"Error getting uptime: {str(e)}", 1
    
    def cmd_help(self, args: List[str]) -> Tuple[str, int]:
        """Show help information."""
        help_text = """
Available commands:
  File Operations:
    ls, ll, la     - List directory contents
    cd             - Change directory
    pwd            - Print working directory
    mkdir          - Create directory
    rm             - Remove files/directories
    rmdir          - Remove empty directories
    cp             - Copy files/directories
    mv             - Move/rename files/directories
    cat            - Display file contents
    echo           - Echo arguments
  
  System Information:
    ps             - Show running processes
    top            - Show top processes by CPU
    df             - Show disk space usage
    free           - Show memory usage
    whoami         - Show current user
    date           - Show current date/time
    uptime         - Show system uptime
  
  Terminal:
    clear          - Clear screen
    history        - Show command history
    help           - Show this help
    exit, quit     - Exit terminal
  
  Aliases:
    ll = ls -la
    la = ls -la
    .. = cd ..
    ... = cd ../..
    h = history
    c = clear
        """
        return help_text.strip(), 0
    
    def cmd_exit(self, args: List[str]) -> Tuple[str, int]:
        """Exit the terminal."""
        return "Goodbye!", -1  # Special exit code
    
    def interpret_natural_language(self, query: str) -> str:
        """Interpret natural language queries into commands (AI-driven)."""
        if not self.openai_client:
            return "AI interpretation not available. Set OPENAI_API_KEY environment variable."
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a terminal command interpreter. Convert natural language requests into appropriate terminal commands. Only respond with the command, no explanations."},
                    {"role": "user", "content": f"Convert this to a terminal command: {query}"}
                ],
                max_tokens=100,
                temperature=0.1
            )
            
            command = response.choices[0].message.content.strip()
            return command
        except Exception as e:
            return f"Error interpreting natural language: {str(e)}"
    
    def run(self):
        """Main terminal loop."""
        print(f"{Fore.CYAN}Welcome to Advanced Python Terminal!{Fore.RESET}")
        print(f"{Fore.YELLOW}Type 'help' for available commands or 'exit' to quit.{Fore.RESET}")
        print(f"{Fore.GREEN}AI-powered natural language interpretation is available!{Fore.RESET}")
        print()
        
        # Set up auto-completion
        commands = list(self.builtin_commands.keys()) + list(self.aliases.keys())
        completer = WordCompleter(commands, ignore_case=True)
        
        while True:
            try:
                # Get user input with auto-completion and history
                user_input = self.session.prompt(
                    self.get_prompt(),
                    completer=completer,
                    auto_suggest=AutoSuggestFromHistory(),
                    complete_while_typing=True
                )
                
                # Check for AI interpretation
                if user_input.startswith('ai '):
                    query = user_input[3:].strip()
                    if query:
                        interpreted_command = self.interpret_natural_language(query)
                        print(f"{Fore.MAGENTA}AI interpreted: {interpreted_command}{Fore.RESET}")
                        user_input = interpreted_command
                
                # Execute command
                output, exit_code = self.execute_command(user_input)
                
                # Handle special exit code
                if exit_code == -1:
                    print(output)
                    break
                
                # Display output
                if output:
                    print(output)
                
                # Show error for non-zero exit codes
                if exit_code != 0 and not output:
                    print(f"{Fore.RED}Command failed with exit code {exit_code}{Fore.RESET}")
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' to quit the terminal{Fore.RESET}")
            except EOFError:
                print(f"\n{Fore.YELLOW}Goodbye!{Fore.RESET}")
                break
            except Exception as e:
                print(f"{Fore.RED}Unexpected error: {str(e)}{Fore.RESET}")

def main():
    """Main entry point."""
    terminal = TerminalBackend()
    terminal.run()

if __name__ == "__main__":
    main()

