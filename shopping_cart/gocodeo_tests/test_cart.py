import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db# happy_path - add_item - Adding an item to the cart with valid parameters.
def test_add_item_valid(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - calculate_total_price - Calculating total price with multiple items.
def test_calculate_total_price_multiple_items(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=3, price=5.0, name='Banana', category='Fruit', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 40.0

# happy_path - list_items - Listing items in the cart.
def test_list_items(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    with patch('builtins.print') as mock_print:
        cart.list_items()
        mock_print.assert_called_once_with('Item: Apple, Quantity: 2, Price per unit: 10.0')

# happy_path - update_item_quantity - Updating item quantity in the cart.
def test_update_item_quantity_valid(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 3, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# happy_path - remove_item - Removing an item from the cart.
def test_remove_item_valid(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []

# happy_path - empty_cart - Emptying the cart.
def test_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Adding an item to the cart with zero quantity.
def test_add_item_zero_quantity(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == []

# edge_case - update_item_quantity - Updating item quantity to zero.
def test_update_item_quantity_zero(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=0)
    assert cart.items == []

# edge_case - remove_item - Removing an item that does not exist in the cart.
def test_remove_item_non_existent(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# edge_case - calculate_total_price - Calculating total price with an empty cart.
def test_calculate_total_price_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - empty_cart - Emptying an already empty cart.
def test_empty_cart_already_empty(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Adding an item with negative price.
def test_add_item_negative_price(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=3, quantity=1, price=-5.0, name='Orange', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 3, 'quantity': 1, 'price': -5.0, 'name': 'Orange', 'category': 'Fruit', 'user_type': 'regular'}]

