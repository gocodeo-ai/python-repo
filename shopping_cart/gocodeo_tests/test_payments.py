import pytest
from unittest.mock import Mock, patch
from shopping_cart.payments import PaymentProcessor, PaymentMethod, process_payments, make_payments, add_payment_to_cart, run_multiple_payments, apply_promotions

@pytest.fixture
def valid_cart_instance():
    cart = Mock()
    cart.items = [Mock(price=100), Mock(price=200)]
    return cart

@pytest.fixture
def valid_payment_method_instance():
    payment_method = Mock(spec=PaymentMethod)
    payment_method.name = "Valid Payment Method"
    payment_method.processing_time = 0.1
    return payment_method

@pytest.fixture
def valid_payment_method_instance1():
    payment_method = Mock(spec=PaymentMethod)
    payment_method.name = "Valid Payment Method 1"
    payment_method.processing_time = 0.1
    return payment_method

@pytest.fixture
def valid_payment_method_instance2():
    payment_method = Mock(spec=PaymentMethod)
    payment_method.name = "Valid Payment Method 2"
    payment_method.processing_time = 0.2
    return payment_method

@pytest.fixture
def valid_cart_instance_with_items():
    cart = Mock()
    cart.items = [Mock(price=100), Mock(price=200)]
    return cart

@pytest.fixture
def empty_cart_instance():
    cart = Mock()
    cart.items = []
    return cart

@pytest.fixture
def promotions():
    spring_sale = Mock(spec=Promotion)
    spring_sale.name = "Spring Sale"
    spring_sale.discount_rate = 0.1
    return [spring_sale]

@pytest.fixture
def no_promotions():
    return []

@pytest.fixture
def mock_sleep():
    with patch('time.sleep', return_value=None) as mock:
        yield mock

@pytest.fixture
def mock_thread_start():
    with patch('threading.Thread.start', return_value=None) as mock:
        yield mock

@pytest.fixture
def mock_thread_join():
    with patch('threading.Thread.join', return_value=None) as mock:
        yield mock# happy_path - payment_processor_init - generate test cases on PaymentProcessor initialization with valid cart and payment method.
def test_payment_processor_init(valid_cart_instance, valid_payment_method_instance):
    processor = PaymentProcessor(valid_cart_instance, valid_payment_method_instance)
    assert processor.cart == valid_cart_instance
    assert processor.payment_method == valid_payment_method_instance

# happy_path - payment_processor_run - generate test cases on successful payment processing in run method.
def test_payment_processor_run(valid_cart_instance, valid_payment_method_instance, mock_sleep):
    processor = PaymentProcessor(valid_cart_instance, valid_payment_method_instance)
    processor.run()
    assert valid_cart_instance.payment_status == 'Valid Payment Method Payment Processed'

# happy_path - process_payments - generate test cases on processing multiple payments successfully.
def test_process_payments(valid_cart_instance, valid_payment_method_instance1, valid_payment_method_instance2, mock_sleep):
    process_payments(valid_cart_instance, [valid_payment_method_instance1, valid_payment_method_instance2])
    assert valid_cart_instance.payment_status == 'Valid Payment Method 1 Payment Processed'
    assert valid_cart_instance.payment_status == 'Valid Payment Method 2 Payment Processed'

# happy_path - make_payments - generate test cases on making payments with valid cart and payment methods.
def test_make_payments(valid_cart_instance, valid_payment_method_instance, mock_sleep):
    make_payments(valid_cart_instance, [valid_payment_method_instance])
    assert valid_cart_instance.payment_status == 'Valid Payment Method Payment Processed'

# happy_path - add_payment_to_cart - generate test cases on adding payment to cart successfully.
def test_add_payment_to_cart(valid_cart_instance, valid_payment_method_instance, mock_sleep):
    add_payment_to_cart(valid_cart_instance, valid_payment_method_instance)
    assert valid_cart_instance.payment_status == 'Valid Payment Method Payment Processed'

# happy_path - run_multiple_payments - generate test cases on running multiple payments successfully.
def test_run_multiple_payments(valid_cart_instance, mock_sleep):
    run_multiple_payments(valid_cart_instance)
    assert valid_cart_instance.payment_status == ['Method 1 Payment Processed', 'Method 2 Payment Processed', 'Method 3 Payment Processed', 'Method 4 Payment Processed']

# happy_path - apply_promotions - generate test cases on applying promotions to cart items.
def test_apply_promotions(valid_cart_instance_with_items, promotions):
    apply_promotions(valid_cart_instance_with_items, promotions)
    assert valid_cart_instance_with_items.items[0].price == 90
    assert valid_cart_instance_with_items.items[1].price == 180

# edge_case - payment_processor_init_null_cart - generate test cases on PaymentProcessor initialization with null cart.
def test_payment_processor_init_null_cart(valid_payment_method_instance):
    with pytest.raises(TypeError):
        PaymentProcessor(None, valid_payment_method_instance)

# edge_case - payment_processor_init_null_payment_method - generate test cases on PaymentProcessor initialization with null payment method.
def test_payment_processor_init_null_payment_method(valid_cart_instance):
    with pytest.raises(TypeError):
        PaymentProcessor(valid_cart_instance, None)

# edge_case - process_payments_empty_methods - generate test cases on processing payments with an empty payment methods list.
def test_process_payments_empty_methods(valid_cart_instance):
    process_payments(valid_cart_instance, [])
    assert valid_cart_instance.payment_status == []

# edge_case - apply_promotions_no_promotions - generate test cases on applying promotions with no promotions provided.
def test_apply_promotions_no_promotions(valid_cart_instance_with_items, no_promotions):
    apply_promotions(valid_cart_instance_with_items, no_promotions)
    assert valid_cart_instance_with_items.items[0].price == 100
    assert valid_cart_instance_with_items.items[1].price == 200

# edge_case - add_payment_to_cart_null_payment_method - generate test cases on adding payment to cart with null payment method.
def test_add_payment_to_cart_null_payment_method(valid_cart_instance):
    with pytest.raises(TypeError):
        add_payment_to_cart(valid_cart_instance, None)

# edge_case - run_multiple_payments_empty_cart - generate test cases on running multiple payments with an empty cart.
def test_run_multiple_payments_empty_cart(empty_cart_instance):
    run_multiple_payments(empty_cart_instance)
    assert empty_cart_instance.payment_status == []

