"""
Base UI components for Kamp Finances application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, List, Dict
from datetime import datetime

class BaseTab(ttk.Frame):
    """Base class for all tabs with common functionality."""
    
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.create_widgets()
    
    def create_widgets(self):
        """Override this method to create tab-specific widgets."""
        pass
    
    def refresh_data(self):
        """Override this method to refresh tab data."""
        pass
    
    def show_error(self, message: str):
        """Show error message."""
        messagebox.showerror("Error", message)
    
    def show_info(self, message: str):
        """Show info message."""
        messagebox.showinfo("Info", message)
    
    def show_confirm(self, message: str) -> bool:
        """Show confirmation dialog."""
        return messagebox.askyesno("Confirm", message)

class DataTable(ttk.Frame):
    """Reusable data table component with sorting and filtering."""
    
    def __init__(self, parent, columns: List[Dict], height: int = 10):
        super().__init__(parent)
        self.columns = columns
        self.height = height
        self.tree = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create the table widgets."""
        # Create treeview
        column_names = [col["name"] for col in self.columns]
        self.tree = ttk.Treeview(self, columns=column_names, show="headings", height=self.height)
        
        # Configure columns
        for i, col in enumerate(self.columns):
            self.tree.heading(column_names[i], text=col["display"], command=lambda c=column_names[i]: self.sort_column(c))
            self.tree.column(column_names[i], width=col.get("width", 100), anchor=col.get("anchor", tk.W))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def clear_data(self):
        """Clear all data from the table."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def add_row(self, values: List, tags: Optional[List] = None):
        """Add a row to the table."""
        if tags is None:
            tags = []
        # Ensure all tags are strings to prevent Tkinter from converting them
        string_tags = [str(tag) for tag in tags]
        self.tree.insert("", tk.END, values=values, tags=string_tags)
    
    def get_selected_item(self):
        """Get the currently selected item."""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])
        return None
    
    def bind_selection_event(self, callback):
        """Bind a selection event to the table."""
        self.tree.bind("<<TreeviewSelect>>", callback)
    
    def get_tree(self):
        """Get the underlying treeview widget."""
        return self.tree
    
    def sort_column(self, column: str):
        """Sort the table by column."""
        # Get all items
        items = [(self.tree.set(item, column), item) for item in self.tree.get_children("")]
        
        # Sort items
        items.sort(key=lambda x: self._sort_key(x[0]))
        
        # Rearrange items
        for index, (val, item) in enumerate(items):
            self.tree.move(item, "", index)
    
    def _sort_key(self, value: str):
        """Convert value to appropriate type for sorting."""
        try:
            # Try to convert to float (for currency values)
            if value.startswith("€"):
                return float(value[1:])
            return float(value)
        except ValueError:
            # Return as string
            return value.lower()

class FormDialog(tk.Toplevel):
    """Base class for form dialogs."""
    
    def __init__(self, parent, title: str, fields: List[Dict]):
        super().__init__(parent)
        self.title(title)
        self.fields = fields
        self.field_widgets = {}
        self.result = None
        
        self.setup_dialog()
        self.create_widgets()
        
        # Center dialog
        self.center_dialog()
    
    def setup_dialog(self):
        """Setup dialog properties."""
        self.transient(self.master)
        self.grab_set()
        self.resizable(False, False)
    
    def create_widgets(self):
        """Create form widgets."""
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create field widgets
        for i, field in enumerate(self.fields):
            # Label
            label = ttk.Label(main_frame, text=field["label"])
            label.grid(row=i, column=0, sticky=tk.W, pady=5, padx=(0, 10))
            
            # Input widget
            if field["type"] == "entry":
                widget = ttk.Entry(main_frame, width=30)
            elif field["type"] == "combobox":
                widget = ttk.Combobox(main_frame, values=field.get("values", []), width=27, state="readonly")
            elif field["type"] == "spinbox":
                widget = ttk.Spinbox(main_frame, from_=field.get("from_", 0), to=field.get("to", 100), width=27)
            
            widget.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5)
            self.field_widgets[field["name"]] = widget
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(self.fields), column=0, columnspan=2, pady=(20, 0))
        
        # OK button
        ok_button = ttk.Button(button_frame, text="OK", command=self.on_ok)
        ok_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def center_dialog(self):
        """Center the dialog on the parent window."""
        self.update_idletasks()
        x = self.master.winfo_rootx() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.master.winfo_rooty() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def get_field_value(self, field_name: str):
        """Get the value of a field."""
        widget = self.field_widgets.get(field_name)
        if widget and widget.winfo_exists():
            try:
                return widget.get()
            except tk.TclError:
                # Widget has been destroyed
                return ""
        return ""
    
    def set_field_value(self, field_name: str, value):
        """Set the value of a field."""
        widget = self.field_widgets.get(field_name)
        if widget and widget.winfo_exists():
            try:
                widget.delete(0, tk.END)
                widget.insert(0, str(value))
            except tk.TclError:
                # Widget has been destroyed
                pass
    
    def validate_form(self) -> bool:
        """Override this method to add form validation."""
        return True
    
    def on_ok(self):
        """Handle OK button click."""
        if self.validate_form():
            self.result = self.get_form_data()
            self.destroy()
    
    def on_cancel(self):
        """Handle Cancel button click."""
        self.result = None
        self.destroy()
    
    def get_form_data(self) -> Dict:
        """Get all form data as a dictionary."""
        data = {}
        for field in self.fields:
            data[field["name"]] = self.get_field_value(field["name"])
        return data

class ActionButton(ttk.Button):
    """Enhanced button with confirmation support."""
    
    def __init__(self, parent, text: str, command: Callable, confirm_message: Optional[str] = None, **kwargs):
        self.confirm_message = confirm_message
        self.original_command = command
        
        if confirm_message:
            super().__init__(parent, text=text, command=command, **kwargs)
        else:
            super().__init__(parent, text=text, command=command, **kwargs)
    
    def _confirmed_command(self):
        """Execute command with confirmation."""
        if messagebox.askyesno("Confirm", self.confirm_message):
            self.original_command() 