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
def mock_time_sleep():
    with patch('time.sleep', return_value=None) as mock:
        yield mock

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock:
        yield mock

@pytest.fixture
def mock_calculate_total_price():
    mock_cart = MagicMock()
    mock_cart.calculate_total_price = MagicMock(return_value=20.0)
    return mock_cart

# happy path - get_all_items_from_cart - Test that get_all_items_from_cart returns all item details from the cart correctly.
def test_get_all_items_from_cart_happy_path(mock_cart, mock_get_item_details_from_db):
    mock_cart.items = [{'item_id': 1}, {'item_id': 2}]
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}
    all_items = get_all_items_from_cart(mock_cart)
    expected_result = [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]
    assert all_items == expected_result


# happy path - get_item_details_from_db - Test that get_item_details_from_db returns correct item details for a valid item_id.
def test_get_item_details_from_db_happy_path(mock_time_sleep):
    item_details = get_item_details_from_db(1)
    expected_result = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_result


# happy path - calculate_discounted_price - Test that calculate_discounted_price returns correct discounted price for a given cart and discount rate.
def test_calculate_discounted_price_happy_path(mock_cart):
    mock_cart.items = [{'price': 100.0, 'quantity': 2}]
    discounted_price = calculate_discounted_price(mock_cart, 0.1)
    expected_result = 180.0
    assert discounted_price == expected_result


# happy path - print_cart_summary - Test that print_cart_summary prints the correct summary of the cart.
def test_print_cart_summary_happy_path(mock_cart, capsys):
    mock_cart.items = [{'name': 'Item 1', 'category': 'general', 'quantity': 2, 'price': 10.0}]
    mock_cart.calculate_total_price = MagicMock(return_value=20.0)
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    expected_output = 'Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 10.0\nTotal Price: 20.0\n'
    assert captured.out == expected_output


# happy path - save_cart_to_db - Test that save_cart_to_db correctly generates and executes queries for all items in the cart.
def test_save_cart_to_db_happy_path(mock_cart, mock_add_item_to_cart_db):
    mock_cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}]
    save_cart_to_db(mock_cart)
    mock_add_item_to_cart_db.assert_called_once_with('INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)')


# edge case - get_all_items_from_cart - Test that get_all_items_from_cart handles an empty cart correctly.
def test_get_all_items_from_cart_edge_case_empty_cart(mock_cart):
    mock_cart.items = []
    all_items = get_all_items_from_cart(mock_cart)
    expected_result = []
    assert all_items == expected_result


# edge case - get_item_details_from_db - Test that get_item_details_from_db handles an invalid item_id gracefully.
def test_get_item_details_from_db_edge_case_invalid_id(mock_time_sleep):
    item_details = get_item_details_from_db(999)
    expected_result = {'name': 'Item 999', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_result


# edge case - calculate_discounted_price - Test that calculate_discounted_price handles a cart with zero total price correctly.
def test_calculate_discounted_price_edge_case_zero_total(mock_cart):
    mock_cart.items = [{'price': 0.0, 'quantity': 0}]
    discounted_price = calculate_discounted_price(mock_cart, 0.1)
    expected_result = 0.0
    assert discounted_price == expected_result


# edge case - print_cart_summary - Test that print_cart_summary handles an empty cart without errors.
def test_print_cart_summary_edge_case_empty_cart(mock_cart, capsys):
    mock_cart.items = []
    mock_cart.calculate_total_price = MagicMock(return_value=0.0)
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    expected_output = 'Cart Summary:\nTotal Price: 0.0\n'
    assert captured.out == expected_output


# edge case - save_cart_to_db - Test that save_cart_to_db handles an empty cart without executing any queries.
def test_save_cart_to_db_edge_case_empty_cart(mock_cart, mock_add_item_to_cart_db):
    mock_cart.items = []
    save_cart_to_db(mock_cart)
    mock_add_item_to_cart_db.assert_not_called()


