#!/usr/bin/env python3
"""
Kamp Finances - Scouting Trip Finance Manager
A Python application to manage expenses during scouting trips.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from typing import Dict, List, Optional

# Import our modules
from models.leader import Leader
from models.receipt import Receipt
from models.expense import Expense, ExpenseCategory
from services.finance_service import FinanceService
from services.data_service import DataService
from ui.main_window import MainWindow


class KampFinancesApp:
    """Main application class for Kamp Finances."""
    
    def __init__(self):
        # Initialize the main window
        self.main_window = MainWindow()
        
        # Configure style
        self._setup_styles()
    
    def _setup_styles(self):
        """Configure application styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Warning.TLabel', foreground='orange')
        style.configure('Error.TLabel', foreground='red')
    
    def run(self):
        """Start the application."""
        try:
            self.main_window.run()
        except KeyboardInterrupt:
            print("Application interrupted by user")
        finally:
            # Data is automatically saved by the new main window
            pass

def main():
    """Main entry point."""
    app = KampFinancesApp()
    app.run()

if __name__ == "__main__":
    main()
