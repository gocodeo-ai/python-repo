import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db

@pytest.fixture
def mock_item():
    with patch('shopping_cart.cart.Item') as mock_item_class:
        mock_item_instance = MagicMock()
        mock_item_class.return_value = mock_item_instance
        yield mock_item_class

@pytest.fixture
def mock_database():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

# happy path - add_item - Test that item is added to cart correctly
def test_add_item_adds_correctly(mock_cart, mock_item):
    cart, mock_db = mock_cart
    cart.add_item(item_id=1, quantity=2, price=100.0, name='Test Item', category='Test Category', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 100.0, 'Test Item', 'Test Category', 'regular')")


# happy path - remove_item - Test that item is removed from cart correctly
def test_remove_item_removes_correctly(mock_cart):
    cart, mock_db = mock_cart
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that item quantity is updated correctly
def test_update_item_quantity_updates_correctly(mock_cart):
    cart, mock_db = mock_cart
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price_correctly(mock_cart):
    cart, _ = mock_cart
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    total_price = cart.calculate_total_price()
    assert total_price == 200.0
    assert cart.total_price == 200.0


# happy path - empty_cart - Test that cart is emptied correctly
def test_empty_cart_empties_correctly(mock_cart):
    cart, mock_db = mock_cart
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_once_with("DELETE FROM cart")


# edge case - add_item - Test adding an item with zero quantity
def test_add_item_with_zero_quantity(mock_cart):
    cart, mock_db = mock_cart
    cart.add_item(item_id=2, quantity=0, price=50.0, name='Zero Quantity Item', category='Test Category', user_type='guest')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 50.0, 'name': 'Zero Quantity Item', 'category': 'Test Category', 'user_type': 'guest'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 50.0, 'Zero Quantity Item', 'Test Category', 'guest')")


# edge case - remove_item - Test removing an item that does not exist
def test_remove_nonexistent_item(mock_cart):
    cart, mock_db = mock_cart
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    cart.remove_item(item_id=99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 99")


# edge case - update_item_quantity - Test updating quantity of an item not in cart
def test_update_quantity_nonexistent_item(mock_cart):
    cart, mock_db = mock_cart
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100.0, 'name': 'Test Item', 'category': 'Test Category', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("UPDATE cart SET quantity = 3 WHERE item_id = 99")


# edge case - calculate_total_price - Test calculating total price of an empty cart
def test_calculate_total_price_empty_cart(mock_cart):
    cart, _ = mock_cart
    total_price = cart.calculate_total_price()
    assert total_price == 0.0
    assert cart.total_price == 0.0


# edge case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(mock_cart):
    cart, mock_db = mock_cart
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_once_with("DELETE FROM cart")


