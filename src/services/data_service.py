"""
Data service for Kamp Finances application.
Handles data persistence and loading using CSV files.
"""

import csv
import os
from typing import List, Dict, Optional
from datetime import datetime

from models.leader import Leader
from models.receipt import Receipt
from models.expense import Expense

class DataService:
    """Service for managing data persistence using CSV files."""
    
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
        """Load leaders from CSV file."""
        file_path = self._get_file_path("leaders.csv")
        
        if not os.path.exists(file_path):
            return []
        
        leaders = []
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Convert string representations back to proper types
                        leader_data = {
                            "id": row["id"],
                            "name": row["name"],
                            "total_pa_expenses": float(row.get("total_pa_expenses", "0.0")),
                            "poef_drink_count": int(row.get("poef_drink_count", "0")),
                            "poef_saf_count": int(row.get("poef_saf_count", "0")),
                            "pa_purchases": self._parse_pa_purchases(row.get("pa_purchases", ""))
                        }
                        leaders.append(Leader.from_dict(leader_data))
                    except (ValueError, KeyError) as e:
                        print(f"Error parsing leader row: {e}, skipping...")
                        continue
        except Exception as e:
            print(f"Error loading leaders: {e}")
            return []
        
        return leaders
    
    def save_leaders(self, leaders: List[Leader]):
        """Save leaders to CSV file."""
        file_path = self._get_file_path("leaders.csv")
        
        if not leaders:
            # Create empty file with headers
            fieldnames = ["id", "name", "total_pa_expenses", 
                         "poef_drink_count", "poef_saf_count", "pa_purchases"]
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            return
        
        try:
            fieldnames = ["id", "name", "total_pa_expenses", 
                        "poef_drink_count", "poef_saf_count", "pa_purchases"]
            
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for leader in leaders:
                    leader_dict = leader.to_dict()
                    # Convert pa_purchases list to string representation
                    leader_dict["pa_purchases"] = self._serialize_pa_purchases(leader.pa_purchases)
                    writer.writerow(leader_dict)
        except Exception as e:
            print(f"Error saving leaders: {e}")
    
    def load_receipts(self) -> List[Receipt]:
        """Load receipts from CSV files."""
        receipts = []
        
        # Load receipt headers
        headers_file = self._get_file_path("receipts.csv")
        if not os.path.exists(headers_file):
            return receipts
        
        try:
            with open(headers_file, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        receipt_data = {
                            "id": row["id"],
                            "date": row["date"],
                            "store_name": row.get("store_name", "Colruyt"),
                            "total_amount": float(row.get("total_amount", "0.0")),
                            "groepskas_total": float(row.get("groepskas_total", "0.0")),
                            "poef_total": float(row.get("poef_total", "0.0")),
                            "pa_total": float(row.get("pa_total", "0.0"))
                        }
                        
                        # Load items for this receipt
                        items = self._load_receipt_items(row["id"])
                        receipt = Receipt.from_dict(receipt_data)
                        receipt.items = items
                        receipts.append(receipt)
                    except (ValueError, KeyError) as e:
                        print(f"Error parsing receipt row: {e}, skipping...")
                        continue
        except Exception as e:
            print(f"Error loading receipts: {e}")
            return []
        
        return receipts
    
    def save_receipts(self, receipts: List[Receipt]):
        """Save receipts to CSV files."""
        # Save receipt headers
        headers_file = self._get_file_path("receipts.csv")
        
        if not receipts:
            # Create empty file with headers
            fieldnames = ["id", "date", "store_name", "total_amount", 
                         "groepskas_total", "poef_total", "pa_total"]
            with open(headers_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            return
        
        try:
            fieldnames = ["id", "date", "store_name", "total_amount", 
                         "groepskas_total", "poef_total", "pa_total"]
            
            with open(headers_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for receipt in receipts:
                    receipt_dict = receipt.to_dict()
                    # Remove items from dict as they're saved separately
                    del receipt_dict["items"]
                    writer.writerow(receipt_dict)
                    
                    # Save items for this receipt
                    self._save_receipt_items(receipt.id, receipt.items)
        except Exception as e:
            print(f"Error saving receipts: {e}")
    
    def _load_receipt_items(self, receipt_id: str) -> List[Expense]:
        """Load items for a specific receipt."""
        items_file = self._get_file_path(f"receipt_items_{receipt_id}.csv")
        
        if not os.path.exists(items_file):
            return []
        
        items = []
        try:
            with open(items_file, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        item_data = {
                            "id": row.get("id", ""),
                            "name": row["name"],
                            "price": float(row["price"]),
                            "quantity": float(row.get("quantity", "1.0")),
                            "category": row.get("category", "Groepskas"),
                            "date": row.get("date", ""),
                            "receipt_id": row.get("receipt_id", receipt_id)
                        }
                        items.append(Expense.from_dict(item_data))
                    except (ValueError, KeyError) as e:
                        print(f"Error parsing receipt item row: {e}, skipping...")
                        continue
        except Exception as e:
            print(f"Error loading receipt items for {receipt_id}: {e}")
        
        return items
    
    def _save_receipt_items(self, receipt_id: str, items: List[Expense]):
        """Save items for a specific receipt."""
        items_file = self._get_file_path(f"receipt_items_{receipt_id}.csv")
        
        if not items:
            # Create empty file with headers
            fieldnames = ["id", "name", "price", "quantity", "category", "date", "receipt_id"]
            with open(items_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            return
        
        try:
            fieldnames = ["id", "name", "price", "quantity", "category", "date", "receipt_id"]
            
            with open(items_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in items:
                    item_dict = item.to_dict()
                    writer.writerow(item_dict)
        except Exception as e:
            print(f"Error saving receipt items for {receipt_id}: {e}")
    
    def _serialize_pa_purchases(self, purchases: Dict[str, float]) -> str:
        """Convert pa_purchases dictionary to CSV-compatible string."""
        if not purchases:
            return ""
        
        # Format: "id1:amount1|id2:amount2|id3:amount3"
        return "|".join([f"{expense_id}:{amount}" for expense_id, amount in purchases.items()])
    
    def _parse_pa_purchases(self, purchases_str: str) -> Dict[str, float]:
        """Parse pa_purchases string back to dictionary of expense IDs and amounts."""
        if not purchases_str:
            return {}
        
        purchases = {}
        for item in purchases_str.split("|"):
            if ":" in item:
                expense_id, amount_str = item.split(":", 1)
                try:
                    amount = float(amount_str)
                    purchases[expense_id] = amount
                except ValueError:
                    # Handle legacy data that might be just IDs without amounts
                    purchases[expense_id] = 0.0
            else:
                # Handle legacy data that might be just IDs
                purchases[item] = 0.0
        
        return purchases
    
    def save_all_data(self, leaders: List[Leader], receipts: List[Receipt]):
        """Save all data to files."""
        self.save_leaders(leaders)
        self.save_receipts(receipts)
    
    def export_summary(self, leaders: List[Leader], receipts: List[Receipt], filename: str = None):
        """Export a summary report to CSV."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_{timestamp}.csv"
        
        file_path = self._get_file_path(filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(["Summary Report", datetime.now().isoformat()])
                writer.writerow([])
                
                # Write totals
                writer.writerow(["Category", "Total"])
                writer.writerow(["Total Groepskas", sum(receipt.groepskas_total for receipt in receipts)])
                writer.writerow(["Total POEF", sum(receipt.poef_total for receipt in receipts)])
                writer.writerow(["Total PA", sum(receipt.pa_total for receipt in receipts)])
                writer.writerow(["Total Leaders Expenses", sum(leader.get_total_expenses() for leader in leaders)])
                writer.writerow([])
                
                # Write leaders summary
                writer.writerow(["Leaders Summary"])
                writer.writerow(["Name", "Total PA Expenses", "POEF Drinks", "POEF SAFs", "POEF Total", "Total Expenses"])
                for leader in leaders:
                    writer.writerow([
                        leader.name,
                        leader.total_pa_expenses,
                        leader.poef_drink_count,
                        leader.poef_saf_count,
                        leader.get_poef_total(),
                        leader.get_total_expenses()
                    ])
                writer.writerow([])
                
                # Write receipts summary
                writer.writerow(["Receipts Summary"])
                writer.writerow(["Date", "Store", "Total Amount", "Groepskas", "POEF", "PA"])
                for receipt in receipts:
                    writer.writerow([
                        receipt.date,
                        receipt.store_name,
                        receipt.total_amount,
                        receipt.groepskas_total,
                        receipt.poef_total,
                        receipt.pa_total
                    ])
            
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
        
        # Get all CSV files to backup
        files_to_backup = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.csv'):
                files_to_backup.append(filename)
        
        for filename in files_to_backup:
            source_path = self._get_file_path(filename)
            backup_path = os.path.join(backup_dir, filename)
            try:
                with open(source_path, 'r', encoding='utf-8') as source:
                    with open(backup_path, 'w', encoding='utf-8') as backup:
                        backup.write(source.read())
            except Exception as e:
                print(f"Error backing up {filename}: {e}")
        
        return backup_dir 