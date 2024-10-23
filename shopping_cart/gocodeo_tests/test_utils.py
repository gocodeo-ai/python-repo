import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_cart():
    return MagicMock(items=[
        {'item_id': 1, 'quantity': 2, 'price': 10.0},
        {'item_id': 2, 'quantity': 1, 'price': 20.0}
    ])

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
def mock_calculate_total_price():
    with patch.object(mock_cart, 'calculate_total_price', return_value=40.0) as mock:
        yield mock

# happy path - calculate_discounted_price - Test that discounted price is calculated correctly for given cart and discount rate
def test_calculate_discounted_price_applies_discount_correctly(mock_cart):
    discount_rate = 0.1
    discounted_price = calculate_discounted_price(mock_cart, discount_rate)
    expected_price = 225.0
    assert discounted_price == expected_price


# happy path - print_cart_summary - Test that cart summary is printed correctly
def test_print_cart_summary_prints_correctly(mock_cart, mock_calculate_total_price, capsys):
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    expected_output = (
        "Cart Summary:\n"
        "Item: Item 1, Category: general, Quantity: 2, Price: 10.0\n"
        "Item: Item 2, Category: general, Quantity: 1, Price: 20.0\n"
        "Total Price: 40.0\n"
    )
    assert captured.out == expected_output


# happy path - save_cart_to_db - Test that all items in the cart are saved to the database
def test_save_cart_to_db_saves_all_items(mock_cart, mock_add_item_to_cart_db):
    save_cart_to_db(mock_cart)
    mock_add_item_to_cart_db.assert_any_call(
        "INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)"
    )
    mock_add_item_to_cart_db.assert_any_call(
        "INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)"
    )
    assert mock_add_item_to_cart_db.call_count == 2


# edge case - get_all_items_from_cart - Test that empty cart returns empty list for all items
def test_get_all_items_from_cart_with_empty_cart(mock_get_item_details_from_db):
    empty_cart = MagicMock(items=[])
    all_items = get_all_items_from_cart(empty_cart)
    assert all_items == []
    mock_get_item_details_from_db.assert_not_called()


# edge case - calculate_discounted_price - Test that discounted price calculation handles zero discount rate
def test_calculate_discounted_price_with_zero_discount(mock_cart):
    discount_rate = 0.0
    discounted_price = calculate_discounted_price(mock_cart, discount_rate)
    expected_price = 250.0
    assert discounted_price == expected_price


# edge case - print_cart_summary - Test that cart summary handles cart with zero quantity items
def test_print_cart_summary_with_zero_quantity_items(capsys):
    cart_with_zero_quantity = MagicMock(items=[
        {'name': 'Item 1', 'category': 'general', 'quantity': 0, 'price': 10.0},
        {'name': 'Item 2', 'category': 'general', 'quantity': 1, 'price': 20.0}
    ])
    with patch.object(cart_with_zero_quantity, 'calculate_total_price', return_value=20.0):
        print_cart_summary(cart_with_zero_quantity)
    captured = capsys.readouterr()
    expected_output = (
        "Cart Summary:\n"
        "Item: Item 1, Category: general, Quantity: 0, Price: 10.0\n"
        "Item: Item 2, Category: general, Quantity: 1, Price: 20.0\n"
        "Total Price: 20.0\n"
    )
    assert captured.out == expected_output


# edge case - save_cart_to_db - Test that save_cart_to_db handles cart with items having zero quantity
def test_save_cart_to_db_with_zero_quantity_items(mock_add_item_to_cart_db):
    cart_with_zero_quantity = MagicMock(items=[
        {'item_id': 1, 'quantity': 0, 'price': 10.0},
        {'item_id': 2, 'quantity': 1, 'price': 20.0}
    ])
    save_cart_to_db(cart_with_zero_quantity)
    mock_add_item_to_cart_db.assert_called_once_with(
        "INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)"
    )


# edge case - delete_item_from_cart - Test that deleting an item from cart with multiple items updates the cart correctly
def test_delete_item_from_cart_with_multiple_items():
    cart = MagicMock(items=[
        {'item_id': 1, 'quantity': 2, 'price': 10.0},
        {'item_id': 2, 'quantity': 1, 'price': 20.0}
    ])
    item_id_to_delete = 1
    # Assuming delete_item_from_cart is a function to test
    delete_item_from_cart(cart, item_id_to_delete)
    remaining_items = [{'item_id': 2, 'quantity': 1, 'price': 20.0}]
    assert cart.items == remaining_items


# edge case - delete_item_from_cart - Test that deleting an item from cart with a single item results in an empty cart
def test_delete_item_from_cart_with_single_item():
    cart = MagicMock(items=[
        {'item_id': 1, 'quantity': 1, 'price': 10.0}
    ])
    item_id_to_delete = 1
    # Assuming delete_item_from_cart is a function to test
    delete_item_from_cart(cart, item_id_to_delete)
    remaining_items = []
    assert cart.items == remaining_items


# edge case - delete_item_from_cart - Test that deleting a non-existent item from cart does not change the cart
def test_delete_non_existent_item_from_cart():
    cart = MagicMock(items=[
        {'item_id': 1, 'quantity': 1, 'price': 10.0},
        {'item_id': 2, 'quantity': 1, 'price': 20.0}
    ])
    item_id_to_delete = 3
    # Assuming delete_item_from_cart is a function to test
    delete_item_from_cart(cart, item_id_to_delete)
    remaining_items = [
        {'item_id': 1, 'quantity': 1, 'price': 10.0},
        {'item_id': 2, 'quantity': 1, 'price': 20.0}
    ]
    assert cart.items == remaining_items


# edge case - delete_item_from_cart - Test that deleting an item with zero quantity does not affect the cart
def test_delete_item_with_zero_quantity():
    cart = MagicMock(items=[
        {'item_id': 1, 'quantity': 0, 'price': 10.0},
        {'item_id': 2, 'quantity': 1, 'price': 20.0}
    ])
    item_id_to_delete = 1
    # Assuming delete_item_from_cart is a function to test
    delete_item_from_cart(cart, item_id_to_delete)
    remaining_items = [{'item_id': 2, 'quantity': 1, 'price': 20.0}]
    assert cart.items == remaining_items


# edge case - delete_item_from_cart - Test that deleting an item updates the total price correctly
def test_delete_item_updates_total_price():
    cart = MagicMock(items=[
        {'item_id': 1, 'quantity': 1, 'price': 10.0},
        {'item_id': 2, 'quantity': 1, 'price': 20.0}
    ])
    item_id_to_delete = 1
    # Assuming delete_item_from_cart is a function to test
    delete_item_from_cart(cart, item_id_to_delete)
    remaining_items = [{'item_id': 2, 'quantity': 1, 'price': 20.0}]
    total_price = 20.0
    assert cart.items == remaining_items
    assert cart.calculate_total_price() == total_price


