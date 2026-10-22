# PyCommerce Core Engine - SQE Unit Test Automation Solution

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Testing Framework: Pytest](https://img.shields.io/badge/testing-pytest-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An open-source modular Python commerce, authentication, and transaction calculation engine. This repository contains the complete implementation and test automation solution for **Software Quality Engineering (SQE) - Assignment 3**.

---

## 📋 Project Architecture & Modules (Task 1 & Task 2)

The application consists of 3 distinct, decoupled business logic modules located in `src/`:

1. **Module 1: Authentication & User Account Service (`src/auth_manager.py`)**
   - Username policy validation (length, regex patterns).
   - Password security complexity validation (BVA: 8–32 characters, uppercase, digit, special character).
   - Email format checking.
   - User age eligibility constraints (BVA: 18–100 years).
   - Account state management and lockout protection after 3 failed attempts.

2. **Module 2: Transaction & Payment Processing Engine (`src/transaction_engine.py`)**
   - Account balance management and minimum balance enforcement ($50.00).
   - Deposit constraints ($10.00 min, $10,000.00 max per transaction).
   - Withdrawal daily limits ($5,000.00) and threshold boundary analysis.
   - Tier-based transfer fee calculations (Standard 2%, Silver 1%, Gold 0.5%, Platinum 0%).
   - Multi-currency conversions (USD, EUR, GBP, JPY).

3. **Module 3: Order, Inventory & Discount Service (`src/inventory_service.py`)**
   - Catalog stock availability verification and dynamic deduction.
   - Progressive volume tier discounts ($100: 10%, $500: 15%, $1000+: 20%).
   - Promo coupon code evaluation and stackable calculations.
   - State-specific sales tax calculation (NY, CA, TX, FL, EXEMPT).
   - End-to-end checkout invoice generation.

---

## 🛠️ Task 1: Local Development Environment Setup

Follow these exact steps to set up the project locally on your machine:

### 1. Prerequisites
- Python 3.10 or higher installed. Check with:
  ```bash
  python --version
  ```

### 2. Clone the Repository
```bash
git clone https://github.com/mohsinshah12309/SQE_Assignment.git
cd SQE_Assignment
```

### 3. Create and Activate Virtual Environment
- **Windows (Command Prompt / PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(If PowerShell execution policy restricts scripts: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

- **Linux / macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Verify Installation
Run pytest to verify the environment:
```bash
pytest
```

---

## 📹 Task 1 Setup Video Demonstration
- **Video File**: Located in `docs/setup_video.mp4` *(or see video walkthrough link below)*
- **Walkthrough Demonstration Covers**:
  1. Cloning the repository.
  2. Setting up the Python virtual environment (`venv`).
  3. Installing all required packages from `requirements.txt`.
  4. Executing the test suite via `pytest`.

---

## 🧪 Running the Tests (Task 4 Configuration)

### Run all tests
```bash
pytest -v
```

### Run tests in parallel (multiprocessing across cores)
```bash
pytest -n auto
```

### Run specific test suites using Markers
- **Smoke Suite**:
  ```bash
  pytest -m smoke
  ```
- **Module 1 (Authentication) Suite**:
  ```bash
  pytest -m module1_auth
  ```
- **Module 2 (Transactions) Suite**:
  ```bash
  pytest -m module2_trans
  ```
- **Module 3 (Inventory & Pricing) Suite**:
  ```bash
  pytest -m module3_inv
  ```
- **Data-Driven Suite (Task 3 CSV Ingestion)**:
  ```bash
  pytest -m data_driven
  ```

---

## 👥 Group Members & Task Distribution
| Member Name | Student ID | Assigned Modules & Deliverables | Git Activity / Commits |
|---|---|---|---|
| Member 1 (Lead) | - | Task 1 (Setup & Video), Task 2 (Module 1 Auth Tests) | Branch `feature/auth-module` |
| Member 2 | - | Task 2 (Module 2 Transaction Tests), Task 3 (Excel & CSV) | Branch `feature/transaction-tests` |
| Member 3 | - | Task 2 (Module 3 Inventory Tests), Task 4 (Pytest Config & Order) | Branch `feature/inventory-tests` |
