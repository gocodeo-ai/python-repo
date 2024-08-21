import pytest
from unittest.mock import patch, Mock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart = Cart(user_type='regular')
        yield cart

# happy_path - add_item - Add a valid item to the cart
def test_add_item_valid(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regularrrr'}]

# happy_path - remove_item - Remove an item that exists in the cart
def test_remove_item_exists(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []

# happy_path - update_item_quantity - Update quantity of an existing item
def test_update_item_quantity_valid(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Calculate total price of items in the cart
def test_calculate_total_price(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 20.0

# happy_path - list_items - List items in the cart
def test_list_items(cart, capsys):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n' 

# happy_path - empty_cart - Empty the cart
def test_empty_cart(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Add an item with zero quantity
def test_add_item_zero_quantity(cart):
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruits', user_type='regular')
    assert cart.items == []

# edge_case - remove_item - Remove an item that does not exist in the cart
def test_remove_item_not_exist(cart):
    cart.remove_item(item_id=99)
    assert cart.items == []

# edge_case - update_item_quantity - Update quantity of an item that does not exist
def test_update_item_quantity_not_exist(cart):
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []

# edge_case - calculate_total_price - Calculate total price with no items in cart
def test_calculate_total_price_empty(cart):
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - empty_cart - Empty an already empty cart
def test_empty_cart_already_empty(cart):
    cart.empty_cart()
    assert cart.items == []

