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
    return Item(item_id=1, price=10.0, name='Apple', category='Fruits')

@pytest.fixture
def setup_cart_with_item(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item_id=item.item_id, quantity=2, price=item.price, name=item.name, category=item.category, user_type=cart.user_type)
    return cart# happy_path - add_item - Test adding a valid item to the cart
def test_add_item_valid(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=2, price=10, name='Apple', category='Fruits', user_type='regular')
    assert cart.items == [{'item_id': 2, 'quantity': 2, 'price': 10, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - remove_item - Test removing an existing item from the cart
def test_remove_item_existing(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.remove_item(item_id=1)
    assert setup_cart_with_item.items == []

# happy_path - update_item_quantity - Test updating the quantity of an existing item in the cart
def test_update_item_quantity_valid(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.update_item_quantity(item_id=1, new_quantity=5)
    assert setup_cart_with_item.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Test calculating the total price of items in the cart
def test_calculate_total_price(setup_cart_with_item):
    total = setup_cart_with_item.calculate_total_price()
    assert total == 20.0

# happy_path - list_items - Test listing items in the cart
def test_list_items(setup_cart_with_item, capsys):
    setup_cart_with_item.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - empty_cart - Test emptying the cart
def test_empty_cart(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.empty_cart()
    assert setup_cart_with_item.items == []

# edge_case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruits', user_type='regular')
    assert cart.items == []

# edge_case - remove_item - Test removing an item that does not exist in the cart
def test_remove_item_non_existing(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=99)
    assert cart.items == []

# edge_case - update_item_quantity - Test updating the quantity of an item that does not exist
def test_update_item_quantity_non_existing(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []

# edge_case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart):
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - list_items - Test listing items when the cart is empty
def test_list_items_empty_cart(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []

