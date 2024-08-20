import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        cart = Cart(user_type='')
        yield cart, mock_add_item_to_cart_db# happy_path - update_item_quantity - Test updating the quantity of an existing item
def test_update_item_quantity_valid(cart):
    cart[0].add_item(1, 5, 10.0, 'Apple', 'Fruits', 'regular')
    cart[0].update_item_quantity(1, 5)
    assert cart[0].items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# edge_case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart):
    cart[0].add_item(2, 0, 10.0, 'Banana', 'Fruits', 'regular')
    assert cart[0].items == []

# edge_case - remove_item - Test removing a non-existing item from the cart
def test_remove_item_non_existing(cart):
    cart[0].remove_item(99)
    assert cart[0].items == []

# edge_case - update_item_quantity - Test updating quantity of an item not in the cart
def test_update_item_quantity_non_existing(cart):
    cart[0].update_item_quantity(99, 3)
    assert cart[0].items == []

# edge_case - calculate_total_price - Test calculating total price with an empty cart
def test_calculate_total_price_empty_cart(cart):
    total_price = cart[0].calculate_total_price()
    assert total_price == 0.0

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart):
    cart[0].empty_cart()
    assert cart[0].items == []

