#!/usr/bin/env python3
"""
Launch DAG Visualizer

This script launches the DAG visualization system with all necessary components.
"""

import os
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import flask
        import flask_cors

        print("✅ Flask dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please install requirements: pip install -r requirements_dag.txt")
        return False


def start_server():
    """Start the Flask server in a separate thread."""
    try:
        from dag_server import app

        print("🚀 Starting DAG visualization server...")
        app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
    except Exception as e:
        print(f"❌ Error starting server: {e}")


def open_browser():
    """Open the browser to the visualization interface."""
    time.sleep(2)  # Wait for server to start
    try:
        webbrowser.open("http://localhost:5000")
        print("🌐 Opening browser to visualization interface...")
    except Exception as e:
        print(f"❌ Error opening browser: {e}")


def main():
    """Main launcher function."""
    print("🤖 Robot Skills DAG Visualizer Launcher")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Check if skills files exist
    required_files = [
        "skills_main.py",
        "skills_tier0.py",
        "skills_tier1.py",
        "skills_tier2.py",
        "skill_composition_analyzer.py",
        "dag_server.py",
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        sys.exit(1)

    print("✅ All required files found")

    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Open browser
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    print("\n🎯 DAG Visualizer is running!")
    print("📊 Features:")
    print("  • Interactive skill hierarchy visualization")
    print("  • Skill composition analysis")
    print("  • Execution path visualization")
    print("  • Workflow builder")
    print("  • Real-time skill statistics")
    print("\n🌐 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")

    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down DAG visualizer...")
        sys.exit(0)


if __name__ == "__main__":
    main()
