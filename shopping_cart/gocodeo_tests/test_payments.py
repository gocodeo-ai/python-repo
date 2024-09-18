import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import PaymentProcessor, PaymentMethod, process_payments, make_payments, add_payment_to_cart, run_multiple_payments

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.payment_status = None
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = MagicMock(spec=PaymentMethod)
    payment_method.name = "sample_payment_method"
    payment_method.processing_time = 0.1
    return payment_method

@pytest.fixture
def mock_payment_methods():
    return [MagicMock(spec=PaymentMethod, name=f'Method {i}', processing_time=i * 0.1) for i in range(1, 5)]

@pytest.fixture
def mock_thread():
    with patch('shopping_cart.payments.Thread') as mock_thread:
        yield mock_thread

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock_sleep:
        yield mock_sleep

@pytest.fixture
def mock_process_payment():
    with patch.object(PaymentMethod, 'process_payment', return_value=None) as mock_process:
        yield mock_process

@pytest.fixture
def mock_process_payments():
    with patch('shopping_cart.payments.process_payments', return_value=None) as mock_process:
        yield mock_process

@pytest.fixture
def mock_add_payment_to_cart():
    with patch('shopping_cart.payments.add_payment_to_cart', return_value=None) as mock_add:
        yield mock_add

@pytest.fixture
def mock_run_multiple_payments():
    with patch('shopping_cart.payments.run_multiple_payments', return_value=None) as mock_run:
        yield mock_run

# happy_path - __init__ - Test that PaymentProcessor initializes with given cart and payment method
def test_payment_processor_initialization(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    assert processor.cart == mock_cart
    assert processor.payment_method == mock_payment_method


# happy_path - run - Test that PaymentProcessor runs and processes payment
def test_payment_processor_run(mock_cart, mock_payment_method, mock_time_sleep):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    processor.run()
    assert mock_cart.payment_status == "sample_payment_method Payment Processed"


# happy_path - process_payments - Test that process_payments starts and joins threads for each payment method
def test_process_payments(mock_cart, mock_payment_methods, mock_thread):
    process_payments(mock_cart, mock_payment_methods)
    assert mock_cart.payment_status == "Method 4 Payment Processed"
    assert mock_thread.call_count == len(mock_payment_methods)


# happy_path - make_payments - Test that make_payments processes all payment methods
def test_make_payments(mock_cart, mock_payment_methods, mock_process_payments):
    make_payments(mock_cart, mock_payment_methods)
    mock_process_payments.assert_called_once_with(mock_cart, mock_payment_methods)


# happy_path - add_payment_to_cart - Test that add_payment_to_cart processes a single payment method
def test_add_payment_to_cart(mock_cart, mock_payment_method, mock_thread):
    add_payment_to_cart(mock_cart, mock_payment_method)
    assert mock_cart.payment_status == "sample_payment_method Payment Processed"
    mock_thread.assert_called_once()


# happy_path - run_multiple_payments - Test that run_multiple_payments processes multiple payment methods
def test_run_multiple_payments(mock_cart, mock_process_payments):
    run_multiple_payments(mock_cart)
    mock_process_payments.assert_called_once_with(mock_cart, mock.ANY)


# edge_case - __init__ - Test that PaymentProcessor handles empty cart gracefully
def test_payment_processor_empty_cart(mock_payment_method):
    processor = PaymentProcessor(None, mock_payment_method)
    assert processor.cart is None
    assert processor.payment_method == mock_payment_method


# edge_case - process_payments - Test that process_payments handles no payment methods
def test_process_payments_no_methods(mock_cart):
    process_payments(mock_cart, [])
    assert mock_cart.payment_status is None


# edge_case - process_payment - Test that process_payment handles zero processing time
def test_process_payment_zero_time(mock_cart):
    payment_method = PaymentMethod('ZeroTime', 0)
    payment_method.process_payment(mock_cart)
    assert mock_cart.payment_status == 'ZeroTime Payment Processed'


# edge_case - add_payment_to_cart - Test that add_payment_to_cart handles null payment method
def test_add_payment_to_cart_null_method(mock_cart):
    add_payment_to_cart(mock_cart, None)
    assert mock_cart.payment_status is None


# edge_case - run_multiple_payments - Test that run_multiple_payments handles large number of methods
def test_run_multiple_payments_large_methods(mock_cart, mock_process_payments):
    run_multiple_payments(mock_cart)
    mock_process_payments.assert_called_once_with(mock_cart, mock.ANY)


