import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import PaymentProcessor, process_payments, PaymentMethod, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.items = [MagicMock(price=100), MagicMock(price=200)]
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = MagicMock(spec=PaymentMethod)
    payment_method.name = "Mocked Payment Method"
    payment_method.processing_time = 0.1
    return payment_method

@pytest.fixture
def mock_promotions():
    return [MagicMock(name="Spring Sale", discount_rate=0.1), MagicMock(name="Black Friday", discount_rate=0.2)]

@pytest.fixture
def mock_payment_processor():
    with patch('shopping_cart.payments.PaymentProcessor.__init__', return_value=None) as mock_init:
        payment_processor = PaymentProcessor(MagicMock(), MagicMock())
        mock_init.assert_called_once()
        yield payment_processor

@pytest.fixture
def mock_process_payment():
    with patch('shopping_cart.payments.PaymentMethod.process_payment') as mock_process:
        yield mock_process

@pytest.fixture
def mock_thread_start():
    with patch('threading.Thread.start') as mock_start:
        yield mock_start

@pytest.fixture
def mock_thread_join():
    with patch('threading.Thread.join') as mock_join:
        yield mock_join

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock_sleep:
        yield mock_sleep

# happy_path - test_payment_processor_init - Test that PaymentProcessor is initialized correctly with cart and payment_method
def test_payment_processor_init(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    assert processor.cart == mock_cart
    assert processor.payment_method == mock_payment_method

# happy_path - test_run_calls_process_payment - Test that run method calls process_payment on payment_method
def test_run_calls_process_payment(mock_cart, mock_payment_method, mock_process_payment):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    processor.run()
    mock_process_payment.assert_called_once_with(mock_cart)

# happy_path - test_process_payments_starts_joins_threads - Test that process_payments starts and joins threads for each payment method
def test_process_payments_starts_joins_threads(mock_cart, mock_payment_method, mock_thread_start, mock_thread_join):
    payment_methods = [mock_payment_method, mock_payment_method]
    process_payments(mock_cart, payment_methods)
    assert mock_thread_start.call_count == len(payment_methods)
    assert mock_thread_join.call_count == len(payment_methods)

# happy_path - test_make_payments_processes_payments - Test that make_payments processes payments for given cart and methods
def test_make_payments_processes_payments(mock_cart, mock_payment_method, mock_process_payment):
    payment_methods = [mock_payment_method, mock_payment_method]
    make_payments(mock_cart, payment_methods)
    assert mock_process_payment.call_count == len(payment_methods)

# happy_path - test_add_payment_to_cart_processes_payment - Test that add_payment_to_cart processes payment for given cart and method
def test_add_payment_to_cart_processes_payment(mock_cart, mock_payment_method, mock_process_payment):
    add_payment_to_cart(mock_cart, mock_payment_method)
    mock_process_payment.assert_called_once_with(mock_cart)

# happy_path - test_run_multiple_payments_processes_methods - Test that run_multiple_payments processes multiple payment methods
def test_run_multiple_payments_processes_methods(mock_cart, mock_thread_start, mock_thread_join):
    run_multiple_payments(mock_cart)
    assert mock_thread_start.call_count == 4
    assert mock_thread_join.call_count == 4

# happy_path - test_apply_promotions_applies_discounts - Test that apply_promotions applies promotions to cart items
def test_apply_promotions_applies_discounts(mock_cart, mock_promotions):
    apply_promotions(mock_cart, mock_promotions)
    for item in mock_cart.items:
        assert item.price < 100 or item.price < 200

# edge_case - test_payment_processor_init_with_null_cart - Test that PaymentProcessor initialization with null cart raises error
def test_payment_processor_init_with_null_cart(mock_payment_method):
    with pytest.raises(TypeError):
        PaymentProcessor(None, mock_payment_method)

# edge_case - test_run_handles_exception - Test that run method handles exception if process_payment fails
def test_run_handles_exception(mock_cart, mock_payment_method):
    mock_payment_method.process_payment.side_effect = Exception("Payment Failed")
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    try:
        processor.run()
    except Exception:
        pytest.fail("run() method did not handle exception")

# edge_case - test_process_payments_with_empty_methods - Test that process_payments handles empty payment_methods list
def test_process_payments_with_empty_methods(mock_cart, mock_thread_start):
    process_payments(mock_cart, [])
    assert mock_thread_start.call_count == 0

# edge_case - test_make_payments_with_invalid_cart - Test that make_payments with invalid cart raises error
def test_make_payments_with_invalid_cart(mock_payment_method):
    with pytest.raises(TypeError):
        make_payments(None, [mock_payment_method])

# edge_case - test_add_payment_to_cart_with_invalid_method - Test that add_payment_to_cart with invalid payment method raises error
def test_add_payment_to_cart_with_invalid_method(mock_cart):
    with pytest.raises(TypeError):
        add_payment_to_cart(mock_cart, None)

# edge_case - test_apply_promotions_with_invalid_name - Test that apply_promotions with invalid promotion name does not alter prices
def test_apply_promotions_with_invalid_name(mock_cart):
    invalid_promotion = MagicMock(name="InvalidPromotion", discount_rate=0.5)
    original_prices = [item.price for item in mock_cart.items]
    apply_promotions(mock_cart, [invalid_promotion])
    for index, item in enumerate(mock_cart.items):
        assert item.price == original_prices[index]

