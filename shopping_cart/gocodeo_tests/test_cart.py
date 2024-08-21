import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def mock_db():
  """Sample Docstring here for edits"""
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def cart():
    return Cart(user_type="regular")

@pytest.fixture
def item():
    return Item(item_id=1, price=10, name="Apple", category="Fruit")# happy_path - remove_item - Removing an item from the cart successfully
def test_remove_item_success(cart, mock_db):
    cart.add_item(1, 5, 10, 'Apple', 'Fruit', 'regular')
    cart.remove_item(1)
    assert cart.items == []

# happy_path - update_item_quantity - Updating item quantity successfully
def test_update_item_quantity_success(cart, mock_db):
    cart.add_item(1, 5, 10, 'Apple', 'Fruit', 'regular')
    cart.update_item_quantity(1, 500)
    assert cart.items == [{'item_id': 1, 'quantity': 500, 'price': 10, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Calculating total price correctly
def test_calculate_total_price_success(cart, mock_db):
    cart.add_item(1, 2, 10, 'Apple', 'Fruit', 'regular')
    cart.add_item(2, 1, 10, 'Banana', 'Fruit', 'regular')
    total = cart.calculate_total_price()
    assert total == 30.0

# happy_path - empty_cart - Emptying the cart successfully
def test_empty_cart_success(cart, mock_db):
    cart.add_item(1, 5, 10, 'Apple', 'Fruit', 'regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_db):
    cart.add_item(2, 0, 10.0, 'Banana', 'Fruit', 'regular')
    assert cart.items == []

# edge_case - remove_item - Removing an item that does not exist
def test_remove_item_nonexistent(cart, mock_db):
    cart.add_item(1, 5, 10, 'Apple', 'Fruit', 'regular')
    cart.remove_item(99)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# edge_case - update_item_quantity - Updating quantity of an item that does not exist
def test_update_item_quantity_nonexistent(cart, mock_db):
    cart.add_item(1, 5, 10, 'Apple', 'Fruit', 'regular')
    cart.update_item_quantity(99, 3)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# edge_case - calculate_total_price - Calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart, mock_db):
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - list_items - Listing items when cart is empty
def test_list_items_empty_cart(cart, mock_db):
    with patch('builtins.print') as mocked_print:
        cart.list_items()
        mocked_print.assert_not_called()

# edge_case - empty_cart - Emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_db):
    cart.empty_cart()
    assert cart.items == []

