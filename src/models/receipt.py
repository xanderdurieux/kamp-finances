"""
Receipt models for Kamp Finances application.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class ExpenseCategory(Enum):
    """Categories for expense allocation."""
    GROEPSKAS = "Groepskas"  # Group account
    POEF = "POEF"           # Fridge drinks
    PA = "PA"               # Personal purchases

@dataclass
class ReceiptItem:
    """Represents a single item on a receipt."""
    
    name: str
    price: float
    quantity: int = 1
    category: ExpenseCategory = ExpenseCategory.GROEPSKAS
    assigned_to: Optional[str] = None  # Leader ID for PA items
    
    def get_total_price(self) -> float:
        """Calculate total price for this item."""
        return self.price * self.quantity
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category.value,
            "assigned_to": self.assigned_to
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReceiptItem':
        """Create from dictionary."""
        return cls(
            name=data["name"],
            price=data["price"],
            quantity=data.get("quantity", 1),
            category=ExpenseCategory(data.get("category", "Groepskas")),
            assigned_to=data.get("assigned_to")
        )

@dataclass
class Receipt:
    """Represents a store receipt."""
    
    date: str
    store_name: str = "Colruyt"
    total_amount: float = 0.0
    items: List[ReceiptItem] = field(default_factory=list)
    id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    # Summary totals
    groepskas_total: float = 0.0
    poef_total: float = 0.0
    pa_total: float = 0.0
    
    def add_item(self, item: ReceiptItem):
        """Add an item to the receipt."""
        self.items.append(item)
        self._update_totals()
    
    def remove_item(self, index: int):
        """Remove an item from the receipt."""
        if 0 <= index < len(self.items):
            del self.items[index]
            self._update_totals()
    
    def _update_totals(self):
        """Update all totals based on current items."""
        self.total_amount = sum(item.get_total_price() for item in self.items)
        
        # Reset category totals
        self.groepskas_total = 0.0
        self.poef_total = 0.0
        self.pa_total = 0.0
        
        # Calculate category totals
        for item in self.items:
            total_price = item.get_total_price()
            if item.category == ExpenseCategory.GROEPSKAS:
                self.groepskas_total += total_price
            elif item.category == ExpenseCategory.POEF:
                self.poef_total += total_price
            elif item.category == ExpenseCategory.PA:
                self.pa_total += total_price
    
    def get_items_by_category(self, category: ExpenseCategory) -> List[ReceiptItem]:
        """Get all items in a specific category."""
        return [item for item in self.items if item.category == category]
    
    def get_pa_items_by_leader(self, leader_id: str) -> List[ReceiptItem]:
        """Get all PA items assigned to a specific leader."""
        return [
            item for item in self.items 
            if item.category == ExpenseCategory.PA and item.assigned_to == leader_id
        ]
    
    def validate_totals(self) -> bool:
        """Validate that category totals match item totals."""
        calculated_total = self.groepskas_total + self.poef_total + self.pa_total
        return abs(calculated_total - self.total_amount) < 0.01
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "date": self.date,
            "store_name": self.store_name,
            "total_amount": self.total_amount,
            "groepskas_total": self.groepskas_total,
            "poef_total": self.poef_total,
            "pa_total": self.pa_total,
            "items": [item.to_dict() for item in self.items]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Receipt':
        """Create from dictionary."""
        receipt = cls(
            date=data["date"],
            store_name=data.get("store_name", "Colruyt"),
            id=data.get("id", "")
        )
        
        receipt.total_amount = data.get("total_amount", 0.0)
        receipt.groepskas_total = data.get("groepskas_total", 0.0)
        receipt.poef_total = data.get("poef_total", 0.0)
        receipt.pa_total = data.get("pa_total", 0.0)
        
        # Load items
        for item_data in data.get("items", []):
            receipt.items.append(ReceiptItem.from_dict(item_data))
        
        return receipt 