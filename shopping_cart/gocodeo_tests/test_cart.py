import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    return Cart(user_type='regular')

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_item_list(cart):
    cart.items = [
        {"item_id": 1, "quantity": 2, "price": 10.0, "name": "Apple", "category": "Fruit", "user_type": "regular"},
        {"item_id": 2, "quantity": 3, "price": 20.0, "name": "Banana", "category": "Fruit", "user_type": "regular"}
    ]

@pytest.fixture
def mock_empty_cart(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart")

# happy path - add_item - Test that an item is added to the cart successfully
def test_add_item_success(cart, mock_add_item_to_cart_db, item):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# happy path - remove_item - Test that an item is removed from the cart successfully
def test_remove_item_success(cart, mock_add_item_to_cart_db, mock_item_list):
    cart.remove_item(1)
    assert cart.items == [{'item_id': 2, 'quantity': 3, 'price': 20.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that the item quantity is updated successfully
def test_update_item_quantity_success(cart, mock_add_item_to_cart_db, mock_item_list):
    cart.update_item_quantity(1, 5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_once_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that the total price is calculated correctly
def test_calculate_total_price_success(cart, mock_item_list):
    total_price = cart.calculate_total_price()
    assert total_price == 80.0


# happy path - empty_cart - Test that the cart is emptied successfully
def test_empty_cart_success(cart, mock_add_item_to_cart_db, mock_item_list):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart")


# edge case - add_item - Test adding item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db, item):
    cart.add_item(item.item_id, 0, item.price, item.name, item.category, cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 0, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 0, 10.0, 'Apple', 'Fruit', 'regular')")


# edge case - remove_item - Test removing an item not in the cart
def test_remove_item_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.remove_item(999)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart WHERE item_id = 999")


# edge case - update_item_quantity - Test updating quantity for an item not in the cart
def test_update_item_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(999, 5)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("UPDATE cart SET quantity = 5 WHERE item_id = 999")


# edge case - calculate_total_price - Test calculating total price with no items
def test_calculate_total_price_no_items(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0


# edge case - empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_once_with("DELETE FROM cart")


