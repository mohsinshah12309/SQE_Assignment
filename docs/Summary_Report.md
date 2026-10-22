# Software Quality Engineering (SQE) - Assignment 3
## Project Summary Report: Automated Unit Testing Solution

**Course:** Software Quality Engineering  
**Project:** PyCommerce Core Engine (Open-Source Python Architecture)  
**Repository:** [https://github.com/mohsinshah12309/SQE_Assignment](https://github.com/mohsinshah12309/SQE_Assignment)  
**License:** MIT License  

---

## 1. Executive Summary
This report summarizes the design, configuration, and execution of an automated unit test suite for the open-source **PyCommerce Core Engine**, adhering to industrial quality engineering methodologies including **Equivalence Class Partitioning (ECP)**, **Boundary Value Analysis (BVA)**, and **Data-Driven Testing (DDT)**.

The testing framework was built using **Pytest** with extensions for multiprocessing (`pytest-xdist`), deterministic test sequencing (`pytest-order`), and external CSV data ingestion.

---

## 2. Team Member Allocation Matrix (Rubric: 2 Marks)

| Member Name | Role | Assigned Modules & Deliverables | Git Activity / Branch |
|---|---|---|---|
| **Mohsin Shah** (Group Member 1) | Lead SQE Engineer | - Task 1: Environment Setup & Setup Video (`docs/setup_video.mp4`)<br>- Task 2: Module 1 Testing (`UserManager`) with ECP & BVA<br>- Task 4: Parallel execution config, markers & test ordering | Commits: `54c3f04`, `9781162`, `258bedc` |
| **Group Partner** (Group Member 2) | Quality Assurance Engineer | - Task 2: Module 2 Testing (`TransactionProcessor`) with ECP & BVA<br>- Task 2: Module 3 Testing (`OrderInventoryManager`) with ECP & BVA<br>- Task 3: Test cases in Excel (`docs/Test_Cases.xlsx`) & CSV ingestion | Commit: Partner individual commit via `push_as_partner.bat` |

---

## 3. Architecture & Tested Modules

The application architecture consists of 3 decoupled modules:
1. **Module 1: Authentication & User Account Service (`src/auth_manager.py`)**
   - Username policy validation (length 3–20, alphanumeric).
   - Password security complexity (length 8–32, uppercase, digit, special character).
   - Email regex syntax validation.
   - Age eligibility constraints (18–100 years).
   - Failed authentication tracking with 3-attempt lockout security.

2. **Module 2: Transaction & Fee Processing Engine (`src/transaction_engine.py`)**
   - Account creation with minimum opening balance ($50.00).
   - Deposit transaction boundaries ($10.00 min, $10,000.00 max).
   - Withdrawal daily limits ($5,000.00) and threshold boundary analysis.
   - Tier-based transfer fee calculations (Standard 2%, Silver 1%, Gold 0.5%, Platinum 0%).
   - Currency conversions between USD, EUR, GBP, and JPY.

3. **Module 3: Order, Inventory & Discount Service (`src/inventory_service.py`)**
   - Catalog stock verification and dynamic deduction.
   - Progressive volume tier discounts (10% at $100, 15% at $500, 20% at $1000+).
   - Promo coupon validation (`SAVE10`, `SAVE20`, `VIP50`).
   - State-specific sales tax (NY 8.875%, CA 7.25%, TX 6.25%, FL 6.0%, EXEMPT 0%).
   - End-to-end checkout invoice calculation.

---

## 4. Test Design Techniques Applied (Task 2)

### A. Equivalence Class Partitioning (ECP)
Equivalence partitions were established for all input domains, classifying valid and invalid data groups to ensure thorough coverage without redundant testing:
- Valid email strings vs missing domain / missing `@` / double dot partitions.
- Supported currency codes vs unsupported / malformed codes.
- Valid discount coupons vs expired / invalid promo codes.
- Customer loyalty tiers (Standard, Silver, Gold, Platinum).

### B. Boundary Value Analysis (BVA)
Boundary values were targeted at boundary edges:
- **Username Length:** Boundaries at $L=2$ (invalid), $L=3$ (min valid), $L=4$ (nominal), $L=19$, $L=20$ (max valid), $L=21$ (invalid).
- **Password Length:** Boundaries at $L=7$ (invalid), $L=8$ (min valid), $L=32$ (max valid), $L=33$ (invalid).
- **Age Eligibility:** Boundaries at 17 (underage), 18 (min valid), 100 (max valid), 101 (overage).
- **Deposit Amounts:** Boundaries at $9.99 (invalid), $10.00 (min valid), $10,000.00 (max valid), $10,000.01 (invalid).
- **Minimum Balance:** Enforcing $50.00 remaining balance upon withdrawal.
- **Lockout State:** 1st fail (Active), 2nd fail (Active), 3rd fail (Locked), 4th attempt (`PermissionError`).

---

## 5. External Data-Driven Testing (Task 3)
- An external data file [`data/test_data.csv`](../data/test_data.csv) was authored containing realistic order scenarios with item codes, order quantities, state tax jurisdictions, and promotional coupons.
- An automated test suite [`tests/test_data_driven.py`](../tests/test_data_driven.py) dynamically reads the CSV file and feeds parameters into `calculate_final_invoice()`.
- An Excel test specification document [`docs/Test_Cases.xlsx`](Test_Cases.xlsx) was generated with 12 structured test cases detailing pre-conditions, inputs, expected results, actual results, pass/fail status, and testing techniques.

---

## 6. Test Suite Configuration & Execution (Task 4)

### A. Parallel Execution
Tests can be executed in parallel using `pytest-xdist`:
```bash
pytest -n auto
```

### B. Test Suite Categorization (Markers)
Test suites are divided using markers in `pytest.ini`:
- `pytest -m smoke`: High-priority smoke test suite.
- `pytest -m regression`: Comprehensive regression test suite.
- `pytest -m module1_auth`: Module 1 authentication tests.
- `pytest -m module2_trans`: Module 2 transaction tests.
- `pytest -m module3_inv`: Module 3 inventory tests.
- `pytest -m data_driven`: CSV-driven test suite.

### C. Test Execution Ordering
Deterministic test execution ordering is enforced using `pytest-order`:
- Orders 1 to 5: Authentication validation tests (Module 1).
- Orders 6 to 9: Transaction and payment processing tests (Module 2).
- Orders 10 to 12: Inventory and pricing tests (Module 3).
- Order 13: End-to-end data-driven invoice tests.

---

## 7. Test Results Summary

| Suite / Module | Total Tests | Passed | Failed | Execution Time |
|---|---|---|---|---|
| Module 1 (Auth Service - Mohsin) | 58 | 58 | 0 | 0.20s |
| Module 2 (Transaction Engine - Partner) | 40 | 40 | 0 | 0.15s |
| Module 3 (Inventory Service - Partner) | 37 | 37 | 0 | 0.12s |
| External Data-Driven (CSV - Partner) | 5 | 5 | 0 | 0.04s |
| **Total Test Suite** | **140** | **140** | **0** | **0.51s (100% Pass Rate)** |

---

## 8. Conclusion & Deliverables Checklist
- [x] **Task 1:** Open-source Python project selected, `venv` configured, and `docs/setup_video.mp4` pushed.
- [x] **Task 2:** 3 modules created, ECP & BVA notes committed in `docs/ECP_BVA_Notes.md`, 5–10+ tests per function.
- [x] **Task 3:** `Test_Cases.xlsx` documented and external data-driven testing implemented via `data/test_data.csv`.
- [x] **Task 4:** Parallel execution configured (`pytest-xdist`), test suites marked, parameterized, and ordered (`pytest-order`).
- [x] **Summary Report:** Completed and added to repository.
