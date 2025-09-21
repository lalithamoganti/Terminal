#!/usr/bin/env python3
"""
Vercel-compatible Flask app for Advanced Python Terminal
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session
import uuid
from terminal import TerminalBackend

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Store terminal instances per session
terminals = {}

def get_terminal():
    """Get or create terminal instance for current session."""
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    
    if session_id not in terminals:
        terminals[session_id] = TerminalBackend()
    
    return terminals[session_id]

@app.route('/')
def index():
    """Main terminal page."""
    return render_template('terminal.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    """Execute a command and return the result."""
    data = request.get_json()
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'output': '', 'exit_code': 0, 'prompt': get_terminal().get_prompt()})
    
    terminal = get_terminal()
    
    # Handle AI interpretation
    if command.startswith('ai '):
        query = command[3:].strip()
        if query:
            interpreted_command = terminal.interpret_natural_language(query)
            return jsonify({
                'output': f"AI interpreted: {interpreted_command}",
                'exit_code': 0,
                'prompt': terminal.get_prompt(),
                'ai_interpreted': interpreted_command
            })
    
    # Execute command
    output, exit_code = terminal.execute_command(command)
    
    # Handle special exit code
    if exit_code == -1:
        return jsonify({
            'output': output,
            'exit_code': exit_code,
            'prompt': terminal.get_prompt(),
            'should_exit': True
        })
    
    return jsonify({
        'output': output,
        'exit_code': exit_code,
        'prompt': terminal.get_prompt()
    })

@app.route('/history')
def get_history():
    """Get command history."""
    terminal = get_terminal()
    return jsonify({'history': terminal.command_history})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear command history."""
    terminal = get_terminal()
    terminal.command_history.clear()
    return jsonify({'success': True})

@app.route('/files')
def get_files():
    """Get current directory files."""
    import os
    try:
        files = []
        for item in os.listdir('.'):
            is_dir = os.path.isdir(item)
            files.append({
                'name': item,
                'isDirectory': is_dir,
                'size': os.path.getsize(item) if not is_dir else 0
            })
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'files': [], 'error': str(e)})

@app.route('/stats')
def get_stats():
    """Get system statistics."""
    import psutil
    import time
    
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        
        # Process count
        process_count = len(psutil.pids())
        
        # Uptime
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_str = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"
        
        return jsonify({
            'cpu': round(cpu_percent, 1),
            'memory': round(memory_percent, 1),
            'disk': round(disk_percent, 1),
            'processes': process_count,
            'uptime': uptime_str
        })
    except Exception as e:
        return jsonify({
            'cpu': 0,
            'memory': 0,
            'disk': 0,
            'processes': 0,
            'uptime': '0s',
            'error': str(e)
        })

# This is the entry point for Render
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
