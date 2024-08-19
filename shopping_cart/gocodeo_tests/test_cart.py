import pytest
from unittest.mock import patch, MagicMock
from shopping_cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def cart():
    return Cart(user_type='regular')

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruits')

@pytest.fixture(autouse=True)
def setup_all_mocks(mock_add_item_to_cart_db):
    pass# happy_path - add_item - Test adding a valid item to the cart
def test_add_item_valid(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - update_item_quantity - Test updating the quantity of an existing item in the cart
def test_update_item_quantity_valid(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Test calculating the total price of items in the cart
def test_calculate_total_price(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 20.0

# happy_path - list_items - Test listing all items in the cart
def test_list_items(cart, capsys):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - empty_cart - Test emptying the cart
def test_empty_cart(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Test adding an item with zero quantity to the cart
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruits', user_type='regular')
    assert cart.items == []

# edge_case - remove_item - Test removing a non-existing item from the cart
def test_remove_item_non_existing(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=99)
    assert cart.items == []

# edge_case - update_item_quantity - Test updating the quantity of a non-existing item
def test_update_item_quantity_non_existing(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []

# edge_case - calculate_total_price - Test calculating total price when cart is empty
def test_calculate_total_price_empty_cart(cart):
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart):
    cart.empty_cart()
    assert cart.items == []

