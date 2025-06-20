"""
Dialog components for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Optional

from models.leader import Leader
from models.receipt import ReceiptItem, ExpenseCategory

class LeaderDialog:
    """Dialog for adding/editing leaders."""
    
    def __init__(self, parent, title: str, leader: Optional[Leader] = None):
        self.result = None
        self.leader = leader
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.create_widgets()
        self.setup_bindings()
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name field
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Phone field
        ttk.Label(main_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(main_frame, textvariable=self.phone_var, width=30)
        self.phone_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Email field
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(main_frame, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # OK button
        ok_button = ttk.Button(button_frame, text="OK", command=self.ok_clicked)
        ok_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Load existing data if editing
        if self.leader:
            self.name_var.set(self.leader.name)
            self.phone_var.set(self.leader.phone_number)
            self.email_var.set(self.leader.email)
        
        # Focus on name field
        self.name_entry.focus()
    
    def setup_bindings(self):
        """Setup event bindings."""
        self.dialog.bind("<Return>", lambda e: self.ok_clicked())
        self.dialog.bind("<Escape>", lambda e: self.cancel_clicked())
    
    def ok_clicked(self):
        """Handle OK button click."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Name is required")
            self.name_entry.focus()
            return
        
        self.result = {
            "name": name,
            "phone": self.phone_var.get().strip(),
            "email": self.email_var.get().strip()
        }
        
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click."""
        self.dialog.destroy()

class ReceiptItemDialog:
    """Dialog for adding/editing receipt items."""
    
    def __init__(self, parent, title: str, item: Optional[ReceiptItem] = None, leaders: list = None):
        self.result = None
        self.item = item
        self.leaders = leaders or []
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.create_widgets()
        self.setup_bindings()
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Item name field
        ttk.Label(main_frame, text="Item Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Price field
        ttk.Label(main_frame, text="Price (€):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(main_frame, textvariable=self.price_var, width=15)
        self.price_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Quantity field
        ttk.Label(main_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_entry = ttk.Entry(main_frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Category field
        ttk.Label(main_frame, text="Category:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value=ExpenseCategory.GROEPSKAS.value)
        self.category_combo = ttk.Combobox(
            main_frame, 
            textvariable=self.category_var,
            values=[cat.value for cat in ExpenseCategory],
            state="readonly",
            width=15
        )
        self.category_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Leader assignment (for PA items)
        ttk.Label(main_frame, text="Assigned to:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.leader_var = tk.StringVar()
        self.leader_combo = ttk.Combobox(
            main_frame,
            textvariable=self.leader_var,
            values=[""] + [leader.name for leader in self.leaders],
            state="readonly",
            width=20
        )
        self.leader_combo.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Bind category change
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_changed)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        # OK button
        ok_button = ttk.Button(button_frame, text="OK", command=self.ok_clicked)
        ok_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Load existing data if editing
        if self.item:
            self.name_var.set(self.item.name)
            self.price_var.set(str(self.item.price))
            self.quantity_var.set(str(self.item.quantity))
            self.category_var.set(self.item.category.value)
            
            if self.item.assigned_to:
                leader = next((l for l in self.leaders if l.id == self.item.assigned_to), None)
                if leader:
                    self.leader_var.set(leader.name)
        
        # Focus on name field
        self.name_entry.focus()
    
    def setup_bindings(self):
        """Setup event bindings."""
        self.dialog.bind("<Return>", lambda e: self.ok_clicked())
        self.dialog.bind("<Escape>", lambda e: self.cancel_clicked())
    
    def on_category_changed(self, event):
        """Handle category change."""
        category = self.category_var.get()
        if category == ExpenseCategory.PA.value:
            self.leader_combo.config(state="readonly")
        else:
            self.leader_var.set("")
            self.leader_combo.config(state="disabled")
    
    def ok_clicked(self):
        """Handle OK button click."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Item name is required")
            self.name_entry.focus()
            return
        
        try:
            price = float(self.price_var.get().replace(',', '.'))
            if price < 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid price")
            self.price_entry.focus()
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            self.quantity_entry.focus()
            return
        
        category = ExpenseCategory(self.category_var.get())
        assigned_to = None
        
        if category == ExpenseCategory.PA:
            leader_name = self.leader_var.get()
            if leader_name:
                leader = next((l for l in self.leaders if l.name == leader_name), None)
                if leader:
                    assigned_to = leader.id
                else:
                    messagebox.showerror("Error", "Selected leader not found")
                    return
            else:
                messagebox.showerror("Error", "PA items must be assigned to a leader")
                return
        
        self.result = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "category": category,
            "assigned_to": assigned_to
        }
        
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click."""
        self.dialog.destroy()

class TextMessageDialog:
    """Dialog for processing text messages with PA orders."""
    
    def __init__(self, parent, title: str, leaders: list = None):
        self.result = None
        self.leaders = leaders or []
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x400")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.create_widgets()
        self.setup_bindings()
        
        # Wait for dialog to close
        parent.wait_window(self.dialog)
    
    def create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Leader selection
        ttk.Label(main_frame, text="Leader:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.leader_var = tk.StringVar()
        self.leader_combo = ttk.Combobox(
            main_frame,
            textvariable=self.leader_var,
            values=[leader.name for leader in self.leaders],
            state="readonly",
            width=30
        )
        self.leader_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Message text
        ttk.Label(main_frame, text="Message:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.message_text = tk.Text(main_frame, height=10, width=50)
        self.message_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=5)
        
        # Scrollbar for text
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.message_text.yview)
        self.message_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S), pady=5)
        
        # Extracted items display
        ttk.Label(main_frame, text="Extracted Items:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        self.items_text = tk.Text(main_frame, height=8, width=50, state=tk.DISABLED)
        self.items_text.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=5)
        
        # Scrollbar for items
        items_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.items_text.yview)
        self.items_text.configure(yscrollcommand=items_scrollbar.set)
        items_scrollbar.grid(row=2, column=2, sticky=(tk.N, tk.S), pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Process button
        process_button = ttk.Button(button_frame, text="Process Message", command=self.process_message)
        process_button.pack(side=tk.LEFT, padx=5)
        
        # OK button
        ok_button = ttk.Button(button_frame, text="OK", command=self.ok_clicked)
        ok_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Focus on leader combo
        self.leader_combo.focus()
    
    def setup_bindings(self):
        """Setup event bindings."""
        self.dialog.bind("<Escape>", lambda e: self.cancel_clicked())
    
    def process_message(self):
        """Process the message and extract items."""
        leader_name = self.leader_var.get()
        if not leader_name:
            messagebox.showerror("Error", "Please select a leader")
            return
        
        leader = next((l for l in self.leaders if l.name == leader_name), None)
        if not leader:
            messagebox.showerror("Error", "Selected leader not found")
            return
        
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return
        
        # Process message using finance service
        from services.finance_service import FinanceService
        finance_service = FinanceService(None)  # We don't need data service for this
        items = finance_service.process_text_message(message, leader)
        
        # Display extracted items
        self.items_text.config(state=tk.NORMAL)
        self.items_text.delete("1.0", tk.END)
        
        if items:
            for item in items:
                self.items_text.insert(tk.END, f"• {item['name']}")
                if item['price'] > 0:
                    self.items_text.insert(tk.END, f" (€{item['price']:.2f})")
                self.items_text.insert(tk.END, "\n")
        else:
            self.items_text.insert(tk.END, "No items found in message")
        
        self.items_text.config(state=tk.DISABLED)
        
        # Store result
        self.result = {
            "leader": leader,
            "message": message,
            "items": items
        }
    
    def ok_clicked(self):
        """Handle OK button click."""
        if not self.result:
            messagebox.showerror("Error", "Please process the message first")
            return
        
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click."""
        self.dialog.destroy() 