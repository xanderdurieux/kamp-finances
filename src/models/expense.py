"""
Expense models for Kamp Finances application.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

class ExpenseCategory(Enum):
    """Categories for expense allocation."""
    GROEPSKAS = "Groepskas"  # Group account
    POEF = "POEF"           # Fridge drinks
    PA = "PA"               # Personal purchases

@dataclass
class Expense:
    """Represents an individual expense entry."""
    
    amount: float
    description: str
    category: ExpenseCategory
    date: str
    leader_id: Optional[str] = None  # For PA expenses
    receipt_id: Optional[str] = None  # Link to receipt if applicable
    id: str = None
    
    def __post_init__(self):
        """Generate ID if not provided."""
        if self.id is None:
            self.id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "category": self.category.value,
            "date": self.date,
            "leader_id": self.leader_id,
            "receipt_id": self.receipt_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
        """Create from dictionary."""
        return cls(
            amount=data["amount"],
            description=data["description"],
            category=ExpenseCategory(data["category"]),
            date=data["date"],
            leader_id=data.get("leader_id"),
            receipt_id=data.get("receipt_id"),
            id=data.get("id")
        ) 