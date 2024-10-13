import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart_instance = Cart(user_type='Regular')
        yield cart_instance

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_item_class():
    with patch('shopping_cart.cart.Item') as mock:
        yield mock

@pytest.fixture
def mock_cart_class():
    with patch('shopping_cart.cart.Cart') as mock:
        yield mock

# happy path - add_item - Test that item is added to cart correctly
def test_add_item_happy_path(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='Regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'Regular')")


# happy path - remove_item - Test that item is removed from cart correctly
def test_remove_item_happy_path(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='Regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that item quantity is updated correctly
def test_update_item_quantity_happy_path(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='Regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price_happy_path(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='Regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0


# happy path - list_items - Test that items are listed correctly
def test_list_items_happy_path(cart, capsys):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='Regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'


# happy path - empty_cart - Test that cart is emptied correctly
def test_empty_cart_happy_path(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='Regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


# edge case - add_item - Test adding item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Orange', category='Fruit', user_type='Regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 5.0, 'name': 'Orange', 'category': 'Fruit', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 5.0, 'Orange', 'Fruit', 'Regular')")


# edge case - remove_item - Test removing item not in cart
def test_remove_item_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 99")


# edge case - update_item_quantity - Test updating item quantity to zero
def test_update_item_quantity_to_zero(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='Regular')
    cart.update_item_quantity(item_id=1, new_quantity=0)
    assert cart.items == [{'item_id': 1, 'quantity': 0, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'Regular'}]
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 0 WHERE item_id = 1")


# edge case - calculate_total_price - Test calculating total price with no items
def test_calculate_total_price_no_items(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - list_items - Test listing items in empty cart
def test_list_items_empty_cart(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''


# edge case - empty_cart - Test emptying already empty cart
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


