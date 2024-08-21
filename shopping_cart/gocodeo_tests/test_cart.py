import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        cart = Cart(user_type="regular")
        yield cart, mock_add_item_to_cart_db

# happy_path - add_item - Add an item to the cart and verify the database call
def test_add_item(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == 1
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - remove_item - Remove an item from the cart and verify the database call
def test_remove_item(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 1")

# happy_path - update_item_quantity - Update the quantity of an item in the cart and verify the database call
def test_update_item_quantity(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_once_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")

# happy_path - calculate_total_price - Calculate total price of items in the cart
def test_calculate_total_price(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=5.0, name='Banana', category='Fruit', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 25.0

# happy_path - list_items - List all items in the cart
def test_list_items(cart, capsys):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=5.0, name='Banana', category='Fruit', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert "Item: Apple, Quantity: 2, Price per unit: 10.0" in captured.out
    assert "Item: Banana, Quantity: 1, Price per unit: 5.0" in captured.out

# happy_path - empty_cart - Empty the cart and verify the database call
def test_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart")

# edge_case - add_item_with_zero_quantity - Attempt to add an item with zero quantity
def test_add_item_with_zero_quantity(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=0, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0]['quantity'] == 0
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 0, 10.0, 'Apple', 'Fruit', 'regular')")

# edge_case - remove_nonexistent_item - Attempt to remove an item that does not exist in the cart
def test_remove_nonexistent_item(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=2)
    assert len(cart.items) == 1
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 2")

# edge_case - update_quantity_of_nonexistent_item - Attempt to update the quantity of an item that does not exist
def test_update_quantity_of_nonexistent_item(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=2, new_quantity=5)
    assert len(cart.items) == 1
    assert cart.items[0]['quantity'] == 2
    mock_add_item_to_cart_db.assert_called_once_with("UPDATE cart SET quantity = 5 WHERE item_id = 2")

# edge_case - calculate_total_price_empty_cart - Calculate total price of an empty cart
def test_calculate_total_price_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    total = cart.calculate_total_price()
    assert total == 0

# edge_case - empty_already_empty_cart - Emptying an already empty cart
def test_empty_already_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart")

