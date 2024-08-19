import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart = Cart(user_type='regular')
        yield cart# happy_path - add_item - Adding a valid item to the cart
def test_add_item_valid(cart):
    cart.add_item(1, 2, 10, 'Apple', 'Fruits', 'regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Calculating total price of items in the cart
def test_calculate_total_price(cart):
    cart.add_item(1, 2, 10, 'Apple', 'Fruits', 'regular')
    total = cart.calculate_total_price()
    assert total == 20.0

# happy_path - remove_item - Removing an item from the cart
def test_remove_item(cart):
    cart.add_item(1, 2, 10, 'Apple', 'Fruits', 'regular')
    cart.remove_item(1)
    assert cart.items == []

# happy_path - update_item_quantity - Updating the quantity of an item in the cart
def test_update_item_quantity(cart):
    cart.add_item(1, 2, 10, 'Apple', 'Fruits', 'regular')
    cart.update_item_quantity(1, 3)
    assert cart.items == [{'item_id': 1, 'quantity': 3, 'price': 10, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - empty_cart - Emptying the cart
def test_empty_cart(cart):
    cart.add_item(1, 2, 10, 'Apple', 'Fruits', 'regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Adding an item with zero quantity
def test_add_item_zero_quantity(cart):
    cart.add_item(2, 0, 10.0, 'Banana', 'Fruits', 'regular')
    assert cart.items == []

# edge_case - calculate_total_price - Calculating total price with no items in cart
def test_calculate_total_price_empty_cart(cart):
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - remove_item - Removing an item that does not exist in the cart
def test_remove_non_existent_item(cart):
    cart.remove_item(99)
    assert cart.items == []

# edge_case - update_item_quantity - Updating quantity of an item that does not exist
def test_update_quantity_non_existent_item(cart):
    cart.update_item_quantity(99, 5)
    assert cart.items == []

# edge_case - empty_cart - Emptying a cart that is already empty
def test_empty_cart_already_empty(cart):
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Adding an item with negative price
def test_add_item_negative_price(cart):
    cart.add_item(3, 1, -5.0, 'Orange', 'Fruits', 'regular')
    assert cart.items == []

