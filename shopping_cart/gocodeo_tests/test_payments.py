import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import PaymentProcessor, PaymentMethod, Promotion, process_payments, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions

@pytest.fixture
def mock_cart():
    return MagicMock()

@pytest.fixture
def mock_payment_method():
    with patch('shopping_cart.payments.PaymentMethod') as mock:
        yield mock

@pytest.fixture
def mock_payment_processor():
    with patch('shopping_cart.payments.PaymentProcessor') as mock:
        yield mock

@pytest.fixture
def mock_process_payment():
    with patch('shopping_cart.payments.PaymentMethod.process_payment') as mock:
        yield mock

@pytest.fixture
def mock_run():
    with patch('shopping_cart.payments.PaymentProcessor.run') as mock:
        yield mock

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock:
        yield mock

@pytest.fixture
def mock_make_payments():
    with patch('shopping_cart.payments.make_payments') as mock:
        yield mock

@pytest.fixture
def mock_add_payment_to_cart():
    with patch('shopping_cart.payments.add_payment_to_cart') as mock:
        yield mock

@pytest.fixture
def mock_run_multiple_payments():
    with patch('shopping_cart.payments.run_multiple_payments') as mock:
        yield mock

# happy path - process_payments - Test that payments are processed for each method in the list.
def test_process_payments_happy_path(mock_cart, mock_payment_method, mock_payment_processor, mock_process_payment):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}, {'name': 'item2', 'price': 150}]
    payment_methods = [
        PaymentMethod('Visa', 0.1),
        PaymentMethod('MasterCard', 0.2)
    ]
    process_payments(cart, payment_methods)
    assert cart.payment_status == 'MasterCard Payment Processed'


# happy path - make_payments - Test that make_payments calls process_payments with the correct parameters.
def test_make_payments_happy_path(mock_cart, mock_payment_method, mock_make_payments):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}]
    payment_methods = [
        PaymentMethod('PayPal', 0.3)
    ]
    make_payments(cart, payment_methods)
    assert cart.payment_status == 'PayPal Payment Processed'


# happy path - add_payment_to_cart - Test that add_payment_to_cart processes a payment.
def test_add_payment_to_cart_happy_path(mock_cart, mock_payment_method, mock_add_payment_to_cart):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}]
    payment_method = PaymentMethod('Stripe', 0.4)
    add_payment_to_cart(cart, payment_method)
    assert cart.payment_status == 'Stripe Payment Processed'


# happy path - run_multiple_payments - Test that run_multiple_payments processes all payments in the list.
def test_run_multiple_payments_happy_path(mock_cart, mock_payment_method, mock_run_multiple_payments):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}, {'name': 'item2', 'price': 150}]
    run_multiple_payments(cart)
    assert cart.payment_status == 'Method 4 Payment Processed'


# happy path - apply_promotions - Test that apply_promotions applies the correct discount for Spring Sale.
def test_apply_promotions_spring_sale(mock_cart, mock_apply_promotions):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}, {'name': 'item2', 'price': 200}]
    promotions = [Promotion('Spring Sale', 0.1)]
    apply_promotions(cart, promotions)
    assert cart.items == [{'name': 'item1', 'price': 90.0}, {'name': 'item2', 'price': 180.0}]


# edge case - process_payments - Test process_payments with an empty list of payment methods.
def test_process_payments_no_methods(mock_cart, mock_payment_processor):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}]
    payment_methods = []
    process_payments(cart, payment_methods)
    assert cart.payment_status is None


# edge case - make_payments - Test make_payments with an empty cart.
def test_make_payments_empty_cart(mock_cart, mock_payment_method, mock_make_payments):
    cart = mock_cart
    cart.items = []
    payment_methods = [
        PaymentMethod('Visa', 0.1)
    ]
    make_payments(cart, payment_methods)
    assert cart.payment_status == 'Visa Payment Processed'


# edge case - add_payment_to_cart - Test add_payment_to_cart with a payment method with zero processing time.
def test_add_payment_to_cart_zero_time(mock_cart, mock_payment_method, mock_add_payment_to_cart):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}]
    payment_method = PaymentMethod('InstantPay', 0.0)
    add_payment_to_cart(cart, payment_method)
    assert cart.payment_status == 'InstantPay Payment Processed'


# edge case - run_multiple_payments - Test run_multiple_payments with a cart having a single item and multiple methods.
def test_run_multiple_payments_single_item(mock_cart, mock_payment_method, mock_run_multiple_payments):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}]
    run_multiple_payments(cart)
    assert cart.payment_status == 'Method 4 Payment Processed'


# edge case - apply_promotions - Test apply_promotions with a promotion not applicable to any items.
def test_apply_promotions_no_applicable(mock_cart, mock_apply_promotions):
    cart = mock_cart
    cart.items = [{'name': 'item1', 'price': 100}]
    promotions = [Promotion('Nonexistent Sale', 0.5)]
    apply_promotions(cart, promotions)
    assert cart.items == [{'name': 'item1', 'price': 100}]


