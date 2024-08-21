import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from your_module import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db

# happy_path - add_item - Test adding a valid item to the cart.
def test_add_item_valid(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0] == {'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - remove_item - Test removing an existing item from the cart.
def test_remove_item_existing(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.remove_item(item_id=1)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")

# happy_path - update_item_quantity - Test updating the quantity of an existing item.
def test_update_item_quantity_valid(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")

# happy_path - calculate_total_price - Test calculating total price with multiple items.
def test_calculate_total_price_multiple_items(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.add_item(item_id=2, quantity=3, price=5.0, name='Banana', category='Fruits', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 50.0

# happy_path - list_items - Test listing items in the cart.
def test_list_items(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.list_items()  # This will print the item
    assert len(cart.items) == 1
    assert cart.items[0]['name'] == 'Apple'

# happy_path - empty_cart - Test emptying the cart.
def test_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")

# edge_case - add_item - Test adding an item with zero quantity.
def test_add_item_zero_quantity(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=2, quantity=0, price=10.0, name='Banana', category='Fruits', user_type='regular')
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - remove_item - Test removing an item that does not exist.
def test_remove_item_non_existing(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.remove_item(item_id=999)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 999")

# edge_case - update_item_quantity - Test updating quantity of an item that does not exist.
def test_update_item_quantity_non_existing(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.update_item_quantity(item_id=999, new_quantity=3)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - calculate_total_price - Test calculating total price with an empty cart.
def test_calculate_total_price_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - empty_cart - Test emptying an already empty cart.
def test_empty_cart_already_empty(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")

# edge_case - add_item - Test adding an item with negative price.
def test_add_item_negative_price(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=3, quantity=1, price=-5.0, name='Orange', category='Fruits', user_type='regular')
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_not_called()

