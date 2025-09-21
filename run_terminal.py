#!/usr/bin/env python3
"""
Terminal Launcher Script
Provides an easy way to launch either the CLI or web interface.
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Advanced Python Terminal Launcher')
    parser.add_argument('--mode', choices=['cli', 'web'], default='cli',
                       help='Choose interface mode: cli or web (default: cli)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port for web interface (default: 5000)')
    parser.add_argument('--host', default='0.0.0.0',
                       help='Host for web interface (default: 0.0.0.0)')
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        print("Starting CLI Terminal...")
        print("=" * 50)
        try:
            from terminal import main as cli_main
            cli_main()
        except ImportError as e:
            print(f"Error importing terminal module: {e}")
            print("Make sure all dependencies are installed: pip install -r requirements.txt")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nTerminal closed.")
            sys.exit(0)
    
    elif args.mode == 'web':
        print("Starting Web Terminal...")
        print("=" * 50)
        print(f"Web interface will be available at: http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        try:
            from web_terminal import app
            app.run(debug=False, host=args.host, port=args.port)
        except ImportError as e:
            print(f"Error importing web_terminal module: {e}")
            print("Make sure all dependencies are installed: pip install -r requirements.txt")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nWeb server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    main()


