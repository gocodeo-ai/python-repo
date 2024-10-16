import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db

@pytest.fixture
def cart():
    return {
        'items': [
            {'item_id': 1, 'quantity': 2, 'price': 20.0},
            {'item_id': 2, 'quantity': 1, 'price': 50.0}
        ]
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

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock:
        yield mock

# happy path - get_item_details_from_db - Test that item details are fetched correctly from the database
def test_get_item_details_from_db(mock_time_sleep):
    result = get_item_details_from_db(3)
    assert result == {'name': 'Item 3', 'price': 10.0, 'categordy': 'general'}
    mock_time_sleep.assert_called_once_with(1)


# happy path - calculate_discounted_price - Test that discounted price is calculated correctly for the cart
def test_calculate_discounted_price(cart):
    cart['items'] = [{'price': 100.0, 'quantity': 2}, {'price': 50.0, 'quantity': 1}]
    result = calculate_discounted_price(cart, 0.1)
    expected = 225.0
    assert result == expected


# happy path - print_cart_summary - Test that cart summary is printed correctly
def test_print_cart_summary(cart, mock_print):
    cart['items'] = [
        {'name': 'Item A', 'category': 'electronics', 'quantity': 1, 'price': 100.0},
        {'name': 'Item B', 'category': 'books', 'quantity': 2, 'price': 15.0}
    ]
    print_cart_summary(cart)
    expected_calls = [
        ('Cart Summary:',),
        ('Item: Item A, Category: electronics, Quantity: 1, Price: 100.0',),
        ('Item: Item B, Category: books, Quantity: 2, Price: 15.0',),
        ('Total Price: 130.0',)
    ]
    mock_print.assert_has_calls(expected_calls, any_order=False)


# happy path - save_cart_to_db - Test that cart items are saved to the database correctly
def test_save_cart_to_db(cart, mock_add_item_to_cart_db):
    save_cart_to_db(cart)
    expected_calls = [
        (f"INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 20.0)",),
        (f"INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 50.0)",)
    ]
    mock_add_item_to_cart_db.assert_has_calls(expected_calls, any_order=False)


# edge case - get_all_items_from_cart - Test that empty cart returns an empty list of items
def test_get_all_items_from_cart_empty():
    cart = {'items': []}
    result = get_all_items_from_cart(cart)
    assert result == []


# edge case - get_item_details_from_db - Test that invalid item ID returns default item details
def test_get_item_details_from_db_invalid(mock_time_sleep):
    result = get_item_details_from_db(-1)
    expected = {'name': 'Item -1', 'price': 10.0, 'category': 'general'}
    assert result == expected
    mock_time_sleep.assert_called_once_with(1)


# edge case - calculate_discounted_price - Test that zero discount rate returns the original total price
def test_calculate_discounted_price_no_discount(cart):
    cart['items'] = [{'price': 100.0, 'quantity': 1}, {'price': 50.0, 'quantity': 1}]
    result = calculate_discounted_price(cart, 0.0)
    expected = 150.0
    assert result == expected


# edge case - print_cart_summary - Test that cart summary with no items prints correctly
def test_print_cart_summary_empty(mock_print):
    cart = {'items': []}
    print_cart_summary(cart)
    expected_calls = [
        ('Cart Summary:',),
        ('Total Price: 0.0',)
    ]
    mock_print.assert_has_calls(expected_calls, any_order=False)


# edge case - save_cart_to_db - Test that saving an empty cart to the database makes no DB calls
def test_save_cart_to_db_empty(mock_add_item_to_cart_db):
    cart = {'items': []}
    save_cart_to_db(cart)
    mock_add_item_to_cart_db.assert_not_called()


# happy path - get_all_items_from_cart - Generate test cases on fetching all items from a cart with multiple items scenario.
def test_get_all_items_from_cart_multiple(cart, mock_get_item_details_from_db):
    result = get_all_items_from_cart(cart)
    expected = [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]
    assert result == expected
    assert mock_get_item_details_from_db.call_count == 2


# happy path - calculate_discounted_price - Generate test cases on calculating discounted price with a 50% discount scenario.
def test_calculate_discounted_price_half_discount(cart):
    cart['items'] = [{'price': 200.0, 'quantity': 1}, {'price': 100.0, 'quantity': 2}]
    result = calculate_discounted_price(cart, 0.5)
    expected = 200.0
    assert result == expected


# happy path - print_cart_summary - Generate test cases on printing cart summary with varied item categories scenario.
def test_print_cart_summary_varied_categories(cart, mock_print):
    cart['items'] = [
        {'name': 'Item A', 'category': 'electronics', 'quantity': 1, 'price': 100.0},
        {'name': 'Item B', 'category': 'clothing', 'quantity': 2, 'price': 25.0}
    ]
    print_cart_summary(cart)
    expected_calls = [
        ('Cart Summary:',),
        ('Item: Item A, Category: electronics, Quantity: 1, Price: 100.0',),
        ('Item: Item B, Category: clothing, Quantity: 2, Price: 25.0',),
        ('Total Price: 150.0',)
    ]
    mock_print.assert_has_calls(expected_calls, any_order=False)


# happy path - save_cart_to_db - Generate test cases on saving a cart with multiple items to the database scenario.
def test_save_cart_to_db_multiple(cart, mock_add_item_to_cart_db):
    cart['items'] = [{'item_id': 1, 'quantity': 3, 'price': 15.0}, {'item_id': 2, 'quantity': 1, 'price': 30.0}]
    save_cart_to_db(cart)
    expected_calls = [
        (f"INSERT INTO cart (item_id, quantity, price) VALUES (1, 3, 15.0)",),
        (f"INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 30.0)",)
    ]
    mock_add_item_to_cart_db.assert_has_calls(expected_calls, any_order=False)


