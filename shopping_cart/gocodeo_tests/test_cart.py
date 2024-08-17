import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def cart():
    return Cart(user_type="regular")

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name="Test Item", category="Test Category")# happy_path - add_item - Add an item to the cart successfully
def test_add_item(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == 1
    assert cart.items[0]['quantity'] == 2
    assert mock_add_item_to_cart_db.call_count == 1


# happy_path - remove_item - Remove an item from the cart successfully
def test_remove_item(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.remove_item(item_id=1)
    assert len(cart.items) == 0
    assert mock_add_item_to_cart_db.call_count == 1


# happy_path - update_item_quantity - Update the quantity of an item in the cart successfully
def test_update_item_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    assert mock_add_item_to_cart_db.call_count == 1


# happy_path - calculate_total_price - Calculate the total price of items in the cart
def test_calculate_total_price(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 20.0


# happy_path - empty_cart - Empty the cart successfully
def test_empty_cart(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.empty_cart()
    assert len(cart.items) == 0
    assert mock_add_item_to_cart_db.call_count == 1


# edge_case - add_item - Add an item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=0, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0]['quantity'] == 0
    assert mock_add_item_to_cart_db.call_count == 1


# edge_case - remove_item - Remove an item that does not exist in the cart
def test_remove_nonexistent_item(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=999)
    assert len(cart.items) == 0
    assert mock_add_item_to_cart_db.call_count == 0


# edge_case - update_item_quantity - Update quantity of a non-existent item
def test_update_quantity_nonexistent_item(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=999, new_quantity=5)
    assert len(cart.items) == 0
    assert mock_add_item_to_cart_db.call_count == 0


