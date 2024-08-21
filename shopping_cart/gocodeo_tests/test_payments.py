import pytest
from unittest.mock import Mock, patch
from mymodule import PaymentProcessor, process_payments, PaymentMethod, make_payments, add_payment_to_cart, run_multiple_payments, Promotion, apply_promotions

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.items = [Mock(price=100), Mock(price=200)]
    cart.payment_status = ""
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = Mock(spec=PaymentMethod)
    payment_method.process_payment = Mock()
    return payment_method

@pytest.fixture
def mock_payment_methods():
    return [Mock(spec=PaymentMethod) for _ in range(4)]

@pytest.fixture
def mock_promotions():
    return [Mock(spec=Promotion) for _ in range(2)]

@pytest.fixture(autouse=True)
def mock_time_sleep():
    with patch('time.sleep', return_value=None):
        yield

@pytest.fixture(autouse=True)
def mock_threading_thread():
    with patch('threading.Thread', autospec=True) as mock_thread:
        yield mock_thread

# happy_path - process_payments - Test processing payments with multiple payment methods
def test_process_payments(mock_cart, mock_payment_methods):
    process_payments(mock_cart, mock_payment_methods)
    for payment_method in mock_payment_methods:
        payment_method.process_payment.assert_called_once_with(mock_cart)

# happy_path - make_payments - Test making payments using the make_payments function
def test_make_payments(mock_cart, mock_payment_methods):
    make_payments(mock_cart, mock_payment_methods)
    for payment_method in mock_payment_methods:
        payment_method.process_payment.assert_called_once_with(mock_cart)

# happy_path - run_multiple_payments - Test running multiple payments with different payment methods
def test_run_multiple_payments(mock_cart):
    run_multiple_payments(mock_cart)
    assert mock_cart.payment_status == "Method 4 Payment Processed"

# edge_case - apply_promotions - Test applying promotions with no items in the cart
def test_apply_promotions_empty_cart():
    cart = Mock()
    cart.items = []
    promotions = [Promotion("Spring Sale", 0.1)]
    apply_promotions(cart, promotions)
    assert len(cart.items) == 0

# edge_case - add_payment_to_cart - Test adding payment to cart with a single payment method
def test_add_payment_to_cart(mock_cart, mock_payment_method):
    add_payment_to_cart(mock_cart, mock_payment_method)
    mock_payment_method.process_payment.assert_called_once_with(mock_cart)

