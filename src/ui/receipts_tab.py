"""
Receipts tab UI for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from datetime import datetime

from models.receipt import Receipt, ReceiptItem, ExpenseCategory
from ui.dialogs import ReceiptItemDialog, TextMessageDialog

class ReceiptsTab(ttk.Frame):
    """Tab for managing receipts."""
    
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.create_widgets()
    
    def create_widgets(self):
        """Create the receipts tab widgets."""
        # Title
        title_label = ttk.Label(self, text="Manage Receipts", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add receipt button
        add_button = ttk.Button(button_frame, text="Add Receipt", command=self.add_receipt)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Process text message button
        text_button = ttk.Button(button_frame, text="Process Text Message", command=self.process_text_message)
        text_button.pack(side=tk.LEFT, padx=5)
        
        # Remove receipt button
        remove_button = ttk.Button(button_frame, text="Remove Receipt", command=self.remove_receipt)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.refresh_display)
        refresh_button.pack(side=tk.RIGHT, padx=5)
        
        # Create main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - receipts list
        self.create_receipts_list(content_frame)
        
        # Right side - receipt details
        self.create_receipt_details(content_frame)
    
    def create_receipts_list(self, parent):
        """Create the receipts list."""
        # Receipts frame
        receipts_frame = ttk.LabelFrame(parent, text="Receipts")
        receipts_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Create treeview
        columns = ("Date", "Store", "Total", "Groepskas", "POEF", "PA")
        self.receipts_tree = ttk.Treeview(receipts_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.receipts_tree.heading("Date", text="Date")
        self.receipts_tree.heading("Store", text="Store")
        self.receipts_tree.heading("Total", text="Total (€)")
        self.receipts_tree.heading("Groepskas", text="Groepskas (€)")
        self.receipts_tree.heading("POEF", text="POEF (€)")
        self.receipts_tree.heading("PA", text="PA (€)")
        
        # Column widths
        self.receipts_tree.column("Date", width=100)
        self.receipts_tree.column("Store", width=100)
        self.receipts_tree.column("Total", width=80)
        self.receipts_tree.column("Groepskas", width=100)
        self.receipts_tree.column("POEF", width=80)
        self.receipts_tree.column("PA", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(receipts_frame, orient=tk.VERTICAL, command=self.receipts_tree.yview)
        self.receipts_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.receipts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.receipts_tree.bind("<<TreeviewSelect>>", self.on_receipt_selected)
    
    def create_receipt_details(self, parent):
        """Create the receipt details area."""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Receipt Details")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Receipt info
        info_frame = ttk.Frame(details_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Date
        ttk.Label(info_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.date_label = ttk.Label(info_frame, text="", style="Header.TLabel")
        self.date_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Store
        ttk.Label(info_frame, text="Store:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.store_label = ttk.Label(info_frame, text="")
        self.store_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Totals
        ttk.Label(info_frame, text="Total:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=2)
        self.total_label = ttk.Label(info_frame, text="", style="Header.TLabel")
        self.total_label.grid(row=0, column=3, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(info_frame, text="Groepskas:").grid(row=1, column=2, sticky=tk.W, padx=(20, 0), pady=2)
        self.groepskas_label = ttk.Label(info_frame, text="")
        self.groepskas_label.grid(row=1, column=3, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(info_frame, text="POEF:").grid(row=2, column=2, sticky=tk.W, padx=(20, 0), pady=2)
        self.poef_label = ttk.Label(info_frame, text="")
        self.poef_label.grid(row=2, column=3, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(info_frame, text="PA:").grid(row=3, column=2, sticky=tk.W, padx=(20, 0), pady=2)
        self.pa_label = ttk.Label(info_frame, text="")
        self.pa_label.grid(row=3, column=3, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Items frame
        items_frame = ttk.LabelFrame(details_frame, text="Items")
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Items buttons
        items_button_frame = ttk.Frame(items_frame)
        items_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_item_button = ttk.Button(items_button_frame, text="Add Item", command=self.add_item)
        add_item_button.pack(side=tk.LEFT, padx=2)
        
        edit_item_button = ttk.Button(items_button_frame, text="Edit Item", command=self.edit_item)
        edit_item_button.pack(side=tk.LEFT, padx=2)
        
        remove_item_button = ttk.Button(items_button_frame, text="Remove Item", command=self.remove_item)
        remove_item_button.pack(side=tk.LEFT, padx=2)
        
        # Items treeview
        items_tree_frame = ttk.Frame(items_frame)
        items_tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create items treeview
        columns = ("Name", "Price", "Qty", "Total", "Category", "Assigned To")
        self.items_tree = ttk.Treeview(items_tree_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        self.items_tree.heading("Name", text="Name")
        self.items_tree.heading("Price", text="Price (€)")
        self.items_tree.heading("Qty", text="Qty")
        self.items_tree.heading("Total", text="Total (€)")
        self.items_tree.heading("Category", text="Category")
        self.items_tree.heading("Assigned To", text="Assigned To")
        
        # Column widths
        self.items_tree.column("Name", width=150)
        self.items_tree.column("Price", width=80)
        self.items_tree.column("Qty", width=50)
        self.items_tree.column("Total", width=80)
        self.items_tree.column("Category", width=100)
        self.items_tree.column("Assigned To", width=100)
        
        # Scrollbar
        items_scrollbar = ttk.Scrollbar(items_tree_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        # Pack items treeview and scrollbar
        self.items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        items_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def refresh_display(self):
        """Refresh the receipts display."""
        # Clear existing items
        for item in self.receipts_tree.get_children():
            self.receipts_tree.delete(item)
        
        # Get current receipts
        receipts = self.main_window.get_receipts()
        
        # Add receipts to treeview
        for receipt in receipts:
            self.receipts_tree.insert("", tk.END, values=(
                receipt.date,
                receipt.store_name,
                f"€{receipt.total_amount:.2f}",
                f"€{receipt.groepskas_total:.2f}",
                f"€{receipt.poef_total:.2f}",
                f"€{receipt.pa_total:.2f}"
            ), tags=(receipt.id,))
        
        # Clear details
        self.clear_details()
    
    def clear_details(self):
        """Clear the receipt details display."""
        self.date_label.config(text="")
        self.store_label.config(text="")
        self.total_label.config(text="")
        self.groepskas_label.config(text="")
        self.poef_label.config(text="")
        self.pa_label.config(text="")
        
        # Clear items treeview
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
    
    def on_receipt_selected(self, event):
        """Handle receipt selection."""
        selection = self.receipts_tree.selection()
        if not selection:
            self.clear_details()
            return
        
        # Get selected receipt
        item = selection[0]
        receipt_id = self.receipts_tree.item(item, "tags")[0]
        receipts = self.main_window.get_receipts()
        receipt = next((r for r in receipts if r.id == receipt_id), None)
        
        if receipt:
            self.display_receipt_details(receipt)
    
    def display_receipt_details(self, receipt: Receipt):
        """Display details for a selected receipt."""
        self.date_label.config(text=receipt.date)
        self.store_label.config(text=receipt.store_name)
        self.total_label.config(text=f"€{receipt.total_amount:.2f}")
        self.groepskas_label.config(text=f"€{receipt.groepskas_total:.2f}")
        self.poef_label.config(text=f"€{receipt.poef_total:.2f}")
        self.pa_label.config(text=f"€{receipt.pa_total:.2f}")
        
        # Display items
        self.display_receipt_items(receipt)
    
    def display_receipt_items(self, receipt: Receipt):
        """Display items for a receipt."""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Get leaders for assignment display
        leaders = self.main_window.get_leaders()
        leader_names = {leader.id: leader.name for leader in leaders}
        
        # Add items to treeview
        for item in receipt.items:
            assigned_to = ""
            if item.assigned_to:
                assigned_to = leader_names.get(item.assigned_to, "Unknown")
            
            self.items_tree.insert("", tk.END, values=(
                item.name,
                f"€{item.price:.2f}",
                item.quantity,
                f"€{item.get_total_price():.2f}",
                item.category.value,
                assigned_to
            ), tags=(item,))
    
    def add_receipt(self):
        """Add a new receipt."""
        # Create a new receipt for today
        today = datetime.now().strftime("%Y-%m-%d")
        receipt = Receipt(date=today)
        self.main_window.add_receipt(receipt)
        self.refresh_display()
        
        # Select the new receipt
        for item in self.receipts_tree.get_children():
            if self.receipts_tree.item(item, "values")[0] == today:
                self.receipts_tree.selection_set(item)
                self.receipts_tree.see(item)
                break
    
    def remove_receipt(self):
        """Remove selected receipt."""
        selection = self.receipts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a receipt to remove")
            return
        
        # Get selected receipt
        item = selection[0]
        receipt_id = self.receipts_tree.item(item, "tags")[0]
        receipts = self.main_window.get_receipts()
        receipt = next((r for r in receipts if r.id == receipt_id), None)
        
        if receipt:
            result = messagebox.askyesno(
                "Confirm Removal",
                f"Are you sure you want to remove the receipt from {receipt.date}?"
            )
            if result:
                self.main_window.remove_receipt(receipt_id)
                self.refresh_display()
    
    def process_text_message(self):
        """Process a text message with PA orders."""
        leaders = self.main_window.get_leaders()
        if not leaders:
            messagebox.showwarning("Warning", "No leaders available. Please add leaders first.")
            return
        
        dialog = TextMessageDialog(self, title="Process Text Message", leaders=leaders)
        if dialog.result:
            # Create receipt from extracted items
            items = dialog.result["items"]
            if items:
                receipt = self.main_window.finance_service.create_receipt_from_items(items)
                self.main_window.add_receipt(receipt)
                self.refresh_display()
                messagebox.showinfo("Success", f"Created receipt with {len(items)} items")
            else:
                messagebox.showinfo("Info", "No items found in message")
    
    def add_item(self):
        """Add item to selected receipt."""
        selection = self.receipts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a receipt first")
            return
        
        # Get selected receipt
        item = selection[0]
        receipt_id = self.receipts_tree.item(item, "tags")[0]
        receipts = self.main_window.get_receipts()
        receipt = next((r for r in receipts if r.id == receipt_id), None)
        
        if receipt:
            leaders = self.main_window.get_leaders()
            dialog = ReceiptItemDialog(self, title="Add Item", leaders=leaders)
            if dialog.result:
                # Create receipt item
                item = ReceiptItem(
                    name=dialog.result["name"],
                    price=dialog.result["price"],
                    quantity=dialog.result["quantity"],
                    category=dialog.result["category"],
                    assigned_to=dialog.result["assigned_to"]
                )
                
                receipt.add_item(item)
                self.main_window.refresh_all_tabs()
                self.display_receipt_details(receipt)
    
    def edit_item(self):
        """Edit selected item."""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return
        
        # Get selected item
        item = selection[0]
        item_data = self.items_tree.item(item, "tags")[0]
        
        # Find the receipt containing this item
        receipts = self.main_window.get_receipts()
        receipt = None
        item_index = None
        
        for r in receipts:
            for i, item_obj in enumerate(r.items):
                if item_obj == item_data:
                    receipt = r
                    item_index = i
                    break
            if receipt:
                break
        
        if receipt and item_index is not None:
            leaders = self.main_window.get_leaders()
            dialog = ReceiptItemDialog(self, title="Edit Item", item=item_data, leaders=leaders)
            if dialog.result:
                # Update item
                item_data.name = dialog.result["name"]
                item_data.price = dialog.result["price"]
                item_data.quantity = dialog.result["quantity"]
                item_data.category = dialog.result["category"]
                item_data.assigned_to = dialog.result["assigned_to"]
                
                receipt._update_totals()
                self.main_window.refresh_all_tabs()
                self.display_receipt_details(receipt)
    
    def remove_item(self):
        """Remove selected item."""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        # Get selected item
        item = selection[0]
        item_data = self.items_tree.item(item, "tags")[0]
        
        # Find the receipt containing this item
        receipts = self.main_window.get_receipts()
        receipt = None
        item_index = None
        
        for r in receipts:
            for i, item_obj in enumerate(r.items):
                if item_obj == item_data:
                    receipt = r
                    item_index = i
                    break
            if receipt:
                break
        
        if receipt and item_index is not None:
            result = messagebox.askyesno(
                "Confirm Removal",
                f"Are you sure you want to remove '{item_data.name}'?"
            )
            if result:
                receipt.remove_item(item_index)
                self.main_window.refresh_all_tabs()
                self.display_receipt_details(receipt) 