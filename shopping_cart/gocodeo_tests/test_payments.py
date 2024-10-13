import pytest
from unittest import mock
from shopping_cart.payments import (
    PaymentProcessor,
    PaymentMethod,
    Promotion,
    process_payments,
    make_payments,
    add_payment_to_cart,
    run_multiple_payments,
    apply_promotions
)

@pytest.fixture
def mock_cart():
    cart = mock.Mock()
    cart.items = []
    cart.payment_status = ''
    return cart

@pytest.fixture
def mock_payment_methods():
    payment_methods = [
        mock.Mock(spec=PaymentMethod, name='Credit Card', processing_time=0.1),
        mock.Mock(spec=PaymentMethod, name='PayPal', processing_time=0.2)
    ]
    return payment_methods

@pytest.fixture
def mock_promotions():
    promotions = [
        mock.Mock(spec=Promotion, name='Spring Sale', discount_rate=0.1),
        mock.Mock(spec=Promotion, name='Black Friday', discount_rate=0.2)
    ]
    return promotions

@pytest.fixture
def mock_payment_processor():
    with mock.patch('shopping_cart.payments.PaymentProcessor.run', return_value=None) as mock_run:
        yield mock_run

@pytest.fixture
def mock_process_payment():
    with mock.patch('shopping_cart.payments.PaymentMethod.process_payment', return_value=None) as mock_process:
        yield mock_process

@pytest.fixture
def mock_time_sleep():
    with mock.patch('time.sleep', return_value=None) as mock_sleep:
        yield mock_sleep

# happy path - process_payments - Test that process_payments starts and joins threads for multiple payment methods
def test_process_payments_multiple_methods(mock_cart, mock_payment_methods, mock_payment_processor):
    process_payments(mock_cart, mock_payment_methods)
    
    # Assert that the payment status is updated correctly
    assert mock_cart.payment_status == 'PayPal Payment Processed'
    
    # Assert that threads are started for each payment method
    assert mock_payment_processor.call_count == len(mock_payment_methods)


# happy path - make_payments - Test that make_payments processes payments with multiple methods
def test_make_payments_multiple_methods(mock_cart, mock_payment_methods, mock_payment_processor):
    make_payments(mock_cart, mock_payment_methods)

    # Assert that the payment status is updated correctly
    assert mock_cart.payment_status == 'PayPal Payment Processed'
    
    # Assert that threads are started for each payment method
    assert mock_payment_processor.call_count == len(mock_payment_methods)


# happy path - add_payment_to_cart - Test that add_payment_to_cart processes a single payment method
def test_add_payment_to_cart_single_method(mock_cart, mock_payment_methods, mock_payment_processor):
    payment_method = mock_payment_methods[0]
    add_payment_to_cart(mock_cart, payment_method)

    # Assert that the payment status is updated correctly
    assert mock_cart.payment_status == 'Credit Card Payment Processed'
    
    # Assert that thread is started
    mock_payment_processor.assert_called_once()


# happy path - run_multiple_payments - Test that run_multiple_payments processes payments with predefined methods
def test_run_multiple_payments_predefined_methods(mock_cart, mock_payment_processor):
    run_multiple_payments(mock_cart)

    # Assert that the payment status is updated correctly
    assert mock_cart.payment_status == 'Method 4 Payment Processed'
    
    # Assert that threads are started for each payment method
    assert mock_payment_processor.call_count == 4


# happy path - apply_promotions - Test that apply_promotions applies Spring Sale discount correctly
def test_apply_promotions_spring_sale(mock_cart, mock_promotions):
    mock_cart.items = [{'price': 100}, {'price': 200}]
    apply_promotions(mock_cart, [mock_promotions[0]])

    # Assert that the prices are updated correctly
    assert mock_cart.items == [{'price': 90}, {'price': 180}]


# edge case - process_payments - Test that process_payments handles empty payment methods list
def test_process_payments_empty_methods(mock_cart, mock_payment_processor):
    process_payments(mock_cart, [])

    # Assert that the payment status remains unchanged
    assert mock_cart.payment_status == ''
    
    # Assert that no threads are started
    mock_payment_processor.assert_not_called()


# edge case - make_payments - Test that make_payments handles empty cart
def test_make_payments_empty_cart(mock_cart, mock_payment_methods, mock_payment_processor):
    make_payments(mock_cart, mock_payment_methods)

    # Assert that the payment status is updated correctly
    assert mock_cart.payment_status == 'Credit Card Payment Processed'
    
    # Assert that threads are started for each payment method
    assert mock_payment_processor.call_count == len(mock_payment_methods)


# edge case - add_payment_to_cart - Test that add_payment_to_cart handles null payment method
def test_add_payment_to_cart_null_method(mock_cart, mock_payment_processor):
    add_payment_to_cart(mock_cart, None)

    # Assert that the payment status remains unchanged
    assert mock_cart.payment_status == ''
    
    # Assert that no thread is started
    mock_payment_processor.assert_not_called()


# edge case - run_multiple_payments - Test that run_multiple_payments handles null cart
def test_run_multiple_payments_null_cart(mock_payment_processor):
    with pytest.raises(AttributeError):
        run_multiple_payments(None)

    # Assert that no threads are started
    mock_payment_processor.assert_not_called()


# edge case - apply_promotions - Test that apply_promotions handles no promotions
def test_apply_promotions_no_promotions(mock_cart):
    mock_cart.items = [{'price': 100}, {'price': 200}]
    apply_promotions(mock_cart, [])

    # Assert that the prices remain unchanged
    assert mock_cart.items == [{'price': 100}, {'price': 200}]


