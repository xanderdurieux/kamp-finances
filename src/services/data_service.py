"""
Data service for Kamp Finances application.
Handles data persistence and loading using SQLite database.
"""

import os
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

from models.leader import Leader
from models.receipt import Receipt
from models.expense import Expense

class DataService:
    """Service for managing data persistence using SQLite."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_directory()
        self.db_path = os.path.join(self.data_dir, "kamp_finances.db")
        self._ensure_tables()

    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _ensure_tables(self):
        """Create tables if they don't exist, and add paid_amount if missing."""
        with self._get_connection() as conn:
            c = conn.cursor()
            # Leaders table
            c.execute('''
                CREATE TABLE IF NOT EXISTS leaders (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    total_pa_expenses REAL DEFAULT 0.0,
                    poef_drink_count INTEGER DEFAULT 0,
                    poef_cigarette_count INTEGER DEFAULT 0,
                    pa_purchases TEXT DEFAULT '',
                    paid_amount REAL DEFAULT 0.0
                )
            ''')
            # Try to add paid_amount if missing (for upgrades)
            try:
                c.execute('ALTER TABLE leaders ADD COLUMN paid_amount REAL DEFAULT 0.0')
            except Exception:
                pass  # Already exists
            # Receipts table
            c.execute('''
                CREATE TABLE IF NOT EXISTS receipts (
                    id TEXT PRIMARY KEY,
                    date TEXT NOT NULL,
                    store_name TEXT DEFAULT 'Colruyt',
                    total_amount REAL DEFAULT 0.0,
                    groepskas_total REAL DEFAULT 0.0,
                    poef_total REAL DEFAULT 0.0,
                    pa_total REAL DEFAULT 0.0
                )
            ''')
            # Receipt items table
            c.execute('''
                CREATE TABLE IF NOT EXISTS receipt_items (
                    id TEXT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity REAL DEFAULT 1.0,
                    category TEXT DEFAULT 'Groepskas',
                    date TEXT,
                    receipt_id TEXT,
                    PRIMARY KEY (id, receipt_id),
                    FOREIGN KEY (receipt_id) REFERENCES receipts(id) ON DELETE CASCADE
                )
            ''')
            conn.commit()

    def load_leaders(self) -> List[Leader]:
        """Load leaders from SQLite database."""
        leaders = []
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT id, name, total_pa_expenses, poef_drink_count, poef_cigarette_count, pa_purchases, paid_amount FROM leaders")
            rows = c.fetchall()
            for row in rows:
                leader_data = {
                    "id": row[0],
                    "name": row[1],
                    "total_pa_expenses": float(row[2]),
                    "poef_drink_count": int(row[3]),
                    "poef_cigarette_count": int(row[4]),
                    "pa_purchases": self._parse_pa_purchases(row[5]),
                    "paid_amount": float(row[6]) if row[6] is not None else 0.0
                }
                leaders.append(Leader.from_dict(leader_data))
        return leaders

    def save_leaders(self, leaders: List[Leader]):
        """Save leaders to SQLite database."""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM leaders")  # Clear table before saving all
            for leader in leaders:
                leader_dict = leader.to_dict()
                pa_purchases_str = self._serialize_pa_purchases(leader.pa_purchases)
                c.execute('''
                    INSERT INTO leaders (id, name, total_pa_expenses, poef_drink_count, poef_cigarette_count, pa_purchases, paid_amount)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    leader_dict["id"],
                    leader_dict["name"],
                    leader_dict["total_pa_expenses"],
                    leader_dict["poef_drink_count"],
                    leader_dict["poef_cigarette_count"],
                    pa_purchases_str,
                    leader_dict["paid_amount"]
                ))
            conn.commit()

    def load_receipts(self) -> List[Receipt]:
        """Load receipts from SQLite database."""
        receipts = []
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT id, date, store_name, total_amount, groepskas_total, poef_total, pa_total FROM receipts")
            rows = c.fetchall()
            for row in rows:
                receipt_data = {
                    "id": row[0],
                    "date": row[1],
                    "store_name": row[2],
                    "total_amount": float(row[3]),
                    "groepskas_total": float(row[4]),
                    "poef_total": float(row[5]),
                    "pa_total": float(row[6])
                }
                items = self._load_receipt_items(row[0], conn)
                receipt = Receipt.from_dict(receipt_data)
                receipt.items = items
                receipts.append(receipt)
        return receipts

    def save_receipts(self, receipts: List[Receipt]):
        """Save receipts to SQLite database."""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM receipts")
            c.execute("DELETE FROM receipt_items")
            for receipt in receipts:
                receipt_dict = receipt.to_dict()
                c.execute('''
                    INSERT INTO receipts (id, date, store_name, total_amount, groepskas_total, poef_total, pa_total)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    receipt_dict["id"],
                    receipt_dict["date"],
                    receipt_dict["store_name"],
                    receipt_dict["total_amount"],
                    receipt_dict["groepskas_total"],
                    receipt_dict["poef_total"],
                    receipt_dict["pa_total"]
                ))
                self._save_receipt_items(receipt.id, receipt.items, conn)
            conn.commit()

    def _load_receipt_items(self, receipt_id: str, conn=None) -> List[Expense]:
        """Load items for a specific receipt from SQLite."""
        close_conn = False
        if conn is None:
            conn = self._get_connection()
            close_conn = True
        items = []
        c = conn.cursor()
        c.execute("SELECT id, name, price, quantity, category, date, receipt_id FROM receipt_items WHERE receipt_id = ?", (receipt_id,))
        rows = c.fetchall()
        for row in rows:
            item_data = {
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "quantity": float(row[3]),
                "category": row[4],
                "date": row[5],
                "receipt_id": row[6]
            }
            items.append(Expense.from_dict(item_data))
        if close_conn:
            conn.close()
        return items

    def _save_receipt_items(self, receipt_id: str, items: List[Expense], conn=None):
        """Save items for a specific receipt to SQLite."""
        close_conn = False
        if conn is None:
            conn = self._get_connection()
            close_conn = True
        c = conn.cursor()
        for item in items:
            item_dict = item.to_dict()
            c.execute('''
                INSERT INTO receipt_items (id, name, price, quantity, category, date, receipt_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                item_dict.get("id", ""),
                item_dict["name"],
                item_dict["price"],
                item_dict.get("quantity", 1.0),
                item_dict.get("category", "Groepskas"),
                item_dict.get("date", ""),
                receipt_id
            ))
        if close_conn:
            conn.commit()
            conn.close()
    
    def _serialize_pa_purchases(self, purchases: Dict[str, float]) -> str:
        """Convert pa_purchases dictionary to serializable string."""
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
        """Export a summary report to CSV (from in-memory data)."""
        import csv
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_{timestamp}.csv"
        file_path = os.path.join(self.data_dir, filename)
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
                writer.writerow(["Name", "Total PA Expenses", "POEF Drinks", "POEF Cigarettes", "POEF Total", "Total Expenses", "Paid Amount", "Remaining to Pay"])
                for leader in leaders:
                    writer.writerow([
                        leader.name,
                        leader.total_pa_expenses,
                        leader.poef_drink_count,
                        leader.poef_cigarette_count,
                        leader.get_poef_total(),
                        leader.get_total_expenses(),
                        leader.paid_amount,
                        leader.get_remaining_to_pay()
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
        """Create a backup of the SQLite database file."""
        from shutil import copy2
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.data_dir, f"backup_{timestamp}")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        db_backup_path = os.path.join(backup_dir, "kamp_finances.db")
        try:
            copy2(self.db_path, db_backup_path)
            return backup_dir
        except Exception as e:
            print(f"Error backing up database: {e}")
            return None 