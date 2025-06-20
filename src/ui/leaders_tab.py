"""
Leaders tab UI for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

from models.leader import Leader
from ui.dialogs import LeaderDialog

class LeadersTab(ttk.Frame):
    """Tab for managing leaders."""
    
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.create_widgets()
    
    def create_widgets(self):
        """Create the leaders tab widgets."""
        # Title
        title_label = ttk.Label(self, text="Manage Leaders", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add leader button
        add_button = ttk.Button(button_frame, text="Add Leader", command=self.add_leader)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Edit leader button
        edit_button = ttk.Button(button_frame, text="Edit Leader", command=self.edit_leader)
        edit_button.pack(side=tk.LEFT, padx=5)
        
        # Remove leader button
        remove_button = ttk.Button(button_frame, text="Remove Leader", command=self.remove_leader)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.refresh_display)
        refresh_button.pack(side=tk.RIGHT, padx=5)
        
        # Create treeview for leaders
        self.create_leaders_tree()
        
        # Create details frame
        self.create_details_frame()
    
    def create_leaders_tree(self):
        """Create the leaders treeview."""
        # Treeview frame
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        columns = ("Name", "Phone", "Email", "PA Total", "POEF Count", "Total Expenses")
        self.leaders_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        self.leaders_tree.heading("Name", text="Name")
        self.leaders_tree.heading("Phone", text="Phone")
        self.leaders_tree.heading("Email", text="Email")
        self.leaders_tree.heading("PA Total", text="PA Total (€)")
        self.leaders_tree.heading("POEF Count", text="POEF Count")
        self.leaders_tree.heading("Total Expenses", text="Total (€)")
        
        # Column widths
        self.leaders_tree.column("Name", width=150)
        self.leaders_tree.column("Phone", width=120)
        self.leaders_tree.column("Email", width=200)
        self.leaders_tree.column("PA Total", width=100)
        self.leaders_tree.column("POEF Count", width=100)
        self.leaders_tree.column("Total Expenses", width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.leaders_tree.yview)
        self.leaders_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.leaders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.leaders_tree.bind("<<TreeviewSelect>>", self.on_leader_selected)
    
    def create_details_frame(self):
        """Create the leader details frame."""
        details_frame = ttk.LabelFrame(self, text="Leader Details")
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Details grid
        details_grid = ttk.Frame(details_frame)
        details_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Name
        ttk.Label(details_grid, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.name_label = ttk.Label(details_grid, text="", style="Header.TLabel")
        self.name_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Phone
        ttk.Label(details_grid, text="Phone:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.phone_label = ttk.Label(details_grid, text="")
        self.phone_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Email
        ttk.Label(details_grid, text="Email:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.email_label = ttk.Label(details_grid, text="")
        self.email_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # PA Expenses
        ttk.Label(details_grid, text="PA Expenses:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.pa_label = ttk.Label(details_grid, text="", style="Header.TLabel")
        self.pa_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        # POEF Count
        ttk.Label(details_grid, text="POEF Count:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.poef_label = ttk.Label(details_grid, text="")
        self.poef_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Total Expenses
        ttk.Label(details_grid, text="Total Expenses:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.total_label = ttk.Label(details_grid, text="", style="Header.TLabel")
        self.total_label.grid(row=2, column=3, sticky=tk.W, padx=5, pady=2)
    
    def refresh_display(self):
        """Refresh the leaders display."""
        # Clear existing items
        for item in self.leaders_tree.get_children():
            self.leaders_tree.delete(item)
        
        # Get current leaders
        leaders = self.main_window.get_leaders()
        
        # Add leaders to treeview
        for leader in leaders:
            total_expenses = leader.get_total_expenses()
            self.leaders_tree.insert("", tk.END, values=(
                leader.name,
                leader.phone_number,
                leader.email,
                f"€{leader.total_pa_expenses:.2f}",
                leader.poef_drink_count,
                f"€{total_expenses:.2f}"
            ), tags=(leader.id,))
        
        # Clear details
        self.clear_details()
    
    def clear_details(self):
        """Clear the details display."""
        self.name_label.config(text="")
        self.phone_label.config(text="")
        self.email_label.config(text="")
        self.pa_label.config(text="")
        self.poef_label.config(text="")
        self.total_label.config(text="")
    
    def on_leader_selected(self, event):
        """Handle leader selection."""
        selection = self.leaders_tree.selection()
        if not selection:
            self.clear_details()
            return
        
        # Get selected leader
        item = selection[0]
        leader_id = self.leaders_tree.item(item, "tags")[0]
        leaders = self.main_window.get_leaders()
        leader = next((l for l in leaders if l.id == leader_id), None)
        
        if leader:
            self.display_leader_details(leader)
    
    def display_leader_details(self, leader: Leader):
        """Display details for a selected leader."""
        self.name_label.config(text=leader.name)
        self.phone_label.config(text=leader.phone_number)
        self.email_label.config(text=leader.email)
        self.pa_label.config(text=f"€{leader.total_pa_expenses:.2f}")
        self.poef_label.config(text=f"{leader.poef_drink_count} drinks (€{leader.get_poef_total():.2f})")
        self.total_label.config(text=f"€{leader.get_total_expenses():.2f}")
    
    def add_leader(self):
        """Add a new leader."""
        dialog = LeaderDialog(self, title="Add Leader")
        if dialog.result:
            leader = Leader(
                name=dialog.result["name"],
                phone_number=dialog.result.get("phone", ""),
                email=dialog.result.get("email", "")
            )
            self.main_window.add_leader(leader)
    
    def edit_leader(self):
        """Edit selected leader."""
        selection = self.leaders_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a leader to edit")
            return
        
        # Get selected leader
        item = selection[0]
        leader_id = self.leaders_tree.item(item, "tags")[0]
        leaders = self.main_window.get_leaders()
        leader = next((l for l in leaders if l.id == leader_id), None)
        
        if leader:
            dialog = LeaderDialog(self, title="Edit Leader", leader=leader)
            if dialog.result:
                # Update leader
                leader.name = dialog.result["name"]
                leader.phone_number = dialog.result.get("phone", "")
                leader.email = dialog.result.get("email", "")
                
                # Force save after editing
                self.main_window.save_all_data()
                self.main_window.refresh_all_tabs()
    
    def remove_leader(self):
        """Remove selected leader."""
        selection = self.leaders_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a leader to remove")
            return
        
        # Get selected leader
        item = selection[0]
        leader_id = self.leaders_tree.item(item, "tags")[0]
        leaders = self.main_window.get_leaders()
        leader = next((l for l in leaders if l.id == leader_id), None)
        
        if leader:
            # Check if leader has expenses
            if leader.get_total_expenses() > 0:
                result = messagebox.askyesno(
                    "Confirm Removal",
                    f"Leader '{leader.name}' has expenses. Are you sure you want to remove them?"
                )
                if not result:
                    return
            
            # Remove leader
            self.main_window.remove_leader(leader_id) 