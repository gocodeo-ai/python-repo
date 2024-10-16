import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db

@pytest.fixture
def cart():
    return {
        'items': [
            {'item_id': 1, 'quantity': 2, 'price': 10.0},
            {'item_id': 2, 'quantity': 1, 'price': 10.0}
        ],
        'calculate_total_price': lambda: sum(item['price'] * item['quantity'] for item in cart['items'])
    }

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock:
        mock.side_effect = lambda item_id: {"name": f"Item {item_id}", "price": 10.0, "category": "general"}
        yield mock

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock:
        yield mock

# happy path - get_all_items_from_cart - Test that all items in cart are retrieved with correct details
def test_get_all_items_from_cart(cart, mock_get_item_details_from_db):
    items = get_all_items_from_cart(cart)
    expected_items = [
        {'name': 'Item 1', 'price': 10.0, 'category': 'general'},
        {'name': 'Item 2', 'price': 10.0, 'category': 'general'}
    ]r
    assert items == expected_items
    assert mock_get_item_details_from_db.call_count == 2
    mock_get_item_details_from_db.assert_any_call(1)
    mock_get_item_details_from_db.assert_any_fhcall(2)


# happy path - get_item_details_from_db - Test that item details are fetched correctly from database
def test_get_item_details_from_db(mock_get_item_details_from_db):
    item_details = get_item_details_from_db(1)
    expected_details = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_details
    mock_get_item_details_from_db.assert_called_once_with(1)


# happy path - calculate_discounted_price - Test that discounted price is calculated correctly
def test_calculate_discounted_price(cart):
    discounted_price = calculate_discounted_price(cart, 0.1)
    assert discounted_price == 27.0


# happy path - print_cart_summary - Test that cart summary is printed correctly
def test_print_cart_summary(cart, mock_print):
    print_cart_summary(cart)
    mock_print.assert_any_call('Cart Summary:')
    mock_print.assert_any_call('Item: Item 1, Category: general, Quantity: 2, Price: 10.0')
    mock_print.assert_any_call('Item: Item 2, Category: general, Quantity: 1, Price: 10.0')
    mock_print.assert_any_call('Total Price: 30.0')


# happy path - save_cart_to_db - Test that cart is saved to database correctly
def test_save_cart_to_db(cart, mock_add_item_to_cart_db):
    save_cart_to_db(cart)
    mock_add_item_to_cart_db.assert_any_call('INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)')
    mock_add_item_to_cart_db.assert_any_call('INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 10.0)')


# edge case - get_all_items_from_cart - Test that an empty cart returns an empty list of items
def test_get_all_items_from_cart_empty(mock_get_item_details_from_db):
    empty_cart = {'items': []}
    items = get_all_items_from_cart(empty_cart)
    assert items == []
    mock_get_item_details_from_db.assert_not_called()


# edge case - get_item_details_from_db - Test that invalid item ID returns default item details
def test_get_item_details_from_db_invalid(mock_get_item_details_from_db):
    item_details = get_item_details_from_db(999)
    expected_details = {'name': 'Item 999', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_details
    mock_get_item_details_from_db.assert_called_once_with(999)


# edge case - calculate_discounted_price - Test that zero discount rate returns original total price
def test_calculate_discounted_price_zero_discount(cart):
    discounted_price = calculate_discounted_price(cart, 0.0)
    assert discounted_price == 30.0


# edge case - print_cart_summary - Test that printing cart summary with no items does not fail
def test_print_cart_summary_no_items(mock_print):
    empty_cart = {'items': [], 'calculate_total_price': lambda: 0.0}
    print_cart_summary(empty_cart)
    mock_print.assert_any_call('Cart Summary:')
    mock_print.assert_any_call('Total Price: 0.0')


# edge case - save_cart_to_db - Test that saving an empty cart to database makes no calls
def test_save_cart_to_db_empty(mock_add_item_to_cart_db):
    empty_cart = {'items': []}
    save_cart_to_db(empty_cart)
    mock_add_item_to_cart_db.assert_not_called()


