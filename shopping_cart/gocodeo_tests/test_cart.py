import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    return Cart(user_type='Regular')

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_x_db:
        yield mock_db

# happy_path - test_remove_item_happy_path - Test that item is removed from cart correctly
def test_remove_item_happy_path(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Orange', 'Fruit', 'Regular')
    cart.remove_item(1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - test_update_item_quantity_happy_path - Test that item quantity is updated correctly
def test_update_item_quantity_happy_path(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'Regular')
    cart.update_item_quantity(1, 5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - test_calculate_total_price_happy_path - Test that total price is calculated correctly
def test_calculate_total_price_happy_path(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'Regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_happy_path - Test that items are listed correctly
def test_list_items_happy_path(cart, capsys):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'Regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - test_empty_cart_happy_path - Test that cart is emptied correctly
def test_empty_cart_happy_path(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'Regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

# edge_case - test_add_item_zero_quantity - Test adding item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(2, 0, 15.0, 'Banana', 'Fruit', 'Premium')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'Premium'}]
    mock_add_item_to_cart_db.assert_called_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 15.0, 'Banana', 'Fruit', 'Premium')")

# edge_case - test_remove_non_existent_item - Test removing non-existent item
def test_remove_non_existent_item(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'Regular')
    cart.remove_item(99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 99')

# edge_case - test_update_quantity_non_existent_item - Test updating quantity of non-existent item
def test_update_quantity_non_existent_item(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'Regular')
    cart.update_item_quantity(99, 3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'Regular'}]

# edge_case - test_calculate_total_price_no_items - Test calculating total price with no items
def test_calculate_total_price_no_items(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when cart is empty
def test_list_items_empty_cart(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - test_empty_cart_already_empty - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

