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
    return Cart(user_type='regular')

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruits')# happy_path - add_item - Test adding a valid item to the cart
def test_add_item_valid(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruits', 'regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - remove_item - Test removing an existing item from the cart
def test_remove_item_existing(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruits', 'regular')
    cart.remove_item(1)
    assert cart.items == []

# happy_path - update_item_quantity - Test updating the quantity of an existing item in the cart
def test_update_item_quantity_valid(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruits', 'regular')
    cart.update_item_quantity(1, 3)
    assert cart.items == [{'item_id': 1, 'quantity': 3, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Test calculating the total price of items in the cart
def test_calculate_total_price(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruits', 'regular')
    assert cart.calculate_total_price() == 20.0

# happy_path - list_items - Test listing all items in the cart
def test_list_items(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 3, 10.0, 'Apple', 'Fruits', 'regular')
    cart.list_items()  # This will print the items, you can check manually.

# happy_path - empty_cart - Test emptying the cart
def test_empty_cart(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruits', 'regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Test adding an item with zero quantity to the cart
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(2, 0, 5.0, 'Banana', 'Fruits', 'regular')
    assert cart.items == []

# edge_case - remove_item - Test removing an item that doesn't exist in the cart
def test_remove_item_non_existing(cart, mock_add_item_to_cart_db):
    cart.remove_item(99)
    assert cart.items == []

# edge_case - update_item_quantity - Test updating the quantity of an item that doesn't exist
def test_update_item_quantity_non_existing(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(99, 5)
    assert cart.items == []

# edge_case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart, mock_add_item_to_cart_db):
    assert cart.calculate_total_price() == 0.0

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []

