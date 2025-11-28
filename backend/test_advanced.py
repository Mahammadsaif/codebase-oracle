import os
from typing import List, Dict

def calculate_total(items: List[float]) -> float:
    """Calculate total price of items."""
    return sum(items)

class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add_item(self, item: str, price: float):
        """Add item to cart."""
        self.items.append({"name": item, "price": price})
    
    def get_total(self) -> float:
        """Calculate cart total."""
        prices = [item["price"] for item in self.items]
        return calculate_total(prices)

def process_order(cart: ShoppingCart) -> Dict[str, float]:
    total = cart.get_total()
    return {"total": total, "tax": total * 0.08}