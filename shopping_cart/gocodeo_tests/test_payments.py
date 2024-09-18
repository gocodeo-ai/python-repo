import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import PaymentProcessor, PaymentMethod, process_payments, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.items = [MagicMock(price=10.0), MagicMock(price=20.0)]
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = MagicMock()
    payment_method.name = "mock_payment_method"
    payment_method.processing_time = 0.1
    payment_method.process_payment = MagicMock(side_effect=lambda cart: time.sleep(payment_method.processing_time) or setattr(cart, 'payment_status', f"{payment_method.name} Payment Processed"))
    return payment_method

@pytest.fixture
def mock_promotions():
    return [MagicMock(name="Spring Sale", discount_rate=0.1), MagicMock(name="Black Friday", discount_rate=0.2)]

@pytest.fixture
def mock_payment_methods():
    return [PaymentMethod(f"Method {i}", i * 0.1) for i in range(1, 5)]

@pytest.fixture
def thread_mock():
    with patch('shopping_cart.payments.Thread') as mock_thread:
        yield mock_thread

@pytest.fixture
def payment_processor_mock():
    with patch('shopping_cart.payments.PaymentProcessor') as mock_processor:
        yield mock_processor

@pytest.fixture
def payment_method_mock():
    with patch('shopping_cart.payments.PaymentMethod') as mock_method:
        yield mock_method

# happy_path - __init__ - Test that PaymentProcessor is initialized with given cart and payment method
def test_payment_processor_initialization(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    assert processor.cart == mock_cart
    assert processor.payment_method == mock_payment_method

# happy_path - run - Test that PaymentProcessor runs process_payment on payment_method
def test_payment_processor_run(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    processor.run()
    assert mock_cart.payment_status == 'mock_payment_method Payment Processed'

# happy_path - process_payments - Test that process_payments creates and starts threads for each payment method
def test_process_payments_starts_threads(mock_cart, mock_payment_methods, thread_mock):
    process_payments(mock_cart, mock_payment_methods)
    assert thread_mock.call_count == len(mock_payment_methods)

# happy_path - make_payments - Test that make_payments calls process_payments with given cart and payment methods
def test_make_payments_calls_process_payments(mock_cart, mock_payment_methods, payment_processor_mock):
    make_payments(mock_cart, mock_payment_methods)
    assert payment_processor_mock.call_count == len(mock_payment_methods)

# happy_path - add_payment_to_cart - Test that add_payment_to_cart starts and joins a PaymentProcessor thread
def test_add_payment_to_cart_starts_and_joins_thread(mock_cart, mock_payment_method, payment_processor_mock):
    add_payment_to_cart(mock_cart, mock_payment_method)
    payment_processor_mock.assert_called_once_with(mock_cart, mock_payment_method)
    payment_processor_mock.return_value.start.assert_called_once()
    payment_processor_mock.return_value.join.assert_called_once()

# happy_path - run_multiple_payments - Test that run_multiple_payments processes payments with multiple methods
def test_run_multiple_payments(mock_cart, payment_processor_mock):
    run_multiple_payments(mock_cart)
    assert payment_processor_mock.call_count == 4
    assert mock_cart.payment_status == 'Method 4 Payment Processed'

# happy_path - apply_promotions - Test that apply_promotions applies Spring Sale discount to cart items
def test_apply_promotions_spring_sale(mock_cart, mock_promotions):
    apply_promotions(mock_cart, mock_promotions)
    assert mock_cart.items[0].price == 9.0
    assert mock_cart.items[1].price == 18.0

# edge_case - __init__ - Test that PaymentProcessor handles None as cart
def test_payment_processor_with_none_cart(mock_payment_method):
    processor = PaymentProcessor(None, mock_payment_method)
    assert processor.cart is None

# edge_case - __init__ - Test that PaymentProcessor handles None as payment method
def test_payment_processor_with_none_payment_method(mock_cart):
    processor = PaymentProcessor(mock_cart, None)
    assert processor.payment_method is None

# edge_case - process_payments - Test that process_payments handles empty list of payment methods
def test_process_payments_with_empty_methods(mock_cart, thread_mock):
    process_payments(mock_cart, [])
    assert thread_mock.call_count == 0

# edge_case - process_payment - Test that process_payment handles zero processing time
def test_process_payment_with_zero_time(mock_cart):
    payment_method = PaymentMethod('Zero Time Method', 0)
    payment_method.process_payment(mock_cart)
    assert mock_cart.payment_status == 'Zero Time Method Payment Processed'

# edge_case - apply_promotions - Test that apply_promotions handles empty promotions list
def test_apply_promotions_with_empty_list(mock_cart):
    apply_promotions(mock_cart, [])
    assert mock_cart.items[0].price == 10.0
    assert mock_cart.items[1].price == 20.0

# edge_case - apply_promotions - Test that apply_promotions handles promotion with zero discount rate
def test_apply_promotions_zero_discount(mock_cart):
    promotions = [Promotion('No Discount', 0.0)]
    apply_promotions(mock_cart, promotions)
    assert mock_cart.items[0].price == 10.0
    assert mock_cart.items[1].price == 20.0

