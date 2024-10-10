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

@pytest.fixture
def mock_cart():
    return MagicMock()

@pytest.fixture
def mock_item_details():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock_get_item_details:
        mock_get_item_details.side_effect = lambda item_id: {"name": f"Item {item_id}", "price": 10.0, "category": "general"}
        yield mock_get_item_details

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

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
    return {
        'items': []
    }

# happy path - get_all_items_from_cart - Test that all items are fetched with correct details from the database
def test_get_all_items_from_cart_happy_path(cart_with_items, mock_item_details):
    items = get_all_items_from_cart(cart_with_items)
    assert items == [
        {'name': 'Item 1', 'price': 10.0, 'category': 'general'},
        {'name': 'Item 2', 'price': 10.0, 'category': 'general'}
    ]


# happy path - get_item_details_from_db - Test that item details are correctly fetched from the database
def test_get_item_details_from_db_happy_path(mock_item_details):
    item_details = get_item_details_from_db(1)
    assert item_details == {'name': 'Item 1', 'price': 10.0, 'category': 'general'}


# happy path - calculate_discounted_price - Test that discounted price is calculated correctly for a given discount rate
def test_calculate_discounted_price_happy_path(cart_with_items):
    discounted_price = calculate_discounted_price(cart_with_items, 0.1)
    assert discounted_price == 315.0


# happy path - print_cart_summary - Test that cart summary is printed correctly
def test_print_cart_summary_happy_path(cart_with_items, capsys):
    cart_with_items.calculate_total_price = lambda: 40.0
    print_cart_summary(cart_with_items)
    captured = capsys.readouterr()
    assert captured.out == (
        "Cart Summary:\n"
        "Item: Item 1, Category: general, Quantity: 2, Price: 10.0\n"
        "Item: Item 2, Category: general, Quantity: 1, Price: 20.0\n"
        "Total Price: 40.0\n"
    )


# happy path - save_cart_to_db - Test that cart is saved to the database with correct queries
def test_save_cart_to_db_happy_path(cart_with_items, mock_add_item_to_cart_db):
    save_cart_to_db(cart_with_items)
    mock_add_item_to_cart_db.assert_any_call("INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)")
    mock_add_item_to_cart_db.assert_any_call("INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)")


# edge case - get_all_items_from_cart - Test that empty cart returns empty item list
def test_get_all_items_from_cart_edge_case_empty_cart(empty_cart, mock_item_details):
    items = get_all_items_from_cart(empty_cart)
    assert items == []


# edge case - get_item_details_from_db - Test that non-existing item ID returns default item details
def test_get_item_details_from_db_edge_case_non_existing_id(mock_item_details):
    item_details = get_item_details_from_db(9999)
    assert item_details == {'name': 'Item 9999', 'price': 10.0, 'category': 'general'}


# edge case - calculate_discounted_price - Test that discount rate of 1 results in a total price of zero
def test_calculate_discounted_price_edge_case_full_discount(cart_with_items):
    discounted_price = calculate_discounted_price(cart_with_items, 1.0)
    assert discounted_price == 0.0


# edge case - print_cart_summary - Test that cart summary prints correctly for an empty cart
def test_print_cart_summary_edge_case_empty_cart(empty_cart, capsys):
    empty_cart.calculate_total_price = lambda: 0.0
    print_cart_summary(empty_cart)
    captured = capsys.readouterr()
    assert captured.out == "Cart Summary:\nTotal Price: 0.0\n"


# edge case - save_cart_to_db - Test that saving an empty cart does not generate any queries
def test_save_cart_to_db_edge_case_empty_cart(empty_cart, mock_add_item_to_cart_db):
    save_cart_to_db(empty_cart)
    mock_add_item_to_cart_db.assert_not_called()


