"""
Test Suite for Module 1: Authentication & User Account Service
Tester / Author: Mohsin Shah (Group Member 1)
Covers Task 2 (ECP & BVA) & Task 4 (Parameterization, Markers, Execution Ordering)
"""
import pytest
from src.auth_manager import UserManager


@pytest.fixture
def user_manager():
    """Provides a fresh UserManager instance for each test."""
    return UserManager()


# ============================================================================
# 1. Tests for validate_username (ECP & BVA)
# ============================================================================
@pytest.mark.module1_auth
@pytest.mark.smoke
@pytest.mark.order(1)
class TestUsernameValidation:

    @pytest.mark.parametrize("valid_username", [
        "abc",                  # BVA: Min boundary (length 3)
        "abcd",                 # BVA: Just above min (length 4)
        "valid_user_name_19",   # BVA: Just below max (length 19)
        "a" * 20,               # BVA: Max boundary (length 20)
        "john_doe",             # ECP: Standard alphanumeric with underscore
        "user12345"             # ECP: Alphanumeric
    ])
    def test_valid_username_ecp_bva(self, user_manager, valid_username):
        """Tests valid username boundaries (3 <= length <= 20)."""
        assert user_manager.validate_username(valid_username) is True

    @pytest.mark.parametrize("invalid_username, reason", [
        ("ab", "BVA: Below minimum length 3"),
        ("", "ECP: Empty string"),
        ("a" * 21, "BVA: Above maximum length 20"),
        ("john doe", "ECP: Contains space"),
        ("user@name", "ECP: Contains illegal special character @"),
        ("user#123", "ECP: Contains illegal special character #"),
        (None, "ECP: Non-string type None"),
        (12345, "ECP: Non-string integer")
    ])
    def test_invalid_username_ecp_bva(self, user_manager, invalid_username, reason):
        """Tests invalid username equivalence classes and boundary limits."""
        assert user_manager.validate_username(invalid_username) is False, f"Failed on {reason}"


# ============================================================================
# 2. Tests for validate_password (ECP & BVA)
# ============================================================================
@pytest.mark.module1_auth
@pytest.mark.regression
@pytest.mark.order(2)
class TestPasswordValidation:

    @pytest.mark.parametrize("valid_password", [
        "Pass1!ab",             # BVA: Exact min length 8 with all character sets
        "Pass1!abc",            # BVA: Just above min (length 9)
        "A1!" + "a" * 28,       # BVA: Just below max (length 31)
        "A1!" + "a" * 29,       # BVA: Exact max length 32
        "StrongP@ssw0rd!"       # ECP: Typical secure password
    ])
    def test_valid_password_ecp_bva(self, user_manager, valid_password):
        """Tests valid password boundaries (8 <= length <= 32 and all character classes)."""
        assert user_manager.validate_password(valid_password) is True

    @pytest.mark.parametrize("invalid_password, reason", [
        ("Pass1!a", "BVA: Length 7 (Just below min 8)"),
        ("A1!" + "a" * 30, "BVA: Length 33 (Just above max 32)"),
        ("securepassword1!", "ECP: Missing uppercase letter"),
        ("SECUREPASSWORD1!", "ECP: Missing lowercase letter check or symbol requirements"),
        ("SecurePassword!", "ECP: Missing numeric digit"),
        ("SecurePassword123", "ECP: Missing special symbol"),
        ("", "ECP: Empty string"),
        (None, "ECP: Non-string type")
    ])
    def test_invalid_password_ecp_bva(self, user_manager, invalid_password, reason):
        """Tests password equivalence classes lacking required constraints."""
        assert user_manager.validate_password(invalid_password) is False, f"Failed on {reason}"


# ============================================================================
# 3. Tests for validate_age (ECP & BVA)
# ============================================================================
@pytest.mark.module1_auth
@pytest.mark.smoke
@pytest.mark.order(3)
class TestAgeValidation:

    @pytest.mark.parametrize("valid_age", [
        18,     # BVA: Exact minimum boundary
        19,     # BVA: Just above min boundary
        50,     # ECP: Typical adult age
        99,     # BVA: Just below max boundary
        100     # BVA: Exact maximum boundary
    ])
    def test_valid_age_boundaries(self, user_manager, valid_age):
        """Tests boundary values for age eligibility (18 <= age <= 100)."""
        assert user_manager.validate_age(valid_age) is True

    @pytest.mark.parametrize("invalid_age, reason", [
        (17, "BVA: Just below minimum age 18"),
        (0, "ECP: Boundary at zero"),
        (-5, "ECP: Negative age"),
        (101, "BVA: Just above maximum age 100"),
        (150, "ECP: Unrealistic upper age"),
        ("18", "ECP: String format of number"),
        (True, "ECP: Boolean value"),
        (25.5, "ECP: Float value")
    ])
    def test_invalid_age_ecp_bva(self, user_manager, invalid_age, reason):
        """Tests invalid age equivalence partitions and boundaries."""
        assert user_manager.validate_age(invalid_age) is False, f"Failed on {reason}"


# ============================================================================
# 4. Tests for validate_email (ECP)
# ============================================================================
@pytest.mark.module1_auth
@pytest.mark.regression
@pytest.mark.order(4)
class TestEmailValidation:

    @pytest.mark.parametrize("valid_email", [
        "user@example.com",
        "first.last@company.co.uk",
        "student_123@university.edu",
        "mohsin.shah+testing@gmail.com"
    ])
    def test_valid_email_formats(self, user_manager, valid_email):
        """Tests valid standard email partitions."""
        assert user_manager.validate_email(valid_email) is True

    @pytest.mark.parametrize("invalid_email", [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@domain",
        "user@domain..com",
        "",
        None
    ])
    def test_invalid_email_formats(self, user_manager, invalid_email):
        """Tests invalid email equivalence partitions."""
        assert user_manager.validate_email(invalid_email) is False


# ============================================================================
# 5. Tests for register_user & authenticate with Lockout (ECP & BVA)
# ============================================================================
@pytest.mark.module1_auth
@pytest.mark.regression
@pytest.mark.order(5)
class TestUserRegistrationAndAuthentication:

    def test_successful_registration(self, user_manager):
        """Tests happy path user registration."""
        res = user_manager.register_user("mohsin_s", "mohsin@example.com", "SecureP@ss1", 25)
        assert res["status"] == "SUCCESS"
        assert res["username"] == "mohsin_s"
        assert "mohsin_s" in user_manager.users

    def test_duplicate_username_registration_raises_error(self, user_manager):
        """Tests duplicate username error handling."""
        user_manager.register_user("duplicate_user", "dup1@example.com", "SecureP@ss1", 30)
        with pytest.raises(ValueError, match="Username already exists"):
            user_manager.register_user("duplicate_user", "dup2@example.com", "SecureP@ss1", 28)

    def test_registration_with_invalid_credentials_raises_error(self, user_manager):
        """Tests that registration enforces validation policies."""
        with pytest.raises(ValueError):
            user_manager.register_user("ab", "invalid_username@test.com", "SecureP@ss1", 25)

        with pytest.raises(ValueError):
            user_manager.register_user("valid_user", "notanemail", "SecureP@ss1", 25)

        with pytest.raises(ValueError):
            user_manager.register_user("valid_user", "valid@test.com", "weak", 25)

        with pytest.raises(ValueError):
            user_manager.register_user("valid_user", "valid@test.com", "SecureP@ss1", 17)

    def test_successful_authentication(self, user_manager):
        """Tests authentication with valid credentials."""
        user_manager.register_user("alice_w", "alice@test.com", "ValidP@ss1", 22)
        assert user_manager.authenticate("alice_w", "ValidP@ss1") is True

    def test_authentication_nonexistent_user(self, user_manager):
        """Tests authentication returns False for unknown user."""
        assert user_manager.authenticate("ghost_user", "ValidP@ss1") is False

    def test_account_lockout_boundary_after_three_failed_attempts(self, user_manager):
        """
        BVA on failed attempts counter:
        Attempt 1: Fail (Active)
        Attempt 2: Fail (Active)
        Attempt 3: Fail (Locked)
        Attempt 4: PermissionError (Account is locked)
        """
        user_manager.register_user("target_user", "target@test.com", "CorrectP@ss1", 35)

        # Attempt 1 (Boundary: 1 failed attempt)
        assert user_manager.authenticate("target_user", "WrongPass1!") is False
        assert user_manager.failed_attempts["target_user"] == 1
        assert "target_user" not in user_manager.locked_accounts

        # Attempt 2 (Boundary: 2 failed attempts)
        assert user_manager.authenticate("target_user", "WrongPass2!") is False
        assert user_manager.failed_attempts["target_user"] == 2
        assert "target_user" not in user_manager.locked_accounts

        # Attempt 3 (Boundary: 3 failed attempts triggers lock)
        assert user_manager.authenticate("target_user", "WrongPass3!") is False
        assert "target_user" in user_manager.locked_accounts

        # Attempt 4 (Subsequent attempt on locked account raises PermissionError)
        with pytest.raises(PermissionError, match="Account is locked"):
            user_manager.authenticate("target_user", "CorrectP@ss1")

    def test_successful_login_resets_failed_attempts_counter(self, user_manager):
        """Tests that successful login clears previous failed attempts counter."""
        user_manager.register_user("reset_user", "reset@test.com", "CorrectP@ss1", 40)
        user_manager.authenticate("reset_user", "WrongPass1!")
        assert user_manager.failed_attempts["reset_user"] == 1

        # Correct password resets counter to 0
        assert user_manager.authenticate("reset_user", "CorrectP@ss1") is True
        assert user_manager.failed_attempts["reset_user"] == 0
