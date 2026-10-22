"""
Test Suite for Module 2: Transaction and Payment Processing Engine
Tester / Author: Group Partner (Group Member 2)
Covers Task 2 (ECP & BVA) & Task 4 (Parameterization, Markers, Execution Ordering)
"""
import re
import pytest
from src.transaction_engine import TransactionProcessor


@pytest.fixture
def transaction_processor():
    """Provides a fresh TransactionProcessor instance."""
    processor = TransactionProcessor()
    processor.create_account("ACC_001", initial_deposit=500.0)
    return processor


# ============================================================================
# 1. Tests for process_deposit (BVA & ECP)
# ============================================================================
@pytest.mark.module2_trans
@pytest.mark.smoke
@pytest.mark.order(6)
class TestProcessDeposit:

    @pytest.mark.parametrize("deposit_amount, expected_new_balance", [
        (10.0, 510.0),          # BVA: Exact minimum deposit ($10.00)
        (10.01, 510.01),        # BVA: Just above minimum ($10.01)
        (500.0, 1000.0),        # ECP: Nominal deposit
        (9999.99, 10499.99),    # BVA: Just below maximum deposit ($9,999.99)
        (10000.0, 10500.0)      # BVA: Exact maximum deposit ($10,000.00)
    ])
    def test_valid_deposit_boundaries(self, transaction_processor, deposit_amount, expected_new_balance):
        """Tests valid deposit equivalence classes and boundary values ($10.00 <= amount <= $10,000.00)."""
        new_balance = transaction_processor.process_deposit("ACC_001", deposit_amount)
        assert new_balance == expected_new_balance
        assert transaction_processor.accounts["ACC_001"] == expected_new_balance

    @pytest.mark.parametrize("invalid_deposit, expected_error_msg", [
        (9.99, "Minimum deposit allowed is $10.00"),            # BVA: Just below minimum
        (0.0, "Minimum deposit allowed is $10.00"),             # Boundary: Zero
        (-50.0, "Minimum deposit allowed is $10.00"),           # ECP: Negative deposit
        (10000.01, "Maximum deposit per transaction is $10,000.00"), # BVA: Just above maximum
        (50000.0, "Maximum deposit per transaction is $10,000.00")   # ECP: Exceeds maximum limit
    ])
    def test_invalid_deposit_boundaries(self, transaction_processor, invalid_deposit, expected_error_msg):
        """Tests invalid deposit boundaries and partitions."""
        with pytest.raises(ValueError, match=re.escape(expected_error_msg)):
            transaction_processor.process_deposit("ACC_001", invalid_deposit)

    def test_deposit_nonexistent_account_raises_key_error(self, transaction_processor):
        """Tests deposit into unknown account."""
        with pytest.raises(KeyError, match=re.escape("Account GHOST not found")):
            transaction_processor.process_deposit("GHOST", 100.0)

    def test_deposit_invalid_type_raises_type_error(self, transaction_processor):
        """Tests invalid data type rejection."""
        with pytest.raises(TypeError, match=re.escape("Deposit amount must be a number")):
            transaction_processor.process_deposit("ACC_001", "one_hundred")


# ============================================================================
# 2. Tests for process_withdrawal (BVA & ECP)
# ============================================================================
@pytest.mark.module2_trans
@pytest.mark.regression
@pytest.mark.order(7)
class TestProcessWithdrawal:

    @pytest.mark.parametrize("withdrawal_amount, expected_remaining_balance", [
        (5.0, 495.0),           # BVA: Exact minimum withdrawal ($5.00)
        (5.01, 494.99),         # BVA: Just above minimum withdrawal
        (200.0, 300.0),         # ECP: Nominal withdrawal
        (450.0, 50.0)           # BVA: Withdraws to exact minimum required balance ($50.00)
    ])
    def test_valid_withdrawal_boundaries(self, transaction_processor, withdrawal_amount, expected_remaining_balance):
        """Tests valid withdrawal boundary cases."""
        new_balance = transaction_processor.process_withdrawal("ACC_001", withdrawal_amount)
        assert new_balance == expected_remaining_balance

    @pytest.mark.parametrize("invalid_amount, expected_err", [
        (4.99, "Minimum withdrawal is $5.00"),                  # BVA: Just below minimum
        (0.0, "Minimum withdrawal is $5.00"),                   # Boundary: Zero
        (-10.0, "Minimum withdrawal is $5.00")                  # ECP: Negative amount
    ])
    def test_withdrawal_below_minimum_boundary(self, transaction_processor, invalid_amount, expected_err):
        """Tests rejection of withdrawals below minimum limit."""
        with pytest.raises(ValueError, match=re.escape(expected_err)):
            transaction_processor.process_withdrawal("ACC_001", invalid_amount)

    def test_withdrawal_violating_minimum_balance_fails(self, transaction_processor):
        """
        BVA: Balance = $500, Min required balance = $50.
        Withdrawing $450.01 leaves $49.99 (< $50) -> raises ValueError.
        """
        with pytest.raises(ValueError, match=re.escape("Insufficient funds. Must maintain minimum balance of $50.00")):
            transaction_processor.process_withdrawal("ACC_001", 450.01)

    def test_daily_withdrawal_limit_boundary(self, transaction_processor):
        """
        Tests cumulative daily withdrawal limit ($5,000.00).
        """
        transaction_processor.create_account("ACC_BIG", initial_deposit=10000.0)
        # Withdraw exactly daily limit $5,000.00
        res = transaction_processor.process_withdrawal("ACC_BIG", 5000.0)
        assert res == 5000.0

        # Attempt to withdraw an additional $5.00 exceeds daily limit
        with pytest.raises(ValueError, match="Withdrawal exceeds daily limit"):
            transaction_processor.process_withdrawal("ACC_BIG", 5.0)


# ============================================================================
# 3. Tests for calculate_transfer_fee (ECP & BVA)
# ============================================================================
@pytest.mark.module2_trans
@pytest.mark.regression
@pytest.mark.order(8)
class TestCalculateTransferFee:

    @pytest.mark.parametrize("amount, tier, expected_fee", [
        (10.0, "standard", 1.00),       # BVA: 2% of $10 is $0.20 -> Clamped to min fee $1.00
        (50.0, "standard", 1.00),       # BVA: 2% of $50 is $1.00 -> Exact min boundary
        (1000.0, "standard", 20.00),    # ECP: Nominal 2% fee ($20.00)
        (5000.0, "standard", 100.00),   # BVA: 2% of $5,000 is $100.00 -> Exact max boundary
        (10000.0, "standard", 100.00),  # BVA: 2% of $10,000 is $200.00 -> Clamped to max fee $100.00
        (25.0, "silver", 0.50),         # BVA: Silver min fee clamp ($0.50)
        (2000.0, "silver", 20.00),      # ECP: Silver nominal 1% fee
        (6000.0, "silver", 50.00),      # BVA: Silver max fee clamp ($50.00)
        (2000.0, "gold", 10.00),        # ECP: Gold 0.5% fee
        (8000.0, "gold", 25.00),        # BVA: Gold max fee clamp ($25.00)
        (5000.0, "platinum", 0.0)       # ECP: Platinum tier has $0.00 fee
    ])
    def test_fee_calculation_across_tiers(self, transaction_processor, amount, tier, expected_fee):
        """Tests transfer fee calculations across customer loyalty tiers."""
        fee = transaction_processor.calculate_transfer_fee(amount, tier)
        assert fee == expected_fee

    def test_invalid_tier_raises_error(self, transaction_processor):
        """Tests unknown tier error handling."""
        with pytest.raises(ValueError, match="Unknown tier: diamond"):
            transaction_processor.calculate_transfer_fee(100.0, "diamond")

    def test_non_positive_amount_fee_raises_error(self, transaction_processor):
        """Tests zero/negative transfer amounts."""
        with pytest.raises(ValueError, match="Transfer amount must be positive"):
            transaction_processor.calculate_transfer_fee(0.0, "standard")


# ============================================================================
# 4. Tests for convert_currency (ECP)
# ============================================================================
@pytest.mark.module2_trans
@pytest.mark.smoke
@pytest.mark.order(9)
class TestConvertCurrency:

    @pytest.mark.parametrize("amount, from_curr, to_curr, expected_result", [
        (100.0, "USD", "EUR", 92.0),
        (100.0, "USD", "GBP", 79.0),
        (10.0, "USD", "JPY", 1550.0),
        (92.0, "EUR", "USD", 100.0),
        (50.0, "USD", "USD", 50.0)
    ])
    def test_supported_currency_conversions(self, transaction_processor, amount, from_curr, to_curr, expected_result):
        """Tests conversion between supported foreign currencies."""
        res = transaction_processor.convert_currency(amount, from_curr, to_curr)
        assert res == expected_result

    def test_unsupported_currency_raises_error(self, transaction_processor):
        """Tests unsupported currency rejection."""
        with pytest.raises(ValueError, match="Unsupported currency conversion"):
            transaction_processor.convert_currency(100.0, "USD", "XYZ")
