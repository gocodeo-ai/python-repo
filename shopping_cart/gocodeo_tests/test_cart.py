import pytest
from unittest.mock import patch
from shopping_cart.cart import Cart

@pytest.fixture
def cart():
    with patch('shopping_cart.cart.add_item_to_cart_db') as mock_db:
        cart = Cart(user_type='regular')
        yield cart, mock_db# happy_path - add_item - generate test cases on adding a valid item to the cart
def test_add_item_valid(cart):
    cart, mock_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruits', 'regular')")

# happy_path - remove_item - generate test cases on removing an existing item from the cart
def test_remove_item_existing(cart):
    cart, mock_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 1")

# happy_path - update_item_quantity - generate test cases on updating the quantity of an existing item in the cart
def test_update_item_quantity_existing(cart):
    cart, mock_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")

# happy_path - calculate_total_price - generate test cases on calculating the total price of items in the cart
def test_calculate_total_price(cart):
    cart, mock_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 20.0

# happy_path - list_items - generate test cases on listing items in the cart
def test_list_items(cart):
    cart, mock_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.list_items()  # This will print output, you may want to capture stdout if needed.

# happy_path - empty_cart - generate test cases on emptying the cart
def test_empty_cart(cart):
    cart, mock_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_once_with("DELETE FROM cart")

# edge_case - add_item - generate test cases on adding an item with zero quantity
def test_add_item_zero_quantity(cart):
    cart, mock_db = cart
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruits', user_type='regular')
    assert cart.items == []

# edge_case - remove_item - generate test cases on removing a non-existing item from the cart
def test_remove_item_non_existing(cart):
    cart, mock_db = cart
    cart.remove_item(item_id=999)
    assert cart.items == []
    mock_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 999")

# edge_case - update_item_quantity - generate test cases on updating the quantity of an item that doesn't exist
def test_update_item_quantity_non_existing(cart):
    cart, mock_db = cart
    cart.update_item_quantity(item_id=999, new_quantity=3)
    assert cart.items == []

# edge_case - calculate_total_price - generate test cases on calculating total price with an empty cart
def test_calculate_total_price_empty_cart(cart):
    cart, mock_db = cart
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - list_items - generate test cases on listing items in an empty cart
def test_list_items_empty_cart(cart):
    cart, mock_db = cart
    cart.list_items()  # This will print output, you may want to capture stdout if needed.

# edge_case - empty_cart - generate test cases on emptying an already empty cart
def test_empty_cart_already_empty(cart):
    cart, mock_db = cart
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_once_with("DELETE FROM cart")

