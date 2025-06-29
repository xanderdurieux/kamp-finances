"""
PA Items Assignment tab for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional

from models.expense import Expense, ExpenseCategory
from models.leader import Leader
from base_components import BaseTab, DataTable, FormDialog, ActionButton

class LeaderAssignmentDialog(FormDialog):
    """Dialog for assigning PA items to leaders."""
    
    def __init__(self, parent, leaders: List[Leader], expense: Expense):
        self.leaders = leaders
        self.expense = expense
        
        # Create leader selection fields
        fields = []
        for leader in leaders:
            fields.append({
                "name": f"leader_{leader.id}",
                "label": f"{leader.name}:",
                "type": "combobox",
                "values": ["Not Assigned", "Assigned"]
            })
        
        super().__init__(parent, f"Assign '{expense.name}' to Leaders", fields)
        
        # Set default values based on current assignments
        for leader in leaders:
            field_name = f"leader_{leader.id}"
            if leader.has_pa_purchase(expense.id):
                self.set_field_value(field_name, "Assigned")
            else:
                self.set_field_value(field_name, "Not Assigned")
    
    def get_assignments(self) -> Dict[str, bool]:
        """Get the leader assignments."""
        assignments = {}
        for leader in self.leaders:
            field_name = f"leader_{leader.id}"
            value = self.get_field_value(field_name)
            assignments[leader.id] = (value == "Assigned")
        return assignments

class PAItemsTab(BaseTab):
    """Tab for assigning PA items to leaders."""
    
    def __init__(self, parent, main_window):
        self.selected_pa_item = None
        super().__init__(parent, main_window)
    
    def create_widgets(self):
        """Create the PA items tab widgets."""
        # Title
        title_label = ttk.Label(self, text="PA Items Assignment", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - PA items list
        self.create_pa_items_section(content_frame)
        
        # Right side - item details and assignments
        self.create_item_details_section(content_frame)
    
    def create_pa_items_section(self, parent):
        """Create the PA items list section."""
        # PA items frame
        pa_items_frame = ttk.LabelFrame(parent, text="PA Items")
        pa_items_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        
        # Buttons frame
        button_frame = ttk.Frame(pa_items_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # PA items table
        columns = [
            {"name": "name", "display": "Item Name", "width": 150},
            {"name": "price", "display": "Price (€)", "width": 80, "anchor": tk.E},
            {"name": "quantity", "display": "Qty", "width": 60, "anchor": tk.E},
            {"name": "total", "display": "Total (€)", "width": 80, "anchor": tk.E},
            {"name": "date", "display": "Date", "width": 100},
            {"name": "assigned_leaders", "display": "Assigned To", "width": 150}
        ]
        
        self.pa_items_table = DataTable(pa_items_frame, columns, height=15)
        self.pa_items_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bind selection event
        self.pa_items_table.tree.bind("<<TreeviewSelect>>", self.on_pa_item_selected)
    
    def create_item_details_section(self, parent):
        """Create the item details section."""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Item Details")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Details content
        self.details_content = ttk.Frame(details_frame)
        self.details_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initially show "No item selected" message
        self.no_selection_label = ttk.Label(self.details_content, text="No PA item selected")
        self.no_selection_label.pack(expand=True)
        
        # Item info frame (initially hidden)
        self.item_info_frame = ttk.Frame(details_frame)
        
        # Item summary at the top
        summary_frame = ttk.LabelFrame(self.item_info_frame, text="Item Summary")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Summary labels in a horizontal layout
        summary_content = ttk.Frame(summary_frame)
        summary_content.pack(fill=tk.X, padx=10, pady=5)
        
        # Left side of summary
        summary_left = ttk.Frame(summary_content)
        summary_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.item_name_label = ttk.Label(summary_left, text="Name: ")
        self.item_name_label.pack(anchor=tk.W, pady=1)
        
        self.item_date_label = ttk.Label(summary_left, text="Date: ")
        self.item_date_label.pack(anchor=tk.W, pady=1)
        
        # Right side of summary
        summary_right = ttk.Frame(summary_content)
        summary_right.pack(side=tk.RIGHT, fill=tk.X)
        
        self.item_price_label = ttk.Label(summary_right, text="Price: ")
        self.item_price_label.pack(anchor=tk.E, pady=1)
        
        self.item_quantity_label = ttk.Label(summary_right, text="Quantity: ")
        self.item_quantity_label.pack(anchor=tk.E, pady=1)
        
        self.item_total_label = ttk.Label(summary_right, text="Total: ", style="Header.TLabel")
        self.item_total_label.pack(anchor=tk.E, pady=1)
        
        # Assignment section
        assignment_frame = ttk.LabelFrame(self.item_info_frame, text="Assignment")
        assignment_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Assignment controls
        assignment_controls = ttk.Frame(assignment_frame)
        assignment_controls.pack(fill=tk.X, padx=10, pady=10)
        
        # Add leader button
        add_leader_button = ttk.Button(assignment_controls, text="+ Add Leader", command=self.add_leader_entry)
        add_leader_button.pack(side=tk.LEFT)
        
        # Leader entries container
        self.leader_entries_frame = ttk.Frame(assignment_frame)
        self.leader_entries_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Current assignment status
        self.assignment_status_label = ttk.Label(assignment_frame, text="Status: Not assigned", font=("TkDefaultFont", 9))
        self.assignment_status_label.pack(pady=(0, 10))
        
        # Advanced assignment section
        advanced_frame = ttk.LabelFrame(self.item_info_frame, text="Advanced Assignment")
        advanced_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Manage assignments button
        manage_button = ttk.Button(advanced_frame, text="Manage Multiple Assignments", command=self.manage_assignments)
        manage_button.pack(pady=10)
        
        # Assignments list
        self.assignments_frame = ttk.Frame(advanced_frame)
        self.assignments_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def refresh_data(self):
        """Refresh the PA items data display."""
        receipts = self.main_window.get_receipts()
        leaders = self.main_window.get_leaders()
        
        # Get all PA items from receipts
        pa_items = []
        for receipt in receipts:
            for item in receipt.items:
                if item.category == ExpenseCategory.PA:
                    pa_items.append(item)
        
        # Clear table
        self.pa_items_table.clear_data()
        
        # Add PA items to table
        for item in pa_items:
            # Get names and amounts of leaders who have this item assigned
            assigned_leaders = []
            for leader in leaders:
                if leader.has_pa_purchase(item.id):
                    amount = leader.get_pa_purchase_amount(item.id)
                    assigned_leaders.append(f"{leader.name} (€{amount:.2f})")
            
            # Format the assigned leaders string
            if assigned_leaders:
                if len(assigned_leaders) == 1:
                    assigned_text = assigned_leaders[0]
                else:
                    assigned_text = ", ".join(assigned_leaders)
            else:
                assigned_text = "Not assigned"
            
            self.pa_items_table.add_row([
                item.name,
                f"€{item.price:.2f}",
                str(item.quantity),
                f"€{item.get_total_price():.2f}",
                item.date,
                assigned_text
            ], tags=[str(item.id)])
    
    def on_pa_item_selected(self, event):
        """Handle PA item selection."""
        item = self.pa_items_table.get_selected_item()
        if item:
            # Get item ID from tags
            item_id = str(item["tags"][0])
            self.selected_pa_item = self.get_pa_item_by_id(item_id)
            
            # Show item details
            self.show_item_details()
        else:
            self.selected_pa_item = None
            self.show_no_selection()
    
    def show_item_details(self):
        """Show details for the selected PA item."""
        # Hide no selection message
        self.no_selection_label.pack_forget()
        
        # Show item info frame
        self.item_info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update item info
        self.item_name_label.config(text=f"Name: {self.selected_pa_item.name}")
        self.item_price_label.config(text=f"Price: €{self.selected_pa_item.price:.2f}")
        self.item_quantity_label.config(text=f"Quantity: {self.selected_pa_item.quantity}")
        self.item_total_label.config(text=f"Total: €{self.selected_pa_item.get_total_price():.2f}")
        self.item_date_label.config(text=f"Date: {self.selected_pa_item.date}")
        
        # Populate leader entries
        self.populate_leader_entries()
        
        # Update assignment status
        self.update_assignment_status()
        
        # Refresh assignments
        self.refresh_assignments()
    
    def populate_leader_entries(self):
        """Populate the leader entries with current assignments."""
        # Clear existing entries
        for widget in self.leader_entries_frame.winfo_children():
            widget.destroy()
        
        leaders = self.main_window.get_leaders()
        leader_names = [leader.name for leader in leaders]
        
        # Get current assignments
        assigned_leaders = []
        for leader in leaders:
            if leader.has_pa_purchase(self.selected_pa_item.id):
                assigned_leaders.append(leader.name)
        
        # If no assignments, create one empty entry
        if not assigned_leaders:
            self.add_leader_entry()
        else:
            # Create entries for each assigned leader
            for leader_name in assigned_leaders:
                self.add_leader_entry(leader_name)
    
    def add_leader_entry(self, selected_leader=None):
        """Add a new leader entry row."""
        entry_frame = ttk.Frame(self.leader_entries_frame)
        entry_frame.pack(fill=tk.X, pady=2)
        
        # Leader dropdown
        leaders = self.main_window.get_leaders()
        leader_names = [leader.name for leader in leaders]
        
        leader_var = tk.StringVar()
        if selected_leader:
            leader_var.set(selected_leader)
        
        leader_combobox = ttk.Combobox(entry_frame, textvariable=leader_var, values=leader_names, state="readonly", width=20)
        leader_combobox.pack(side=tk.LEFT, padx=(0, 5))
        
        # Auto-save when selection changes
        def on_selection_change(event):
            self.auto_save_assignments()
        
        leader_combobox.bind('<<ComboboxSelected>>', on_selection_change)
        
        # Remove button (only show if there's more than one entry)
        def remove_entry():
            if len(self.leader_entries_frame.winfo_children()) > 1:
                entry_frame.destroy()
                self.auto_save_assignments()  # Save after removal
        
        remove_button = ttk.Button(entry_frame, text="×", width=3, command=remove_entry)
        remove_button.pack(side=tk.RIGHT)
        
        # Store references for later access
        entry_frame.leader_var = leader_var
        entry_frame.leader_combobox = leader_combobox
    
    def auto_save_assignments(self):
        """Automatically save the current assignments."""
        if not self.selected_pa_item:
            return
        
        # Store current selection
        current_item_id = self.selected_pa_item.id
        
        # Get all leader entries
        leader_entries = []
        for entry_frame in self.leader_entries_frame.winfo_children():
            leader_name = entry_frame.leader_var.get()
            if leader_name:  # Only include non-empty selections
                leader_entries.append(leader_name)
        
        # Remove duplicates
        leader_entries = list(set(leader_entries))
        
        # Get all leaders
        leaders = self.main_window.get_leaders()
        
        # Clear all current assignments for this item
        for leader in leaders:
            if leader.has_pa_purchase(self.selected_pa_item.id):
                leader.remove_pa_purchase(self.selected_pa_item.id, 0)  # Amount doesn't matter for removal
        
        # Calculate the amount each leader should pay
        total_price = self.selected_pa_item.get_total_price()
        if leader_entries:
            amount_per_leader = total_price / len(leader_entries)
        else:
            amount_per_leader = 0
        
        # Add new assignments with split amounts
        for leader_name in leader_entries:
            for leader in leaders:
                if leader.name == leader_name:
                    leader.add_pa_purchase(self.selected_pa_item.id, amount_per_leader)
                    break
        
        self.main_window.save_data()
        
        # Update displays without losing selection
        self.update_assignment_status()
        self.refresh_assignments()
        
        # Refresh data but preserve selection
        self.refresh_data_preserve_selection(current_item_id)
    
    def refresh_data_preserve_selection(self, item_id_to_select=None):
        """Refresh the PA items data display while preserving selection."""
        receipts = self.main_window.get_receipts()
        leaders = self.main_window.get_leaders()
        
        # Get all PA items from receipts
        pa_items = []
        for receipt in receipts:
            for item in receipt.items:
                if item.category == ExpenseCategory.PA:
                    pa_items.append(item)
        
        # Clear table
        self.pa_items_table.clear_data()
        
        # Add PA items to table
        for item in pa_items:
            # Get names and amounts of leaders who have this item assigned
            assigned_leaders = []
            for leader in leaders:
                if leader.has_pa_purchase(item.id):
                    amount = leader.get_pa_purchase_amount(item.id)
                    assigned_leaders.append(f"{leader.name} (€{amount:.2f})")
            
            # Format the assigned leaders string
            if assigned_leaders:
                if len(assigned_leaders) == 1:
                    assigned_text = assigned_leaders[0]
                else:
                    assigned_text = ", ".join(assigned_leaders)
            else:
                assigned_text = "Not assigned"
            
            self.pa_items_table.add_row([
                item.name,
                f"€{item.price:.2f}",
                str(item.quantity),
                f"€{item.get_total_price():.2f}",
                item.date,
                assigned_text
            ], tags=[str(item.id)])
        
        # Restore selection if specified
        if item_id_to_select:
            # Find the row with the specified item ID and select it
            for i, item in enumerate(pa_items):
                if item.id == item_id_to_select:
                    # Select the corresponding row in the table
                    self.pa_items_table.tree.selection_set(self.pa_items_table.tree.get_children()[i])
                    # Update the selected item
                    self.selected_pa_item = item
                    break
    
    def update_assignment_status(self):
        """Update the assignment status label."""
        leaders = self.main_window.get_leaders()
        assigned_leaders = [leader.name for leader in leaders if leader.has_pa_purchase(self.selected_pa_item.id)]
        
        if not assigned_leaders:
            self.assignment_status_label.config(text="Status: Not assigned", foreground="red")
        elif len(assigned_leaders) == 1:
            amount = next(leader.get_pa_purchase_amount(self.selected_pa_item.id) for leader in leaders if leader.has_pa_purchase(self.selected_pa_item.id))
            self.assignment_status_label.config(text=f"Status: Assigned to {assigned_leaders[0]} (€{amount:.2f})", foreground="green")
        else:
            total_price = self.selected_pa_item.get_total_price()
            amount_per_leader = total_price / len(assigned_leaders)
            self.assignment_status_label.config(text=f"Status: Assigned to {len(assigned_leaders)} leaders (€{amount_per_leader:.2f} each, total: €{total_price:.2f})", foreground="blue")
    
    def show_no_selection(self):
        """Show no selection message."""
        self.item_info_frame.pack_forget()
        self.no_selection_label.pack(expand=True)
    
    def refresh_assignments(self):
        """Refresh the leader assignments display."""
        if not self.selected_pa_item:
            return
        
        # Clear existing assignments
        for widget in self.assignments_frame.winfo_children():
            widget.destroy()
        
        # Get leaders
        leaders = self.main_window.get_leaders()
        
        # Show assignments
        for leader in leaders:
            is_assigned = leader.has_pa_purchase(self.selected_pa_item.id)
            if is_assigned:
                amount = leader.get_pa_purchase_amount(self.selected_pa_item.id)
                status = f"✓ Assigned (€{amount:.2f})"
                color = "green"
            else:
                status = "✗ Not Assigned"
                color = "red"
            
            label = ttk.Label(self.assignments_frame, text=f"{leader.name}: {status}")
            label.pack(anchor=tk.W, pady=1)
    
    def get_pa_item_by_id(self, item_id: str) -> Optional[Expense]:
        """Get a PA item by its ID."""
        receipts = self.main_window.get_receipts()
        for receipt in receipts:
            for item in receipt.items:
                if item.id == item_id and item.category == ExpenseCategory.PA:
                    return item
        return None
    
    def manage_assignments(self):
        """Manage leader assignments for the selected PA item."""
        if not self.selected_pa_item:
            self.show_error("Please select a PA item first")
            return
        
        leaders = self.main_window.get_leaders()
        if not leaders:
            self.show_error("No leaders available for assignment")
            return
        
        dialog = LeaderAssignmentDialog(self, leaders, self.selected_pa_item)
        self.wait_window(dialog)
        
        if dialog.result:
            assignments = dialog.get_assignments()
            
            # Clear all current assignments for this item
            for leader in leaders:
                if leader.has_pa_purchase(self.selected_pa_item.id):
                    leader.remove_pa_purchase(self.selected_pa_item.id, 0)
            
            # Calculate the amount each leader should pay
            assigned_leaders = [leader for leader in leaders if assignments.get(leader.id, False)]
            total_price = self.selected_pa_item.get_total_price()
            
            if assigned_leaders:
                amount_per_leader = total_price / len(assigned_leaders)
            else:
                amount_per_leader = 0
            
            # Add new assignments with split amounts
            for leader in assigned_leaders:
                leader.add_pa_purchase(self.selected_pa_item.id, amount_per_leader)
            
            self.main_window.save_data()
            self.refresh_assignments()
            self.show_info("Leader assignments updated successfully")