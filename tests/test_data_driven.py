"""
Task 3 & 4: External Data-Driven Test Automation
Tester / Author: Group Partner (Group Member 2)
Consumes external test data from 'data/test_data.csv' to validate checkout invoices.
"""
import csv
import os
import pytest
from src.inventory_service import OrderInventoryManager


def load_test_data_from_csv():
    """Utility function to parse external CSV test records for data-driven testing."""
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.csv")
    test_cases = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            coupon = None if row["coupon_code"].strip().upper() == "NONE" else row["coupon_code"].strip()
            test_cases.append((
                row["item_id"],
                int(row["quantity"]),
                row["state_code"],
                coupon,
                float(row["expected_base_price"]),
                float(row["expected_tier_discount"]),
                float(row["expected_coupon_discount"]),
                float(row["expected_tax"]),
                float(row["expected_grand_total"])
            ))
    return test_cases


@pytest.fixture
def inventory_manager():
    return OrderInventoryManager()


@pytest.mark.data_driven
@pytest.mark.regression
@pytest.mark.order(13)
class TestExternalDataDrivenSuite:

    @pytest.mark.parametrize(
        "item_id, qty, state_code, coupon_code, exp_base, exp_tier_disc, exp_coupon_disc, exp_tax, exp_total",
        load_test_data_from_csv()
    )
    def test_invoice_calculation_from_external_csv(
        self, inventory_manager, item_id, qty, state_code, coupon_code,
        exp_base, exp_tier_disc, exp_coupon_disc, exp_tax, exp_total
    ):
        """
        Executes automated data-driven test cases loaded directly from external CSV resource.
        """
        invoice = inventory_manager.calculate_final_invoice(
            item_id=item_id,
            quantity=qty,
            state_code=state_code,
            coupon_code=coupon_code
        )

        assert invoice["base_price"] == pytest.approx(exp_base, abs=0.01)
        assert invoice["tier_discount"] == pytest.approx(exp_tier_disc, abs=0.01)
        assert invoice["coupon_discount"] == pytest.approx(exp_coupon_disc, abs=0.01)
        assert invoice["tax"] == pytest.approx(exp_tax, abs=0.01)
        assert invoice["grand_total"] == pytest.approx(exp_total, abs=0.01)
