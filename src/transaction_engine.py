"""
Module 2: Transaction and Payment Processing Engine
Part of PyCommerce Open-Source Engine
"""
from typing import Dict


class TransactionProcessor:
    def __init__(self):
        self.accounts: Dict[str, float] = {}
        self.daily_withdrawals: Dict[str, float] = {}
        self.daily_limit = 5000.0
        self.minimum_balance = 50.0

    def create_account(self, account_id: str, initial_deposit: float = 100.0) -> float:
        """
        Creates account with initial deposit. Minimum initial deposit is $50.0.
        """
        if account_id in self.accounts:
            raise ValueError(f"Account {account_id} already exists.")
        if initial_deposit < self.minimum_balance:
            raise ValueError(f"Initial deposit must be at least ${self.minimum_balance:.2f}.")

        self.accounts[account_id] = round(initial_deposit, 2)
        self.daily_withdrawals[account_id] = 0.0
        return self.accounts[account_id]

    def process_deposit(self, account_id: str, amount: float) -> float:
        """
        Deposits funds into account.
        Boundaries:
        - Minimum deposit: $10.00
        - Maximum deposit per transaction: $10,000.00
        """
        if account_id not in self.accounts:
            raise KeyError(f"Account {account_id} not found.")
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be a number.")
        if amount < 10.0:
            raise ValueError("Minimum deposit allowed is $10.00.")
        if amount > 10000.0:
            raise ValueError("Maximum deposit per transaction is $10,000.00.")

        self.accounts[account_id] += round(amount, 2)
        return self.accounts[account_id]

    def process_withdrawal(self, account_id: str, amount: float) -> float:
        """
        Withdraws funds from account.
        Boundaries:
        - Minimum withdrawal: $5.00
        - Must leave at least minimum balance ($50.00)
        - Cannot exceed daily withdrawal limit ($5,000.00)
        """
        if account_id not in self.accounts:
            raise KeyError(f"Account {account_id} not found.")
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdrawal amount must be a number.")
        if amount < 5.0:
            raise ValueError("Minimum withdrawal is $5.00.")
        if (self.daily_withdrawals[account_id] + amount) > self.daily_limit:
            raise ValueError(f"Withdrawal exceeds daily limit of ${self.daily_limit:.2f}.")
        if (self.accounts[account_id] - amount) < self.minimum_balance:
            raise ValueError(f"Insufficient funds. Must maintain minimum balance of ${self.minimum_balance:.2f}.")

        self.accounts[account_id] -= round(amount, 2)
        self.daily_withdrawals[account_id] += round(amount, 2)
        return self.accounts[account_id]

    def calculate_transfer_fee(self, amount: float, tier: str = "standard") -> float:
        """
        Calculates fee based on customer tier:
        - standard: 2% (min $1.00, max $100.00)
        - silver: 1% (min $0.50, max $50.00)
        - gold: 0.5% (no minimum, max $25.00)
        - platinum: 0% fee ($0.00)
        """
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")

        tier = tier.lower()
        if tier == "standard":
            fee = amount * 0.02
            return round(max(1.0, min(fee, 100.0)), 2)
        elif tier == "silver":
            fee = amount * 0.01
            return round(max(0.5, min(fee, 50.0)), 2)
        elif tier == "gold":
            fee = amount * 0.005
            return round(min(fee, 25.0), 2)
        elif tier == "platinum":
            return 0.0
        else:
            raise ValueError(f"Unknown tier: {tier}")

    def convert_currency(self, amount: float, from_curr: str, to_curr: str) -> float:
        """
        Converts currency using fixed conversion rates against USD:
        USD: 1.0, EUR: 0.92, GBP: 0.79, JPY: 155.0
        """
        rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 155.0}
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()

        if from_curr not in rates or to_curr not in rates:
            raise ValueError(f"Unsupported currency conversion: {from_curr} to {to_curr}")
        if amount < 0:
            raise ValueError("Amount cannot be negative.")

        amount_in_usd = amount / rates[from_curr]
        converted = amount_in_usd * rates[to_curr]
        return round(converted, 2)
