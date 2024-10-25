import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import PaymentProcessor, PaymentMethod, Promotion, process_payments, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions

@pytest.fixture
def mock_cart():
    return MagicMock(items=[{'name': 'item1', 'price': 100}, {'name': 'item2', 'price': 200}], payment_status='')

@pytest.fixture
def mock_payment_method():
    with patch('shopping_cart.payments.PaymentMethod') as MockPaymentMethod:
        yield MockPaymentMethod

@pytest.fixture
def mock_payment_processor():
    with patch('shopping_cart.payments.PaymentProcessor') as MockPaymentProcessor:
        yield MockPaymentProcessor

@pytest.fixture
def mock_process_payment():
    with patch('shopping_cart.payments.PaymentMethod.process_payment') as mock_process_payment:
        yield mock_process_payment

@pytest.fixture
def mock_run():
    with patch('shopping_cart.payments.PaymentProcessor.run') as mock_run:
        yield mock_run

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock_apply_promotions:
        yield mock_apply_promotions

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock_time_sleep:
        yield mock_time_sleep

@pytest.fixture
def mock_promotions():
    return MagicMock(name='Promotion', spec=Promotion)

@pytest.fixture
def mock_process_payments():
    with patch('shopping_cart.payments.process_payments') as mock_process_payments:
        yield mock_process_payments

@pytest.fixture
def mock_make_payments():
    with patch('shopping_cart.payments.make_payments') as mock_make_payments:
        yield mock_make_payments

@pytest.fixture
def mock_add_payment_to_cart():
    with patch('shopping_cart.payments.add_payment_to_cart') as mock_add_payment_to_cart:
        yield mock_add_payment_to_cart

@pytest.fixture
def mock_run_multiple_payments():
    with patch('shopping_cart.payments.run_multiple_payments') as mock_run_multiple_payments:
        yield mock_run_multiple_payments

# happy path - process_payments - Test that process_payments processes payments for each payment method in the list.
def test_process_payments_multiple_methods(mock_cart, mock_payment_method, mock_time_sleep):
    mock_payment_methods = [mock_payment_method.return_value, mock_payment_method.return_value]
    mock_payment_methods[0].name = 'Credit Card'
    mock_payment_methods[1].name = 'PayPal'
    process_payments(mock_cart, mock_payment_methods)
    assert mock_cart.payment_status == 'PayPal Payment Processed'


# happy path - make_payments - Test that make_payments processes payments for each payment method in the list.
def test_make_payments_multiple_methods(mock_cart, mock_payment_method, mock_time_sleep):
    mock_payment_methods = [mock_payment_method.return_value, mock_payment_method.return_value]
    mock_payment_methods[0].name = 'Credit Card'
    mock_payment_methods[1].name = 'PayPal'
    make_payments(mock_cart, mock_payment_methods)
    assert mock_cart.payment_status == 'PayPal Payment Processed'


# happy path - add_payment_to_cart - Test that add_payment_to_cart processes a single payment method.
def test_add_payment_to_cart_single_method(mock_cart, mock_payment_method, mock_time_sleep):
    mock_payment_method.return_value.name = 'Credit Card'
    add_payment_to_cart(mock_cart, mock_payment_method.return_value)
    assert mock_cart.payment_status == 'Credit Card Payment Processed'


# happy path - run_multiple_payments - Test that run_multiple_payments processes payments with multiple payment methods.
def test_run_multiple_payments(mock_cart, mock_payment_method, mock_time_sleep, mock_run_multiple_payments):
    mock_run_multiple_payments.return_value = None
    run_multiple_payments(mock_cart)
    assert mock_cart.payment_status == 'Method 4 Payment Processed'


# happy path - apply_promotions - Test that apply_promotions applies promotions correctly to the cart items.
def test_apply_promotions_multiple_promotions(mock_cart, mock_promotions):
    promotions = [mock_promotions, mock_promotions]
    promotions[0].name = 'Spring Sale'
    promotions[0].discount_rate = 0.1
    promotions[1].name = 'Black Friday'
    promotions[1].discount_rate = 0.2
    apply_promotions(mock_cart, promotions)
    assert mock_cart.items[0]['price'] == 72
    assert mock_cart.items[1]['price'] == 144


# edge case - process_payments - Test that process_payments handles an empty list of payment methods without error.
def test_process_payments_empty_methods(mock_cart):
    process_payments(mock_cart, [])
    assert mock_cart.payment_status == ''


# edge case - make_payments - Test that make_payments handles an empty cart without error.
def test_make_payments_empty_cart(mock_cart, mock_payment_method):
    mock_cart.items = []
    make_payments(mock_cart, [mock_payment_method.return_value])
    assert mock_cart.payment_status == ''


# edge case - add_payment_to_cart - Test that add_payment_to_cart handles a payment method with zero processing time.
def test_add_payment_to_cart_zero_processing_time(mock_cart, mock_payment_method, mock_time_sleep):
    mock_payment_method.return_value.name = 'Credit Card'
    mock_payment_method.return_value.processing_time = 0
    add_payment_to_cart(mock_cart, mock_payment_method.return_value)
    assert mock_cart.payment_status == 'Credit Card Payment Processed'


# edge case - run_multiple_payments - Test that run_multiple_payments handles a cart with no items.
def test_run_multiple_payments_empty_cart(mock_cart, mock_run_multiple_payments):
    mock_cart.items = []
    mock_run_multiple_payments.return_value = None
    run_multiple_payments(mock_cart)
    assert mock_cart.payment_status == ''


# edge case - apply_promotions - Test that apply_promotions handles no promotions without altering cart items.
def test_apply_promotions_no_promotions(mock_cart):
    apply_promotions(mock_cart, [])
    assert mock_cart.items[0]['price'] == 100
    assert mock_cart.items[1]['price'] == 200


