"""
Finance service for Kamp Finances application.
Handles business logic for calculations and expense management.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re

from models.leader import Leader
from models.receipt import Receipt
from models.expense import Expense, ExpenseCategory
from services.data_service import DataService

class FinanceService:
    """Service for handling finance-related business logic."""
    
    def __init__(self, data_service: DataService):
        self.data_service = data_service
    
    def process_text_message(self, message: str, leader: Leader) -> List[Dict]:
        """Process a text message containing PA orders and extract items."""
        items = []
        
        # Simple pattern matching for common formats
        # Look for patterns like "PA: item1, item2" or "PA item1 €2.50"
        pa_patterns = [
            r'PA:\s*(.+)',  # PA: item1, item2
            r'PA\s+(.+)',   # PA item1 €2.50
            r'persoonlijke aankoop:\s*(.+)',  # persoonlijke aankoop: item1
        ]
        
        for pattern in pa_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                # Split by common separators
                item_list = re.split(r'[,;]', match.strip())
                for item in item_list:
                    item = item.strip()
                    if item:
                        # Try to extract price if present
                        price_match = re.search(r'€?\s*(\d+[.,]\d{2})', item)
                        price = float(price_match.group(1).replace(',', '.')) if price_match else 0.0
                        
                        # Clean item name
                        item_name = re.sub(r'€?\s*\d+[.,]\d{2}', '', item).strip()
                        
                        if item_name:
                            items.append({
                                "name": item_name,
                                "price": price,
                                "leader_id": leader.id,
                                "date": datetime.now().strftime("%Y-%m-%d")
                            })
        
        return items
    
    def create_receipt_from_items(self, items: List[Dict], date: str = None) -> Receipt:
        """Create a receipt from a list of items."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        receipt = Receipt(date=date)
        
        for item_data in items:
            item = Expense(
                name=item_data["name"],
                price=item_data["price"],
                category=ExpenseCategory.PA,
                date=date
            )
            receipt.add_item(item)
        
        return receipt
    
    def calculate_leader_expenses(self, leader: Leader, receipts: List[Receipt]) -> Dict:
        """Calculate total expenses for a leader."""
        pa_total = leader.total_pa_expenses
        poef_total = leader.get_poef_total()
        
        # Add PA items from receipts that are in the leader's pa_purchases
        for receipt in receipts:
            pa_items = receipt.get_items_by_category(ExpenseCategory.PA)
            for item in pa_items:
                if leader.has_pa_purchase(item.id):
                    pa_total += item.get_total_price()
        
        return {
            "leader_id": leader.id,
            "leader_name": leader.name,
            "pa_expenses": pa_total,
            "poef_expenses": poef_total,
            "total_expenses": pa_total + poef_total,
            "pa_items_count": len(leader.pa_purchases),
            "poef_drinks_count": leader.poef_drink_count,
            "poef_saf_count": leader.poef_saf_count
        }
    
    def generate_summary_report(self, leaders: List[Leader], receipts: List[Receipt]) -> Dict:
        """Generate a comprehensive summary report."""
        leader_summaries = []
        total_groepskas = 0.0
        total_poef = 0.0
        total_pa = 0.0
        
        # Calculate receipt totals
        for receipt in receipts:
            total_groepskas += receipt.groepskas_total
            total_poef += receipt.poef_total
            total_pa += receipt.pa_total
        
        # Calculate leader expenses
        for leader in leaders:
            summary = self.calculate_leader_expenses(leader, receipts)
            leader_summaries.append(summary)
        
        return {
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "receipts_summary": {
                "total_receipts": len(receipts),
                "total_groepskas": total_groepskas,
                "total_poef": total_poef,
                "total_pa": total_pa,
                "grand_total": total_groepskas + total_poef + total_pa
            },
            "leaders_summary": leader_summaries,
            "total_leaders_expenses": sum(s["total_expenses"] for s in leader_summaries)
        }
    
    def validate_receipt(self, receipt: Receipt) -> Tuple[bool, List[str]]:
        """Validate a receipt for consistency."""
        errors = []
        
        # Check if totals match
        if not receipt.validate_totals():
            errors.append("Receipt totals don't match item totals")
        
        # Check for items without categories
        uncategorized = [item for item in receipt.items if item.category is None]
        if uncategorized:
            errors.append(f"Found {len(uncategorized)} items without categories")
        
        return len(errors) == 0, errors
    
    def set_poef_drink_count(self, leader: Leader, count: int):
        """Set the POEF drink count for a leader from the paper list."""
        leader.set_poef_drink_count(count)
    
    def add_poef_drinks(self, leader: Leader, count: int):
        """Add drinks to the existing POEF count for a leader."""
        leader.add_poef_drinks(count)
    
    def set_poef_saf_count(self, leader: Leader, count: int):
        """Set the POEF SAF count for a leader from the paper list."""
        leader.set_poef_saf_count(count)
    
    def add_poef_safs(self, leader: Leader, count: int):
        """Add SAFs to the existing POEF count for a leader."""
        leader.add_poef_safs(count)
    
    def get_leaders_by_name(self, leaders: List[Leader], name: str) -> List[Leader]:
        """Find leaders by name (partial match)."""
        name_lower = name.lower()
        return [leader for leader in leaders if name_lower in leader.name.lower()]
    
    def get_receipts_by_date(self, receipts: List[Receipt], date: str) -> List[Receipt]:
        """Get receipts for a specific date."""
        return [receipt for receipt in receipts if receipt.date == date]
    
    def calculate_daily_totals(self, receipts: List[Receipt], date: str) -> Dict:
        """Calculate totals for a specific date."""
        daily_receipts = self.get_receipts_by_date(receipts, date)
        
        return {
            "date": date,
            "receipts_count": len(daily_receipts),
            "groepskas_total": sum(r.groepskas_total for r in daily_receipts),
            "poef_total": sum(r.poef_total for r in daily_receipts),
            "pa_total": sum(r.pa_total for r in daily_receipts),
            "grand_total": sum(r.total_amount for r in daily_receipts)
        } 