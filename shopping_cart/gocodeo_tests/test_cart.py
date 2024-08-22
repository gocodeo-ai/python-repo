import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def setup_cart():
    with patch('shopping_cart.cart.add_item_to_cart_db', MagicMock()) as mock_add_item_to_cart_db:
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db

# happy_path - add_item - Test adding a valid item to the cart
def test_add_item_valid(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruits', 'regular')")

# happy_path - calculate_total_price - Test calculating total price after adding items
def test_calculate_total_price(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 20.0
    assert cart.total_price == 20.0

# happy_path - remove_item - Test removing an existing item from the cart
def test_remove_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 1")

# happy_path - update_item_quantity - Test updating the quantity of an item in the cart
def test_update_item_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 3, 'price': 10.0, 'name': 'Apple', 'category': 'Fruits', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("UPDATE cart SET quantity = 3 WHERE item_id = 1")

# happy_path - list_items - Test listing items in the cart
def test_list_items(setup_cart, capsys):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# edge_case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.add_item(item_id=2, quantity=0, price=15.0, name='Banana', category='Fruits', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - remove_item - Test removing a non-existent item from the cart
def test_remove_non_existent_item(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.remove_item(item_id=999)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 999")

# edge_case - update_item_quantity - Test updating quantity of a non-existent item
def test_update_non_existent_item_quantity(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.update_item_quantity(item_id=999, new_quantity=5)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - calculate_total_price - Test calculating total price with an empty cart
def test_calculate_total_price_empty_cart(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    total = cart.calculate_total_price()
    assert total == 0.0
    assert cart.total_price == 0.0

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(setup_cart):
    cart, mock_add_item_to_cart_db = setup_cart
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart")

