"""
POEF tab for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional
from datetime import datetime

from models.expense import Expense, ExpenseCategory
from models.leader import Leader, POEF_DRINK_PRICE, POEF_SAF_PRICE
from base_components import BaseTab, DataTable, FormDialog

class POEFCountDialog(FormDialog):
    """Dialog for updating POEF counts for leaders."""
    
    def __init__(self, parent, leaders: List[Leader]):
        self.leaders = leaders
        
        # Create fields for each leader
        fields = []
        for leader in leaders:
            fields.append({
                "name": f"drinks_{leader.id}",
                "label": f"{leader.name} - Drinks:",
                "type": "spinbox",
                "from_": 0,
                "to": 1000
            })
            fields.append({
                "name": f"safs_{leader.id}",
                "label": f"{leader.name} - SAFs:",
                "type": "spinbox",
                "from_": 0,
                "to": 1000
            })
        
        super().__init__(parent, "Update POEF Counts", fields)
        
        # Set current values
        for leader in leaders:
            drinks_field = f"drinks_{leader.id}"
            safs_field = f"safs_{leader.id}"
            self.set_field_value(drinks_field, str(leader.poef_drink_count))
            self.set_field_value(safs_field, str(leader.poef_saf_count))
    
    def get_counts(self) -> Dict[str, Dict[str, int]]:
        """Get the POEF counts for each leader."""
        counts = {}
        for leader in self.leaders:
            drinks_field = f"drinks_{leader.id}"
            safs_field = f"safs_{leader.id}"
            
            # Get values with safe conversion
            try:
                drinks_value = self.get_field_value(drinks_field)
                drinks_count = int(drinks_value) if drinks_value else 0
            except (ValueError, TypeError):
                drinks_count = 0
                
            try:
                safs_value = self.get_field_value(safs_field)
                safs_count = int(safs_value) if safs_value else 0
            except (ValueError, TypeError):
                safs_count = 0
            
            counts[leader.id] = {
                "drinks": drinks_count,
                "safs": safs_count
            }
        return counts

class POEFTab(BaseTab):
    """Tab for managing POEF items and tracking consumption."""
    
    def __init__(self, parent, main_window):
        super().__init__(parent, main_window)
    
    def create_widgets(self):
        """Create the POEF tab widgets."""
        # Title
        title_label = ttk.Label(self, text="POEF Management", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Top section - POEF items from receipts
        self.create_poef_items_section(content_frame)
        
        # Bottom section - leader consumption and comparison
        self.create_consumption_section(content_frame)
    
    def create_poef_items_section(self, parent):
        """Create the POEF items section."""
        # POEF items frame
        poef_items_frame = ttk.LabelFrame(parent, text="POEF Items from Receipts")
        poef_items_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(poef_items_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # POEF items table
        columns = [
            {"name": "name", "display": "Item Name", "width": 200},
            {"name": "price", "display": "Price (€)", "width": 80, "anchor": tk.E},
            {"name": "quantity", "display": "Qty", "width": 60, "anchor": tk.E},
            {"name": "total", "display": "Total (€)", "width": 80, "anchor": tk.E},
            {"name": "date", "display": "Date", "width": 100},
            {"name": "receipt", "display": "Receipt", "width": 120}
        ]
        
        self.poef_items_table = DataTable(poef_items_frame, columns, height=8)
        self.poef_items_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def create_consumption_section(self, parent):
        """Create the consumption and comparison section."""
        # Consumption frame
        consumption_frame = ttk.LabelFrame(parent, text="Leader Consumption & Comparison")
        consumption_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top row - summary
        top_row = ttk.Frame(consumption_frame)
        top_row.pack(fill=tk.X, padx=10, pady=5)
        
        # Summary labels
        summary_frame = ttk.Frame(top_row)
        summary_frame.pack(side=tk.RIGHT)
        
        self.total_bought_label = ttk.Label(summary_frame, text="Total Bought: €0.00")
        self.total_bought_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.total_paid_label = ttk.Label(summary_frame, text="Total Paid: €0.00")
        self.total_paid_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.difference_label = ttk.Label(summary_frame, text="Difference: €0.00")
        self.difference_label.pack(side=tk.LEFT)
        
        # Leader consumption table
        columns = [
            {"name": "name", "display": "Leader", "width": 150},
            {"name": "drinks", "display": "Drinks", "width": 80, "anchor": tk.E},
            {"name": "drinks_total", "display": "Drinks Total (€)", "width": 120, "anchor": tk.E},
            {"name": "safs", "display": "SAFs", "width": 80, "anchor": tk.E},
            {"name": "safs_total", "display": "SAFs Total (€)", "width": 120, "anchor": tk.E},
            {"name": "total", "display": "Total (€)", "width": 100, "anchor": tk.E}
        ]
        
        self.consumption_table = DataTable(consumption_frame, columns, height=10)
        self.consumption_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def refresh_data(self):
        """Refresh all POEF data."""
        self.refresh_poef_items()
        self.refresh_consumption()
        self.update_summary()
    
    def refresh_poef_items(self):
        """Refresh the POEF items table."""
        receipts = self.main_window.get_receipts()
        
        # Clear table
        self.poef_items_table.clear_data()
        
        # Get all POEF items from receipts
        poef_items = []
        for receipt in receipts:
            for item in receipt.items:
                if item.category == ExpenseCategory.POEF:
                    poef_items.append((item, receipt))
        
        # Add POEF items to table
        for item, receipt in poef_items:
            self.poef_items_table.add_row([
                item.name,
                f"€{item.price:.2f}",
                str(item.quantity),
                f"€{item.get_total_price():.2f}",
                item.date,
                f"{receipt.store_name} ({receipt.date})"
            ])
    
    def refresh_consumption(self):
        """Refresh the leader consumption table."""
        leaders = self.main_window.get_leaders()
        
        # Clear table
        self.consumption_table.clear_data()
        
        # Add leader consumption to table
        for leader in leaders:
            drinks_total = leader.poef_drink_count * POEF_DRINK_PRICE
            safs_total = leader.poef_saf_count * POEF_SAF_PRICE
            total = drinks_total + safs_total
            
            self.consumption_table.add_row([
                leader.name,
                str(leader.poef_drink_count),
                f"€{drinks_total:.2f}",
                str(leader.poef_saf_count),
                f"€{safs_total:.2f}",
                f"€{total:.2f}"
            ])
    
    def update_summary(self):
        """Update the summary labels."""
        receipts = self.main_window.get_receipts()
        leaders = self.main_window.get_leaders()
        
        # Calculate total bought (from receipts)
        total_bought = 0.0
        for receipt in receipts:
            total_bought += receipt.poef_total
        
        # Calculate total paid (from leader consumption)
        total_paid = 0.0
        for leader in leaders:
            total_paid += leader.get_poef_total()
        
        # Calculate difference
        difference = total_bought - total_paid
        
        # Update labels
        self.total_bought_label.config(text=f"Total Bought: €{total_bought:.2f}")
        self.total_paid_label.config(text=f"Total Paid: €{total_paid:.2f}")
        
        # Color code the difference
        if abs(difference) < 0.01:  # Within 1 cent
            self.difference_label.config(text=f"Difference: €{difference:.2f}", foreground="green")
        elif difference > 0:
            self.difference_label.config(text=f"Difference: €{difference:.2f} (Overbought)", foreground="orange")
        else:
            self.difference_label.config(text=f"Difference: €{abs(difference):.2f} (Underbought)", foreground="red")
    
    def update_poef_counts(self):
        """Update POEF counts for all leaders."""
        leaders = self.main_window.get_leaders()
        if not leaders:
            self.show_error("No leaders available")
            return
        
        dialog = POEFCountDialog(self, leaders)
        self.wait_window(dialog)
        
        if dialog.result:
            counts = dialog.get_counts()
            
            # Update leader counts
            for leader in leaders:
                leader_counts = counts.get(leader.id, {})
                leader.poef_drink_count = leader_counts.get("drinks", 0)
                leader.poef_saf_count = leader_counts.get("safs", 0)
            
            self.main_window.save_data()
            self.refresh_consumption()
            self.update_summary()
    
    def get_poef_summary_report(self) -> Dict:
        """Generate a POEF summary report."""
        receipts = self.main_window.get_receipts()
        leaders = self.main_window.get_leaders()
        
        # Calculate totals
        total_bought = sum(receipt.poef_total for receipt in receipts)
        total_paid = sum(leader.get_poef_total() for leader in leaders)
        difference = total_bought - total_paid
        
        # Get POEF items breakdown
        poef_items = []
        for receipt in receipts:
            for item in receipt.items:
                if item.category == ExpenseCategory.POEF:
                    poef_items.append({
                        "name": item.name,
                        "price": item.price,
                        "quantity": item.quantity,
                        "total": item.get_total_price(),
                        "date": item.date,
                        "receipt": f"{receipt.store_name} ({receipt.date})"
                    })
        
        # Get leader breakdown
        leader_breakdown = []
        for leader in leaders:
            drinks_total = leader.poef_drink_count * POEF_DRINK_PRICE
            safs_total = leader.poef_saf_count * POEF_SAF_PRICE
            total = drinks_total + safs_total
            
            leader_breakdown.append({
                "name": leader.name,
                "drinks_count": leader.poef_drink_count,
                "drinks_total": drinks_total,
                "safs_count": leader.poef_saf_count,
                "safs_total": safs_total,
                "total": total
            })
        
        return {
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_bought": total_bought,
            "total_paid": total_paid,
            "difference": difference,
            "poef_items": poef_items,
            "leader_breakdown": leader_breakdown,
            "prices": {
                "drink_price": POEF_DRINK_PRICE,
                "saf_price": POEF_SAF_PRICE
            }
        } 