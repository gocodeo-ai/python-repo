import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.utils import (
    get_all_items_from_cart,
    get_item_details_from_db,
    calculate_discounted_price,
    print_cart_summary,
    save_cart_to_db,
)

@pytest.fixture
def mock_cart():
    return MagicMock()

@pytest.fixture
def mock_item_details():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock:
        mock.side_effect = lambda item_id: {"name": f"Item {item_id}", "price": 10.0, "category": "general"}
        yield mock

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def cart_with_items():
    return {
        'items': [
            {'item_id': 1, 'quantity': 2, 'price': 10.0},
            {'item_id': 2, 'quantity': 1, 'price': 20.0}
        ]
    }

@pytest.fixture
def empty_cart():
    return {'items': []}

@pytest.fixture
def mock_calculate_total_price():
    mock_cart = MagicMock()
    mock_cart.calculate_total_price.return_value = 60.0
    return mock_cart

# happy path - get_all_items_from_cart - Test that all items are retrieved from a cart with multiple items
def test_get_all_items_from_cart_multiple_items(cart_with_items, mock_item_details):
    all_items = get_all_items_from_cart(cart_with_items)
    expected_items = [
        {'name': 'Item 1', 'price': 10.0, 'category': 'general'},
        {'name': 'Item 2', 'price': 10.0, 'category': 'general'}
    ]
    assert all_items == expected_items


# happy path - get_item_details_from_db - Test that item details are retrieved correctly from the database
def test_get_item_details_from_db():
    item_details = get_item_details_from_db(1)
    expected_details = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_details


# happy path - calculate_discounted_price - Test that the discounted price is calculated correctly with a valid discount rate
def test_calculate_discounted_price_valid_discount(cart_with_items):
    discount_rate = 0.1
    discounted_price = calculate_discounted_price(cart_with_items, discount_rate)
    assert discounted_price == 225.0


# happy path - print_cart_summary - Test that cart summary is printed correctly for a cart with multiple items
def test_print_cart_summary_multiple_items(cart_with_items, capsys, mock_calculate_total_price):
    print_cart_summary(mock_calculate_total_price)
    captured = capsys.readouterr()
    expected_output = (
        "Cart Summary:\n"
        "Item: Item 1, Category: general, Quantity: 2, Price: 10.0\n"
        "Item: Item 2, Category: general, Quantity: 1, Price: 20.0\n"
        "Total Price: 60.0\n"
    )
    assert captured.out == expected_output


# happy path - save_cart_to_db - Test that all items in the cart are saved to the database
def test_save_cart_to_db(cart_with_items, mock_add_item_to_cart_db):
    save_cart_to_db(cart_with_items)
    expected_queries = [
        'INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)',
        'INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)'
    ]
    mock_add_item_to_cart_db.assert_has_calls([
        patch.call(expected_queries[0]),
        patch.call(expected_queries[1])
    ])


# edge case - get_all_items_from_cart - Test that an empty cart returns an empty list of items
def test_get_all_items_from_cart_empty(empty_cart, mock_item_details):
    all_items = get_all_items_from_cart(empty_cart)
    assert all_items == []


# edge case - get_item_details_from_db - Test that item details retrieval handles non-existent item ID gracefully
def test_get_item_details_from_db_non_existent_id():
    item_details = get_item_details_from_db(999)
    expected_details = {'name': 'Item 999', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_details


# edge case - calculate_discounted_price - Test that the discounted price calculation handles a 100% discount rate
def test_calculate_discounted_price_full_discount(cart_with_items):
    discount_rate = 1.0
    discounted_price = calculate_discounted_price(cart_with_items, discount_rate)
    assert discounted_price == 0.0


# edge case - print_cart_summary - Test that cart summary prints correctly for an empty cart
def test_print_cart_summary_empty_cart(empty_cart, capsys):
    print_cart_summary(empty_cart)
    captured = capsys.readouterr()
    expected_output = "Cart Summary:\nTotal Price: 0.0\n"
    assert captured.out == expected_output


# edge case - save_cart_to_db - Test that saving an empty cart to the database results in no queries being executed
def test_save_cart_to_db_empty_cart(empty_cart, mock_add_item_to_cart_db):
    save_cart_to_db(empty_cart)
    mock_add_item_to_cart_db.assert_not_called()


