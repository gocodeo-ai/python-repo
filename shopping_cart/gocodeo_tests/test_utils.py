import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
import time

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('your_module_path.get_item_details_from_db') as mock:
        yield mock

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock:
        yield mock

@pytest.fixture
def cart_with_items():
    return {
        'items': [
            {'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Item 1', 'category': 'general'},
            {'item_id': 2, 'quantity': 1, 'price': 20.0, 'name': 'Item 2', 'category': 'general'}
        ],
        'calculate_total_price': lambda: 40.0
    }

@pytest.fixture
def empty_cart():
    return {
        'items': [],
        'calculate_total_price': lambda: 0.0
    }# happy_path - get_all_items_from_cart - Test retrieving all items from a populated cart
def test_get_all_items_from_cart(mock_get_item_details_from_db, cart_with_items):
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}
    result = get_all_items_from_cart(cart_with_items)
    assert result == [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]

# happy_path - get_item_details_from_db - Test getting item details from db
def test_get_item_details_from_db(mock_get_item_details_from_db):
    mock_get_item_details_from_db.return_value = {'name': 'Item 3', 'price': 10.0, 'category': 'general'}
    result = get_item_details_from_db(3)
    assert result == {'name': 'Item 3', 'price': 10.0, 'category': 'general'}

# happy_path - calculate_discounted_price - Test calculating discounted price with valid discount rate
def test_calculate_discounted_price(cart_with_items):
    result = calculate_discounted_price(cart_with_items, 0.1)
    assert result == 27.0

# happy_path - print_cart_summary - Test printing cart summary for a populated cart
def test_print_cart_summary(mock_time_sleep, cart_with_items, capsys):
    print_cart_summary(cart_with_items)
    captured = capsys.readouterr()
    assert captured.out == 'Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 10.0\nItem: Item 2, Category: general, Quantity: 1, Price: 20.0\nTotal Price: 40.0\n'

# happy_path - save_cart_to_db - Test saving a cart to the database
def test_save_cart_to_db(mock_add_item_to_cart_db, cart_with_items):
    save_cart_to_db(cart_with_items)
    assert mock_add_item_to_cart_db.call_count == 2

# edge_case - get_all_items_from_cart - Test retrieving items from an empty cart
def test_get_all_items_from_empty_cart(mock_get_item_details_from_db, empty_cart):
    result = get_all_items_from_cart(empty_cart)
    assert result == []

# edge_case - get_item_details_from_db - Test getting item details with an invalid item ID
def test_get_item_details_from_invalid_item_id():
    with pytest.raises(KeyError):
        get_item_details_from_db(-1)

# edge_case - calculate_discounted_price - Test calculating discounted price with a discount rate greater than 1
def test_calculate_discounted_price_high_discount():
    cart = {'items': [{'price': 10.0, 'quantity': 1}]}
    result = calculate_discounted_price(cart, 1.5)
    assert result == 0.0

# edge_case - print_cart_summary - Test printing cart summary with no items
def test_print_cart_summary_empty(mock_time_sleep, empty_cart, capsys):
    print_cart_summary(empty_cart)
    captured = capsys.readouterr()
    assert captured.out == 'Cart Summary:\nTotal Price: 0.0\n'

# edge_case - save_cart_to_db - Test saving an empty cart to the database
def test_save_empty_cart_to_db(mock_add_item_to_cart_db, empty_cart):
    save_cart_to_db(empty_cart)
    assert mock_add_item_to_cart_db.call_count == 0

