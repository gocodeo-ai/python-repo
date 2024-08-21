import pytest
from unittest.mock import patch
from shopping_cart.cart import Cart

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db
```# happy_path - add_item - Test adding an item to the cart successfully
def test_add_item_success(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]

# happy_path - remove_item - Test removing an item from the cart successfully
def test_remove_item_success(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []

# happy_path - update_item_quantity - Test updating item quantity successfully
def test_update_item_quantity_success(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Test calculating total price correctly
def test_calculate_total_price_success(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - list_items - Test listing items in the cart successfully
def test_list_items_success(cart, capsys):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Test Item, Quantity: 2, Price per unit: 10.0\n'

# happy_path - empty_cart - Test emptying the cart successfully
def test_empty_cart_success(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Test Item', category='Test Category', user_type='regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Zero Quantity Item', category='Test Category', user_type='regular')
    assert cart.items == []

# edge_case - remove_item - Test removing an item that does not exist
def test_remove_item_not_exist(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.remove_item(item_id=99)
    assert cart.items == []

# edge_case - update_item_quantity - Test updating quantity of an item that does not exist
def test_update_item_quantity_not_exist(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []

# edge_case - calculate_total_price - Test calculating total price with no items in cart
def test_calculate_total_price_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - list_items - Test listing items when cart is empty
def test_list_items_empty_cart(cart, capsys):
    cart, mock_add_item_to_cart_db = cart
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.empty_cart()
    assert cart.items == []

