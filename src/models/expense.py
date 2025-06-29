"""
Expense models for Kamp Finances application.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ExpenseCategory(Enum):
    """Categories for expense allocation."""
    GROEPSKAS = "Groepskas"  
    POEF = "POEF"           
    PA = "PA"               

@dataclass
class Expense:
    """Represents an individual expense entry."""
    
    name: str
    price: float
    category: ExpenseCategory
    date: str
    quantity: float = 1.0
    receipt_id: str = None 
    id: str = None
    
    def __post_init__(self):
        """Generate ID if not provided"""
        if self.id is None:
            self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def get_total_price(self) -> float:
        """Calculate total price for this expense."""
        return self.price * self.quantity
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category.value,
            "date": self.date,
            "receipt_id": self.receipt_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
        """Create from dictionary."""
        return cls(
            name=data["name"],
            price=data["price"],
            quantity=data.get("quantity", 1.0),
            category=ExpenseCategory(data["category"]),
            date=data["date"],
            receipt_id=data.get("receipt_id"),
            id=data.get("id")
        ) 