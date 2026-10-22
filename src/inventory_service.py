"""
Module 3: Order, Inventory and Discount Calculation Service
Part of PyCommerce Open-Source Engine
"""
from typing import Dict, List, Optional


class OrderInventoryManager:
    def __init__(self):
        self.inventory: Dict[str, dict] = {
            "ITEM001": {"name": "Laptop", "price": 1200.0, "stock": 15},
            "ITEM002": {"name": "Wireless Mouse", "price": 25.0, "stock": 50},
            "ITEM003": {"name": "Keyboard", "price": 75.0, "stock": 30},
            "ITEM004": {"name": "Monitor", "price": 300.0, "stock": 20},
        }
        self.valid_coupons = {
            "SAVE10": 0.10,
            "SAVE20": 0.20,
            "VIP50": 0.50
        }
        self.tax_rates = {
            "NY": 0.08875,
            "CA": 0.0725,
            "TX": 0.0625,
            "FL": 0.060,
            "EXEMPT": 0.0
        }

    def check_stock_availability(self, item_id: str, requested_qty: int) -> bool:
        """
        Checks if the requested quantity is available in stock.
        """
        if item_id not in self.inventory:
            raise KeyError(f"Item {item_id} not found in inventory catalog.")
        if not isinstance(requested_qty, int) or requested_qty <= 0:
            raise ValueError("Requested quantity must be a positive integer.")
        return self.inventory[item_id]["stock"] >= requested_qty

    def deduct_stock(self, item_id: str, quantity: int) -> int:
        """
        Deducts stock after successful order placement.
        """
        if not self.check_stock_availability(item_id, quantity):
            raise ValueError(f"Insufficient stock for item {item_id}.")
        self.inventory[item_id]["stock"] -= quantity
        return self.inventory[item_id]["stock"]

    def calculate_tier_discount(self, total_amount: float) -> float:
        """
        Volume tier discount (ECP / BVA):
        - $0.00 to $99.99: 0% discount
        - $100.00 to $499.99: 10% discount
        - $500.00 to $999.99: 15% discount
        - $1000.00 and above: 20% discount
        """
        if total_amount < 0:
            raise ValueError("Total amount cannot be negative.")

        if total_amount < 100.0:
            rate = 0.0
        elif total_amount < 500.0:
            rate = 0.10
        elif total_amount < 1000.0:
            rate = 0.15
        else:
            rate = 0.20

        return round(total_amount * rate, 2)

    def apply_coupon(self, subtotal: float, coupon_code: Optional[str]) -> float:
        """
        Applies a validated promotional coupon code.
        """
        if not coupon_code:
            return 0.0
        code = coupon_code.upper().strip()
        if code not in self.valid_coupons:
            raise ValueError(f"Invalid coupon code: {coupon_code}")

        discount_rate = self.valid_coupons[code]
        return round(subtotal * discount_rate, 2)

    def calculate_tax(self, amount: float, state_code: str) -> float:
        """
        Calculates sales tax based on US state jurisdiction.
        """
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        state = state_code.upper().strip()
        if state not in self.tax_rates:
            raise ValueError(f"Unsupported or invalid state code: {state_code}")

        rate = self.tax_rates[state]
        return round(amount * rate, 2)

    def calculate_final_invoice(self, item_id: str, quantity: int, state_code: str, coupon_code: Optional[str] = None) -> dict:
        """
        Calculates itemized checkout totals.
        """
        if item_id not in self.inventory:
            raise KeyError(f"Item {item_id} not found.")
        if not self.check_stock_availability(item_id, quantity):
            raise ValueError("Item out of stock.")

        base_price = self.inventory[item_id]["price"] * quantity
        tier_disc = self.calculate_tier_discount(base_price)
        subtotal_after_tier = base_price - tier_disc
        coupon_disc = self.apply_coupon(subtotal_after_tier, coupon_code)
        taxable_amount = max(0.0, subtotal_after_tier - coupon_disc)
        tax = self.calculate_tax(taxable_amount, state_code)
        grand_total = round(taxable_amount + tax, 2)

        return {
            "base_price": round(base_price, 2),
            "tier_discount": tier_disc,
            "coupon_discount": coupon_disc,
            "tax": tax,
            "grand_total": grand_total
        }
