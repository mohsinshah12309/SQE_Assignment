"""
Test Suite for Module 3: Order, Inventory and Discount Calculation Service
Tester / Author: Group Partner (Group Member 2)
Covers Task 2 (ECP & BVA) & Task 4 (Parameterization, Markers, Execution Ordering)
"""
import pytest
from src.inventory_service import OrderInventoryManager


@pytest.fixture
def inventory_manager():
    """Provides a fresh OrderInventoryManager instance."""
    return OrderInventoryManager()


# ============================================================================
# 1. Tests for check_stock_availability & deduct_stock (ECP & BVA)
# ============================================================================
@pytest.mark.module3_inv
@pytest.mark.smoke
@pytest.mark.order(10)
class TestStockManagement:

    @pytest.mark.parametrize("item_id, qty, expected_result", [
        ("ITEM001", 1, True),       # Nominal available stock
        ("ITEM001", 15, True),      # BVA: Exact available stock boundary (15 units)
        ("ITEM001", 16, False),     # BVA: Just above stock boundary (16 units)
        ("ITEM002", 50, True),      # BVA: Exact stock limit for mouse
        ("ITEM002", 51, False)      # BVA: Exceeds stock limit
    ])
    def test_stock_availability_boundaries(self, inventory_manager, item_id, qty, expected_result):
        """Tests stock boundary checks."""
        assert inventory_manager.check_stock_availability(item_id, qty) is expected_result

    def test_stock_check_invalid_item_raises_key_error(self, inventory_manager):
        """Tests unknown item query error handling."""
        with pytest.raises(KeyError, match="Item ITEM999 not found"):
            inventory_manager.check_stock_availability("ITEM999", 1)

    @pytest.mark.parametrize("invalid_qty", [0, -1, -10, "5", None])
    def test_stock_check_invalid_quantity_raises_error(self, inventory_manager, invalid_qty):
        """Tests non-positive or non-integer requested quantity rejection."""
        with pytest.raises(ValueError, match="Requested quantity must be a positive integer"):
            inventory_manager.check_stock_availability("ITEM001", invalid_qty)

    def test_deduct_stock_success(self, inventory_manager):
        """Tests stock deduction updates inventory correctly."""
        remaining = inventory_manager.deduct_stock("ITEM003", 5)
        assert remaining == 25
        assert inventory_manager.inventory["ITEM003"]["stock"] == 25


# ============================================================================
# 2. Tests for calculate_tier_discount (BVA & ECP)
# ============================================================================
@pytest.mark.module3_inv
@pytest.mark.regression
@pytest.mark.order(11)
class TestTierDiscount:

    @pytest.mark.parametrize("amount, expected_discount", [
        (0.0, 0.0),             # Boundary: Zero
        (99.99, 0.0),           # BVA: Just below Tier 1 ($100.00) -> 0%
        (100.0, 10.0),          # BVA: Exact Tier 1 boundary ($100.00) -> 10%
        (250.0, 25.0),          # ECP: Nominal Tier 1 amount -> 10%
        (499.99, 50.0),         # BVA: Just below Tier 2 ($500.00) -> 10% ($49.999 -> rounded 50.0)
        (500.0, 75.0),          # BVA: Exact Tier 2 boundary ($500.00) -> 15%
        (750.0, 112.5),         # ECP: Nominal Tier 2 amount -> 15%
        (999.99, 150.0),        # BVA: Just below Tier 3 ($1000.00) -> 15% ($149.9985 -> rounded 150.0)
        (1000.0, 200.0),        # BVA: Exact Tier 3 boundary ($1000.00) -> 20%
        (2000.0, 400.0)         # ECP: Above Tier 3 boundary -> 20%
    ])
    def test_tier_discount_boundaries(self, inventory_manager, amount, expected_discount):
        """Tests volume tier discount boundaries."""
        disc = inventory_manager.calculate_tier_discount(amount)
        assert disc == pytest.approx(expected_discount, abs=0.01)

    def test_negative_amount_tier_discount_raises_error(self, inventory_manager):
        """Tests negative amount rejection."""
        with pytest.raises(ValueError, match="Total amount cannot be negative"):
            inventory_manager.calculate_tier_discount(-10.0)


# ============================================================================
# 3. Tests for apply_coupon & calculate_tax (ECP)
# ============================================================================
@pytest.mark.module3_inv
@pytest.mark.regression
@pytest.mark.order(12)
class TestCouponAndTaxCalculation:

    @pytest.mark.parametrize("subtotal, coupon_code, expected_coupon_disc", [
        (100.0, "SAVE10", 10.0),
        (100.0, "save10", 10.0),      # Case-insensitive
        (200.0, "SAVE20", 40.0),
        (500.0, "VIP50", 250.0),
        (100.0, None, 0.0),           # None coupon
        (100.0, "", 0.0)              # Empty string coupon
    ])
    def test_valid_coupons_ecp(self, inventory_manager, subtotal, coupon_code, expected_coupon_disc):
        """Tests valid promo coupons."""
        disc = inventory_manager.apply_coupon(subtotal, coupon_code)
        assert disc == expected_coupon_disc

    def test_invalid_coupon_raises_error(self, inventory_manager):
        """Tests rejection of invalid coupon code."""
        with pytest.raises(ValueError, match="Invalid coupon code"):
            inventory_manager.apply_coupon(100.0, "FAKEDISCOUNT99")

    @pytest.mark.parametrize("amount, state_code, expected_tax", [
        (100.0, "NY", 8.88),        # 8.875% rounded to 8.88
        (100.0, "CA", 7.25),        # 7.25%
        (100.0, "TX", 6.25),        # 6.25%
        (100.0, "FL", 6.00),        # 6.0%
        (100.0, "EXEMPT", 0.0),     # Tax exempt
        (0.0, "NY", 0.0)            # Boundary: Zero
    ])
    def test_state_sales_tax_ecp(self, inventory_manager, amount, state_code, expected_tax):
        """Tests tax calculations across state jurisdictions."""
        tax = inventory_manager.calculate_tax(amount, state_code)
        assert tax == expected_tax

    def test_unsupported_state_tax_raises_error(self, inventory_manager):
        """Tests unsupported state code rejection."""
        with pytest.raises(ValueError, match="Unsupported or invalid state code"):
            inventory_manager.calculate_tax(100.0, "ZZ")
