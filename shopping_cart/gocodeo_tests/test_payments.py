import pytest
from unittest import mock
from shopping_cart.payments import process_payments, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions, PaymentProcessor, PaymentMethod, Promotion

@pytest.fixture
def cart():
    class Cart:
        def __init__(self):
            self.items = [{'price': 100}, {'price': 200}]
            self.payment_status = None
            
    return Cart()

@pytest.fixture
def payment_methods():
    return [
        PaymentMethod(name='CreditCard', processing_time=0.1),
        PaymentMethod(name='PayPal', processing_time=0.2)
    ]

@pytest.fixture
def promotions():
    return [
        Promotion(name='Spring Sale', discount_rate=0.1)
    ]

@pytest.fixture(autouse=True)
def mock_dependencies():
    with mock.patch('shopping_cart.payments.PaymentProcessor.run') as mock_run, \
         mock.patch('shopping_cart.payments.PaymentMethod.process_payment') as mock_process_payment, \
         mock.patch('time.sleep', return_value=None):
        yield {
            'mock_run': mock_run,
            'mock_process_payment': mock_process_payment
        }

@pytest.fixture
def empty_cart():
    class EmptyCart:
        def __init__(self):
            self.items = []
            self.payment_status = None
            
    return EmptyCart()

# happy path - process_payments - Test that process_payments starts and joins threads for multiple payment methods
def test_process_payments_multiple_methods(cart, payment_methods, mock_dependencies):
    process_payments(cart, payment_methods)
    assert mock_dependencies['mock_process_payment'].call_count == len(payment_methods)
    assert cart.payment_status == 'PayPal Payment Processed'


# happy path - make_payments - Test that make_payments processes payments using given payment methods
def test_make_payments(cart, payment_methods, mock_dependencies):
    make_payments(cart, payment_methods)
    assert mock_dependencies['mock_process_payment'].call_count == len(payment_methods)
    assert cart.payment_status == 'PayPal Payment Processed'


# happy path - add_payment_to_cart - Test that add_payment_to_cart processes payment for a single payment method
def test_add_payment_to_cart(cart, mock_dependencies):
    payment_method = PaymentMethod(name='CreditCard', processing_time=0.1)
    add_payment_to_cart(cart, payment_method)
    mock_dependencies['mock_process_payment'].assert_called_once_with(cart)
    assert cart.payment_status == 'CreditCard Payment Processed'


# happy path - run_multiple_payments - Test that run_multiple_payments processes payments for multiple methods
def test_run_multiple_payments(cart, mock_dependencies):
    run_multiple_payments(cart)
    assert mock_dependencies['mock_process_payment'].call_count == 4
    assert cart.payment_status == 'Method 4 Payment Processed'


# happy path - apply_promotions - Test that apply_promotions applies Spring Sale promotion correctly
def test_apply_promotions_spring_sale(cart, promotions):
    apply_promotions(cart, promotions)
    assert cart.items[0]['price'] == 90
    assert cart.items[1]['price'] == 180


# edge case - process_payments - Test that process_payments handles empty payment methods list
def test_process_payments_empty_methods(cart, mock_dependencies):
    process_payments(cart, [])
    mock_dependencies['mock_process_payment'].assert_not_called()
    assert cart.payment_status is None


# edge case - make_payments - Test that make_payments handles empty cart
def test_make_payments_empty_cart(empty_cart, payment_methods, mock_dependencies):
    make_payments(empty_cart, payment_methods)
    assert mock_dependencies['mock_process_payment'].call_count == len(payment_methods)
    assert empty_cart.payment_status == 'CreditCard Payment Processed'


# edge case - add_payment_to_cart - Test that add_payment_to_cart handles payment method with zero processing time
def test_add_payment_to_cart_zero_processing_time(cart, mock_dependencies):
    payment_method = PaymentMethod(name='CreditCard', processing_time=0)
    add_payment_to_cart(cart, payment_method)
    mock_dependencies['mock_process_payment'].assert_called_once_with(cart)
    assert cart.payment_status == 'CreditCard Payment Processed'


# edge case - run_multiple_payments - Test that run_multiple_payments handles cart with no items
def test_run_multiple_payments_empty_cart(empty_cart, mock_dependencies):
    run_multiple_payments(empty_cart)
    assert mock_dependencies['mock_process_payment'].call_count == 4
    assert empty_cart.payment_status == 'Method 4 Payment Processed'


# edge case - apply_promotions - Test that apply_promotions handles empty promotions list
def test_apply_promotions_empty_promotions(cart):
    apply_promotions(cart, [])
    assert cart.items[0]['price'] == 100
    assert cart.items[1]['price'] == 200


