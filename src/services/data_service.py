"""
Data service for Kamp Finances application.
Handles data persistence and loading.
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime

from models.leader import Leader
from models.receipt import Receipt
from models.expense import Expense

class DataService:
    """Service for managing data persistence."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _get_file_path(self, filename: str) -> str:
        """Get full path for a data file."""
        return os.path.join(self.data_dir, filename)
    
    def load_leaders(self) -> List[Leader]:
        """Load leaders from JSON file."""
        file_path = self._get_file_path("leaders.json")
        
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Leader.from_dict(leader_data) for leader_data in data]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading leaders: {e}")
            return []
    
    def save_leaders(self, leaders: List[Leader]):
        """Save leaders to JSON file."""
        file_path = self._get_file_path("leaders.json")
        
        try:
            data = [leader.to_dict() for leader in leaders]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving leaders: {e}")
    
    def load_receipts(self) -> List[Receipt]:
        """Load receipts from JSON file."""
        file_path = self._get_file_path("receipts.json")
        
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Receipt.from_dict(receipt_data) for receipt_data in data]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading receipts: {e}")
            return []
    
    def save_receipts(self, receipts: List[Receipt]):
        """Save receipts to JSON file."""
        file_path = self._get_file_path("receipts.json")
        
        try:
            data = [receipt.to_dict() for receipt in receipts]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving receipts: {e}")
    
    def save_all_data(self, leaders: List[Leader], receipts: List[Receipt]):
        """Save all data to files."""
        self.save_leaders(leaders)
        self.save_receipts(receipts)
    
    def export_summary(self, leaders: List[Leader], receipts: List[Receipt], filename: str = None):
        """Export a summary report to JSON."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_{timestamp}.json"
        
        file_path = self._get_file_path(filename)
        
        summary = {
            "export_date": datetime.now().isoformat(),
            "leaders": [leader.to_dict() for leader in leaders],
            "receipts": [receipt.to_dict() for receipt in receipts],
            "totals": {
                "total_groepskas": sum(receipt.groepskas_total for receipt in receipts),
                "total_poef": sum(receipt.poef_total for receipt in receipts),
                "total_pa": sum(receipt.pa_total for receipt in receipts),
                "total_leaders_expenses": sum(leader.get_total_expenses() for leader in leaders)
            }
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            return file_path
        except Exception as e:
            print(f"Error exporting summary: {e}")
            return None
    
    def backup_data(self):
        """Create a backup of all data files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.data_dir, f"backup_{timestamp}")
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        files_to_backup = ["leaders.json", "receipts.json"]
        
        for filename in files_to_backup:
            source_path = self._get_file_path(filename)
            if os.path.exists(source_path):
                backup_path = os.path.join(backup_dir, filename)
                try:
                    with open(source_path, 'r', encoding='utf-8') as source:
                        with open(backup_path, 'w', encoding='utf-8') as backup:
                            backup.write(source.read())
                except Exception as e:
                    print(f"Error backing up {filename}: {e}")
        
        return backup_dir 