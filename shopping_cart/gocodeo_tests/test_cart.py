import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def setup_cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart = Cart(user_type="regular")
        yield cart, mock_add_item_to_cart_db# happy_path - add_item - Add item to cart successfully
def test_add_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == 1
    assert cart.items[0]['quantity'] == 2
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - remove_item - Remove item from cart successfully
def test_remove_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.remove_item(item_id=1)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - update_item_quantity - Update item quantity in cart successfully
def test_update_item_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - calculate_total_price - Calculate total price of items in cart correctly
def test_calculate_total_price(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=20.0, name='Banana', category='Fruits', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 40.0

# happy_path - list_items - List all items in the cart
def test_list_items(capfd, setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.list_items()
    captured = capfd.readouterr()
    assert 'Item: Apple, Quantity: 2, Price per unit: 10.0' in captured.out

# happy_path - empty_cart - Empty the cart successfully
def test_empty_cart(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

