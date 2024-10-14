import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_fixture():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None  # Mock the return value if needed
        cart = Cart(user_type='regular')
        yield cart, mock_add_item_to_cart_db

@pytest.fixture
def item_fixture():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

# happy path - add_item - Test that a new item is added to the cart successfully
def test_add_item_success(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# happy path - remove_item - Test that an item is removed from the cart successfully
def test_remove_item_success(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that the item quantity is updated successfully
def test_update_item_quantity_success(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that the total price is calculated correctly
def test_calculate_total_price_success(cart_fixture):
    cart, _ = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0


# happy path - empty_cart - Test that the cart is emptied successfully
def test_empty_cart_success(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


# edge case - add_item - Test adding an item with zero quantity is handled gracefully
def test_add_item_zero_quantity(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 5.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 5.0, 'Banana', 'Fruit', 'regular')")


# edge case - remove_item - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.remove_item(item_id=99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 99")


# edge case - update_item_quantity - Test updating quantity of an item not in the cart
def test_update_quantity_nonexistent_item(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 3 WHERE item_id = 99")


# edge case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart_fixture):
    cart, _ = cart_fixture
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


