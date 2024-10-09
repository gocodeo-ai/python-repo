import pytest
from unittest import mock
from shopping_cart.payments import (
    process_payments,
    make_payments,
    add_payment_to_cart,
    run_multiple_payments,
    apply_promotions,
    PaymentProcessor,
    PaymentMethod,
    Promotion
)

@pytest.fixture
def mock_cart():
    cart = mock.Mock()
    cart.items = [{'name': 'item1', 'price': 100}, {'name': 'item2', 'price': 200}]
    cart.payment_status = ''
    return cart

@pytest.fixture
def mock_payment_methods():
    return [
        mock.Mock(spec=PaymentMethod, name='Credit Card', processing_time=0.1),
        mock.Mock(spec=PaymentMethod, name='PayPal', processing_time=0.2)
    ]

@pytest.fixture
def mock_promotions():
    return [
        mock.Mock(spec=Promotion, name='Spring Sale', discount_rate=0.1),
        mock.Mock(spec=Promotion, name='Black Friday', discount_rate=0.2)
    ]

@pytest.fixture
def mock_payment_processor():
    with mock.patch('shopping_cart.payments.PaymentProcessor.run') as mock_run:
        yield mock_run

@pytest.fixture
def mock_process_payment():
    with mock.patch('shopping_cart.payments.PaymentMethod.process_payment') as mock_process:
        yield mock_process

@pytest.fixture
def mock_time_sleep():
    with mock.patch('time.sleep') as mock_sleep:
        yield mock_sleep

# happy path - process_payments - Test that process_payments launches threads for each payment method and processes payments
def test_process_payments_multiple_methods(mock_cart, mock_payment_methods, mock_time_sleep, mock_process_payment):
    process_payments(mock_cart, mock_payment_methods)
    assert mock_process_payment.call_count == 2
    assert mock_cart.payment_status == 'PayPal Payment Processed'


# happy path - make_payments - Test that make_payments processes payments using provided payment methods
def test_make_payments(mock_cart, mock_payment_methods, mock_time_sleep, mock_process_payment):
    make_payments(mock_cart, mock_payment_methods)
    assert mock_process_payment.call_count == 2
    assert mock_cart.payment_status == 'Debit Card Payment Processed'


# happy path - add_payment_to_cart - Test that add_payment_to_cart processes a single payment method
def test_add_payment_to_cart_single_method(mock_cart, mock_payment_methods, mock_time_sleep, mock_process_payment):
    add_payment_to_cart(mock_cart, mock_payment_methods[0])
    mock_process_payment.assert_called_once()
    assert mock_cart.payment_status == 'Credit Card Payment Processed'


# happy path - run_multiple_payments - Test that run_multiple_payments processes payments for multiple methods
def test_run_multiple_payments(mock_cart, mock_time_sleep, mock_process_payment):
    run_multiple_payments(mock_cart)
    assert mock_process_payment.call_count == 4
    assert mock_cart.payment_status == 'Method 4 Payment Processed'


# happy path - apply_promotions - Test that apply_promotions applies discounts based on promotions
def test_apply_promotions_spring_sale(mock_cart, mock_promotions):
    apply_promotions(mock_cart, [mock_promotions[0]])
    assert mock_cart.items[0]['price'] == 90
    assert mock_cart.items[1]['price'] == 180


# edge case - process_payments - Test that process_payments handles an empty list of payment methods gracefully
def test_process_payments_empty_methods(mock_cart, mock_time_sleep, mock_process_payment):
    process_payments(mock_cart, [])
    assert mock_process_payment.call_count == 0
    assert mock_cart.payment_status == ''


# edge case - make_payments - Test that make_payments handles empty cart gracefully
def test_make_payments_empty_cart(mock_cart, mock_payment_methods, mock_time_sleep, mock_process_payment):
    mock_cart.items = []
    make_payments(mock_cart, [mock_payment_methods[0]])
    mock_process_payment.assert_called_once()
    assert mock_cart.payment_status == 'Credit Card Payment Processed'


# edge case - add_payment_to_cart - Test that add_payment_to_cart handles null payment method
def test_add_payment_to_cart_null_method(mock_cart, mock_time_sleep, mock_process_payment):
    add_payment_to_cart(mock_cart, None)
    assert mock_process_payment.call_count == 0
    assert mock_cart.payment_status == ''


# edge case - run_multiple_payments - Test that run_multiple_payments handles cart with no items
def test_run_multiple_payments_no_items(mock_cart, mock_time_sleep, mock_process_payment):
    mock_cart.items = []
    run_multiple_payments(mock_cart)
    assert mock_process_payment.call_count == 4
    assert mock_cart.payment_status == 'Method 4 Payment Processed'


# edge case - apply_promotions - Test that apply_promotions handles promotions with zero discount rate
def test_apply_promotions_zero_discount(mock_cart, mock_promotions):
    apply_promotions(mock_cart, [{'name': 'Zero Discount', 'discount_rate': 0.0}])
    assert mock_cart.items[0]['price'] == 100


