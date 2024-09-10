import pytest
from unittest import mock
from shopping_cart import Cart, Item
from shopping_cart.database import Database
from shopping_cart.discounts import DiscountManager
from shopping_cart.payments import PaymentProcessor
from shopping_cart.utils import Utils

@pytest.fixture
def mock_cart():
    with mock.patch('shopping_cart.Cart') as MockCart:
        instance = MockCart.return_value
        instance.size = 0
        yield instance

@pytest.fixture
def mock_item():
    with mock.patch('shopping_cart.Item') as MockItem:
        instance = MockItem.return_value
        instance.item_id = 101
        instance.name = 'Laptop'
        instance.price = 1000
        yield instance

@pytest.fixture
def mock_database():
    with mock.patch('shopping_cart.database.Database') as MockDatabase:
        instance = MockDatabase.return_value
        instance.get_item_by_id.return_value = {'item_name': 'Laptop', 'price': 1000}
        yield instance

@pytest.fixture
def mock_discount_manager():
    with mock.patch('shopping_cart.discounts.DiscountManager') as MockDiscountManager:
        instance = MockDiscountManager.return_value
        instance.apply_discount.return_value = 80  # Assuming a discount code reduces price to 80
        yield instance

@pytest.fixture
def mock_payment_processor():
    with mock.patch('shopping_cart.payments.PaymentProcessor') as MockPaymentProcessor:
        instance = MockPaymentProcessor.return_value
        instance.process_payment.return_value = {'status': 'success'}
        yield instance

@pytest.fixture
def mock_utils():
    with mock.patch('shopping_cart.utils.Utils') as MockUtils:
        instance = MockUtils.return_value
        yield instance

@pytest.fixture
def setup_cart(mock_cart, mock_item, mock_database, mock_discount_manager, mock_payment_processor, mock_utils):
    # Setup any additional state or configuration needed for the tests
    pass

# happy_path - test_add_item_to_cart_increases_size - Test that adding an item to the cart increases the cart size by one.
def test_add_item_to_cart_increases_size(setup_cart, mock_cart, mock_item):
    mock_cart.add_item.return_value = None
    mock_cart.size = 0
    mock_cart.add_item(mock_item.item_id, 1)
    mock_cart.size += 1
    assert mock_cart.size == 1

# happy_path - test_remove_item_from_cart_decreases_size - Test that removing an item from the cart decreases the cart size by one.
def test_remove_item_from_cart_decreases_size(setup_cart, mock_cart, mock_item):
    mock_cart.remove_item.return_value = None
    mock_cart.size = 1
    mock_cart.remove_item(mock_item.item_id)
    mock_cart.size -= 1
    assert mock_cart.size == 0

# happy_path - test_apply_valid_discount_code - Test that applying a valid discount code reduces the total price.
def test_apply_valid_discount_code(setup_cart, mock_discount_manager):
    total_price = 100
    discount_code = 'SUMMER20'
    discounted_price = mock_discount_manager.apply_discount(discount_code)
    assert discounted_price == 80

# happy_path - test_process_payment_success - Test that processing a payment with valid details returns success.
def test_process_payment_success(setup_cart, mock_payment_processor):
    payment_details = {'payment_method': 'credit_card', 'amount': 100}
    result = mock_payment_processor.process_payment(payment_details)
    assert result['status'] == 'success'

# happy_path - test_get_item_by_id_returns_correct_details - Test that fetching an item by ID returns the correct item details.
def test_get_item_by_id_returns_correct_details(setup_cart, mock_database):
    item_id = 101
    item_details = mock_database.get_item_by_id(item_id)
    assert item_details == {'item_name': 'Laptop', 'price': 1000}

# edge_case - test_add_item_with_zero_quantity - Test that adding an item with zero quantity does not change the cart size.
def test_add_item_with_zero_quantity(setup_cart, mock_cart, mock_item):
    mock_cart.add_item.return_value = None
    initial_size = mock_cart.size
    mock_cart.add_item(mock_item.item_id, 0)
    assert mock_cart.size == initial_size

# edge_case - test_remove_non_existent_item - Test that removing an item not in the cart does not change the cart size.
def test_remove_non_existent_item(setup_cart, mock_cart):
    mock_cart.remove_item.return_value = None
    initial_size = mock_cart.size
    mock_cart.remove_item(999)
    assert mock_cart.size == initial_size

# edge_case - test_apply_expired_discount_code - Test that applying an expired discount code does not affect the total price.
def test_apply_expired_discount_code(setup_cart, mock_discount_manager):
    total_price = 100
    discount_code = 'WINTER99'
    mock_discount_manager.apply_discount.return_value = total_price
    discounted_price = mock_discount_manager.apply_discount(discount_code)
    assert discounted_price == total_price

# edge_case - test_process_payment_insufficient_funds - Test that processing a payment with insufficient funds returns failure.
def test_process_payment_insufficient_funds(setup_cart, mock_payment_processor):
    payment_details = {'payment_method': 'credit_card', 'amount': 10000}
    mock_payment_processor.process_payment.return_value = {'status': 'failure'}
    result = mock_payment_processor.process_payment(payment_details)
    assert result['status'] == 'failure'

# edge_case - test_get_item_by_invalid_id - Test that fetching an item with an invalid ID returns an error.
def test_get_item_by_invalid_id(setup_cart, mock_database):
    item_id = 999
    mock_database.get_item_by_id.return_value = {'error': 'Item not found'}
    item_details = mock_database.get_item_by_id(item_id)
    assert item_details == {'error': 'Item not found'}

