import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db

@pytest.fixture
def mock_cart():
    return MagicMock()

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock:
        yield mock

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_print_function(monkeypatch):
    mock_print = MagicMock()
    monkeypatch.setattr("builtins.print", mock_print)
    return mock_print

@pytest.fixture
def cart_with_items():
    return {
        'items': [
            {'item_id': 1, 'quantity': 2, 'price': 10.0},
            {'item_id': 2, 'quantity': 1, 'price': 15.0}
        ]
    }

@pytest.fixture
def empty_cart():
    return {'items': []}

# happy path - get_all_items_from_cart - Test that all items are retrieved from the cart with correct details
def test_get_all_items_from_cart(cart_with_items, mock_get_item_details_from_db):
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}
    all_items = get_all_items_from_cart(cart_with_items)
    expected_result = [
        {'name': 'Item 1', 'price': 10.0, 'category': 'general'},
        {'name': 'Item 2', 'price': 10.0, 'category': 'general'}
    ]
    assert all_items == expected_result


# happy path - get_item_details_from_db - Test that item details are fetched correctly from the database
def test_get_item_details_from_db():
    item_details = get_item_details_from_db(1)
    expected_result = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_result


# happy path - calculate_discounted_price - Test that discounted price is calculated correctly for the cart
def test_calculate_discounted_price(cart_with_items):
    discounted_price = calculate_discounted_price(cart_with_items, 0.1)
    expected_result = 180.0
    assert discounted_price == expected_result


# happy path - print_cart_summary - Test that cart summary is printed correctly
def test_print_cart_summary(cart_with_items, mock_print_function):
    cart_with_items.calculate_total_price.return_value = 20.0
    print_cart_summary(cart_with_items)
    mock_print_function.assert_any_call('Cart Summary:')
    mock_print_function.assert_any_call('Item: Item 1, Category: general, Quantity: 2, Price: 10.0')
    mock_print_function.assert_any_call('Total Price: 20.0')


# happy path - save_cart_to_db - Test that cart items are saved to the database correctly
def test_save_cart_to_db(cart_with_items, mock_add_item_to_cart_db):
    save_cart_to_db(cart_with_items)
    mock_add_item_to_cart_db.assert_any_call('INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)')


# edge case - get_all_items_from_cart - Test that function handles empty cart correctly when retrieving items
def test_get_all_items_from_cart_empty(empty_cart, mock_get_item_details_from_db):
    all_items = get_all_items_from_cart(empty_cart)
    expected_result = []
    assert all_items == expected_result


# edge case - get_item_details_from_db - Test that function handles invalid item_id gracefully
def test_get_item_details_from_db_invalid_id():
    item_details = get_item_details_from_db(999)
    expected_result = {'name': 'Item 999', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_result


# edge case - calculate_discounted_price - Test that function handles zero discount rate correctly
def test_calculate_discounted_price_zero_discount(cart_with_items):
    discounted_price = calculate_discounted_price(cart_with_items, 0.0)
    expected_result = 100.0
    assert discounted_price == expected_result


# edge case - print_cart_summary - Test that function handles empty cart correctly when printing summary
def test_print_cart_summary_empty(empty_cart, mock_print_function):
    empty_cart.calculate_total_price.return_value = 0.0
    print_cart_summary(empty_cart)
    mock_print_function.assert_any_call('Cart Summary:')
    mock_print_function.assert_any_call('Total Price: 0.0')


# edge case - save_cart_to_db - Test that function handles cart with zero quantity items correctly when saving
def test_save_cart_to_db_zero_quantity(mock_add_item_to_cart_db):
    cart = {'items': [{'item_id': 2, 'quantity': 0, 'price': 10.0}]}
    save_cart_to_db(cart)
    mock_add_item_to_cart_db.assert_any_call('INSERT INTO cart (item_id, quantity, price) VALUES (2, 0, 10.0)')


