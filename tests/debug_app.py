#!/usr/bin/env python3
"""
Debug version of Kamp Finances to help identify saving issues.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import tkinter as tk
from tkinter import ttk, messagebox

from models.leader import Leader
from services.finance_service import FinanceService
from services.data_service import DataService
from ui.main_window import MainWindow

class DebugKampFinancesApp:
    """Debug version of the main application."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kamp Finances - DEBUG MODE")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        print("🔧 DEBUG: Initializing application...")
        
        # Initialize services
        self.data_service = DataService()
        self.finance_service = FinanceService(self.data_service)
        
        # Load existing data
        self.leaders = self.data_service.load_leaders()
        self.receipts = self.data_service.load_receipts()
        
        print(f"🔧 DEBUG: Loaded {len(self.leaders)} leaders and {len(self.receipts)} receipts")
        
        # Create main window with data references
        self.main_window = MainWindow(
            self.root, 
            self.finance_service,
            self.data_service,
            self.leaders,  # Pass reference to leaders list
            self.receipts  # Pass reference to receipts list
        )
        
        # Override the add_leader method to add debugging
        original_add_leader = self.main_window.add_leader
        def debug_add_leader(leader):
            print(f"🔧 DEBUG: Adding leader: {leader.name}")
            print(f"🔧 DEBUG: Leaders before adding: {len(self.leaders)}")
            original_add_leader(leader)
            print(f"🔧 DEBUG: Leaders after adding: {len(self.leaders)}")
            print(f"🔧 DEBUG: Checking if leader is in list...")
            found = any(l.name == leader.name for l in self.leaders)
            print(f"🔧 DEBUG: Leader found in list: {found}")
            
            # Force save and check file
            print("🔧 DEBUG: Forcing save...")
            self.data_service.save_all_data(self.leaders, self.receipts)
            
            # Load from file to verify
            loaded = self.data_service.load_leaders()
            file_found = any(l.name == leader.name for l in loaded)
            print(f"🔧 DEBUG: Leader found in file: {file_found}")
            print(f"🔧 DEBUG: Total leaders in file: {len(loaded)}")
        
        self.main_window.add_leader = debug_add_leader
        
        # Configure style
        self._setup_styles()
        
        print("🔧 DEBUG: Application initialized successfully")
    
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
        print("🔧 DEBUG: Starting application...")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application interrupted by user")
        finally:
            print("🔧 DEBUG: Application closing, saving data...")
            # Save data before closing
            self.data_service.save_all_data(
                self.leaders, 
                self.receipts
            )
            print("🔧 DEBUG: Data saved")

def main():
    """Main entry point."""
    print("🚀 Starting Kamp Finances in DEBUG MODE...")
    app = DebugKampFinancesApp()
    app.run()

if __name__ == "__main__":
    main() 