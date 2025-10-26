from dataclasses import dataclass

@dataclass
class ClothingItem:
    """Class for keeping track of a clothing item."""
    name: str
    category: str
    size: str

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
