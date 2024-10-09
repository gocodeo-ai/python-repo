import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        cart_instance = Cart(user_type='regular')
        yield cart_instance, mock_add_item_to_cart_db

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_add_item_to_cart_db_function():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

# happy path - add_item - Test that an item is added to the cart successfully.
def test_add_item_success(cart, item):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# happy path - remove_item - Test that an item is removed from the cart successfully.
def test_remove_item_success(cart, item):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.remove_item(item.item_id)
    assert cart_instance.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")


# happy path - update_item_quantity - Test that the quantity of an item is updated successfully.
def test_update_item_quantity_success(cart, item):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.update_item_quantity(item.item_id, 5)
    assert cart_instance.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")


# happy path - calculate_total_price - Test that the total price is calculated correctly after adding items.
def test_calculate_total_price(cart, item):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    total_price = cart_instance.calculate_total_price()
    assert total_price == 20.0


# happy path - empty_cart - Test that the cart is emptied successfully.
def test_empty_cart_success(cart, item):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.empty_cart()
    assert cart_instance.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


# edge case - add_item - Test that adding an item with zero quantity does not change the cart.
def test_add_item_zero_quantity(cart):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.add_item(2, 0, 5.0, 'Banana', 'Fruit', 'regular')
    assert cart_instance.items == []
    mock_add_item_to_cart_db.assert_not_called()


# edge case - remove_item - Test that removing an item not in the cart does not affect the cart.
def test_remove_item_not_in_cart(cart, item):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.remove_item(99)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# edge case - update_item_quantity - Test that updating the quantity of an item not in the cart does not affect the cart.
def test_update_quantity_item_not_in_cart(cart, item):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.update_item_quantity(99, 3)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")


# edge case - calculate_total_price - Test that calculating total price for an empty cart returns zero.
def test_calculate_total_price_empty_cart(cart):
    cart_instance, mock_add_item_to_cart_db = cart
    total_price = cart_instance.calculate_total_price()
    assert total_price == 0


# edge case - empty_cart - Test that emptying an already empty cart does not cause errors.
def test_empty_cart_already_empty(cart):
    cart_instance, mock_add_item_to_cart_db = cart
    cart_instance.empty_cart()
    assert cart_instance.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")


