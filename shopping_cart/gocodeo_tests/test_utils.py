import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import (
    get_all_items_from_cart,
    get_item_details_from_db,
    calculate_discounted_price,
    print_cart_summary,
    save_cart_to_db
)
from shopping_cart.database import add_item_to_cart_db
import time

@pytest.fixture
def mock_db_functions():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        yield mock_add_item_to_cart_db

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock_sleep:
        yield mock_sleep

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock_get_item_details:
        yield mock_get_item_details

@pytest.fixture
def mock_cart():
    return MagicMock()

# happy path - get_all_items_from_cart - Test that all items are retrieved from the cart with correct details
def test_get_all_items_from_cart(mock_cart, mock_get_item_details_from_db):
    mock_cart.items = [{'item_id': 1}, {'item_id': 2}]
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}
    expected_result = [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]
    result = get_all_items_from_cart(mock_cart)
    assert result == expected_result


# happy path - get_item_details_from_db - Test that item details are correctly fetched from the database
def test_get_item_details_from_db(mock_time_sleep):
    item_id = 1
    expected_result = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    result = get_item_details_from_db(item_id)
    assert result == expected_result


# happy path - calculate_discounted_price - Test that the discounted price is calculated correctly for a given discount rate
def test_calculate_discounted_price(mock_cart):
    mock_cart.items = [{'price': 100.0, 'quantity': 2}, {'price': 50.0, 'quantity': 1}]
    discount_rate = 0.1
    expected_result = 225.0
    result = calculate_discounted_price(mock_cart, discount_rate)
    assert result == expected_result


# happy path - print_cart_summary - Test that cart summary is printed correctly
def test_print_cart_summary(mock_cart, capsys):
    mock_cart.items = [{'name': 'Item 1', 'category': 'general', 'quantity': 2, 'price': 10.0}]
    mock_cart.calculate_total_price.return_value = 20.0
    expected_output = "Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 10.0\nTotal Price: 20.0\n"
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    assert captured.out == expected_output


# happy path - save_cart_to_db - Test that cart items are saved to the database correctly
def test_save_cart_to_db(mock_cart, mock_db_functions):
    mock_cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 1, 'price': 20.0}]
    save_cart_to_db(mock_cart)
    expected_queries = [
        'INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)',
        'INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)'
    ]
    mock_db_functions.assert_any_call(expected_queries[0])
    mock_db_functions.assert_any_call(expected_queries[1])


# edge case - get_all_items_from_cart - Test that function handles an empty cart gracefully
def test_get_all_items_from_cart_empty(mock_cart):
    mock_cart.items = []
    expected_result = []
    result = get_all_items_from_cart(mock_cart)
    assert result == expected_result


# edge case - get_item_details_from_db - Test that function handles invalid item_id gracefully
def test_get_item_details_from_db_invalid_id(mock_time_sleep):
    item_id = -1
    expected_result = {'name': 'Item -1', 'price': 10.0, 'category': 'general'}
    result = get_item_details_from_db(item_id)
    assert result == expected_result


# edge case - calculate_discounted_price - Test that function handles zero discount rate correctly
def test_calculate_discounted_price_zero_discount(mock_cart):
    mock_cart.items = [{'price': 100.0, 'quantity': 2}]
    discount_rate = 0.0
    expected_result = 200.0
    result = calculate_discounted_price(mock_cart, discount_rate)
    assert result == expected_result


# edge case - print_cart_summary - Test that function handles cart with zero quantity items
def test_print_cart_summary_zero_quantity(mock_cart, capsys):
    mock_cart.items = [{'name': 'Item 1', 'category': 'general', 'quantity': 0, 'price': 10.0}]
    mock_cart.calculate_total_price.return_value = 0.0
    expected_output = "Cart Summary:\nItem: Item 1, Category: general, Quantity: 0, Price: 10.0\nTotal Price: 0.0\n"
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    assert captured.out == expected_output


# edge case - save_cart_to_db - Test that function handles database save error gracefully
def test_save_cart_to_db_error(mock_cart, mock_db_functions):
    mock_cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}]
    mock_db_functions.side_effect = Exception('Database save error')
    with pytest.raises(Exception) as excinfo:
        save_cart_to_db(mock_cart)
    assert str(excinfo.value) == 'Database save error'


