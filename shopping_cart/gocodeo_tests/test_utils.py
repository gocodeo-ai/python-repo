import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db
from shopping_cart.database import add_item_to_cart_db

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

# happy path - get_all_items_from_cart - Test that all items are retrieved correctly from a cart with multiple items.
def test_get_all_items_from_cart_multiple_items(cart_with_items, mock_item_details):
    result = get_all_items_from_cart(cart_with_items)
    assert result == [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]


# happy path - get_item_details_from_db - Test that item details are fetched correctly for a valid item_id.
def test_get_item_details_from_db_valid_id(mock_item_details):
    item_details = get_item_details_from_db(1)
    assert item_details == {'name': 'Item 1', 'price': 10.0, 'category': 'general'}


# happy path - calculate_discounted_price - Test that discounted price is calculated correctly with a valid discount rate.
def test_calculate_discounted_price_valid_discount(cart_with_items):
    discounted_price = calculate_discounted_price(cart_with_items, 0.1)
    assert discounted_price == 36.0


# happy path - print_cart_summary - Test that cart summary prints correctly for a cart with multiple items.
def test_print_cart_summary_multiple_items(cart_with_items, capsys):
    cart_with_items.calculate_total_price = lambda: 40.0
    print_cart_summary(cart_with_items)
    captured = capsys.readouterr()
    assert captured.out == "Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 10.0\nItem: Item 2, Category: general, Quantity: 1, Price: 20.0\nTotal Price: 40.0\n"


# happy path - save_cart_to_db - Test that cart items are saved to the database correctly.
def test_save_cart_to_db_multiple_items(cart_with_items, mock_add_item_to_cart_db):
    save_cart_to_db(cart_with_items)
    mock_add_item_to_cart_db.assert_any_call('INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)')
    mock_add_item_to_cart_db.assert_any_call('INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)')


# edge case - get_all_items_from_cart - Test that an empty cart returns an empty list of items.
def test_get_all_items_from_cart_empty(empty_cart, mock_item_details):
    result = get_all_items_from_cart(empty_cart)
    assert result == []


# edge case - get_item_details_from_db - Test that an invalid item_id returns default item details.
def test_get_item_details_from_db_invalid_id(mock_item_details):
    item_details = get_item_details_from_db(999)
    assert item_details == {'name': 'Item 999', 'price': 10.0, 'category': 'general'}


# edge case - calculate_discounted_price - Test that a zero discount rate returns the total price without discount.
def test_calculate_discounted_price_zero_discount(cart_with_items):
    discounted_price = calculate_discounted_price(cart_with_items, 0.0)
    assert discounted_price == 40.0


# edge case - print_cart_summary - Test that print_cart_summary handles an empty cart gracefully.
def test_print_cart_summary_empty_cart(empty_cart, capsys):
    empty_cart.calculate_total_price = lambda: 0.0
    print_cart_summary(empty_cart)
    captured = capsys.readouterr()
    assert captured.out == "Cart Summary:\nTotal Price: 0.0\n"


# edge case - save_cart_to_db - Test that save_cart_to_db handles an empty cart without errors.
def test_save_cart_to_db_empty(empty_cart, mock_add_item_to_cart_db):
    save_cart_to_db(empty_cart)
    mock_add_item_to_cart_db.assert_not_called()


