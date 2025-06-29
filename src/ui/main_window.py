"""
New main window for Kamp Finances application with modular tab system.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Optional
import os

from models.leader import Leader
from models.receipt import Receipt
from services.data_service import DataService
from services.finance_service import FinanceService
from ui.tabs.leaders_tab import LeadersTab
from ui.tabs.receipts_tab import ReceiptsTab
from ui.tabs.pa_items_tab import PAItemsTab
from ui.tabs.poef_tab import POEFTab

class MainWindow(tk.Tk):
    """Main application window with modular tab system."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize services
        self.data_service = DataService()
        self.finance_service = FinanceService(self.data_service)
        
        # Setup window
        self.setup_window()
        self.create_widgets()
        self.apply_styles()
        
        # Load data after UI is created
        self.load_data()
        
        # Refresh all tabs
        self.refresh_all_tabs()
    
    def setup_window(self):
        """Setup the main window properties."""
        self.title("Kamp Finances - New UI")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create the main window widgets."""
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_container, text="Kamp Finances Management System", style="MainTitle.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_tabs()
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_tabs(self):
        """Create all the application tabs."""
        # Leaders tab
        self.leaders_tab = LeadersTab(self.notebook, self)
        self.notebook.add(self.leaders_tab, text="Leaders")
        
        # Receipts tab
        self.receipts_tab = ReceiptsTab(self.notebook, self)
        self.notebook.add(self.receipts_tab, text="Receipts")
        
        # PA Items tab
        self.pa_items_tab = PAItemsTab(self.notebook, self)
        self.notebook.add(self.pa_items_tab, text="PA Items")
        
        # POEF tab
        self.poef_tab = POEFTab(self.notebook, self)
        self.notebook.add(self.poef_tab, text="POEF")
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def create_status_bar(self, parent):
        """Create the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="Ready", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT)
        
        # Data info
        self.data_info_label = ttk.Label(status_frame, text="", style="Status.TLabel")
        self.data_info_label.pack(side=tk.RIGHT)
    
    def apply_styles(self):
        """Apply custom styles to the application."""
        style = ttk.Style()
        
        # Configure styles
        style.configure("MainTitle.TLabel", font=("Arial", 16, "bold"))
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure("Status.TLabel", font=("Arial", 9))
    
    def load_data(self):
        """Load data from files."""
        try:
            # Load leaders and receipts separately
            leaders = self.data_service.load_leaders()
            receipts = self.data_service.load_receipts()
            
            # Store data in the service
            self.data_service.leaders = leaders
            self.data_service.receipts = receipts
            
            self.status_label.config(text="Data loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.status_label.config(text="Failed to load data")
    
    def save_data(self):
        """Save data to files."""
        try:
            leaders = self.get_leaders()
            receipts = self.get_receipts()
            self.data_service.save_all_data(leaders, receipts)
            self.status_label.config(text="Data saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            self.status_label.config(text="Failed to save data")
    
    def refresh_all_tabs(self):
        """Refresh all tabs."""
        self.leaders_tab.refresh_data()
        self.receipts_tab.refresh_data()
        self.pa_items_tab.refresh_data()
        self.poef_tab.refresh_data()
        self.update_data_info()
    
    def update_data_info(self):
        """Update the data info in the status bar."""
        leaders = self.get_leaders()
        receipts = self.get_receipts()
        
        info_text = f"Leaders: {len(leaders)} | Receipts: {len(receipts)}"
        self.data_info_label.config(text=info_text)
    
    def on_tab_changed(self, event):
        """Handle tab change events."""
        current_tab = self.notebook.select()
        tab_widget = self.nametowidget(current_tab)
        tab_name = self.notebook.tab(current_tab, "text")
        self.status_label.config(text=f"Current tab: {tab_name}")
        # Refresh data for the selected tab if possible
        if hasattr(tab_widget, 'refresh_data'):
            tab_widget.refresh_data()
    
    # Data access methods for tabs
    def get_leaders(self) -> List[Leader]:
        """Get all leaders."""
        return getattr(self.data_service, 'leaders', [])
    
    def get_receipts(self) -> List[Receipt]:
        """Get all receipts."""
        return getattr(self.data_service, 'receipts', [])
    
    def get_leader_by_id(self, leader_id: str) -> Optional[Leader]:
        """Get a leader by ID."""
        leaders = self.get_leaders()
        for leader in leaders:
            if leader.id == leader_id:
                return leader
        return None
    
    def get_receipt_by_id(self, receipt_id: str) -> Optional[Receipt]:
        """Get a receipt by ID."""
        receipts = self.get_receipts()
        for receipt in receipts:
            if receipt.id == receipt_id:
                return receipt
        return None
    
    def add_leader(self, leader: Leader):
        """Add a new leader."""
        leaders = self.get_leaders()
        leaders.append(leader)
        self.data_service.leaders = leaders
        self.save_data()
        self.refresh_all_tabs()
    
    def remove_leader(self, leader_id: str):
        """Remove a leader by ID."""
        leaders = self.get_leaders()
        leaders = [l for l in leaders if l.id != leader_id]
        self.data_service.leaders = leaders
        self.save_data()
        self.refresh_all_tabs()
    
    def add_receipt(self, receipt: Receipt):
        """Add a new receipt."""
        receipts = self.get_receipts()
        receipts.append(receipt)
        self.data_service.receipts = receipts
        self.save_data()
        self.refresh_all_tabs()
    
    def remove_receipt(self, receipt_id: str):
        """Remove a receipt by ID and clean up all references."""
        receipts = self.get_receipts()
        
        # Find the receipt to be removed
        receipt_to_remove = None
        for receipt in receipts:
            if receipt.id == receipt_id:
                receipt_to_remove = receipt
                break
        
        if not receipt_to_remove:
            return
        
        # Clean up PA expenses from leaders
        leaders = self.get_leaders()
        for leader in leaders:
            # Remove all PA expenses from this receipt
            expenses_to_remove = []
            for expense_id, amount in leader.pa_purchases.items():
                # Check if this expense belongs to the receipt being removed
                for expense in receipt_to_remove.items:
                    if expense.id == expense_id and expense.category.value == "PA":
                        expenses_to_remove.append(expense_id)
                        break
            
            # Remove the expenses
            for expense_id in expenses_to_remove:
                leader.remove_pa_purchase(expense_id, 0)
        
        # Remove the receipt from the list
        receipts = [r for r in receipts if r.id != receipt_id]
        self.data_service.receipts = receipts
        
        # Delete the receipt's items CSV file
        try:
            import os
            items_file = os.path.join(self.data_service.data_dir, f"receipt_items_{receipt_id}.csv")
            if os.path.exists(items_file):
                os.remove(items_file)
        except Exception as e:
            print(f"Warning: Could not delete receipt items file: {e}")
        
        # Save the updated data
        self.save_data()
        self.refresh_all_tabs()
    
    def export_summary(self):
        """Export a global summary report."""
        # Implementation placeholder
        pass
    
    def export_leader_details(self, leader: Leader):
        """Export details for a specific leader."""
        # Implementation placeholder
        pass
    
    def write_summary_to_file(self, filepath: str, summary: dict):
        """Write a summary report to a file."""
        # Implementation placeholder
        pass
    
    def write_leader_details_to_file(self, filepath: str, leader: Leader):
        """Write leader details to a file."""
        # Implementation placeholder
        pass
    
    def get_timestamp(self) -> str:
        """Get a timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def run(self):
        """Start the main loop."""
        self.mainloop()

def main():
    app = NewMainWindow()
    app.run()
