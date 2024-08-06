import pytest
import json
from unittest.mock import Mock, patch
from threading import Thread
import time
from shopping_cart.cart import Cart
from shopping_cart.payments import PaymentProcessor, PaymentMethod, process_payments, make_payments, add_payment_to_cart, run_multiple_payments

# Load test data from JSON file
with open('test_data_payments.json') as f:
    test_data = json.load(f)

@pytest.fixture
def setup_cart():
    cart = Cart(user_type="regular")
    return cart

@pytest.mark.parametrize("test_case", test_data["test_data_process_payments"])
def test_process_payments(setup_cart, test_case):
    cart = setup_cart
    payment_methods = [PaymentMethod(name=method["name"], processing_time=method["processing_time"]) for method in test_case["payment_methods"]]

    with patch('time.sleep') as mock_sleep:
        process_payments(cart, payment_methods)

        # Assert that each payment method was processed
        for method in test_case["payment_methods"]:
            assert cart.payment_status == f"{method['name']} Payment Processed"

        # Assert that sleep was called for each payment method
        assert mock_sleep.call_count == len(test_case["payment_methods"])

@pytest.mark.parametrize("test_case", test_data["test_data_make_payments"])
def test_make_payments(setup_cart, test_case):
    cart = setup_cart
    payment_methods = [PaymentMethod(name=method["name"], processing_time=method["processing_time"]) for method in test_case["payment_methods"]]

    with patch('time.sleep') as mock_sleep:
        make_payments(cart, payment_methods)

        # Assert that each payment method was processed
        for method in test_case["payment_methods"]:
            assert cart.payment_status == f"{method['name']} Payment Processed"

        # Assert that sleep was called for each payment method
        assert mock_sleep.call_count == len(test_case["payment_methods"])

@pytest.mark.parametrize("test_case", test_data["test_data_add_payment_to_cart"])
def test_add_payment_to_cart(setup_cart, test_case):
    cart = setup_cart
    payment_method = PaymentMethod(name=test_case["payment_method"]["name"], processing_time=test_case["payment_method"]["processing_time"])

    with patch('time.sleep') as mock_sleep:
        add_payment_to_cart(cart, payment_method)

        # Assert that the payment method was processed
        assert cart.payment_status == f"{test_case['payment_method']['name']} Payment Processed"

        # Assert that sleep was called
        assert mock_sleep.call_count == 1

@pytest.mark.parametrize("test_case", test_data["test_data_run_multiple_payments"])
def test_run_multiple_payments(setup_cart, test_case):
    cart = setup_cart
    with patch('time.sleep') as mock_sleep:
        run_multiple_payments(cart)

        # Assert that each payment method was processed
        assert cart.payment_status == f"Method 4 Payment Processed"

        # Assert that sleep was called for each payment method
        assert mock_sleep.call_count == 10

if __name__ == "__main__":
    pytest.main()