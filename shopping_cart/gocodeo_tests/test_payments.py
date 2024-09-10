import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.payments import PaymentProcessor, PaymentMethod, process_payments, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions, Promotion

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 50}]
    return cart

@pytest.fixture
def mock_payment_method():
    payment_method = MagicMock(spec=PaymentMethod)
    payment_method.name = 'Credit Card'
    payment_method.processing_time = 0.1
    return payment_method

@pytest.fixture
def mock_payment_methods():
    payment_methods = [MagicMock(spec=PaymentMethod) for _ in range(2)]
    payment_methods[0].name = 'Credit Card'
    payment_methods[0].processing_time = 0.1
    payment_methods[1].name = 'PayPal'
    payment_methods[1].processing_time = 0.2
    return payment_methods

@pytest.fixture
def mock_promotions():
    promotions = [MagicMock(spec=Promotion) for _ in range(1)]
    promotions[0].name = 'Spring Sale'
    promotions[0].discount_rate = 0.1
    return promotions

@pytest.fixture
def mock_empty_cart():
    cart = MagicMock()
    cart.items = []
    return cart

@pytest.fixture
def mock_zero_processing_payment_method():
    payment_method = MagicMock(spec=PaymentMethod)
    payment_method.name = 'Instant'
    payment_method.processing_time = 0
    return payment_method

@pytest.fixture
def mock_invalid_payment_method():
    return None

@pytest.fixture
def mock_empty_payment_methods():
    return []

@pytest.fixture
def mock_no_promotions():
    return []

@pytest.fixture
def mock_multiple_payment_methods():
    payment_methods = [MagicMock(spec=PaymentMethod) for i in range(1, 5)]
    for i, method in enumerate(payment_methods, start=1):
        method.name = f"Method {i}"
        method.processing_time = i * 0.1
    return payment_methods

@pytest.fixture
def mock_promotion():
    promotion = MagicMock(spec=Promotion)
    promotion.name = 'Sale'
    promotion.discount_rate = 0.1
    return promotion

@pytest.fixture
def mock_payment_status():
    cart = MagicMock()
    cart.payment_status = None
    return cart

@pytest.fixture
def mock_cart_with_items():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 100}]
    return cart

@pytest.fixture
def mock_cart_with_price_50():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 50}]
    return cart

@pytest.fixture
def mock_cart_with_price_1000():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 1000}]
    return cart

@pytest.fixture
def mock_cart_with_discounted_items():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 90}]
    return cart

@pytest.fixture
def mock_cart_with_price_100():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 100}]
    return cart

@pytest.fixture
def mock_cart_with_price_90():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 90}]
    return cart

@pytest.fixture
def mock_cart_with_price_100():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 100}]
    return cart

@pytest.fixture
def mock_cart_with_price_100():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 100}]
    return cart

@pytest.fixture
def mock_cart_with_price_50():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 50}]
    return cart

@pytest.fixture
def mock_cart_with_price_1000():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 1000}]
    return cart

@pytest.fixture
def mock_cart_with_discounted_items():
    cart = MagicMock()
    cart.items = [{'name': 'item1', 'price': 90}]
    return cart

# happy_path - make_payments - Test that make_payments processes multiple payment methods
def test_make_payments_processes_multiple_methods(mock_cart, mock_payment_methods):
    make_payments(mock_cart, mock_payment_methods)
    assert mock_cart.payment_status == 'Stripe Payment Processed'

# happy_path - add_payment_to_cart - Test that add_payment_to_cart processes a single payment method
def test_add_payment_to_cart_processes_single_method(mock_cart_with_price_1000, mock_payment_method):
    add_payment_to_cart(mock_cart_with_price_1000, mock_payment_method)
    assert mock_cart_with_price_1000.payment_status == 'Debit Card Payment Processed'

# happy_path - run_multiple_payments - Test that run_multiple_payments processes payments with multiple methods
def test_run_multiple_payments_processes_payments(mock_cart):
    run_multiple_payments(mock_cart)
    assert mock_cart.payment_status == 'Method 4 Payment Processed'

# happy_path - apply_promotions - Test that apply_promotions applies promotions to cart items
def test_apply_promotions_applies_discounts(mock_cart, mock_promotions):
    apply_promotions(mock_cart, mock_promotions)
    assert mock_cart.items[0]['price'] == 222

# edge_case - __init__ - Test that PaymentProcessor handles empty cart
def test_payment_processor_with_empty_cart(mock_empty_cart, mock_payment_method):
    processor = PaymentProcessor(mock_empty_cart, mock_payment_method)
    processor.run()
    assert mock_empty_cart.items == []

# edge_case - run - Test that run method handles payment method with zero processing time
def test_run_with_zero_processing_time(mock_cart, mock_zero_processing_payment_method):
    processor = PaymentProcessor(mock_cart, mock_zero_processing_payment_method)
    processor.run()
    assert mock_cart.payment_status == 'Instant Payment Processed'

# edge_case - process_payments - Test that process_payments handles empty payment methods list
def test_process_payments_with_empty_methods_list(mock_cart, mock_empty_payment_methods):
    process_payments(mock_cart, mock_empty_payment_methods)
    assert mock_cart.payment_status is None

# edge_case - make_payments - Test that make_payments with no payment methods does nothing
def test_make_payments_with_no_methods(mock_cart_with_price_50, mock_empty_payment_methods):
    make_payments(mock_cart_with_price_50, mock_empty_payment_methods)
    assert mock_cart_with_price_50.payment_status is None

# edge_case - add_payment_to_cart - Test that add_payment_to_cart with invalid payment method raises error
def test_add_payment_to_cart_with_invalid_method(mock_cart, mock_invalid_payment_method):
    with pytest.raises(AttributeError):
        add_payment_to_cart(mock_cart, mock_invalid_payment_method)

# edge_case - apply_promotions - Test that apply_promotions with no promotions does not change prices
def test_apply_promotions_with_no_promotions(mock_cart_with_price_100, mock_no_promotions):
    apply_promotions(mock_cart_with_price_100, mock_no_promotions)
    assert mock_cart_with_price_100.items[0]['price'] == 100

