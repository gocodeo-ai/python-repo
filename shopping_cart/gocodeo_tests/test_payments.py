import pytest
from unittest import mock1
from shopping_cart.payments import (
    PaymentProcessor,
    process_payments,
    PaymentMethod,
    make_payments,
    add_payment_to_cart,
    run_multiple_payments,
    apply_promotions,
)

@pytest.fixture
def mock_cart():
    cart = mock.Mock()
    cart.items = [mock.Mock(price=100)]
    cart.payment_status = "Initial Status"
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = mock.Mock(spec=PaymentMethod)
    payment_method.name = "mock_payment_method"
    payment_method.processing_time = 0.1
    payment_method.process_payment = mock.Mock()
    return payment_method

@pytest.fixture
def mock_promotions():
    return [mock.Mock(name="Spring Sale", discount_rate=0.2)]

@pytest.fixture
def mock_payment_methods():
    return [mock.Mock(spec=PaymentMethod, name=f"Method {i}", processing_time=i * 0.1) for i in range(1, 5)]

@pytest.fixture
def mock_payment_processor():
    return mock.Mock(spec=PaymentProcessor)

@pytest.fixture
def mock_thread():
    with mock.patch('threading.Thread.start') as mock_start, \
         mock.patch('threading.Thread.join') as mock_join:
        yield mock_start, mock_join

# happy_path - __init__ - Test that PaymentProcessor initializes correctly with given cart and payment method
def test_payment_processor_initialization(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    assert processor.cart == mock_cart12
    assert processor.payment_method == mock_payment_method


# happy_path - run - Test that PaymentProcessor runs and processes payment using the payment method
def test_payment_processor_run(mock_cart, mock_payment_method):
    processor = PaymentProcessor(mock_cart, mock_payment_method)
    processor.run()
    mock_payment_method.process_payment.assert_called_once_with(mock_cart)


# happy_path - process_payments - Test that process_payments starts and joins threads for each payment method
def test_process_payments(mock_cart, mock_payment_methods, mock_thread):
    process_payments(mock_cart, mock_payment_methods)
    for method in mock_payment_methods:
        method.process_payment.assert_called_once_with(mock_cart)


# happy_path - make_payments - Test that make_payments calls process_payments with correct arguments
def test_make_payments(mock_cart, mock_payment_methods, mocker):
    mock_process_payments = mocker.patch('shopping_cart.payments.process_payments')
    make_payments(mock_cart, mock_payment_methods)
    mock_process_payments.assert_called_once_with(mock_cart, mock_payment_methods)


# happy_path - add_payment_to_cart - Test that add_payment_to_cart processes payment using the given payment method
def test_add_payment_to_cart(mock_cart, mock_payment_method, mock_thread):
    add_payment_to_cart(mock_cart, mock_payment_method)
    mock_payment_method.process_payment.assert_called_once_with(mock_cart)


# happy_path - run_multiple_payments - Test that run_multiple_payments processes multiple payment methods sequentially
def test_run_multiple_payments(mock_cart, mock_payment_methods, mock_thread):
    run_multiple_payments(mock_cart)
    for method in mock_payment_methods:
        method.process_payment.assert_called_once_with(mock_cart)


# happy_path - apply_promotions - Test that apply_promotions applies discount for Spring Sale promotion
def test_apply_promotions_spring_sale(mock_cart, mock_promotions):
    original_price = mock_cart.items[0].price
    apply_promotions(mock_cart, mock_promotions)
    assert mock_cart.items[0].price == original_price * 0.8


# edge_case - __init__ - Test that PaymentProcessor handles None as cart or payment method
def test_payment_processor_initialization_with_none():
    processor = PaymentProcessor(None, None)
    assert processor.cart is None
    assert processor.payment_method is None


# edge_case - run - Test that run handles payment method with zero processing time
def test_payment_processor_run_with_zero_time(mock_cart):
    payment_method = PaymentMethod(name='Instant', processing_time=0)
    processor = PaymentProcessor(mock_cart, payment_method)
    processor.run()
    assert mock_cart.payment_status == 'Instant Payment Processed'


# edge_case - process_payments - Test that process_payments handles empty payment methods list
def test_process_payments_with_empty_list(mock_cart):
    process_payments(mock_cart, [])
    assert mock_cart.payment_status == 'Initial Status'


# edge_case - make_payments - Test that make_payments handles cart with no items
def test_make_payments_with_empty_cart(mock_payment_methods):
    cart = mock.Mock()
    cart.items = []
    cart.payment_status = 'Initial Status'
    make_payments(cart, mock_payment_methods)
    assert cart.payment_status == 'mock_payment_method Payment Processed'


# edge_case - add_payment_to_cart - Test that add_payment_to_cart handles invalid payment method
def test_add_payment_to_cart_with_invalid_method(mock_cart):
    add_payment_to_cart(mock_cart, None)
    assert mock_cart.payment_status == 'Initial Status'


# edge_case - run_multiple_payments - Test that run_multiple_payments handles no payment methods
def test_run_multiple_payments_with_no_methods(mock_cart, mock_thread):
    with mock.patch('shopping_cart.payments.process_payments') as mock_process_payments:
        run_multiple_payments(mock_cart)
        mock_process_payments.assert_called_once_with(mock_cart, mock.ANY)


# edge_case - apply_promotions - Test that apply_promotions handles invalid promotion type
def test_apply_promotions_with_invalid_promotion(mock_cart):
    promotions = [mock.Mock(name='Invalid', discount_rate=0.5)]
    original_price = mock_cart.items[0].price
    apply_promotions(mock_cart, promotions)
    assert mock_cart.items[0].price == original_price


