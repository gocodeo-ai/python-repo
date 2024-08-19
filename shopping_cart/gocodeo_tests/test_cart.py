import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart_instance = Cart(user_type='regular')
        yield cart_instance# happy_path - add_item - Adding an item to the cart successfully.
def test_add_item_success(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# edge_case - add_item - Adding an item with zero quantity.
def test_add_item_zero_quantity(cart):
    cart.add_item(item_id=1, quantity=0, price=10.0, name='Banana', category='Fruits', user_type='regular')
    assert cart.items == []

