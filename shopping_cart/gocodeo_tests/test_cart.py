import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db', MagicMock()) as mock_db:
        yield mock_db

@pytest.fixture
def cart():
    return Cart(user_type="regular")

@pytest.fixture
def item():
    return Item(item_id=1, price=100, name="Test Item", category="Test Category")# happy_path - add_item - Add an item to the cart successfully
def test_add_item(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=100, name='Test Item', category='Test Category', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == 1
    assert cart.items[0]['quantity'] == 2
    assert mock_add_item_to_cart_db.called


# happy_path - remove_item - Remove an item from the cart successfully
def test_remove_item(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=100, name='Test Item', category='Test Category', user_type='regular')
    cart.remove_item(item_id=1)
    assert len(cart.items) == 0
    assert mock_add_item_to_cart_db.called


# happy_path - update_item_quantity - Update the quantity of an item in the cart
def test_update_item_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=100, name='Test Item', category='Test Category', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    assert mock_add_item_to_cart_db.called


# happy_path - calculate_total_price - Calculate the total price of items in the cart
def test_calculate_total_price(cart):
    cart.add_item(item_id=1, quantity=2, price=100, name='Test Item', category='Test Category', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 200


# happy_path - list_items - List items in the cart
def test_list_items(cart, capsys):
    cart.add_item(item_id=1, quantity=2, price=100, name='Test Item', category='Test Category', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert 'Item: Test Item, Quantity: 2, Price per unit: 100' in captured.out


# happy_path - empty_cart - Empty the cart successfully
def test_empty_cart(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=100, name='Test Item', category='Test Category', user_type='regular')
    cart.empty_cart()
    assert len(cart.items) == 0
    assert mock_add_item_to_cart_db.called


# edge_case - add_item - Add an item with quantity zero
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=0, price=100, name='Test Item', category='Test Category', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0]['quantity'] == 0
    assert mock_add_item_to_cart_db.called


# edge_case - remove_item - Remove an item that does not exist in the cart
def test_remove_nonexistent_item(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=99)
    assert len(cart.items) == 0
    assert not mock_add_item_to_cart_db.called


# edge_case - update_item_quantity - Update quantity of an item that does not exist
def test_update_quantity_nonexistent_item(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=99, new_quantity=5)
    assert len(cart.items) == 0
    assert not mock_add_item_to_cart_db.called


# edge_case - calculate_total_price - Calculate total price with no items in the cart
def test_calculate_total_price_empty_cart(cart):
    total = cart.calculate_total_price()
    assert total == 0


# edge_case - empty_cart - Empty an already empty cart
def test_empty_already_empty_cart(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert len(cart.items) == 0
    assert mock_add_item_to_cart_db.called


