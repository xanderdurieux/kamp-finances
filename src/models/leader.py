"""
Leader model for Kamp Finances application.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

@dataclass
class Leader:
    """Represents a scouting leader."""
    
    name: str
    phone_number: str = ""
    email: str = ""
    id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    # Financial tracking
    total_pa_expenses: float = 0.0  # Personal purchases
    poef_drink_count: int = 0       # Total drinks from paper list
    poef_price_per_drink: float = 0.75  # Universal price per drink
    
    # History
    pa_purchases: List[Dict] = field(default_factory=list)
    
    def add_pa_purchase(self, item_name: str, price: float, date: str = None):
        """Add a personal purchase."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        purchase = {
            "item": item_name,
            "price": price,
            "date": date
        }
        
        self.pa_purchases.append(purchase)
        self.total_pa_expenses += price
    
    def set_poef_drink_count(self, count: int):
        """Set the total number of drinks from the paper list."""
        self.poef_drink_count = count
    
    def add_poef_drinks(self, count: int):
        """Add drinks to the existing count."""
        self.poef_drink_count += count
    
    def get_poef_total(self) -> float:
        """Calculate total POEF expenses."""
        return self.poef_drink_count * self.poef_price_per_drink
    
    def get_total_expenses(self) -> float:
        """Calculate total expenses for this leader."""
        return self.total_pa_expenses + self.get_poef_total()
    
    def to_dict(self) -> Dict:
        """Convert leader to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "total_pa_expenses": self.total_pa_expenses,
            "poef_drink_count": self.poef_drink_count,
            "poef_price_per_drink": self.poef_price_per_drink,
            "pa_purchases": self.pa_purchases
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Leader':
        """Create leader from dictionary."""
        leader = cls(
            name=data["name"],
            phone_number=data.get("phone_number", ""),
            email=data.get("email", ""),
            id=data.get("id", "")
        )
        
        leader.total_pa_expenses = data.get("total_pa_expenses", 0.0)
        leader.poef_drink_count = data.get("poef_drink_count", 0)
        leader.poef_price_per_drink = data.get("poef_price_per_drink", 0.75)
        leader.pa_purchases = data.get("pa_purchases", [])
        
        return leader 