import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.payments import PaymentProcessor, process_payments, make_payments, add_payment_to_cart, run_multiple_payments, PaymentMethod, Promotion, apply_promotions

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.items = []
    cart.payment_status = None
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = MagicMock(spec=PaymentMethod)
    payment_method.name = "MockPaymentMethod"
    payment_method.processing_time = 0.1
    return payment_method

@pytest.fixture
def mock_payment_methods():
    method1 = MagicMock(spec=PaymentMethod)
    method1.name = "MockPaymentMethod1"
    method1.processing_time = 0.1

    method2 = MagicMock(spec=PaymentMethod)
    method2.name = "MockPaymentMethod2"
    method2.processing_time = 0.2

    return [method1, method2]

@pytest.fixture
def mock_promotions():
    promotion1 = MagicMock(spec=Promotion)
    promotion1.name = "Spring Sale"
    promotion1.discount_rate = 0.1

    promotion2 = MagicMock(spec=Promotion)
    promotion2.name = "Black Friday"
    promotion2.discount_rate = 0.2

    return [promotion1, promotion2]

@pytest.fixture
def mock_empty_cart():
    cart = MagicMock()
    cart.items = []
    cart.payment_status = None
    return cart

@pytest.fixture
def mock_empty_payment_methods():
    return []

@pytest.fixture
def mock_empty_promotions():
    return []

@pytest.fixture
def mock_payment_processor():
    with patch('shopping_cart.payments.PaymentProcessor.run', MagicMock()) as mock_run:
        yield mock_run

@pytest.fixture
def mock_process_payment():
    with patch('shopping_cart.payments.PaymentMethod.process_payment', MagicMock()) as mock_process:
        yield mock_process

# happy_path - test_payment_processor_init - Test that PaymentProcessor initializes with given cart and payment method
def test_payment_processor_init(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    assert processor.cart == mock_cart
    assert processor.payment_method == mock_payment_method

# happy_path - test_payment_processor_run - Test that PaymentProcessor run method processes payment
def test_payment_processor_run(mock_cart, mock_payment_method, mock_process_payment):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    processor.run()
    mock_process_payment.assert_called_once_with(mock_cart)

# happy_path - test_process_payments - Test that process_payments starts and joins threads for each payment method
def test_process_payments(mock_cart, mock_payment_methods, mock_process_payment):
    process_payments(mock_cart, mock_payment_methods)
    assert mock_process_payment.call_count == len(mock_payment_methods)

# happy_path - test_make_payments - Test that make_payments processes payments using process_payments
def test_make_payments(mock_cart, mock_payment_methods, mock_process_payment):
    make_payments(mock_cart, mock_payment_methods)
    assert mock_process_payment.call_count == len(mock_payment_methods)

# happy_path - test_add_payment_to_cart - Test that add_payment_to_cart processes a single payment method
def test_add_payment_to_cart(mock_cart, mock_payment_method, mock_process_payment):
    add_payment_to_cart(mock_cart, mock_payment_method)
    mock_process_payment.assert_called_once_with(mock_cart)

# edge_case - test_payment_processor_init_empty_cart - Test that PaymentProcessor handles empty cart gracefully
def test_payment_processor_init_empty_cart(mock_empty_cart, mock_payment_method):
    processor = PaymentProcessor(mock_empty_cart, mock_payment_method)
    assert processor.cart == mock_empty_cart
    assert processor.payment_method == mock_payment_method

# edge_case - test_process_payments_empty_methods - Test that process_payments handles empty payment methods list
def test_process_payments_empty_methods(mock_cart, mock_empty_payment_methods, mock_process_payment):
    process_payments(mock_cart, mock_empty_payment_methods)
    mock_process_payment.assert_not_called()

# edge_case - test_make_payments_no_methods - Test that make_payments handles when no payment methods are provided
def test_make_payments_no_methods(mock_cart, mock_empty_payment_methods, mock_process_payment):
    make_payments(mock_cart, mock_empty_payment_methods)
    mock_process_payment.assert_not_called()

# edge_case - test_add_payment_to_cart_null_method - Test that add_payment_to_cart handles null payment method
def test_add_payment_to_cart_null_method(mock_cart):
    with pytest.raises(AttributeError):
        add_payment_to_cart(mock_cart, None)

# edge_case - test_apply_promotions_empty_list - Test that apply_promotions handles empty promotions list
def test_apply_promotions_empty_list(mock_cart, mock_empty_promotions):
    apply_promotions(mock_cart, mock_empty_promotions)
    assert mock_cart.items == []

