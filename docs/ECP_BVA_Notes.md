# Equivalence Class Partitioning (ECP) & Boundary Value Analysis (BVA) Test Design Notes

This document contains the formal specification of test design techniques applied to the 3 application modules of **PyCommerce Core Engine** as required by **Task 2**.

---

## 📌 Task Distribution Summary
- **Module 1 (Auth & User Account Management)**: Assigned to **Mohsin Shah** (Group Member 1)
- **Module 2 (Transaction & Fee Engine)**: Assigned to **Group Partner** (Group Member 2)
- **Module 3 (Order, Inventory & Discount Service)**: Assigned to **Group Partner** (Group Member 2)

---

## Module 1: Authentication & User Account Service (`src/auth_manager.py`)
**Assigned Tester:** Mohsin Shah

### 1. `validate_username(username: str)`
- **Specification:** Length must be between 3 and 20 alphanumeric characters (underscores allowed).
- **Equivalence Class Partitioning (ECP):**
  - **Class 1 (Valid):** Alphanumeric string with length $3 \le L \le 20$ (e.g., `"john_doe"`, `"user123"`).
  - **Class 2 (Invalid - Length too short):** Length $< 3$ (e.g., `"ab"`, `""`).
  - **Class 3 (Invalid - Length too long):** Length $> 20$ (e.g., `"a_very_long_username_exceeding_limit"`).
  - **Class 4 (Invalid - Disallowed characters):** Contains spaces or special characters like `!@#$%` (e.g., `"john doe"`, `"user@name"`).
  - **Class 5 (Invalid - Non-string type):** Integers, None, lists (e.g., `12345`, `None`).
- **Boundary Value Analysis (BVA):**
  - Boundary $L = 3$:
    - $L = 2$ (Just below min): `"ab"` $\rightarrow$ **Invalid (False)**
    - $L = 3$ (Exact min): `"abc"` $\rightarrow$ **Valid (True)**
    - $L = 4$ (Just above min): `"abcd"` $\rightarrow$ **Valid (True)**
  - Boundary $L = 20$:
    - $L = 19$ (Just below max): `"a" * 19` $\rightarrow$ **Valid (True)**
    - $L = 20$ (Exact max): `"a" * 20` $\rightarrow$ **Valid (True)**
    - $L = 21$ (Just above max): `"a" * 21` $\rightarrow$ **Invalid (False)**

---

### 2. `validate_password(password: str)`
- **Specification:** Length 8 to 32 characters; must contain at least 1 digit, 1 uppercase letter, and 1 special symbol (`!@#$%^&*()-_`).
- **Equivalence Class Partitioning (ECP):**
  - **Class 1 (Valid):** Meets all 4 conditions (e.g., `"SecurePass1!"`).
  - **Class 2 (Invalid - Too short):** Length $< 8$ (e.g., `"Pass1!"`).
  - **Class 3 (Invalid - Too long):** Length $> 32$.
  - **Class 4 (Invalid - Missing uppercase):** Only lowercase, digit, symbol (e.g., `"securepass1!"`).
  - **Class 5 (Invalid - Missing digit):** Letters and symbol only (e.g., `"SecurePassword!"`).
  - **Class 6 (Invalid - Missing special character):** Letters and digits only (e.g., `"SecurePass123"`).
- **Boundary Value Analysis (BVA):**
  - Lower Length Boundary:
    - $L = 7$: `"Pass1!a"` $\rightarrow$ **Invalid (False)**
    - $L = 8$: `"Pass1!ab"` $\rightarrow$ **Valid (True)**
    - $L = 9$: `"Pass1!abc"` $\rightarrow$ **Valid (True)**
  - Upper Length Boundary:
    - $L = 31$: Valid pattern of length 31 $\rightarrow$ **Valid (True)**
    - $L = 32$: Valid pattern of length 32 $\rightarrow$ **Valid (True)**
    - $L = 33$: Valid pattern of length 33 $\rightarrow$ **Invalid (False)**

---

### 3. `validate_age(age: int)`
- **Specification:** Integer age between 18 and 100 inclusive.
- **Equivalence Class Partitioning (ECP):**
  - **Class 1 (Valid):** $18 \le \text{age} \le 100$.
  - **Class 2 (Invalid - Underage):** $\text{age} < 18$.
  - **Class 3 (Invalid - Overage):** $\text{age} > 100$.
  - **Class 4 (Invalid - Non-integer):** Negative numbers, floats, strings, booleans (`"18"`, `25.5`, `True`).
- **Boundary Value Analysis (BVA):**
  - Lower Boundary:
    - $\text{age} = 17$: Underage $\rightarrow$ **Invalid (False)**
    - $\text{age} = 18$: Minimum eligible age $\rightarrow$ **Valid (True)**
    - $\text{age} = 19$: Nominal lower age $\rightarrow$ **Valid (True)**
  - Upper Boundary:
    - $\text{age} = 99$: Nominal upper age $\rightarrow$ **Valid (True)**
    - $\text{age} = 100$: Maximum eligible age $\rightarrow$ **Valid (True)**
    - $\text{age} = 101$: Exceeds maximum age $\rightarrow$ **Invalid (False)**

---

### 4. `validate_email(email: str)`
- **Equivalence Classes:**
  - **Class 1 (Valid):** Standard format `username@domain.tld` (e.g., `"test@example.com"`).
  - **Class 2 (Invalid - Missing @):** `"testexample.com"`.
  - **Class 3 (Invalid - Missing domain):** `"test@"`.
  - **Class 4 (Invalid - Missing TLD):** `"test@example"`.
  - **Class 5 (Invalid - Empty or Non-string):** `""`, `None`, `123`.

---

### 5. `authenticate(username, password)` (Account Lockout)
- **Specification:** 3 consecutive failed attempts lock the account.
- **Boundary Analysis on Failed Counter:**
  - Attempt 1 (Wrong password): Counter = 1 $\rightarrow$ Account Active (Returns False).
  - Attempt 2 (Wrong password): Counter = 2 $\rightarrow$ Account Active (Returns False).
  - Attempt 3 (Wrong password): Counter = 3 $\rightarrow$ Account Locked (Returns False).
  - Attempt 4 (Subsequent attempt): Raises `PermissionError` (Account is locked).
  - Correct password before 3 attempts resets counter to 0.

---

## Module 2: Transaction & Fee Engine (`src/transaction_engine.py`)
**Assigned Tester:** Group Partner

### 1. `process_deposit(account_id, amount)`
- **Boundaries:**
  - Min deposit: $\$10.00$
  - Max deposit per transaction: $\$10,000.00$
- **BVA Points:**
  - $\$9.99$: Just below min $\rightarrow$ `ValueError`
  - $\$10.00$: Min valid deposit $\rightarrow$ Success
  - $\$10.01$: Just above min $\rightarrow$ Success
  - $\$9,999.99$: Just below max $\rightarrow$ Success
  - $\$10,000.00$: Max valid deposit $\rightarrow$ Success
  - $\$10,000.01$: Above max limit $\rightarrow$ `ValueError`

### 2. `process_withdrawal(account_id, amount)`
- **Boundaries:**
  - Min withdrawal: $\$5.00$
  - Account Minimum Balance: $\$50.00$ must remain
  - Daily Limit: $\$5,000.00$
- **BVA Points:**
  - Amount = $\$4.99$: Below minimum $\rightarrow$ `ValueError`
  - Amount = $\$5.00$: Minimum withdrawal $\rightarrow$ Success
  - Balance = $\$100$, Withdraw = $\$50$: Remaining = $\$50$ (Exact min balance) $\rightarrow$ Success
  - Balance = $\$100$, Withdraw = $\$50.01$: Remaining = $\$49.99$ (Below min balance) $\rightarrow$ `ValueError`
  - Cumulative withdrawals = $\$5,000.00$ (Daily limit hit) $\rightarrow$ Success
  - Cumulative withdrawals = $\$5,000.01$ $\rightarrow$ `ValueError`

### 3. `calculate_transfer_fee(amount, tier)`
- **Tiers & Boundaries:**
  - **Standard (2%):** Min fee $\$1.00$, Max fee $\$100.00$.
    - Amount = $\$10$ ($0.02 \times 10 = 0.20 \rightarrow$ clamped to min $\$1.00$).
    - Amount = $\$1000$ ($0.02 \times 1000 = \$20.00$).
    - Amount = $\$10,000$ ($0.02 \times 10,000 = \$200 \rightarrow$ clamped to max $\$100.00$).
  - **Silver (1%):** Min fee $\$0.50$, Max fee $\$50.00$.
  - **Gold (0.5%):** Max fee $\$25.00$, no min fee.
  - **Platinum (0%):** Fee is always $\$0.00$.

---

## Module 3: Order, Inventory & Discount Service (`src/inventory_service.py`)
**Assigned Tester:** Group Partner

### 1. `calculate_tier_discount(total_amount)`
- **ECP / BVA Tiers:**
  - Tier 0 ($0\%): $0.00 \le \text{amount} < 100.00$
  - Tier 1 ($10\%): 100.00 \le \text{amount} < 500.00$
  - Tier 2 ($15\%): 500.00 \le \text{amount} < 1000.00$
  - Tier 3 ($20\%): \text{amount} \ge 1000.00$
- **Boundary Points:**
  - $\$99.99 \rightarrow 0\%$ discount ($\$0.00$)
  - $\$100.00 \rightarrow 10\%$ discount ($\$10.00$)
  - $\$499.99 \rightarrow 10\%$ discount ($\$49.99$)
  - $\$500.00 \rightarrow 15\%$ discount ($\$75.00$)
  - $\$999.99 \rightarrow 15\%$ discount ($\$150.00$)
  - $\$1000.00 \rightarrow 20\%$ discount ($\$200.00$)

### 2. `calculate_tax(amount, state_code)`
- **ECP State Classes:**
  - NY: $8.875\%$
  - CA: $7.25\%$
  - TX: $6.25\%$
  - FL: $6.0\%$
  - EXEMPT: $0.0\%$
  - Invalid state (e.g. `"ZZ"`) $\rightarrow$ `ValueError`
