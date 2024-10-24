import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db
from shopping_cart.database import add_item_to_cart_db
import time

@pytest.fixture
def mock_dependencies():
    with patch('shopping_cart.utils.add_item_to_cart_db') as mock_add_item_to_cart_db, \
         patch('shopping_cart.utils.get_item_details_from_db') as mock_get_item_details_from_db, \
         patch('time.sleep', return_value=None) as mock_sleep:
        
        yield {
            'mock_add_item_to_cart_db': mock_add_item_to_cart_db,
            'mock_get_item_details_from_db': mock_get_item_details_from_db,
            'mock_sleep': mock_sleep
        }

# happy path - get_all_items_from_cart - Test that get_all_items_from_cart returns all item details correctly
def test_get_all_items_from_cart_happy_path(mock_dependencies):
    cart = MagicMock()
    cart.items = [{'item_id': 1}, {'item_id': 2}]
    mock_dependencies['mock_get_item_details_from_db'].side_effect = [
        {'name': 'Item 1', 'price': 10.0, 'category': 'general'},
        {'name': 'Item 2', 'price': 10.0, 'category': 'general'}
    ]
    result = get_all_items_from_cart(cart)
    assert result == [
        {'name': 'Item 1', 'price': 10.0, 'category': 'general'},
        {'name': 'Item 2', 'price': 10.0, 'category': 'general'}
    ]


# happy path - get_item_details_from_db - Test that get_item_details_from_db returns correct item details
def test_get_item_details_from_db_happy_path(mock_dependencies):
    mock_dependencies['mock_get_item_details_from_db'].return_value = {
        'name': 'Item 1', 'price': 10.0, 'category': 'general'
    }
    result = get_item_details_from_db(1)
    assert result == {'name': 'Item 1', 'price': 10.0, 'category': 'general'}


# happy path - calculate_discounted_price - Test that calculate_discounted_price calculates the correct discounted price
def test_calculate_discounted_price_happy_path():
    cart = MagicMock()
    cart.items = [{'price': 20.0, 'quantity': 2}, {'price': 10.0, 'quantity': 1}]
    discount_rate = 0.1
    result = calculate_discounted_price(cart, discount_rate)
    assert result == 45.0


# happy path - print_cart_summary - Test that print_cart_summary prints the correct summary
def test_print_cart_summary_happy_path(capfd):
    cart = MagicMock()
    cart.items = [
        {'name': 'Item 1', 'category': 'general', 'quantity': 1, 'price': 10.0},
        {'name': 'Item 2', 'category': 'general', 'quantity': 2, 'price': 20.0}
    ]
    cart.calculate_total_price = MagicMock(return_value=60.0)
    print_cart_summary(cart)
    captured = capfd.readouterr()
    assert captured.out == "Cart Summary:\nItem: Item 1, Category: general, Quantity: 1, Price: 10.0\nItem: Item 2, Category: general, Quantity: 2, Price: 20.0\nTotal Price: 60.0\n"


# happy path - save_cart_to_db - Test that save_cart_to_db saves all items to the database
def test_save_cart_to_db_happy_path(mock_dependencies):
    cart = MagicMock()
    cart.items = [
        {'item_id': 1, 'quantity': 1, 'price': 10.0},
        {'item_id': 2, 'quantity': 2, 'price': 20.0}
    ]
    save_cart_to_db(cart)
    mock_dependencies['mock_add_item_to_cart_db'].assert_any_call(
        'INSERT INTO cart (item_id, quantity, price) VALUES (1, 1, 10.0)'
    )
    mock_dependencies['mock_add_item_to_cart_db'].assert_any_call(
        'INSERT INTO cart (item_id, quantity, price) VALUES (2, 2, 20.0)'
    )


# edge case - get_all_items_from_cart - Test that get_all_items_from_cart handles empty cart gracefully
def test_get_all_items_from_cart_empty_cart(mock_dependencies):
    cart = MagicMock()
    cart.items = []
    result = get_all_items_from_cart(cart)
    assert result == []


# edge case - get_item_details_from_db - Test that get_item_details_from_db handles non-existent item_id gracefully
def test_get_item_details_from_db_non_existent_item(mock_dependencies):
    mock_dependencies['mock_get_item_details_from_db'].return_value = {
        'name': 'Item 999', 'price': 10.0, 'category': 'general'
    }
    result = get_item_details_from_db(999)
    assert result == {'name': 'Item 999', 'price': 10.0, 'category': 'general'}


# edge case - calculate_discounted_price - Test that calculate_discounted_price handles zero discount rate
def test_calculate_discounted_price_zero_discount():
    cart = MagicMock()
    cart.items = [{'price': 20.0, 'quantity': 2}, {'price': 10.0, 'quantity': 1}]
    discount_rate = 0.0
    result = calculate_discounted_price(cart, discount_rate)
    assert result == 50.0


# edge case - print_cart_summary - Test that print_cart_summary handles empty cart gracefully
def test_print_cart_summary_empty_cart(capfd):
    cart = MagicMock()
    cart.items = []
    cart.calculate_total_price = MagicMock(return_value=0.0)
    print_cart_summary(cart)
    captured = capfd.readouterr()
    assert captured.out == "Cart Summary:\nTotal Price: 0.0\n"


# edge case - save_cart_to_db - Test that save_cart_to_db handles cart with no items
def test_save_cart_to_db_empty_cart(mock_dependencies):
    cart = MagicMock()
    cart.items = []
    save_cart_to_db(cart)
    mock_dependencies['mock_add_item_to_cart_db'].assert_not_called()


