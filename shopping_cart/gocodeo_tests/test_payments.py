import pytest
from unittest.mock import Mock, patch
from threading import Thread

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.items = []
    cart.payment_status = None
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = Mock()
    payment_method.name = "MockPaymentMethod"
    payment_method.processing_time = 0.1
    return payment_method

@pytest.fixture
def mock_payment_method_zero_time():
    payment_method = Mock()
    payment_method.name = "ZeroProcessingTimeMethod"
    payment_method.processing_time = 0
    return payment_method

@pytest.fixture
def mock_payment_methods():
    payment_method1 = Mock()
    payment_method1.name = "MockPaymentMethod1"
    payment_method1.processing_time = 0.1

    payment_method2 = Mock()
    payment_method2.name = "MockPaymentMethod2"
    payment_method2.processing_time = 0.2

    return [payment_method1, payment_method2]

@pytest.fixture
def empty_cart():
    cart = Mock()
    cart.items = []
    cart.payment_status = None
    return cart

@pytest.fixture
def mock_promotions():
    promotion1 = Mock()
    promotion1.name = "Spring Sale"
    promotion1.discount_rate = 0.1

    promotion2 = Mock()
    promotion2.name = "Black Friday"
    promotion2.discount_rate = 0.2

    return [promotion1, promotion2]

@pytest.fixture
def mock_thread():
    with patch('threading.Thread', new=Mock()) as mock_thread:
        yield mock_thread

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep', new=Mock()) as mock_sleep:
        yield mock_sleep

# happy_path - __init__ - Test that PaymentProcessor initializes with cart and payment method
def test_payment_processor_init(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    assert processor.cart == mock_cart
    assert processor.payment_method == mock_payment_method

# happy_path - run - Test that PaymentProcessor run method processes payment
def test_payment_processor_run(mock_cart, mock_payment_method, mock_time_sleep):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    processor.run()
    assert mock_cart.payment_status == "MockPaymentMethod Payment Processed"

# happy_path - process_payments - Test that process_payments starts and joins threads for payment methods
def test_process_payments(mock_cart, mock_payment_methods, mock_thread):
    process_payments(mock_cart, mock_payment_methods)
    assert mock_cart.payment_status == "MockPaymentMethod2 Payment Processed"

# happy_path - make_payments - Test that make_payments processes payments through process_payments
def test_make_payments(mock_cart, mock_payment_methods, mock_thread):
    make_payments(mock_cart, mock_payment_methods)
    assert mock_cart.payment_status == "MockPaymentMethod2 Payment Processed"

# happy_path - add_payment_to_cart - Test that add_payment_to_cart processes a single payment
def test_add_payment_to_cart(mock_cart, mock_payment_method, mock_thread):
    add_payment_to_cart(mock_cart, mock_payment_method)
    assert mock_cart.payment_status == "MockPaymentMethod Payment Processed"

# edge_case - __init__ - Test that PaymentProcessor initializes with an empty cart
def test_payment_processor_init_empty_cart(empty_cart, mock_payment_method):
    processor = PaymentProcessor(empty_cart, mock_payment_method)
    assert processor.cart == empty_cart
    assert processor.payment_method == mock_payment_method

# edge_case - run - Test that run method handles payment method with zero processing time
def test_payment_processor_run_zero_processing_time(mock_cart, mock_payment_method_zero_time, mock_time_sleep):
    processor = PaymentProcessor(mock_cart, mock_payment_method_zero_time)
    processor.run()
    assert mock_cart.payment_status == "ZeroProcessingTimeMethod Payment Processed"

# edge_case - process_payments - Test that process_payments handles no payment methods
def test_process_payments_no_methods(mock_cart):
    process_payments(mock_cart, [])
    assert mock_cart.payment_status is None

# edge_case - make_payments - Test that make_payments handles a cart with no items
def test_make_payments_empty_cart(empty_cart, mock_payment_methods, mock_thread):
    make_payments(empty_cart, mock_payment_methods)
    assert empty_cart.payment_status == "MockPaymentMethod2 Payment Processed"

# edge_case - apply_promotions - Test that apply_promotions applies no promotions to an empty cart
def test_apply_promotions_empty_cart(empty_cart):
    apply_promotions(empty_cart, [])
    assert empty_cart.items == []

