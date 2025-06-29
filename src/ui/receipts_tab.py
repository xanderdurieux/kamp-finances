"""
Receipts tab for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict, Optional
from datetime import datetime

from models.receipt import Receipt
from models.expense import Expense, ExpenseCategory
from base_components import BaseTab, DataTable, FormDialog, ActionButton

class ReceiptFormDialog(FormDialog):
    """Dialog for adding/editing receipts."""
    
    def __init__(self, parent, receipt: Optional[Receipt] = None):
        fields = [
            {"name": "date", "label": "Date:", "type": "entry"},
            {"name": "store_name", "label": "Store Name:", "type": "entry"}
        ]
        
        super().__init__(parent, "Add Receipt" if receipt is None else "Edit Receipt", fields)
        
        if receipt:
            self.set_field_value("date", receipt.date)
            self.set_field_value("store_name", receipt.store_name)
        else:
            # Set default values
            self.set_field_value("date", datetime.now().strftime("%Y-%m-%d"))
            self.set_field_value("store_name", "Colruyt")
    
    def validate_form(self) -> bool:
        """Validate the form data."""
        date = self.get_field_value("date")
        store_name = self.get_field_value("store_name")
        
        if not date or not date.strip():
            messagebox.showerror("Error", "Date is required")
            return False
        
        if not store_name or not store_name.strip():
            messagebox.showerror("Error", "Store name is required")
            return False
        
        return True

class ExpenseFormDialog(FormDialog):
    """Dialog for adding/editing expenses."""
    
    def __init__(self, parent, expense: Optional[Expense] = None):
        fields = [
            {"name": "name", "label": "Item Name:", "type": "entry"},
            {"name": "price", "label": "Price (€):", "type": "entry"},
            {"name": "quantity", "label": "Quantity:", "type": "entry"},
            {"name": "category", "label": "Category:", "type": "combobox", "values": [cat.value for cat in ExpenseCategory]}
        ]
        
        super().__init__(parent, "Add Expense" if expense is None else "Edit Expense", fields)
        
        if expense:
            self.set_field_value("name", expense.name)
            self.set_field_value("price", str(expense.price))
            self.set_field_value("quantity", str(expense.quantity))
            self.set_field_value("category", expense.category.value)
        else:
            # Set default values
            self.set_field_value("quantity", "1")
            self.set_field_value("category", ExpenseCategory.GROEPSKAS.value)
    
    def validate_form(self) -> bool:
        """Validate the form data."""
        name = self.get_field_value("name")
        price = self.get_field_value("price")
        quantity = self.get_field_value("quantity")
        category = self.get_field_value("category")
        
        if not name or not name.strip():
            messagebox.showerror("Error", "Item name is required")
            return False
        
        try:
            float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")
            return False
        
        try:
            float(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid number")
            return False
        
        if not category:
            messagebox.showerror("Error", "Category is required")
            return False
        
        return True

class ReceiptsTab(BaseTab):
    """Tab for managing receipts and expenses."""
    
    def __init__(self, parent, main_window):
        self.selected_receipt = None
        self.selected_expense_index = None
        super().__init__(parent, main_window)
    
    def create_widgets(self):
        """Create the receipts tab widgets."""
        # Title
        title_label = ttk.Label(self, text="Receipts Management", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - receipts list
        self.create_receipts_section(content_frame)
        
        # Right side - receipt details and expenses
        self.create_receipt_details_section(content_frame)
    
    def create_receipts_section(self, parent):
        """Create the receipts list section."""
        # Receipts frame
        receipts_frame = ttk.LabelFrame(parent, text="Receipts")
        receipts_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        
        # Buttons frame
        button_frame = ttk.Frame(receipts_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add receipt button
        add_button = ttk.Button(button_frame, text="Add Receipt", command=self.add_receipt)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Edit receipt button
        self.edit_receipt_button = ttk.Button(button_frame, text="Edit Receipt", command=self.edit_receipt, state=tk.DISABLED)
        self.edit_receipt_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Remove receipt button
        self.remove_receipt_button = ActionButton(
            button_frame, 
            text="Remove Receipt", 
            command=self.remove_receipt,
            state=tk.DISABLED
        )
        self.remove_receipt_button.pack(side=tk.LEFT)
        
        # Receipts table
        columns = [
            {"name": "date", "display": "Date", "width": 80},
            {"name": "store", "display": "Store", "width": 100},
            {"name": "total", "display": "Total (€)", "width": 80, "anchor": tk.E}
        ]
        
        self.receipts_table = DataTable(receipts_frame, columns, height=15)
        self.receipts_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bind selection event
        self.receipts_table.bind_selection_event(self.on_receipt_selected)
    
    def create_receipt_details_section(self, parent):
        """Create the receipt details section."""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Receipt Details")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Details content
        self.details_content = ttk.Frame(details_frame)
        self.details_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initially show "No receipt selected" message
        self.no_selection_label = ttk.Label(self.details_content, text="No receipt selected")
        self.no_selection_label.pack(expand=True)
        
        # Receipt info frame (initially hidden)
        self.receipt_info_frame = ttk.Frame(details_frame)
        
        # Receipt summary at the top
        summary_frame = ttk.LabelFrame(self.receipt_info_frame, text="Receipt Summary")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Summary labels in a horizontal layout
        summary_content = ttk.Frame(summary_frame)
        summary_content.pack(fill=tk.X, padx=10, pady=5)
        
        # Left side of summary
        summary_left = ttk.Frame(summary_content)
        summary_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.date_label = ttk.Label(summary_left, text="Date: ")
        self.date_label.pack(anchor=tk.W, pady=1)
        
        self.store_label = ttk.Label(summary_left, text="Store: ")
        self.store_label.pack(anchor=tk.W, pady=1)
        
        # Right side of summary
        summary_right = ttk.Frame(summary_content)
        summary_right.pack(side=tk.RIGHT, fill=tk.X)
        
        self.groepskas_label = ttk.Label(summary_right, text="Groepskas: €0.00")
        self.groepskas_label.pack(anchor=tk.E, pady=1)
        
        self.poef_label = ttk.Label(summary_right, text="POEF: €0.00")
        self.poef_label.pack(anchor=tk.E, pady=1)
        
        self.pa_label = ttk.Label(summary_right, text="PA: €0.00")
        self.pa_label.pack(anchor=tk.E, pady=1)
        
        self.total_label = ttk.Label(summary_right, text="Total: €0.00", style="Header.TLabel")
        self.total_label.pack(anchor=tk.E, pady=1)
        
        # Expenses frame taking up most of the space
        expenses_frame = ttk.LabelFrame(self.receipt_info_frame, text="Expenses")
        expenses_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Expenses buttons
        expenses_button_frame = ttk.Frame(expenses_frame)
        expenses_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add expense button
        add_expense_button = ttk.Button(expenses_button_frame, text="Add Expense", command=self.add_expense)
        add_expense_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Edit expense button
        self.edit_expense_button = ttk.Button(expenses_button_frame, text="Edit Expense", command=self.edit_expense, state=tk.DISABLED)
        self.edit_expense_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Remove expense button
        self.remove_expense_button = ActionButton(
            expenses_button_frame, 
            text="Remove Expense", 
            command=self.remove_expense,
            state=tk.DISABLED
        )
        self.remove_expense_button.pack(side=tk.LEFT)
        
        # Expenses table
        expense_columns = [
            {"name": "name", "display": "Item Name", "width": 200},
            {"name": "price", "display": "Price (€)", "width": 100, "anchor": tk.E},
            {"name": "quantity", "display": "Qty", "width": 80, "anchor": tk.E},
            {"name": "total", "display": "Total (€)", "width": 100, "anchor": tk.E},
            {"name": "category", "display": "Category", "width": 120}
        ]
        
        self.expenses_table = DataTable(expenses_frame, expense_columns, height=20)
        self.expenses_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bind selection event
        self.expenses_table.bind_selection_event(self.on_expense_selected)
    
    def refresh_data(self):
        """Refresh the receipts data display."""
        receipts = self.main_window.get_receipts()
        
        # Clear table
        self.receipts_table.clear_data()
        
        # Add receipts to table
        for receipt in receipts:
            self.receipts_table.add_row([
                receipt.date,
                receipt.store_name,
                f"€{receipt.total_amount:.2f}"
            ], tags=[str(receipt.id)])
    
    def on_receipt_selected(self, event):
        """Handle receipt selection."""
        item = self.receipts_table.get_selected_item()
        if item:
            # Get receipt ID from tags
            receipt_id = str(item["tags"][0])
            self.selected_receipt = self.main_window.get_receipt_by_id(receipt_id)
            
            # Only proceed if we actually found the receipt
            if self.selected_receipt:
                # Enable buttons
                self.edit_receipt_button.config(state=tk.NORMAL)
                self.remove_receipt_button.config(state=tk.NORMAL)
                
                # Show receipt details
                self.show_receipt_details()
            else:
                # Receipt not found, disable buttons
                self.edit_receipt_button.config(state=tk.DISABLED)
                self.remove_receipt_button.config(state=tk.DISABLED)
                self.show_no_selection()
        else:
            self.selected_receipt = None
            self.edit_receipt_button.config(state=tk.DISABLED)
            self.remove_receipt_button.config(state=tk.DISABLED)
            self.show_no_selection()
    
    def on_expense_selected(self, event):
        """Handle expense selection."""
        item = self.expenses_table.get_selected_item()
        if item and self.selected_receipt:
            # Get expense index from tags
            try:
                expense_index = int(item["tags"][0])
                # Verify the index is valid
                if 0 <= expense_index < len(self.selected_receipt.items):
                    self.selected_expense_index = expense_index
                    
                    # Enable expense buttons
                    self.edit_expense_button.config(state=tk.NORMAL)
                    self.remove_expense_button.config(state=tk.NORMAL)
                else:
                    # Invalid index
                    self.selected_expense_index = None
                    self.edit_expense_button.config(state=tk.DISABLED)
                    self.remove_expense_button.config(state=tk.DISABLED)
            except (ValueError, IndexError):
                # Invalid tag or index
                self.selected_expense_index = None
                self.edit_expense_button.config(state=tk.DISABLED)
                self.remove_expense_button.config(state=tk.DISABLED)
        else:
            self.selected_expense_index = None
            self.edit_expense_button.config(state=tk.DISABLED)
            self.remove_expense_button.config(state=tk.DISABLED)
    
    def show_receipt_details(self):
        """Show details for the selected receipt."""
        # Hide no selection message
        self.no_selection_label.pack_forget()
        
        # Show receipt info frame
        self.receipt_info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update receipt info
        self.date_label.config(text=f"Date: {self.selected_receipt.date}")
        self.store_label.config(text=f"Store: {self.selected_receipt.store_name}")
        self.groepskas_label.config(text=f"Groepskas: €{self.selected_receipt.groepskas_total:.2f}")
        self.poef_label.config(text=f"POEF: €{self.selected_receipt.poef_total:.2f}")
        self.pa_label.config(text=f"PA: €{self.selected_receipt.pa_total:.2f}")
        self.total_label.config(text=f"Total: €{self.selected_receipt.total_amount:.2f}")
        
        # Refresh expenses table
        self.refresh_expenses_table()
    
    def show_no_selection(self):
        """Show no selection message."""
        self.receipt_info_frame.pack_forget()
        self.no_selection_label.pack(expand=True)
    
    def refresh_expenses_table(self):
        """Refresh the expenses table for the selected receipt."""
        if not self.selected_receipt:
            return
        
        # Clear table
        self.expenses_table.clear_data()
        
        # Add expenses to table
        for i, expense in enumerate(self.selected_receipt.items):
            self.expenses_table.add_row([
                expense.name,
                f"€{expense.price:.2f}",
                str(expense.quantity),
                f"€{expense.get_total_price():.2f}",
                expense.category.value
            ], tags=[str(i)])
    
    def add_receipt(self):
        """Add a new receipt."""
        dialog = ReceiptFormDialog(self)
        self.wait_window(dialog)
        
        if dialog.result:
            data = dialog.result
            receipt = Receipt(
                date=data["date"],
                store_name=data["store_name"]
            )
            
            self.main_window.add_receipt(receipt)
            self.refresh_data()
    
    def edit_receipt(self):
        """Edit the selected receipt."""
        if not self.selected_receipt:
            return
        
        dialog = ReceiptFormDialog(self, self.selected_receipt)
        self.wait_window(dialog)
        
        if dialog.result:
            data = dialog.result
            self.selected_receipt.date = data["date"]
            self.selected_receipt.store_name = data["store_name"]
            
            self.main_window.save_data()
            self.refresh_data()
            self.show_receipt_details()
    
    def remove_receipt(self):
        """Remove the selected receipt."""
        if not self.selected_receipt:
            return
        
        # Show confirmation dialog
        receipt_info = f"{self.selected_receipt.store_name} on {self.selected_receipt.date}"
        num_expenses = len(self.selected_receipt.items)
        
        if not self.show_confirm(f"Are you sure you want to remove receipt '{receipt_info}'?\n\nThis will also remove all {num_expenses} expenses and any PA assignments to leaders."):
            return
        
        self.main_window.remove_receipt(self.selected_receipt.id)
        self.selected_receipt = None
        
        self.refresh_data()
        self.show_no_selection()
        self.edit_receipt_button.config(state=tk.DISABLED)
        self.remove_receipt_button.config(state=tk.DISABLED)
    
    def add_expense(self):
        """Add a new expense to the selected receipt."""
        if not self.selected_receipt:
            self.show_error("Please select a receipt first")
            return
        
        dialog = ExpenseFormDialog(self)
        self.wait_window(dialog)
        
        if dialog.result:
            data = dialog.result
            expense = Expense(
                name=data["name"],
                price=float(data["price"]),
                quantity=float(data["quantity"]),
                category=ExpenseCategory(data["category"]),
                date=self.selected_receipt.date,
                receipt_id=self.selected_receipt.id
            )
            
            self.selected_receipt.add_item(expense)
            self.main_window.save_data()
            self.refresh_expenses_table()
            self.show_receipt_details()  # Refresh totals
    
    def edit_expense(self):
        """Edit the selected expense."""
        if not self.selected_receipt or self.selected_expense_index is None:
            return
        
        expense = self.selected_receipt.items[self.selected_expense_index]
        dialog = ExpenseFormDialog(self, expense)
        self.wait_window(dialog)
        
        if dialog.result:
            data = dialog.result
            expense.name = data["name"]
            expense.price = float(data["price"])
            expense.quantity = float(data["quantity"])
            expense.category = ExpenseCategory(data["category"])
            
            # Update receipt totals
            self.selected_receipt._update_totals()
            
            self.main_window.save_data()
            self.refresh_expenses_table()
            self.show_receipt_details()  # Refresh totals
    
    def remove_expense(self):
        """Remove the selected expense."""
        if not self.selected_receipt or self.selected_expense_index is None:
            return
        
        expense = self.selected_receipt.items[self.selected_expense_index]
        expense_name = expense.name
        
        # Show confirmation dialog
        if not self.show_confirm(f"Are you sure you want to remove expense '{expense_name}'?\n\nThis will also remove any PA assignments to leaders."):
            return
        
        self.selected_receipt.remove_item(self.selected_expense_index)
        self.selected_expense_index = None
        
        self.main_window.save_data()
        self.refresh_expenses_table()
        self.show_receipt_details()  # Refresh totals
        self.edit_expense_button.config(state=tk.DISABLED)
        self.remove_expense_button.config(state=tk.DISABLED) 