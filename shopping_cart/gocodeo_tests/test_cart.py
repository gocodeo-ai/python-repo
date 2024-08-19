import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        cart = Cart(user_type='guest')
        yield cart, mock_add_item_to_cart_db# happy_path - add_item - Adding a valid item to the cart
def test_add_item_valid(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='guest')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'guest'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - remove_item - Removing an existing item from the cart
def test_remove_item_existing(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='guest')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - update_item_quantity - Updating the quantity of an existing item
def test_update_item_quantity_valid(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='guest')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'guest'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - calculate_total_price - Calculating total price of items in the cart
def test_calculate_total_price(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='guest')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0
    assert cart.total_price == 20.0

# happy_path - list_items - Listing items in the cart
def test_list_items(cart, capsys):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='guest')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n' 

# happy_path - empty_cart - Emptying the cart
def test_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='guest')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - add_item - Adding an item with zero quantity
def test_add_item_zero_quantity(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruits', user_type='guest')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - remove_item - Removing a non-existing item from the cart
def test_remove_item_non_existing(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.remove_item(item_id=999)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - update_item_quantity - Updating quantity of an item that doesn't exist
def test_update_item_quantity_non_existing(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.update_item_quantity(item_id=999, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - calculate_total_price - Calculating total price when cart is empty
def test_calculate_total_price_empty_cart(cart):
    cart, mock_add_item_to_cart_db = cart
    total_price = cart.calculate_total_price()
    assert total_price == 0.0
    assert cart.total_price == 0.0

# edge_case - list_items - Listing items when cart is empty
def test_list_items_empty_cart(cart, capsys):
    cart, mock_add_item_to_cart_db = cart
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - empty_cart - Emptying an already empty cart
def test_empty_cart_already_empty(cart):
    cart, mock_add_item_to_cart_db = cart
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

