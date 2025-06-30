"""
Leaders tab for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict, Optional
from datetime import datetime

from models.leader import Leader, POEF_DRINK_PRICE, POEF_SAF_PRICE
from models.expense import ExpenseCategory
from .base_components import BaseTab, DataTable, FormDialog, ActionButton

class LeaderFormDialog(FormDialog):
    """Dialog for adding/editing leaders."""
    
    def __init__(self, parent, leader: Optional[Leader] = None):
        fields = [
            {"name": "name", "label": "Leader Name:", "type": "entry"},
        ]
        
        super().__init__(parent, "Add Leader" if leader is None else "Edit Leader", fields)
        
        if leader:
            self.set_field_value("name", leader.name)
    
    def validate_form(self) -> bool:
        """Validate the form data."""
        name = self.get_field_value("name")
        if not name or not name.strip():
            messagebox.showerror("Error", "Leader name is required")
            return False
        return True

class LeadersTab(BaseTab):
    """Tab for managing leaders and their expenses."""
    
    def __init__(self, parent, main_window):
        self.selected_leader = None
        super().__init__(parent, main_window)
    
    def create_widgets(self):
        """Create the leaders tab widgets."""
        # Title
        title_label = ttk.Label(self, text="Leaders Management", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - leaders list
        self.create_leaders_section(content_frame)
        
        # Right side - leader details and actions
        self.create_leader_details_section(content_frame)
    
    def create_leaders_section(self, parent):
        """Create the leaders list section."""
        # Leaders frame
        leaders_frame = ttk.LabelFrame(parent, text="Leaders")
        leaders_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        
        # Buttons frame
        button_frame = ttk.Frame(leaders_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add leader button
        add_button = ttk.Button(button_frame, text="Add Leader", command=self.add_leader)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Edit leader button
        self.edit_button = ttk.Button(button_frame, text="Edit Leader", command=self.edit_leader, state=tk.DISABLED)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Remove leader button
        self.remove_button = ActionButton(
            button_frame, 
            text="Remove Leader", 
            command=self.remove_leader,
            confirm_message="Are you sure you want to remove this leader?",
            state=tk.DISABLED
        )
        self.remove_button.pack(side=tk.LEFT)
        
        # Leaders table
        columns = [
            {"name": "name", "display": "Name", "width": 120},
            {"name": "total", "display": "Total (€)", "width": 80, "anchor": tk.E}
        ]
        
        self.leaders_table = DataTable(leaders_frame, columns, height=15)
        self.leaders_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bind selection event
        self.leaders_table.bind_selection_event(self.on_leader_selected)
    
    def create_leader_details_section(self, parent):
        """Create the leader details section."""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Leader Details")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Details content
        self.details_content = ttk.Frame(details_frame)
        self.details_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initially show "No leader selected" message
        self.no_selection_label = ttk.Label(self.details_content, text="No leader selected")
        self.no_selection_label.pack(expand=True)
        
        # Leader info frame (initially hidden)
        self.leader_info_frame = ttk.Frame(details_frame)
        
        # Leader summary at the top
        summary_frame = ttk.LabelFrame(self.leader_info_frame, text="Leader Summary")
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Summary labels in a horizontal layout
        summary_content = ttk.Frame(summary_frame)
        summary_content.pack(fill=tk.X, padx=10, pady=5)
        
        # Left side of summary
        summary_left = ttk.Frame(summary_content)
        summary_left.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.leader_name_label = ttk.Label(summary_left, text="Name: ")
        self.leader_name_label.pack(anchor=tk.W, pady=1)
        
        # Right side of summary
        summary_right = ttk.Frame(summary_content)
        summary_right.pack(side=tk.RIGHT, fill=tk.X)
        
        self.pa_expenses_label = ttk.Label(summary_right, text="PA Expenses: €0.00")
        self.pa_expenses_label.pack(anchor=tk.E, pady=1)
        
        self.poef_total_label = ttk.Label(summary_right, text="POEF Total: €0.00")
        self.poef_total_label.pack(anchor=tk.E, pady=1)
        
        self.total_expenses_label = ttk.Label(summary_right, text="Total: €0.00", style="Header.TLabel")
        self.total_expenses_label.pack(anchor=tk.E, pady=1)
        
        # POEF Management frame
        poef_frame = ttk.LabelFrame(self.leader_info_frame, text="POEF Management")
        poef_frame.pack(fill=tk.X, pady=(0, 10))
        
        # POEF controls in a grid layout
        poef_controls_frame = ttk.Frame(poef_frame)
        poef_controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Headers
        ttk.Label(poef_controls_frame, text="Item", font=("TkDefaultFont", 9, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Label(poef_controls_frame, text="Count", font=("TkDefaultFont", 9, "bold")).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Label(poef_controls_frame, text="Price", font=("TkDefaultFont", 9, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        ttk.Label(poef_controls_frame, text="Total", font=("TkDefaultFont", 9, "bold")).grid(row=0, column=3, sticky=tk.W)
        
        # Drinks row
        ttk.Label(poef_controls_frame, text="Drinks:").grid(row=1, column=0, sticky=tk.W, padx=(0, 20), pady=5)
        
        drinks_controls = ttk.Frame(poef_controls_frame)
        drinks_controls.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        
        self.drinks_decrement_btn = ttk.Button(drinks_controls, text="-", width=3, command=lambda: self.decrement_poef_count("drinks"))
        self.drinks_decrement_btn.pack(side=tk.LEFT)
        
        self.drinks_var = tk.StringVar()
        self.drinks_entry = ttk.Entry(drinks_controls, textvariable=self.drinks_var, width=8)
        self.drinks_entry.pack(side=tk.LEFT, padx=2)
        
        self.drinks_increment_btn = ttk.Button(drinks_controls, text="+", width=3, command=lambda: self.increment_poef_count("drinks"))
        self.drinks_increment_btn.pack(side=tk.LEFT)
        
        ttk.Label(poef_controls_frame, text=f"€{POEF_DRINK_PRICE:.2f}").grid(row=1, column=2, sticky=tk.W, padx=(0, 20), pady=5)
        self.drinks_total_label = ttk.Label(poef_controls_frame, text="€0.00")
        self.drinks_total_label.grid(row=1, column=3, sticky=tk.W, pady=5)
        
        # Cigarettes row
        ttk.Label(poef_controls_frame, text="Cigarettes:").grid(row=2, column=0, sticky=tk.W, padx=(0, 20), pady=5)
        
        cigarettes_controls = ttk.Frame(poef_controls_frame)
        cigarettes_controls.grid(row=2, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        
        self.cigarettes_decrement_btn = ttk.Button(cigarettes_controls, text="-", width=3, command=lambda: self.decrement_poef_count("cigarettes"))
        self.cigarettes_decrement_btn.pack(side=tk.LEFT)
        
        self.cigarettes_var = tk.StringVar()
        self.cigarettes_entry = ttk.Entry(cigarettes_controls, textvariable=self.cigarettes_var, width=8)
        self.cigarettes_entry.pack(side=tk.LEFT, padx=2)
        
        self.cigarettes_increment_btn = ttk.Button(cigarettes_controls, text="+", width=3, command=lambda: self.increment_poef_count("cigarettes"))
        self.cigarettes_increment_btn.pack(side=tk.LEFT)
        
        ttk.Label(poef_controls_frame, text=f"€{POEF_SAF_PRICE:.2f}").grid(row=2, column=2, sticky=tk.W, padx=(0, 20), pady=5)
        self.cigarettes_total_label = ttk.Label(poef_controls_frame, text="€0.00")
        self.cigarettes_total_label.grid(row=2, column=3, sticky=tk.W, pady=5)
        
        # Detailed Summary section
        detailed_summary_frame = ttk.LabelFrame(self.leader_info_frame, text="Detailed Summary")
        detailed_summary_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Summary content with scrollable text
        summary_text_frame = ttk.Frame(detailed_summary_frame)
        summary_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create text widget with scrollbar
        self.summary_text = tk.Text(summary_text_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)
        summary_scrollbar = ttk.Scrollbar(summary_text_frame, orient=tk.VERTICAL, command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=summary_scrollbar.set)
        
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export buttons
        export_frame = ttk.Frame(detailed_summary_frame)
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        
        export_txt_button = ttk.Button(export_frame, text="Export to TXT", command=self.export_leader_summary_txt)
        export_txt_button.pack(side=tk.LEFT, padx=(0, 5))
        
        export_csv_button = ttk.Button(export_frame, text="Export to CSV", command=self.export_leader_summary_csv)
        export_csv_button.pack(side=tk.LEFT)
    
    def refresh_data(self):
        """Refresh the leaders data display."""
        leaders = self.main_window.get_leaders()
        
        # Clear table
        self.leaders_table.clear_data()
        
        # Add leaders to table
        for leader in leaders:
            pa_expenses = leader.total_pa_expenses
            poef_total = leader.get_poef_total()
            total = leader.get_total_expenses()
            
            self.leaders_table.add_row([
                leader.name,
                f"€{total:.2f}"
            ], tags=[str(leader.id)])
    
    def refresh_data_preserve_selection(self, leader_id_to_select=None):
        """Refresh the leaders data display while preserving selection."""
        leaders = self.main_window.get_leaders()
        
        # Clear table
        self.leaders_table.clear_data()
        
        # Add leaders to table
        for leader in leaders:
            pa_expenses = leader.total_pa_expenses
            poef_total = leader.get_poef_total()
            total = leader.get_total_expenses()
            
            self.leaders_table.add_row([
                leader.name,
                f"€{total:.2f}"
            ], tags=[str(leader.id)])
        
        # Restore selection if specified
        if leader_id_to_select:
            # Find the row with the specified leader ID and select it
            for i, leader in enumerate(leaders):
                if leader.id == leader_id_to_select:
                    # Select the corresponding row in the table
                    self.leaders_table.tree.selection_set(self.leaders_table.tree.get_children()[i])
                    # Update the selected leader
                    self.selected_leader = leader
                    break
    
    def on_leader_selected(self, event):
        """Handle leader selection."""
        item = self.leaders_table.get_selected_item()
        if item:
            # Get leader ID from tags
            leader_id = str(item["tags"][0])
            self.selected_leader = self.main_window.get_leader_by_id(leader_id)
            
            # Only proceed if we actually found the leader
            if self.selected_leader:
                # Enable buttons
                self.edit_button.config(state=tk.NORMAL)
                self.remove_button.config(state=tk.NORMAL)
                
                # Show leader details
                self.show_leader_details()
            else:
                # Leader not found, disable buttons
                self.edit_button.config(state=tk.DISABLED)
                self.remove_button.config(state=tk.DISABLED)
                self.show_no_selection()
        else:
            self.selected_leader = None
            self.edit_button.config(state=tk.DISABLED)
            self.remove_button.config(state=tk.DISABLED)
            self.show_no_selection()
    
    def show_leader_details(self):
        """Show details for the selected leader."""
        self.no_selection_label.pack_forget()
        
        self.leader_info_frame.pack(fill=tk.BOTH, expand=True)
        
        self.drinks_var.set(str(self.selected_leader.poef_drink_count))
        self.cigarettes_var.set(str(self.selected_leader.poef_saf_count))
        
        # Add event bindings for auto-save on direct entry
        self.drinks_entry.bind('<FocusOut>', self.on_poef_entry_change)
        self.cigarettes_entry.bind('<FocusOut>', self.on_poef_entry_change)
        self.drinks_entry.bind('<Return>', self.on_poef_entry_change)
        self.cigarettes_entry.bind('<Return>', self.on_poef_entry_change)
        
        self.leader_name_label.config(text=f"Name: {self.selected_leader.name}")
        self.pa_expenses_label.config(text=f"PA Expenses: €{self.selected_leader.total_pa_expenses:.2f}")
        self.poef_total_label.config(text=f"POEF Total: €{self.selected_leader.get_poef_total():.2f}")
        self.total_expenses_label.config(text=f"Total: €{self.selected_leader.get_total_expenses():.2f}")
        
        # Update POEF totals
        self.drinks_total_label.config(text=f"€{self.selected_leader.poef_drink_count * POEF_DRINK_PRICE:.2f}")
        self.cigarettes_total_label.config(text=f"€{self.selected_leader.poef_saf_count * POEF_SAF_PRICE:.2f}")
        
        # Populate detailed summary
        self.populate_detailed_summary()
    
    def on_poef_entry_change(self, event):
        """Handle POEF entry field changes for auto-save."""
        if not self.selected_leader:
            return
        
        # Store current selection
        selected_leader_id = self.selected_leader.id
        
        try:
            # Get values from entry fields
            drinks = int(self.drinks_var.get())
            cigarettes = int(self.cigarettes_var.get())
            
            if drinks < 0 or cigarettes < 0:
                self.show_error("Counts cannot be negative")
                # Reset to current values
                self.drinks_var.set(str(self.selected_leader.poef_drink_count))
                self.cigarettes_var.set(str(self.selected_leader.poef_saf_count))
                return
            
            # Update leader counts
            self.selected_leader.poef_drink_count = drinks
            self.selected_leader.poef_saf_count = cigarettes
            
            # Update totals display
            self.drinks_total_label.config(text=f"€{drinks * POEF_DRINK_PRICE:.2f}")
            self.cigarettes_total_label.config(text=f"€{cigarettes * POEF_SAF_PRICE:.2f}")
            
            # Auto-save the changes
            self.main_window.save_data()
            self.refresh_data_preserve_selection(selected_leader_id)
            self.populate_detailed_summary()
            
        except ValueError:
            self.show_error("Please enter valid numbers for POEF counts")
            # Reset to current values
            self.drinks_var.set(str(self.selected_leader.poef_drink_count))
            self.cigarettes_var.set(str(self.selected_leader.poef_saf_count))
    
    def populate_detailed_summary(self):
        """Populate the detailed summary text widget."""
        if not self.selected_leader:
            return
        
        # Enable text widget for editing
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        
        # Generate detailed summary
        summary_lines = []
        summary_lines.append(f"LEADER SUMMARY - {self.selected_leader.name}")
        summary_lines.append("=" * 50)
        summary_lines.append(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append("")
        
        # PA Expenses
        summary_lines.append("PA EXPENSES:")
        summary_lines.append("-" * 20)
        if self.selected_leader.pa_purchases:
            for purchase_id, amount in self.selected_leader.pa_purchases.items():
                # Try to find the item name
                item_name = self.get_pa_item_name(purchase_id)
                # Get the total price of the item to show sharing info
                total_item_price = self.get_pa_item_total_price(purchase_id)
                num_leaders = self.get_pa_item_leader_count(purchase_id)
                
                if num_leaders > 1:
                    summary_lines.append(f"  {item_name}: €{amount:.2f} (shared with {num_leaders} leaders, total: €{total_item_price:.2f})")
                else:
                    summary_lines.append(f"  {item_name}: €{amount:.2f}")
        else:
            summary_lines.append("  No PA expenses")
        summary_lines.append(f"Total PA Expenses: €{self.selected_leader.total_pa_expenses:.2f}")
        summary_lines.append("")
        
        # POEF Expenses
        summary_lines.append("POEF EXPENSES:")
        summary_lines.append("-" * 20)
        summary_lines.append(f"  Drinks: {self.selected_leader.poef_drink_count} × €{POEF_DRINK_PRICE:.2f} = €{self.selected_leader.poef_drink_count * POEF_DRINK_PRICE:.2f}")
        summary_lines.append(f"  Cigarettes: {self.selected_leader.poef_saf_count} × €{POEF_SAF_PRICE:.2f} = €{self.selected_leader.poef_saf_count * POEF_SAF_PRICE:.2f}")
        summary_lines.append(f"Total POEF Expenses: €{self.selected_leader.get_poef_total():.2f}")
        summary_lines.append("")
        
        # Overall Summary
        summary_lines.append("OVERALL SUMMARY:")
        summary_lines.append("-" * 20)
        summary_lines.append(f"PA Expenses: €{self.selected_leader.total_pa_expenses:.2f}")
        summary_lines.append(f"POEF Expenses: €{self.selected_leader.get_poef_total():.2f}")
        summary_lines.append(f"Grand Total: €{self.selected_leader.get_total_expenses():.2f}")
        
        # Insert the summary text
        self.summary_text.insert("1.0", "\n".join(summary_lines))
        
        # Disable text widget for read-only
        self.summary_text.config(state=tk.DISABLED)
    
    def get_pa_item_name(self, item_id: str) -> str:
        """Get the name of a PA item by its ID."""
        receipts = self.main_window.get_receipts()
        for receipt in receipts:
            for item in receipt.items:
                if item.id == item_id and item.category == ExpenseCategory.PA:
                    return item.name
        return f"Unknown Item ({item_id})"
    
    def get_pa_item_total_price(self, item_id: str) -> float:
        """Get the total price of a PA item by its ID."""
        receipts = self.main_window.get_receipts()
        for receipt in receipts:
            for item in receipt.items:
                if item.id == item_id and item.category == ExpenseCategory.PA:
                    return item.get_total_price()
        return 0.0
    
    def get_pa_item_leader_count(self, item_id: str) -> int:
        """Get the number of leaders sharing a PA item by its ID."""
        leaders = self.main_window.get_leaders()
        count = 0
        for leader in leaders:
            if leader.has_pa_purchase(item_id):
                count += 1
        return count
    
    def show_no_selection(self):
        """Show no selection message."""
        self.leader_info_frame.pack_forget()
        self.no_selection_label.pack(expand=True)
    
    def add_leader(self):
        """Add a new leader."""
        dialog = LeaderFormDialog(self)
        self.wait_window(dialog)
        
        if dialog.result:
            data = dialog.result
            leader = Leader(name=data["name"])
            
            self.main_window.add_leader(leader)
            self.refresh_data()
    
    def edit_leader(self):
        """Edit the selected leader."""
        if not self.selected_leader:
            return
        
        dialog = LeaderFormDialog(self, self.selected_leader)
        self.wait_window(dialog)
        
        if dialog.result:
            data = dialog.result
            self.selected_leader.name = data["name"]
            
            self.main_window.save_data()
            self.refresh_data()
    
    def remove_leader(self):
        """Remove the selected leader."""
        if not self.selected_leader:
            return
        
        # Show confirmation dialog
        leader_name = self.selected_leader.name
        if not self.show_confirm(f"Are you sure you want to remove leader '{leader_name}'?\n\nThis will also remove all their PA expenses and POEF counts."):
            return
        
        self.main_window.remove_leader(self.selected_leader.id)
        self.selected_leader = None
        
        self.refresh_data()
        self.show_no_selection()
        self.edit_button.config(state=tk.DISABLED)
        self.remove_button.config(state=tk.DISABLED)
    
    def update_poef_counts(self):
        """Update POEF counts for the selected leader."""
        if not self.selected_leader:
            return
        
        try:
            drinks = int(self.drinks_var.get())
            cigarettes = int(self.cigarettes_var.get())
            
            if drinks < 0 or cigarettes < 0:
                self.show_error("Counts cannot be negative")
                return
            
            self.selected_leader.poef_drink_count = drinks
            self.selected_leader.poef_saf_count = cigarettes
            
            self.main_window.save_data()
            self.refresh_data()
            
            # Update the display
            self.show_leader_details()
            
        except ValueError:
            self.show_error("Please enter valid numbers for POEF counts")
    
    def increment_poef_count(self, count_type):
        """Increment POEF count for the specified type."""
        if not self.selected_leader:
            return
        
        # Store current selection
        selected_leader_id = self.selected_leader.id
        
        try:
            if count_type == "drinks":
                current_value = int(self.drinks_var.get())
                new_value = current_value + 1
                self.drinks_var.set(str(new_value))
                self.drinks_total_label.config(text=f"€{new_value * POEF_DRINK_PRICE:.2f}")
                self.selected_leader.poef_drink_count = new_value
            elif count_type == "cigarettes":
                current_value = int(self.cigarettes_var.get())
                new_value = current_value + 1
                self.cigarettes_var.set(str(new_value))
                self.cigarettes_total_label.config(text=f"€{new_value * POEF_SAF_PRICE:.2f}")
                self.selected_leader.poef_saf_count = new_value
            
            # Auto-save the changes
            self.main_window.save_data()
            self.refresh_data_preserve_selection(selected_leader_id)
            self.populate_detailed_summary()
            
        except ValueError:
            # If the current value is not a valid number, set it to 1
            if count_type == "drinks":
                self.drinks_var.set("1")
                self.drinks_total_label.config(text=f"€{POEF_DRINK_PRICE:.2f}")
                self.selected_leader.poef_drink_count = 1
            elif count_type == "cigarettes":
                self.cigarettes_var.set("1")
                self.cigarettes_total_label.config(text=f"€{POEF_SAF_PRICE:.2f}")
                self.selected_leader.poef_saf_count = 1
            
            # Auto-save the changes
            self.main_window.save_data()
            self.refresh_data_preserve_selection(selected_leader_id)
            self.populate_detailed_summary()
    
    def decrement_poef_count(self, count_type):
        """Decrement POEF count for the specified type."""
        if not self.selected_leader:
            return
        
        # Store current selection
        selected_leader_id = self.selected_leader.id
        
        try:
            if count_type == "drinks":
                current_value = int(self.drinks_var.get())
                if current_value > 0:
                    new_value = current_value - 1
                    self.drinks_var.set(str(new_value))
                    self.drinks_total_label.config(text=f"€{new_value * POEF_DRINK_PRICE:.2f}")
                    self.selected_leader.poef_drink_count = new_value
            elif count_type == "cigarettes":
                current_value = int(self.cigarettes_var.get())
                if current_value > 0:
                    new_value = current_value - 1
                    self.cigarettes_var.set(str(new_value))
                    self.cigarettes_total_label.config(text=f"€{new_value * POEF_SAF_PRICE:.2f}")
                    self.selected_leader.poef_saf_count = new_value
            
            # Auto-save the changes
            self.main_window.save_data()
            self.refresh_data_preserve_selection(selected_leader_id)
            self.populate_detailed_summary()
            
        except ValueError:
            # If the current value is not a valid number, set it to 0
            if count_type == "drinks":
                self.drinks_var.set("0")
                self.drinks_total_label.config(text="€0.00")
                self.selected_leader.poef_drink_count = 0
            elif count_type == "cigarettes":
                self.cigarettes_var.set("0")
                self.cigarettes_total_label.config(text="€0.00")
                self.selected_leader.poef_saf_count = 0
            
            # Auto-save the changes
            self.main_window.save_data()
            self.refresh_data_preserve_selection(selected_leader_id)
            self.populate_detailed_summary()
    
    def generate_leader_report(self):
        """Generate a detailed report for the selected leader."""
        if not self.selected_leader:
            self.show_error("Please select a leader first")
            return
        
        filename = f"leader_report_{self.selected_leader.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialname=filename
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"LEADER REPORT - {self.selected_leader.name}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    f.write("PA EXPENSES:\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"Total PA Expenses: €{self.selected_leader.total_pa_expenses:.2f}\n")
                    f.write(f"Number of PA Items: {len(self.selected_leader.pa_purchases)}\n\n")
                    
                    f.write("POEF EXPENSES:\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"Drinks Count: {self.selected_leader.poef_drink_count}\n")
                    f.write(f"Drinks Price: €{POEF_DRINK_PRICE:.2f} each\n")
                    f.write(f"Drinks Total: €{self.selected_leader.poef_drink_count * POEF_DRINK_PRICE:.2f}\n\n")
                    f.write(f"Cigarettes Count: {self.selected_leader.poef_saf_count}\n")
                    f.write(f"Cigarettes Price: €{POEF_SAF_PRICE:.2f} each\n")
                    f.write(f"Cigarettes Total: €{self.selected_leader.poef_saf_count * POEF_SAF_PRICE:.2f}\n\n")
                    
                    f.write("SUMMARY:\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"PA Expenses: €{self.selected_leader.total_pa_expenses:.2f}\n")
                    f.write(f"POEF Total: €{self.selected_leader.get_poef_total():.2f}\n")
                    f.write(f"Grand Total: €{self.selected_leader.get_total_expenses():.2f}\n")
                
                self.show_info(f"Leader report saved to {filepath}")
                
            except Exception as e:
                self.show_error(f"Error saving report: {str(e)}")
    
    def generate_global_summary(self):
        """Generate a global summary of all leaders."""
        leaders = self.main_window.get_leaders()
        receipts = self.main_window.get_receipts()
        
        if not leaders and not receipts:
            self.show_info("No data available to generate summary")
            return
        
        filename = f"global_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialname=filename
        )
        
        if filepath:
            try:
                summary = self.main_window.finance_service.generate_summary_report(leaders, receipts)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("KAMP FINANCES - GLOBAL SUMMARY REPORT\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Report Date: {summary['report_date']}\n\n")
                    
                    f.write("RECEIPTS SUMMARY:\n")
                    f.write("-" * 20 + "\n")
                    receipts_summary = summary['receipts_summary']
                    f.write(f"Total Receipts: {receipts_summary['total_receipts']}\n")
                    f.write(f"Total Groepskas: €{receipts_summary['total_groepskas']:.2f}\n")
                    f.write(f"Total POEF: €{receipts_summary['total_poef']:.2f}\n")
                    f.write(f"Total PA: €{receipts_summary['total_pa']:.2f}\n")
                    f.write(f"Grand Total: €{receipts_summary['grand_total']:.2f}\n\n")
                    
                    f.write("LEADERS SUMMARY:\n")
                    f.write("-" * 20 + "\n")
                    for leader_summary in summary['leaders_summary']:
                        f.write(f"{leader_summary['leader_name']}:\n")
                        f.write(f"  PA Expenses: €{leader_summary['pa_expenses']:.2f}\n")
                        f.write(f"  POEF Expenses: €{leader_summary['poef_expenses']:.2f}\n")
                        f.write(f"  Total: €{leader_summary['total_expenses']:.2f}\n\n")
                    
                    f.write(f"Total Leader Expenses: €{summary['total_leaders_expenses']:.2f}\n")
                
                self.show_info(f"Global summary saved to {filepath}")
                
            except Exception as e:
                self.show_error(f"Error saving summary: {str(e)}") 

    def export_leader_summary_txt(self):
        """Export the leader summary to a TXT file."""
        if not self.selected_leader:
            self.show_error("Please select a leader first")
            return
        
        filename = f"leader_summary_{self.selected_leader.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialname=filename
        )
        
        if filepath:
            try:
                summary_text = self.summary_text.get("1.0", tk.END)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(summary_text)
                
                self.show_info(f"Leader summary exported to {filepath}")
                
            except Exception as e:
                self.show_error(f"Error exporting summary: {str(e)}")

    def export_leader_summary_csv(self):
        """Export the leader summary to a CSV file."""
        if not self.selected_leader:
            self.show_error("Please select a leader first")
            return
        
        filename = f"leader_summary_{self.selected_leader.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialname=filename
        )
        
        if filepath:
            try:
                summary_text = self.summary_text.get("1.0", tk.END)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(summary_text)
                
                self.show_info(f"Leader summary exported to {filepath}")
                
            except Exception as e:
                self.show_error(f"Error exporting summary: {str(e)}") 
