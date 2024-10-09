import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import (
    PaymentProcessor,
    PaymentMethod,
    Promotion,
    process_payments,
    make_payments,
    add_payment_to_cart,
    run_multiple_payments,
    apply_promotions
)

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 100}, {'name': 'item2', 'price': 200}]
    cart.payment_status = ''
    return cart

@pytest.fixture
def mock_payment_methods():
    payment_methods = [
        PaymentMethod(name='Credit Card', processing_time=0.1),
        PaymentMethod(name='PayPal', processing_time=0.2)
    ]
    return payment_methods

@pytest.fixture
def mock_promotions():
    promotions = [
        Promotion(name='Spring Sale', discount_rate=0.1),
        Promotion(name='Black Friday', discount_rate=0.2)
    ]
    return promotions

@pytest.fixture
def mock_payment_processor():
    with patch('shopping_cart.payments.PaymentProcessor.__init__', return_value=None) as mock_init:
        with patch('shopping_cart.payments.PaymentProcessor.run', return_value=None) as mock_run:
            yield mock_init, mock_run

@pytest.fixture
def mock_payment_method_process_payment():
    with patch('shopping_cart.payments.PaymentMethod.process_payment', return_value=None) as mock_process:
        yield mock_process

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep', return_value=None) as mock_sleep:
        yield mock_sleep

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions', return_value=None) as mock_apply:
        yield mock_apply

# happy path - process_payments - Test that process_payments starts and joins threads for each payment method
def test_process_payments_starts_and_joins_threads(mock_cart, mock_payment_methods, mock_payment_processor, mock_time_sleep):
    process_payments(mock_cart, mock_payment_methods)
    assert mock_cart.payment_status == 'PayPal Payment Processed'


# happy path - make_payments - Test that make_payments processes payments correctly
def test_make_payments_processes_correctly(mock_cart, mock_payment_methods, mock_payment_processor, mock_time_sleep):
    make_payments(mock_cart, [mock_payment_methods[0]])
    assert mock_cart.payment_status == 'Credit Card Payment Processed'


# happy path - add_payment_to_cart - Test that add_payment_to_cart processes a single payment
def test_add_payment_to_cart_single_payment(mock_cart, mock_payment_methods, mock_payment_processor, mock_time_sleep):
    add_payment_to_cart(mock_cart, mock_payment_methods[0])
    assert mock_cart.payment_status == 'Credit Card Payment Processed'


# happy path - run_multiple_payments - Test that run_multiple_payments processes multiple payments
def test_run_multiple_payments(mock_cart, mock_payment_processor, mock_time_sleep):
    run_multiple_payments(mock_cart)
    assert mock_cart.payment_status == 'Method 4 Payment Processed'


# happy path - apply_promotions - Test that apply_promotions applies Spring Sale correctly
def test_apply_promotions_spring_sale(mock_cart, mock_promotions):
    apply_promotions(mock_cart, [mock_promotions[0]])
    assert mock_cart.items[0]['price'] == 90
    assert mock_cart.items[1]['price'] == 180


# edge case - process_payments - Test that process_payments handles an empty payment_methods list
def test_process_payments_empty_methods(mock_cart, mock_time_sleep):
    process_payments(mock_cart, [])
    assert mock_cart.payment_status == ''


# edge case - make_payments - Test that make_payments handles an empty cart
def test_make_payments_empty_cart(mock_cart, mock_payment_methods, mock_payment_processor, mock_time_sleep):
    mock_cart.items = []
    make_payments(mock_cart, [mock_payment_methods[0]])
    assert mock_cart.payment_status == 'Credit Card Payment Processed'


# edge case - add_payment_to_cart - Test that add_payment_to_cart handles a payment method with zero processing time
def test_add_payment_to_cart_zero_processing_time(mock_cart, mock_payment_processor, mock_time_sleep):
    payment_method = PaymentMethod(name='Instant Pay', processing_time=0)
    add_payment_to_cart(mock_cart, payment_method)
    assert mock_cart.payment_status == 'Instant Pay Payment Processed'


# edge case - run_multiple_payments - Test that run_multiple_payments handles a cart with no items
def test_run_multiple_payments_no_items(mock_cart, mock_payment_processor, mock_time_sleep):
    mock_cart.items = []
    run_multiple_payments(mock_cart)
    assert mock_cart.payment_status == 'Method 4 Payment Processed'


# edge case - apply_promotions - Test that apply_promotions handles promotions with zero discount rate
def test_apply_promotions_zero_discount(mock_cart, mock_promotions):
    apply_promotions(mock_cart, [{'name': 'No Discount', 'discount_rate': 0}])
    assert mock_cart.items[0]['price'] == 100


