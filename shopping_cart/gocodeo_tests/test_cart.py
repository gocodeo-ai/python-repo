import pytest
from unittest import mock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        yield Cart(user_type='regular'), mock_add_item_to_cart_db

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_database():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

# happy_path - test_add_item - Test that add_item correctly adds an item to the cart and database
def test_add_item(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - test_remove_item - Test that remove_item correctly removes an item from the cart and database
def test_remove_item(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.remove_item(item.item_id)
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - test_update_item_quantity - Test that update_item_quantity correctly updates the item quantity in cart and database
def test_update_item_quantity(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.update_item_quantity(item.item_id, 5)
    assert cart_instance.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - test_calculate_total_price - Test that calculate_total_price correctly calculates the total price of items in cart
def test_calculate_total_price(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    total_price = cart_instance.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items - Test that list_items correctly lists all items in the cart
def test_list_items(cart, item, capsys):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - test_empty_cart - Test that empty_cart correctly empties the cart and database
def test_empty_cart(cart, item):
    cart_instance, mock_db = cart
    cart_instance.add_item(item.item_id, 2, item.price, item.name, item.category, cart_instance.user_type)
    cart_instance.empty_cart()
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart')

# edge_case - test_add_item_zero_quantity - Test that add_item handles adding an item with zero quantity
def test_add_item_zero_quantity(cart):
    cart_instance, mock_db = cart
    cart_instance.add_item(2, 0, 5.0, 'Banana', 'Fruit', 'guest')
    assert cart_instance.items == [{'item_id': 2, 'quantity': 0, 'price': 5.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'guest'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 5.0, 'Banana', 'Fruit', 'guest')")

# edge_case - test_remove_item_not_in_cart - Test that remove_item handles removing an item not present in the cart
def test_remove_item_not_in_cart(cart):
    cart_instance, mock_db = cart
    cart_instance.remove_item(99)
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 99')

# edge_case - test_update_quantity_non_existent_item - Test that update_item_quantity handles updating quantity for a non-existent item
def test_update_quantity_non_existent_item(cart):
    cart_instance, mock_db = cart
    cart_instance.update_item_quantity(99, 3)
    assert cart_instance.items == []
    mock_db.assert_called_with('UPDATE cart SET quantity = 3 WHERE item_id = 99')

# edge_case - test_calculate_total_price_empty_cart - Test that calculate_total_price handles an empty cart
def test_calculate_total_price_empty_cart(cart):
    cart_instance, mock_db = cart
    total_price = cart_instance.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test that list_items handles an empty cart
def test_list_items_empty_cart(cart, capsys):
    cart_instance, mock_db = cart
    cart_instance.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - test_empty_cart_already_empty - Test that empty_cart handles an already empty cart
def test_empty_cart_already_empty(cart):
    cart_instance, mock_db = cart
    cart_instance.empty_cart()
    assert cart_instance.items == []
    mock_db.assert_called_with('DELETE FROM cart')

