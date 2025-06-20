#!/usr/bin/env python3
"""
Launcher script for Kamp Finances application.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Launch the Kamp Finances application."""
    try:
        from main import main as app_main
        print("🚀 Starting Kamp Finances...")
        app_main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 