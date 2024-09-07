import pytest
from unittest.mock import Mock, patch
import time
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.utils import (
    get_all_items_from_cart,
    get_item_details_from_db,
    calculate_discounted_price,
    print_cart_summary,
    save_cart_to_db
)

class MockCart:
    def __init__(self):
        self.items = []

    def calculate_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.items)

@pytest.fixture
def mock_cart():
    cart = MockCart()
    cart.items = [
        {'item_id': 1, 'name': 'Item 1', 'category': 'general', 'quantity': 2, 'price': 10.0},
        {'item_id': 2, 'name': 'Item 2', 'category': 'general', 'quantity': 1, 'price': 15.0}
    ]
    return cart

@pytest.fixture
def mock_time():
    with patch('time.sleep') as mock_sleep:
        yield mock_sleep

@pytest.fixture
def mock_get_item_details():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock:
        mock.return_value = {"name": "Mocked Item", "price": 10.0, "category": "general"}
        yield mock

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock_print:
        yield mock_print

# happy path - get_all_items_from_cart - Generate test cases on successful retrieval of all items from cart
def test_get_all_items_from_cart_success(mock_cart, mock_get_item_details):
    result = get_all_items_from_cart(mock_cart)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    assert all('name' in item and 'price' in item and 'category' in item for item in result)

# happy path - get_item_details_from_db - Generate test cases on correct item details retrieval from database
def test_get_item_details_from_db_success(mock_time):
    result = get_item_details_from_db(1)
    assert isinstance(result, dict)
    assert 'name' in result and 'price' in result and 'category' in result
    assert result['name'] == 'Item 1'
    assert result['price'] == 10.0
    assert result['category'] == 'general'

# happy path - calculate_discounted_price - Generate test cases on accurate calculation of discounted price
def test_calculate_discounted_price_success(mock_cart):
    discount_rate = 0.1
    result = calculate_discounted_price(mock_cart, discount_rate)
    expected_price = (2 * 10.0 + 1 * 15.0) * (1 - discount_rate)
    assert result == pytest.approx(expected_price)

# happy path - print_cart_summary - Generate test cases on proper printing of cart summary
def test_print_cart_summary_success(mock_cart, mock_print):
    print_cart_summary(mock_cart)
    mock_print.assert_called()
    assert mock_print.call_count >= 4  # Header, 2 items, total price

# happy path - save_cart_to_db - Generate test cases on successful saving of cart to database
def test_save_cart_to_db_success(mock_cart, mock_add_item_to_cart_db):
    save_cart_to_db(mock_cart)
    assert mock_add_item_to_cart_db.call_count == 2  # Two items in the cart

# happy path - add_item_to_cart_db - Generate test cases on correct addition of item to cart database
def test_add_item_to_cart_db_success(mock_add_item_to_cart_db):
    query = "INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)"
    add_item_to_cart_db(query)
    mock_add_item_to_cart_db.assert_called_once_with(query)

# edge case - get_all_items_from_cart - Generate test cases on empty cart scenario
def test_get_all_items_from_empty_cart(mock_get_item_details):
    empty_cart = MockCart()
    result = get_all_items_from_cart(empty_cart)
    assert len(result) == 0

# edge case - get_item_details_from_db - Generate test cases on invalid item_id for database retrieval
def test_get_item_details_invalid_id(mock_time):
    result = get_item_details_from_db(-1)
    assert isinstance(result, dict)
    assert result['name'] == 'Item -1'
    assert result['price'] == 10.0
    assert result['category'] == 'general'

# edge case - calculate_discounted_price - Generate test cases on zero discount rate
def test_calculate_discounted_price_zero_discount(mock_cart):
    discount_rate = 0
    result = calculate_discounted_price(mock_cart, discount_rate)
    expected_price = mock_cart.calculate_total_price()
    assert result == expected_price

# edge case - print_cart_summary - Generate test cases on cart with fractional quantities
def test_print_cart_summary_fractional_quantities(mock_print):
    cart = MockCart()
    cart.items = [{'item_id': 1, 'name': 'Item 1', 'category': 'general', 'quantity': 1.5, 'price': 10.0}]
    print_cart_summary(cart)
    mock_print.assert_called()
    assert any('1.5' in str(call) for call in mock_print.call_args_list)

# edge case - save_cart_to_db - Generate test cases on database connection failure
def test_save_cart_to_db_connection_failure(mock_cart, mock_add_item_to_cart_db):
    mock_add_item_to_cart_db.side_effect = Exception('Database connection failed')
    with pytest.raises(Exception):
        save_cart_to_db(mock_cart)

# edge case - add_item_to_cart_db - Generate test cases on invalid SQL query
def test_add_item_to_cart_db_invalid_query(mock_add_item_to_cart_db):
    invalid_query = "INSERT INTO cart (invalid_column) VALUES (1)"
    mock_add_item_to_cart_db.side_effect = Exception('Invalid SQL query')
    with pytest.raises(Exception):
        add_item_to_cart_db(invalid_query)

