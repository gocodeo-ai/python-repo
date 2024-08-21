import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
import time

@pytest.fixture
def mock_cart():
    return MagicMock()

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock:
        yield mock

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('__main__.get_item_details_from_db') as mock:
        yield mock

@pytest.fixture
def mock_calculate_total_price():
    with patch.object(mock_cart, 'calculate_total_price', return_value=40.0) as mock:
        yield mock# happy_path - get_all_items_from_cart - Test retrieving all items from a cart with valid item IDs.
def test_get_all_items_from_cart_valid_ids(mock_get_item_details_from_db):
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}
    cart = {'items': [{'item_id': 1, 'quantity': 2}, {'item_id': 2, 'quantity': 1}]}
    expected_result = [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]
    assert get_all_items_from_cart(cart) == expected_result


# happy_path - calculate_discounted_price - Test calculating discounted price for a cart with multiple items.
def test_calculate_discounted_price_multiple_items():
    cart = {'items': [{'price': 10.0, 'quantity': 2}, {'price': 20.0, 'quantity': 1}]}
    discount_rate = 0.1
    expected_result = 27.0
    assert calculate_discounted_price(cart, discount_rate) == expected_result


# happy_path - print_cart_summary - Test printing cart summary with valid items.
def test_print_cart_summary_valid_items(mock_calculate_total_price, capsys):
    cart = {'items': [{'name': 'Item 1', 'category': 'general', 'quantity': 2, 'price': 10.0}, {'name': 'Item 2', 'category': 'general', 'quantity': 1, 'price': 20.0}], 'calculate_total_price': lambda: 40.0}
    print_cart_summary(cart)
    captured = capsys.readouterr()
    expected_output = 'Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 10.0\nItem: Item 2, Category: general, Quantity: 1, Price: 20.0\nTotal Price: 40.0\n'
    assert captured.out == expected_output


# happy_path - save_cart_to_db - Test saving cart to database with valid items.
def test_save_cart_to_db_valid_items(mock_add_item_to_cart_db):
    cart = {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 1, 'price': 20.0}]}
    save_cart_to_db(cart)
    assert mock_add_item_to_cart_db.call_count == 2


# happy_path - get_item_details_from_db - Test getting item details from database with valid item ID.
def test_get_item_details_from_db_valid_id():
    item_id = 1
    expected_result = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    assert get_item_details_from_db(item_id) == expected_result


# edge_case - get_all_items_from_cart - Test retrieving all items from an empty cart.
def test_get_all_items_from_cart_empty_cart():
    cart = {'items': []}
    expected_result = []
    assert get_all_items_from_cart(cart) == expected_result


# edge_case - calculate_discounted_price - Test calculating discounted price with zero items in the cart.
def test_calculate_discounted_price_zero_items():
    cart = {'items': []}
    discount_rate = 0.1
    expected_result = 0.0
    assert calculate_discounted_price(cart, discount_rate) == expected_result


# edge_case - print_cart_summary - Test printing cart summary with no items.
def test_print_cart_summary_no_items(mock_calculate_total_price, capsys):
    cart = {'items': [], 'calculate_total_price': lambda: 0.0}
    print_cart_summary(cart)
    captured = capsys.readouterr()
    expected_output = 'Cart Summary:\nTotal Price: 0.0\n'
    assert captured.out == expected_output


# edge_case - save_cart_to_db - Test saving an empty cart to database.
def test_save_cart_to_db_empty_cart(mock_add_item_to_cart_db):
    cart = {'items': []}
    save_cart_to_db(cart)
    assert mock_add_item_to_cart_db.call_count == 0


# edge_case - get_item_details_from_db - Test getting item details from database with invalid item ID.
def test_get_item_details_from_db_invalid_id():
    item_id = -1
    expected_result = 'Item not found.'
    assert get_item_details_from_db(item_id) == expected_result


