import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def setup_cart():
    with patch('shopping_cart.database.add_item_to_cart_db', MagicMock()) as mock_db:
        cart = Cart(user_type='regular')
        yield cart, mock_db

@pytest.fixture
def setup_cart_with_items():
    with patch('shopping_cart.database.add_item_to_cart_db', MagicMock()) as mock_db:
        cart = Cart(user_type='regular')
        cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
        yield cart, mock_db

# happy_path - test_add_item_success - Test that an item is added to the cart successfully with correct details.
def test_add_item_success(setup_cart):
    cart, mock_db = setup_cart
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - test_remove_item_success - Test that an item is removed from the cart successfully.
def test_remove_item_success(setup_cart_with_items):
    cart, mock_db = setup_cart_with_items
    cart.remove_item(1)
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - test_update_item_quantity_success - Test that the item quantity is updated successfully in the cart.
def test_update_item_quantity_success(setup_cart_with_items):
    cart, mock_db = setup_cart_with_items
    cart.update_item_quantity(1, 5)
    assert cart.items[0]['quantity'] == 5
    mock_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - test_calculate_total_price_success - Test that the total price of the cart is calculated correctly.
def test_calculate_total_price_success(setup_cart_with_items):
    cart, _ = setup_cart_with_items
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_success - Test that the list of items in the cart is displayed correctly.
def test_list_items_success(setup_cart_with_items, capsys):
    cart, _ = setup_cart_with_items
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - test_empty_cart_success - Test that the cart is emptied successfully.
def test_empty_cart_success(setup_cart_with_items):
    cart, mock_db = setup_cart_with_items
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart')

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity is handled correctly.
def test_add_item_zero_quantity(setup_cart_with_items):
    cart, mock_db = setup_cart_with_items
    cart.add_item(2, 0, 15.0, 'Banana', 'Fruit', 'guest')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 15.0, 'Banana', 'Fruit', 'guest')")

# edge_case - test_remove_item_not_in_cart - Test that removing an item not in the cart does not alter the cart.
def test_remove_item_not_in_cart(setup_cart_with_items):
    cart, mock_db = setup_cart_with_items
    cart.remove_item(99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 99')

# edge_case - test_update_item_quantity_not_in_cart - Test that updating the quantity of an item not in the cart does not alter the cart.
def test_update_item_quantity_not_in_cart(setup_cart_with_items):
    cart, mock_db = setup_cart_with_items
    cart.update_item_quantity(99, 3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with('UPDATE cart SET quantity = 3 WHERE item_id = 99')

# edge_case - test_calculate_total_price_empty_cart - Test that calculating total price of an empty cart returns zero.
def test_calculate_total_price_empty_cart(setup_cart):
    cart, _ = setup_cart
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test that listing items in an empty cart returns no output.
def test_list_items_empty_cart(setup_cart, capsys):
    cart, _ = setup_cart
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - test_empty_cart_already_empty - Test that emptying an already empty cart does not cause errors.
def test_empty_cart_already_empty(setup_cart):
    cart, mock_db = setup_cart
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart')

