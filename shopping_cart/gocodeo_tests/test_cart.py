import pytest
from unittest import mock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        cart_instance = Cart(user_type='Regular')
        yield cart_instance, mock_db

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

# happy path - add_item - Test that adding an item to the cart updates the items list and calls the database function.
def test_add_item_updates_cart(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'Regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'Regular')")


# happy path - remove_item - Test that removing an item from the cart updates the items list and calls the database function.
def test_remove_item_updates_cart(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.remove_item(item.item_id)
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')


# happy path - update_item_quantity - Test that updating item quantity in the cart modifies the item and calls the database function.
def test_update_item_quantity(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.update_item_quantity(item.item_id, 5)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'Regular'}]
    mock_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')


# happy path - calculate_total_price - Test that calculating total price returns the correct total and updates the cart's total price.
def test_calculate_total_price(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    total_price = cart_instance.calculate_total_price()
    assert total_price == 20.0
    assert cart_instance.total_price == 20.0


# happy path - list_items - Test that listing items prints the correct item details.
def test_list_items(cart, item, capsys):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'


# happy path - empty_cart - Test that emptying the cart clears the items list and calls the database function.
def test_empty_cart(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.empty_cart()
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart')


# edge case - add_item - Test that adding an item with zero quantity does not add to the cart.
def test_add_item_zero_quantity(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(2, 0, 5.0, 'Banana', 'Fruit', 'Regular')
    assert cart_instance.items == []
    mock_db.assert_not_called()


# edge case - remove_item - Test that removing an item not in the cart does not alter the cart.
def test_remove_nonexistent_item(cart):
    cart_instance, mock_db = cart
    cart_instance.remove_item(99)
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 99')


# edge case - update_item_quantity - Test that updating the quantity of an item not in the cart does not alter the cart.
def test_update_nonexistent_item_quantity(cart):
    cart_instance, mock_db = cart
    cart_instance.update_item_quantity(99, 1)
    assert cart_instance.items == []
    mock_db.assert_called_with('UPDATE cart SET quantity = 1 WHERE item_id = 99')


# edge case - calculate_total_price - Test that calculating total price on an empty cart returns zero.
def test_calculate_total_price_empty_cart(cart):
    cart_instance, mock_db = cart
    total_price = cart_instance.calculate_total_price()
    assert total_price == 0
    assert cart_instance.total_price == 0


# edge case - list_items - Test that listing items on an empty cart does not print any items.
def test_list_items_empty_cart(cart, capsys):
    cart_instance, mock_db = cart
    cart_instance.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''


# edge case - empty_cart - Test that emptying an already empty cart does not cause errors.
def test_empty_already_empty_cart(cart):
    cart_instance, mock_db = cart
    cart_instance.empty_cart()
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart')


