#!/usr/bin/env python3
"""
Terminal Demo Script
Demonstrates the capabilities of the Advanced Python Terminal.
"""

import os
import sys
import time
from terminal import TerminalBackend

def run_demo():
    """Run a demonstration of terminal capabilities."""
    print("🐍 Advanced Python Terminal - Demo Mode")
    print("=" * 50)
    print("This demo will showcase various terminal features...")
    print()
    
    terminal = TerminalBackend()
    
    # Demo commands
    demo_commands = [
        "help",
        "whoami",
        "pwd",
        "date",
        "uptime",
        "ls -la",
        "mkdir demo_folder",
        "cd demo_folder",
        "echo 'Hello from Python Terminal!' > demo.txt",
        "cat demo.txt",
        "ls",
        "cd ..",
        "ps",
        "df -h",
        "free -h",
        "history",
        "rm -rf demo_folder"
    ]
    
    print("Running demo commands...")
    print("-" * 30)
    
    for i, command in enumerate(demo_commands, 1):
        print(f"\n[{i:2d}] Executing: {command}")
        print("-" * 40)
        
        output, exit_code = terminal.execute_command(command)
        
        if output:
            print(output)
        
        if exit_code != 0:
            print(f"Command failed with exit code: {exit_code}")
        
        # Small delay for better demo experience
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("Demo completed! Try running the terminal yourself:")
    print("  CLI: python terminal.py")
    print("  Web: python web_terminal.py")
    print("=" * 50)

if __name__ == "__main__":
    run_demo()


