#!/usr/bin/env python3
"""
Kamp Finances - Scouting Trip Finance Manager
A Python application to manage expenses during scouting trips.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Import our modules
from models.leader import Leader
from models.receipt import Receipt, ReceiptItem
from models.expense import Expense, ExpenseCategory
from services.finance_service import FinanceService
from services.data_service import DataService
from ui.main_window import MainWindow

class KampFinancesApp:
    """Main application class for Kamp Finances."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kamp Finances - Scouting Trip Manager")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Initialize services
        self.data_service = DataService()
        self.finance_service = FinanceService(self.data_service)
        
        # Load existing data
        self.leaders = self.data_service.load_leaders()
        self.receipts = self.data_service.load_receipts()
        
        # Create main window with data references
        self.main_window = MainWindow(
            self.root, 
            self.finance_service,
            self.data_service,
            self.leaders,  # Pass reference to leaders list
            self.receipts  # Pass reference to receipts list
        )
        
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
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application interrupted by user")
        finally:
            # Save data before closing
            self.data_service.save_all_data(
                self.leaders, 
                self.receipts
            )

def main():
    """Main entry point."""
    app = KampFinancesApp()
    app.run()

if __name__ == "__main__":
    main()
