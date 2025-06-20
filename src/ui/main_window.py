"""
Main window UI for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict

from models.leader import Leader
from models.receipt import Receipt, ExpenseCategory
from services.finance_service import FinanceService
from services.data_service import DataService

from ui.leaders_tab import LeadersTab
from ui.receipts_tab import ReceiptsTab
from ui.poef_tab import PoefTab
from ui.summary_tab import SummaryTab

class MainWindow:
    """Main application window with tabbed interface."""
    
    def __init__(self, root: tk.Tk, finance_service: FinanceService, data_service: DataService, leaders: List[Leader], receipts: List[Receipt]):
        self.root = root
        self.finance_service = finance_service
        self.data_service = data_service
        
        # Use data references from main app
        self.leaders = leaders
        self.receipts = receipts
        
        # Create UI first
        self.create_widgets()
        self.setup_bindings()
        
        # Update displays (data is already loaded)
        self.refresh_all_tabs()
    
    def create_widgets(self):
        """Create the main UI widgets."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.leaders_tab = LeadersTab(self.notebook, self)
        self.receipts_tab = ReceiptsTab(self.notebook, self)
        self.poef_tab = PoefTab(self.notebook, self)
        self.summary_tab = SummaryTab(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.add(self.leaders_tab, text="Leaders")
        self.notebook.add(self.receipts_tab, text="Receipts")
        self.notebook.add(self.poef_tab, text="POEF")
        self.notebook.add(self.summary_tab, text="Summary")
        
        # Create status bar
        self.create_status_bar()
        
        # Create menu bar
        self.create_menu_bar()
    
    def create_status_bar(self):
        """Create status bar at bottom of window."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Add save indicator
        self.save_indicator = ttk.Label(self.status_frame, text="", foreground="green")
        self.save_indicator.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def create_menu_bar(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save All", command=self.save_all_data)
        file_menu.add_command(label="Export Summary", command=self.export_summary)
        file_menu.add_command(label="Backup Data", command=self.backup_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Data menu
        data_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Data", menu=data_menu)
        data_menu.add_command(label="Refresh All", command=self.refresh_all_tabs)
        data_menu.add_command(label="Validate Data", command=self.validate_data)
    
    def setup_bindings(self):
        """Setup event bindings."""
        # Auto-save on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def save_all_data(self):
        """Save all data to storage."""
        try:
            self.data_service.save_all_data(self.leaders, self.receipts)
            self.update_save_indicator("Saved")
            self.update_status("Data saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
            self.update_status("Error saving data")
    
    def export_summary(self):
        """Export summary report."""
        try:
            summary_path = self.data_service.export_summary(self.leaders, self.receipts)
            if summary_path:
                messagebox.showinfo("Success", f"Summary exported to: {summary_path}")
                self.update_status("Summary exported successfully")
            else:
                messagebox.showerror("Error", "Failed to export summary")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export summary: {e}")
    
    def backup_data(self):
        """Create backup of data."""
        try:
            backup_path = self.data_service.backup_data()
            messagebox.showinfo("Success", f"Backup created at: {backup_path}")
            self.update_status("Backup created successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {e}")
    
    def validate_data(self):
        """Validate all data for consistency."""
        errors = []
        
        # Validate receipts
        for receipt in self.receipts:
            is_valid, receipt_errors = self.finance_service.validate_receipt(receipt)
            if not is_valid:
                errors.extend([f"Receipt {receipt.id}: {error}" for error in receipt_errors])
        
        # Check for orphaned PA items
        for receipt in self.receipts:
            pa_items = receipt.get_items_by_category(ExpenseCategory.PA)
            for item in pa_items:
                if item.assigned_to:
                    leader_exists = any(leader.id == item.assigned_to for leader in self.leaders)
                    if not leader_exists:
                        errors.append(f"PA item '{item.name}' assigned to non-existent leader")
        
        if errors:
            error_text = "\n".join(errors)
            messagebox.showerror("Validation Errors", f"Found {len(errors)} errors:\n\n{error_text}")
        else:
            messagebox.showinfo("Validation", "All data is valid!")
    
    def refresh_all_tabs(self):
        """Refresh all tab displays."""
        self.leaders_tab.refresh_display()
        self.receipts_tab.refresh_display()
        self.poef_tab.refresh_display()
        self.summary_tab.refresh_display()
        self.update_status("All displays refreshed")
    
    def on_tab_changed(self, event):
        """Handle tab change events."""
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        self.update_status(f"Switched to {tab_name} tab")
    
    def on_closing(self):
        """Handle window closing."""
        # Auto-save before closing
        self.save_all_data()
        self.root.destroy()
    
    def update_status(self, message: str):
        """Update status bar message."""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
    
    def update_save_indicator(self, message: str):
        """Update save indicator."""
        if hasattr(self, 'save_indicator'):
            self.save_indicator.config(text=message)
            # Clear after 3 seconds
            self.root.after(3000, lambda: self.save_indicator.config(text=""))
    
    def get_leaders(self) -> List[Leader]:
        """Get current leaders list."""
        return self.leaders
    
    def get_receipts(self) -> List[Receipt]:
        """Get current receipts list."""
        return self.receipts
    
    def add_leader(self, leader: Leader):
        """Add a new leader."""
        self.leaders.append(leader)
        self.refresh_all_tabs()
        self.update_save_indicator("Modified")
        self.save_all_data()
    
    def remove_leader(self, leader_id: str):
        """Remove a leader."""
        self.leaders = [l for l in self.leaders if l.id != leader_id]
        self.refresh_all_tabs()
        self.update_save_indicator("Modified")
        self.save_all_data()
    
    def add_receipt(self, receipt: Receipt):
        """Add a new receipt."""
        self.receipts.append(receipt)
        self.refresh_all_tabs()
        self.update_save_indicator("Modified")
        self.save_all_data()
    
    def remove_receipt(self, receipt_id: str):
        """Remove a receipt."""
        self.receipts = [r for r in self.receipts if r.id != receipt_id]
        self.refresh_all_tabs()
        self.update_save_indicator("Modified")
        self.save_all_data() 