"""
Leader model for Kamp Finances application.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from models.expense import Expense

POEF_DRINK_PRICE = 0.75
POEF_CIGARETTE_PRICE = 12

@dataclass
class Leader:
    """Represents a scouting leader."""
    
    name: str
    id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d%H%M%S"))
    
    # Financial tracking
    total_pa_expenses: float = 0.0  # Personal purchases
    poef_drink_count: int = 0       # Total drinks from paper list
    poef_cigarette_count: int = 0         # Total cigarettes from paper list
    paid_amount: float = 0.0
    
    # History - stores expense IDs and amounts that belong to this leader
    pa_purchases: Dict[str, float] = field(default_factory=dict)
    
    def add_pa_purchase(self, expense_id: str, amount: float):
        """Add a personal purchase expense."""
        self.pa_purchases[expense_id] = amount
        self._recalculate_pa_total()
    
    def remove_pa_purchase(self, expense_id: str, amount: float):
        """Remove a personal purchase expense."""
        if expense_id in self.pa_purchases:
            del self.pa_purchases[expense_id]
            self._recalculate_pa_total()
    
    def has_pa_purchase(self, expense_id: str) -> bool:
        """Check if leader has a specific PA purchase."""
        return expense_id in self.pa_purchases
    
    def get_pa_purchase_amount(self, expense_id: str) -> float:
        """Get the amount this leader pays for a specific PA purchase."""
        return self.pa_purchases.get(expense_id, 0.0)
    
    def _recalculate_pa_total(self):
        """Recalculate the total PA expenses."""
        self.total_pa_expenses = sum(self.pa_purchases.values())
    
    def set_poef_drink_count(self, count: int):
        """Set the total number of drinks from the paper list."""
        self.poef_drink_count = count
    
    def add_poef_drinks(self, count: int):
        """Add drinks to the existing count."""
        self.poef_drink_count += count
    
    def set_poef_cigarette_count(self, count: int):
        """Set the total number of cigarettes from the paper list."""
        self.poef_cigarette_count = count
    
    def add_poef_cigarettes(self, count: int):
        """Add cigarettes to the existing count."""
        self.poef_cigarette_count += count
    
    def get_poef_total(self) -> float:
        """Calculate total POEF expenses."""
        return self.poef_drink_count * POEF_DRINK_PRICE + self.poef_cigarette_count * POEF_CIGARETTE_PRICE
    
    def get_total_expenses(self) -> float:
        """Calculate total expenses for this leader."""
        return self.total_pa_expenses + self.get_poef_total()
    
    def get_remaining_to_pay(self) -> float:
        """Return what is left to pay after subtracting paid_amount from total expenses."""
        return self.get_total_expenses() - self.paid_amount
    
    def to_dict(self) -> Dict:
        """Convert leader to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "total_pa_expenses": self.total_pa_expenses,
            "poef_drink_count": self.poef_drink_count,
            "poef_cigarette_count": self.poef_cigarette_count,
            "pa_purchases": self.pa_purchases,
            "paid_amount": self.paid_amount
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Leader':
        """Create leader from dictionary."""
        leader = cls(
            name=data["name"],
            id=data.get("id", "")
        )
        
        leader.total_pa_expenses = data.get("total_pa_expenses", 0.0)
        leader.poef_drink_count = data.get("poef_drink_count", 0)
        leader.poef_cigarette_count = data.get("poef_cigarette_count", 0)
        leader.pa_purchases = data.get("pa_purchases", {})
        leader.paid_amount = data.get("paid_amount", 0.0)
        
        return leader 