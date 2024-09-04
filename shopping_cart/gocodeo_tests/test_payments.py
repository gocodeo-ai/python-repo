import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import PaymentProcessor, process_payments, PaymentMethod, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions, Promotion

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.items = [MagicMock(price=100), MagicMock(price=200)]
    cart.payment_status = None
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = MagicMock()
    payment_method.name = "Mock Payment Method"
    payment_method.processing_time = 0.1
    payment_method.process_payment = MagicMock()
    return payment_method

@pytest.fixture
def mock_payment_method1():
    payment_method = MagicMock()
    payment_method.name = "Mock Payment Method 1"
    payment_method.processing_time = 0.1
    payment_method.process_payment = MagicMock()
    return payment_method

@pytest.fixture
def mock_payment_method2():
    payment_method = MagicMock()
    payment_method.name = "Mock Payment Method 2"
    payment_method.processing_time = 0.2
    payment_method.process_payment = MagicMock()
    return payment_method

@pytest.fixture
def mock_promotions():
    promotion1 = MagicMock()
    promotion1.name = "Spring Sale"
    promotion1.discount_rate = 0.1

    promotion2 = MagicMock()
    promotion2.name = "Black Friday"
    promotion2.discount_rate = 0.2

    return [promotion1, promotion2]

@pytest.fixture
def mock_threads():
    with patch('shopping_cart.payments.Thread') as mock_thread:
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance
        yield mock_thread_instance

@pytest.fixture
def mock_time_sleep():
    with patch('shopping_cart.payments.time.sleep', return_value=None) as mock_sleep:
        yield mock_sleep

@pytest.fixture
def mock_process_payments():
    with patch('shopping_cart.payments.process_payments') as mock_process:
        yield mock_process

@pytest.fixture
def mock_payment_processor():
    with patch('shopping_cart.payments.PaymentProcessor') as mock_processor:
        yield mock_processor

@pytest.fixture
def mock_promotion_class():
    with patch('shopping_cart.payments.Promotion') as mock_promotion:
        yield mock_promotion

# happy_path - __init__ - Test that PaymentProcessor is initialized correctly with cart and payment method
def test_payment_processor_initialization(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    assert processor.cart == mock_cart
    assert processor.payment_method == mock_payment_method

# happy_path - run - Test that PaymentProcessor run method processes payment
def test_payment_processor_run(mock_cart, mock_payment_method, mock_time_sleep):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    processor.run()
    mock_payment_method.process_payment.assert_called_once_with(mock_cart)
    assert mock_cart.payment_status == 'Mock Payment Method Payment Processed'

# happy_path - process_payments - Test that process_payments function starts and joins threads for each payment method
def test_process_payments(mock_cart, mock_payment_method1, mock_payment_method2, mock_threads):
    payment_methods = [mock_payment_method1, mock_payment_method2]
    process_payments(mock_cart, payment_methods)
    assert mock_threads.start.call_count == 2
    assert mock_threads.join.call_count == 2

# happy_path - make_payments - Test that make_payments calls process_payments with correct arguments
def test_make_payments(mock_cart, mock_payment_method1, mock_process_payments):
    payment_methods = [mock_payment_method1]
    make_payments(mock_cart, payment_methods)
    mock_process_payments.assert_called_once_with(mock_cart, payment_methods)

# happy_path - add_payment_to_cart - Test that add_payment_to_cart starts and joins PaymentProcessor thread
def test_add_payment_to_cart(mock_cart, mock_payment_method, mock_payment_processor):
    add_payment_to_cart(mock_cart, mock_payment_method)
    mock_payment_processor.assert_called_once_with(mock_cart, mock_payment_method)
    mock_payment_processor.return_value.start.assert_called_once()
    mock_payment_processor.return_value.join.assert_called_once()

# happy_path - run_multiple_payments - Test that run_multiple_payments processes payments for multiple methods
def test_run_multiple_payments(mock_cart, mock_time_sleep):
    run_multiple_payments(mock_cart)
    assert mock_cart.payment_status == 'Method 4 Payment Processed'

# happy_path - apply_promotions - Test that apply_promotions applies Spring Sale discount correctly
def test_apply_promotions_spring_sale(mock_cart, mock_promotions):
    initial_prices = [item.price for item in mock_cart.items]
    apply_promotions(mock_cart, [mock_promotions[0]])
    for i, item in enumerate(mock_cart.items):
        assert item.price == initial_prices[i] * 0.9

# edge_case - __init__ - Test that PaymentProcessor initialization fails with None values
def test_payment_processor_initialization_with_none():
    with pytest.raises(TypeError):
        PaymentProcessor(None, None)

# edge_case - run - Test that PaymentProcessor run method handles exception if payment method is None
def test_payment_processor_run_with_none(mock_cart):
    processor = PaymentProcessor(mock_cart, None)
    with pytest.raises(AttributeError):
        processor.run()

# edge_case - process_payments - Test that process_payments handles empty payment methods list
def test_process_payments_with_empty_list(mock_cart, mock_threads):
    process_payments(mock_cart, [])
    assert mock_threads.start.call_count == 0
    assert mock_threads.join.call_count == 0

# edge_case - make_payments - Test that make_payments handles None as payment methods
def test_make_payments_with_none(mock_cart):
    with pytest.raises(TypeError):
        make_payments(mock_cart, None)

# edge_case - add_payment_to_cart - Test that add_payment_to_cart handles None as payment method
def test_add_payment_to_cart_with_none(mock_cart):
    with pytest.raises(TypeError):
        add_payment_to_cart(mock_cart, None)

# edge_case - run_multiple_payments - Test that run_multiple_payments handles empty cart
def test_run_multiple_payments_with_empty_cart():
    empty_cart = MagicMock()
    empty_cart.items = []
    run_multiple_payments(empty_cart)
    assert empty_cart.payment_status is None

# edge_case - apply_promotions - Test that apply_promotions handles empty promotions list
def test_apply_promotions_with_empty_list(mock_cart):
    initial_prices = [item.price for item in mock_cart.items]
    apply_promotions(mock_cart, [])
    for i, item in enumerate(mock_cart.items):
        assert item.price == initial_prices[i]

