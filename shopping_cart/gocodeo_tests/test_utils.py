import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('__main__.get_item_details_from_db') as mock_details:
        yield mock_details

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock_sleep:
        yield mock_sleep

@pytest.fixture
def cart():
    return MagicMock()

@pytest.fixture
def cart_with_items():
    cart = MagicMock()
    cart.items = [
        {'item_id': 1, 'quantity': 2, 'price': 10.0},
        {'item_id': 2, 'quantity': 1, 'price': 15.0}
    ]
    cart.calculate_total_price = MagicMock(return_value=35.0)
    return cart

@pytest.fixture
def empty_cart():
    cart = MagicMock()
    cart.items = []
    cart.calculate_total_price = MagicMock(return_value=0.0)
    return cart# happy_path - get_item_details_from_db - Test getting item details from the database with a valid ID
def test_get_item_details_valid_id():
    result = get_item_details_from_db(1)
    assert result == {'name': 'Item 1', 'price': 10.0, 'category': 'general'}

# edge_case - get_all_items_from_cart - Test getting all items from an empty cart
def test_get_all_items_from_cart_empty(empty_cart):
    result = get_all_items_from_cart(empty_cart)
    assert result == []

# edge_case - get_item_details_from_db - Test getting item details from the database with an invalid ID
def test_get_item_details_invalid_id():
    result = get_item_details_from_db(-1)
    assert result is None

# edge_case - calculate_discounted_price - Test calculating discounted price with a negative discount rate
def test_calculate_discounted_price_negative_discount():
    cart = {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0}]}
    result = calculate_discounted_price(cart, -0.1)
    assert result == 22.0

# edge_case - print_cart_summary - Test printing cart summary with an empty cart
def test_print_cart_summary_empty(empty_cart, capsys):
    print_cart_summary(empty_cart)
    captured = capsys.readouterr()
    assert captured.out == 'Cart Summary:\nTotal Price: 0.0\n'

# edge_case - save_cart_to_db - Test saving an empty cart to database
def test_save_cart_to_db_empty(mock_add_item_to_cart_db, empty_cart):
    save_cart_to_db(empty_cart)
    mock_add_item_to_cart_db.assert_not_called()

