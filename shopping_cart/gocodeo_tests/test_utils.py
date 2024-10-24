import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db
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
def mock_get_item_details_from_db():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock:
        yield mock

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock:
        yield mock

@pytest.fixture
def mock_calculate_total_price():
    with patch.object(mock_cart, 'calculate_total_price', return_value=20.0) as mock:
        yield mock

# happy path - get_all_items_from_cart - Test that all items are retrieved from the cart with correct details.
def test_get_all_items_from_cart(mock_cart, mock_get_item_details_from_db):
    mock_cart.items = [{'item_id': 1}, {'item_id': 2}]
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}
    
    all_items = get_all_items_from_cart(mock_cart)
    
    assert all_items == [
        {'name': 'Item 1', 'price': 10.0, 'category': 'general'},
        {'name': 'Item 2', 'price': 10.0, 'category': 'general'}
    ]


# happy path - get_item_details_from_db - Test that item details are fetched correctly from the database.
def test_get_item_details_from_db(mock_time_sleep):
    item_details = get_item_details_from_db(1)
    assert item_details == {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    mock_time_sleep.assert_called_once_with(1)


# happy path - calculate_discounted_price - Test that the discounted price is calculated correctly for a given discount rate.
def test_calculate_discounted_price(mock_cart):
    mock_cart.items = [{'price': 100.0, 'quantity': 2}]
    discounted_price = calculate_discounted_price(mock_cart, 0.1)
    assert discounted_price == 180.0


# happy path - print_cart_summary - Test that the cart summary is printed correctly without errors.
def test_print_cart_summary(mock_cart, capsys, mock_calculate_total_price):
    mock_cart.items = [{'name': 'Item 1', 'category': 'general', 'quantity': 2, 'price': 10.0}]
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    assert captured.out == 'Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 10.0\nTotal Price: 20.0\n'


# happy path - save_cart_to_db - Test that the cart is saved to the database correctly.
def test_save_cart_to_db(mock_cart, mock_add_item_to_cart_db):
    mock_cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}]
    save_cart_to_db(mock_cart)
    mock_add_item_to_cart_db.assert_called_once_with('INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)')


# edge case - get_all_items_from_cart - Test that getting all items from an empty cart returns an empty list.
def test_get_all_items_from_empty_cart(mock_cart, mock_get_item_details_from_db):
    mock_cart.items = []
    all_items = get_all_items_from_cart(mock_cart)
    assert all_items == []


# edge case - get_item_details_from_db - Test that fetching item details with a non-existent item_id returns None or raises an error.
def test_get_item_details_from_non_existent_id(mock_time_sleep):
    with pytest.raises(Exception) as excinfo:
        get_item_details_from_db(999)
    assert 'Item not found' in str(excinfo.value)
    mock_time_sleep.assert_called_once_with(1)


# edge case - calculate_discounted_price - Test that calculating discounted price with a discount rate of 1 returns zero.
def test_calculate_discounted_price_full_discount(mock_cart):
    mock_cart.items = [{'price': 100.0, 'quantity': 2}]
    discounted_price = calculate_discounted_price(mock_cart, 1.0)
    assert discounted_price == 0.0


# edge case - print_cart_summary - Test that printing cart summary with no items does not cause errors.
def test_print_cart_summary_empty_cart(mock_cart, capsys, mock_calculate_total_price):
    mock_cart.items = []
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    assert captured.out == 'Cart Summary:\nTotal Price: 0.0\n'


# edge case - save_cart_to_db - Test that saving an empty cart to the database does not execute any queries.
def test_save_empty_cart_to_db(mock_cart, mock_add_item_to_cart_db):
    mock_cart.items = []
    save_cart_to_db(mock_cart)
    mock_add_item_to_cart_db.assert_not_called()


