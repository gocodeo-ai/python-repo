import pytest
from unittest.mock import Mock, patch, create_autospec
from shopping_cart.payments import PaymentProcessor, PaymentMethod, process_payments, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions, Promotion

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.items = [Mock(price=100.0), Mock(price=150.0)]
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = create_autospec(PaymentMethod, instance=True)
    payment_method.name = "mock_payment_method"
    payment_method.processing_time = 0.1
    return payment_method

@pytest.fixture
def mock_payment_methods():
    method1 = create_autospec(PaymentMethod, instance=True)
    method1.name = "method1"
    method1.processing_time = 0.1

    method2 = create_autospec(PaymentMethod, instance=True)
    method2.name = "method2"
    method2.processing_time = 0.2

    return [method1, method2]

@pytest.fixture
def mock_promotions():
    promotion1 = create_autospec(Promotion, instance=True)
    promotion1.name = "Spring Sale"
    promotion1.discount_rate = 0.1

    promotion2 = create_autospec(Promotion, instance=True)
    promotion2.name = "Black Friday"
    promotion2.discount_rate = 0.2

    return [promotion1, promotion2]

@pytest.fixture
def mock_thread():
    with patch('shopping_cart.payments.Thread', autospec=True) as mock_thread:
        yield mock_thread

@pytest.fixture
def mock_time_sleep():
    with patch('shopping_cart.payments.time.sleep', autospec=True) as mock_sleep:
        yield mock_sleep

# happy_path - run - Test that PaymentProcessor run method calls process_payment
def test_payment_processor_run(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    processor.run()
    mock_payment_method.process_payment.assert_called_once_with(mock_cart)
    assert mock_cart.payment_status == 'mock_payment_method Payment Processed'

# happy_path - process_payments - Test that process_payments starts and joins threads for each payment method
def test_process_payments(mock_cart, mock_payment_methods, mock_thread):
    process_payments(mock_cart, mock_payment_methods)
    assert mock_thread.call_count == 2
    for method in mock_payment_methods:
        method.process_payment.assert_called_once_with(mock_cart)

# happy_path - make_payments - Test that make_payments processes payments for all methods
def test_make_payments(mock_cart, mock_payment_methods):
    make_payments(mock_cart, mock_payment_methods)
    for method in mock_payment_methods:
        method.process_payment.assert_called_once_with(mock_cart)
    assert mock_cart.payment_status == 'method2 Payment Processed'

# happy_path - add_payment_to_cart - Test that add_payment_to_cart processes payment for a single method
def test_add_payment_to_cart(mock_cart, mock_payment_method):
    add_payment_to_cart(mock_cart, mock_payment_method)
    mock_payment_method.process_payment.assert_called_once_with(mock_cart)
    assert mock_cart.payment_status == 'mock_payment_method Payment Processed'

# edge_case - __init__ - Test that PaymentProcessor __init__ handles None as cart
def test_payment_processor_init_none_cart(mock_payment_method):
    processor = PaymentProcessor(None, mock_payment_method)
    assert processor.cart is None
    assert processor.payment_method == mock_payment_method

# edge_case - process_payments - Test that process_payments handles empty payment methods list
def test_process_payments_empty_methods(mock_cart, mock_thread):
    process_payments(mock_cart, [])
    mock_thread.assert_not_called()

# edge_case - process_payment - Test that PaymentMethod process_payment handles zero processing time
def test_process_payment_zero_time(mock_cart, mock_payment_method, mock_time_sleep):
    mock_payment_method.processing_time = 0
    mock_payment_method.process_payment(mock_cart)
    mock_time_sleep.assert_called_once_with(0)
    assert mock_cart.payment_status == 'mock_payment_method Payment Processed'

# edge_case - run_multiple_payments - Test that run_multiple_payments handles multiple payment methods
def test_run_multiple_payments(mock_cart, mock_thread):
    run_multiple_payments(mock_cart)
    assert mock_thread.call_count == 4
    assert mock_cart.payment_status == 'Method 4 Payment Processed'

# edge_case - apply_promotions - Test that apply_promotions applies multiple promotions correctly
def test_apply_promotions(mock_cart, mock_promotions):
    apply_promotions(mock_cart, mock_promotions)
    for item in mock_cart.items:
        assert item.price == pytest.approx(72.0, 0.01) or item.price == pytest.approx(144.0, 0.01)

