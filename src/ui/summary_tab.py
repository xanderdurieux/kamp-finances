"""
Summary tab UI for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
from datetime import datetime

from models.leader import Leader
from models.receipt import Receipt

class SummaryTab(ttk.Frame):
    """Tab for displaying financial summaries."""
    
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.create_widgets()
    
    def create_widgets(self):
        """Create the summary tab widgets."""
        # Title
        title_label = ttk.Label(self, text="Financial Summary", style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Generate summary button
        generate_button = ttk.Button(button_frame, text="Generate Summary", command=self.generate_summary)
        generate_button.pack(side=tk.LEFT, padx=5)
        
        # Export summary button
        export_button = ttk.Button(button_frame, text="Export Summary", command=self.export_summary)
        export_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.refresh_display)
        refresh_button.pack(side=tk.RIGHT, padx=5)
        
        # Create main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - overall summary
        self.create_overall_summary(content_frame)
        
        # Right side - leader details
        self.create_leader_details(content_frame)
    
    def create_overall_summary(self, parent):
        """Create the overall summary area."""
        # Summary frame
        summary_frame = ttk.LabelFrame(parent, text="Overall Summary")
        summary_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Summary grid
        summary_grid = ttk.Frame(summary_frame)
        summary_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Receipts summary
        ttk.Label(summary_grid, text="Receipts Summary:", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(summary_grid, text="Total Receipts:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.total_receipts_label = ttk.Label(summary_grid, text="0")
        self.total_receipts_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(summary_grid, text="Total Groepskas:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.total_groepskas_label = ttk.Label(summary_grid, text="€0.00")
        self.total_groepskas_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(summary_grid, text="Total POEF:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.total_poef_label = ttk.Label(summary_grid, text="€0.00")
        self.total_poef_label.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(summary_grid, text="Total PA:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.total_pa_label = ttk.Label(summary_grid, text="€0.00")
        self.total_pa_label.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(summary_grid, text="Grand Total:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.grand_total_label = ttk.Label(summary_grid, text="€0.00", style="Header.TLabel")
        self.grand_total_label.grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Separator
        separator = ttk.Separator(summary_grid, orient=tk.HORIZONTAL)
        separator.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Leaders summary
        ttk.Label(summary_grid, text="Leaders Summary:", style="Header.TLabel").grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(summary_grid, text="Total Leaders:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.total_leaders_label = ttk.Label(summary_grid, text="0")
        self.total_leaders_label.grid(row=8, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(summary_grid, text="Total Leader Expenses:").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.total_leader_expenses_label = ttk.Label(summary_grid, text="€0.00")
        self.total_leader_expenses_label.grid(row=9, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(summary_grid, text="Average per Leader:").grid(row=10, column=0, sticky=tk.W, pady=2)
        self.avg_per_leader_label = ttk.Label(summary_grid, text="€0.00")
        self.avg_per_leader_label.grid(row=10, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Configure grid weights
        summary_grid.columnconfigure(1, weight=1)
    
    def create_leader_details(self, parent):
        """Create the leader details area."""
        # Details frame
        details_frame = ttk.LabelFrame(parent, text="Leader Details")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Create treeview for leader details
        columns = ("Leader", "PA Expenses", "POEF Count", "POEF Total", "Total")
        self.leader_tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.leader_tree.heading("Leader", text="Leader")
        self.leader_tree.heading("PA Expenses", text="PA Expenses (€)")
        self.leader_tree.heading("POEF Count", text="POEF Count")
        self.leader_tree.heading("POEF Total", text="POEF Total (€)")
        self.leader_tree.heading("Total", text="Total (€)")
        
        # Column widths
        self.leader_tree.column("Leader", width=150)
        self.leader_tree.column("PA Expenses", width=120)
        self.leader_tree.column("POEF Count", width=100)
        self.leader_tree.column("POEF Total", width=120)
        self.leader_tree.column("Total", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.leader_tree.yview)
        self.leader_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.leader_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.leader_tree.bind("<<TreeviewSelect>>", self.on_leader_selected)
        
        # Leader details frame
        leader_details_frame = ttk.LabelFrame(details_frame, text="Selected Leader Details")
        leader_details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Details grid
        details_grid = ttk.Frame(leader_details_frame)
        details_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # PA purchases
        ttk.Label(details_grid, text="PA Purchases:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pa_purchases_label = ttk.Label(details_grid, text="")
        self.pa_purchases_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # POEF count
        ttk.Label(details_grid, text="POEF Count:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.poef_count_label = ttk.Label(details_grid, text="")
        self.poef_count_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Price per drink
        ttk.Label(details_grid, text="Price per Drink:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.price_per_drink_label = ttk.Label(details_grid, text="")
        self.price_per_drink_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
    
    def refresh_display(self):
        """Refresh the summary display."""
        # Clear existing items
        for item in self.leader_tree.get_children():
            self.leader_tree.delete(item)
        
        # Get current data
        leaders = self.main_window.get_leaders()
        receipts = self.main_window.get_receipts()
        
        # Calculate overall summary
        total_receipts = len(receipts)
        total_groepskas = sum(receipt.groepskas_total for receipt in receipts)
        total_poef = sum(receipt.poef_total for receipt in receipts)
        total_pa = sum(receipt.pa_total for receipt in receipts)
        grand_total = total_groepskas + total_poef + total_pa
        
        # Update overall summary labels
        self.total_receipts_label.config(text=str(total_receipts))
        self.total_groepskas_label.config(text=f"€{total_groepskas:.2f}")
        self.total_poef_label.config(text=f"€{total_poef:.2f}")
        self.total_pa_label.config(text=f"€{total_pa:.2f}")
        self.grand_total_label.config(text=f"€{grand_total:.2f}")
        
        # Calculate leader summary
        total_leaders = len(leaders)
        total_leader_expenses = sum(leader.get_total_expenses() for leader in leaders)
        avg_per_leader = total_leader_expenses / total_leaders if total_leaders > 0 else 0
        
        # Update leader summary labels
        self.total_leaders_label.config(text=str(total_leaders))
        self.total_leader_expenses_label.config(text=f"€{total_leader_expenses:.2f}")
        self.avg_per_leader_label.config(text=f"€{avg_per_leader:.2f}")
        
        # Add leader details to treeview
        for leader in leaders:
            pa_expenses = leader.total_pa_expenses
            poef_count = leader.poef_drink_count
            poef_total = leader.get_poef_total()
            total = leader.get_total_expenses()
            
            self.leader_tree.insert("", tk.END, values=(
                leader.name,
                f"€{pa_expenses:.2f}",
                poef_count,
                f"€{poef_total:.2f}",
                f"€{total:.2f}"
            ), tags=(leader.id,))
        
        # Clear leader details
        self.clear_leader_details()
    
    def clear_leader_details(self):
        """Clear the leader details display."""
        self.pa_purchases_label.config(text="")
        self.poef_count_label.config(text="")
        self.price_per_drink_label.config(text="")
    
    def on_leader_selected(self, event):
        """Handle leader selection."""
        selection = self.leader_tree.selection()
        if not selection:
            self.clear_leader_details()
            return
        
        # Get selected leader
        item = selection[0]
        leader_id = self.leader_tree.item(item, "tags")[0]
        leaders = self.main_window.get_leaders()
        leader = next((l for l in leaders if l.id == leader_id), None)
        
        if leader:
            self.display_leader_details(leader)
    
    def display_leader_details(self, leader: Leader):
        """Display details for a selected leader."""
        # PA purchases
        pa_count = len(leader.pa_purchases)
        self.pa_purchases_label.config(text=f"{pa_count} items")
        
        # POEF count
        self.poef_count_label.config(text=f"{leader.poef_drink_count} drinks")
        
        # Price per drink
        self.price_per_drink_label.config(text=f"€{leader.poef_price_per_drink:.2f}")
    
    def generate_summary(self):
        """Generate a comprehensive summary report."""
        leaders = self.main_window.get_leaders()
        receipts = self.main_window.get_receipts()
        
        if not leaders and not receipts:
            messagebox.showinfo("Info", "No data available to generate summary")
            return
        
        # Generate summary using finance service
        summary = self.main_window.finance_service.generate_summary_report(leaders, receipts)
        
        # Display summary in a dialog
        self.show_summary_dialog(summary)
    
    def show_summary_dialog(self, summary: Dict):
        """Show summary in a dialog."""
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Financial Summary Report")
        dialog.geometry("800x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.geometry("+%d+%d" % (
            self.winfo_rootx() + 50,
            self.winfo_rooty() + 50
        ))
        
        # Create text widget for summary
        text_widget = tk.Text(dialog, wrap=tk.WORD, padx=20, pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Format and display summary
        text_widget.insert(tk.END, "KAMP FINANCES - SUMMARY REPORT\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        text_widget.insert(tk.END, f"Report Date: {summary['report_date']}\n\n")
        
        # Receipts summary
        text_widget.insert(tk.END, "RECEIPTS SUMMARY:\n")
        text_widget.insert(tk.END, "-" * 20 + "\n")
        receipts_summary = summary['receipts_summary']
        text_widget.insert(tk.END, f"Total Receipts: {receipts_summary['total_receipts']}\n")
        text_widget.insert(tk.END, f"Total Groepskas: €{receipts_summary['total_groepskas']:.2f}\n")
        text_widget.insert(tk.END, f"Total POEF: €{receipts_summary['total_poef']:.2f}\n")
        text_widget.insert(tk.END, f"Total PA: €{receipts_summary['total_pa']:.2f}\n")
        text_widget.insert(tk.END, f"Grand Total: €{receipts_summary['grand_total']:.2f}\n\n")
        
        # Leaders summary
        text_widget.insert(tk.END, "LEADERS SUMMARY:\n")
        text_widget.insert(tk.END, "-" * 20 + "\n")
        for leader_summary in summary['leaders_summary']:
            text_widget.insert(tk.END, f"{leader_summary['leader_name']}:\n")
            text_widget.insert(tk.END, f"  PA Expenses: €{leader_summary['pa_expenses']:.2f}\n")
            text_widget.insert(tk.END, f"  POEF Expenses: €{leader_summary['poef_expenses']:.2f}\n")
            text_widget.insert(tk.END, f"  Total: €{leader_summary['total_expenses']:.2f}\n\n")
        
        text_widget.insert(tk.END, f"Total Leader Expenses: €{summary['total_leaders_expenses']:.2f}\n")
        
        # Make text read-only
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_button = ttk.Button(dialog, text="Close", command=dialog.destroy)
        close_button.pack(pady=10)
    
    def export_summary(self):
        """Export summary to file."""
        self.main_window.export_summary() 