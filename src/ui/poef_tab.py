"""
POEF tab UI for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
from datetime import datetime

from models.leader import Leader

class PoefTab(ttk.Frame):
    """Tab for managing POEF (fridge drinks) tracking."""
    
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.create_widgets()
    
    def create_widgets(self):
        """Create the POEF tab widgets."""
        # Title
        title_label = ttk.Label(self, text="POEF Management", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Description
        desc_label = ttk.Label(self, text="Enter drink counts from the paper POEF list", style="Header.TLabel")
        desc_label.pack(pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Set drink count button
        set_count_button = ttk.Button(button_frame, text="Set Drink Count", command=self.set_drink_count)
        set_count_button.pack(side=tk.LEFT, padx=5)
        
        # Add drinks button
        add_drinks_button = ttk.Button(button_frame, text="Add Drinks", command=self.add_drinks)
        add_drinks_button.pack(side=tk.LEFT, padx=5)
        
        # Clear all counts button
        clear_button = ttk.Button(button_frame, text="Clear All Counts", command=self.clear_all_counts)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.refresh_display)
        refresh_button.pack(side=tk.RIGHT, padx=5)
        
        # Create main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - leader summary
        self.create_leader_summary(content_frame)
        
        # Right side - POEF info
        self.create_poef_info(content_frame)
    
    def create_leader_summary(self, parent):
        """Create the leader summary area."""
        # Summary frame
        summary_frame = ttk.LabelFrame(parent, text="Leader POEF Summary")
        summary_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Create treeview for leader summary
        columns = ("Leader", "Drink Count", "Price per Drink", "Total")
        self.summary_tree = ttk.Treeview(summary_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.summary_tree.heading("Leader", text="Leader")
        self.summary_tree.heading("Drink Count", text="Drink Count")
        self.summary_tree.heading("Price per Drink", text="Price per Drink (€)")
        self.summary_tree.heading("Total", text="Total (€)")
        
        # Column widths
        self.summary_tree.column("Leader", width=150)
        self.summary_tree.column("Drink Count", width=100)
        self.summary_tree.column("Price per Drink", width=120)
        self.summary_tree.column("Total", width=100)
        
        # Scrollbar
        summary_scrollbar = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=summary_scrollbar.set)
        
        # Pack summary treeview and scrollbar
        self.summary_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Summary totals frame
        totals_frame = ttk.LabelFrame(summary_frame, text="Totals")
        totals_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Total drinks
        ttk.Label(totals_frame, text="Total Drinks:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.total_drinks_label = ttk.Label(totals_frame, text="0", style="Header.TLabel")
        self.total_drinks_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Total amount
        ttk.Label(totals_frame, text="Total Amount:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.total_amount_label = ttk.Label(totals_frame, text="€0.00", style="Header.TLabel")
        self.total_amount_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
    
    def create_poef_info(self, parent):
        """Create the POEF information area."""
        # Info frame
        info_frame = ttk.LabelFrame(parent, text="POEF Information")
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Information text
        info_text = """
POEF System:

• Drinks are counted manually on paper during the trip
• Each drink costs €0.75 (universal price)
• Enter the final counts here at the end of the trip
• Use "Set Drink Count" to enter the total from paper
• Use "Add Drinks" to add to existing counts

Instructions:
1. Count all drinks from the paper POEF list
2. Select a leader and click "Set Drink Count"
3. Enter the total number of drinks for that leader
4. Repeat for all leaders
5. Review the summary on the left
        """
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, wraplength=300)
        info_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def refresh_display(self):
        """Refresh the POEF display."""
        # Clear existing items
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)
        
        # Get current data
        leaders = self.main_window.get_leaders()
        
        # Add leader summary
        total_drinks = 0
        total_amount = 0.0
        
        for leader in leaders:
            drink_count = leader.poef_drink_count
            price_per_drink = leader.poef_price_per_drink
            total = leader.get_poef_total()
            
            self.summary_tree.insert("", tk.END, values=(
                leader.name,
                drink_count,
                f"€{price_per_drink:.2f}",
                f"€{total:.2f}"
            ), tags=(leader.id,))
            
            total_drinks += drink_count
            total_amount += total
        
        # Update totals
        self.total_drinks_label.config(text=str(total_drinks))
        self.total_amount_label.config(text=f"€{total_amount:.2f}")
    
    def set_drink_count(self):
        """Set the drink count for a selected leader."""
        leaders = self.main_window.get_leaders()
        if not leaders:
            messagebox.showwarning("Warning", "No leaders available. Please add leaders first.")
            return
        
        # Create dialog for setting drink count
        dialog = PoefCountDialog(self, leaders=leaders, mode="set")
        if dialog.result:
            leader = dialog.result["leader"]
            count = dialog.result["count"]
            
            self.main_window.finance_service.set_poef_drink_count(leader, count)
            self.main_window.refresh_all_tabs()
            self.refresh_display()
            self.main_window.save_all_data()
    
    def add_drinks(self):
        """Add drinks to a selected leader."""
        leaders = self.main_window.get_leaders()
        if not leaders:
            messagebox.showwarning("Warning", "No leaders available. Please add leaders first.")
            return
        
        # Create dialog for adding drinks
        dialog = PoefCountDialog(self, leaders=leaders, mode="add")
        if dialog.result:
            leader = dialog.result["leader"]
            count = dialog.result["count"]
            
            self.main_window.finance_service.add_poef_drinks(leader, count)
            self.main_window.refresh_all_tabs()
            self.refresh_display()
            self.main_window.save_all_data()
    
    def clear_all_counts(self):
        """Clear all POEF drink counts."""
        result = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to clear all POEF drink counts?"
        )
        if result:
            leaders = self.main_window.get_leaders()
            for leader in leaders:
                leader.set_poef_drink_count(0)
            
            self.main_window.refresh_all_tabs()
            self.refresh_display()
            self.main_window.save_all_data()

class PoefCountDialog:
    """Dialog for setting POEF drink counts."""
    
    def __init__(self, parent, leaders: List[Leader], mode: str = "set"):
        self.result = None
        self.leaders = leaders
        self.mode = mode  # "set" or "add"
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Set POEF Drink Count" if mode == "set" else "Add POEF Drinks")
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
        
        # Drink count field
        action_text = "Set drink count to:" if self.mode == "set" else "Add drinks:"
        ttk.Label(main_frame, text=action_text).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.count_var = tk.StringVar()
        self.count_entry = ttk.Entry(main_frame, textvariable=self.count_var, width=10)
        self.count_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Price info
        ttk.Label(main_frame, text="Price per drink: €0.75").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # OK button
        ok_button = ttk.Button(button_frame, text="OK", command=self.ok_clicked)
        ok_button.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Focus on leader combo
        self.leader_combo.focus()
    
    def setup_bindings(self):
        """Setup event bindings."""
        self.dialog.bind("<Return>", lambda e: self.ok_clicked())
        self.dialog.bind("<Escape>", lambda e: self.cancel_clicked())
    
    def ok_clicked(self):
        """Handle OK button click."""
        leader_name = self.leader_var.get()
        if not leader_name:
            messagebox.showerror("Error", "Please select a leader")
            return
        
        leader = next((l for l in self.leaders if l.name == leader_name), None)
        if not leader:
            messagebox.showerror("Error", "Selected leader not found")
            return
        
        try:
            count = int(self.count_var.get())
            if count < 0:
                raise ValueError("Count must be non-negative")
        except ValueError:
            messagebox.showerror("Error", "Invalid count")
            self.count_entry.focus()
            return
        
        self.result = {
            "leader": leader,
            "count": count
        }
        
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button click."""
        self.dialog.destroy() 