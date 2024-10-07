import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        mock_db.return_value = None
        cart_instance = Cart(user_type='regular')
        yield cart_instance

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_print(capsys):
    with patch('builtins.print') as mock:
        yield mock, capsys

# happy_path - test_add_item - Test that an item is added to the cart with correct details
def test_add_item(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - test_remove_item - Test that an item is removed from the cart
def test_remove_item(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.remove_item(item.item_id)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")

# happy_path - test_update_item_quantity - Test that the item quantity is updated correctly
def test_update_item_quantity(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.update_item_quantity(item.item_id, 5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")

# happy_path - test_calculate_total_price - Test that the total price is calculated correctly
def test_calculate_total_price(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items - Test that items are listed correctly
def test_list_items(cart, item, mock_print):
    mock, capsys = mock_print
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == "Item: Apple, Quantity: 2, Price per unit: 10.0\n"

# happy_path - test_empty_cart - Test that the cart is emptied correctly
def test_empty_cart(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(2, 0, 15.0, 'Banana', 'Fruit', 'regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 15.0, 'Banana', 'Fruit', 'regular')")

# edge_case - test_remove_item_not_in_cart - Test removing an item not in the cart
def test_remove_item_not_in_cart(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.remove_item(99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 99")

# edge_case - test_update_item_quantity_not_in_cart - Test updating quantity of an item not in the cart
def test_update_item_quantity_not_in_cart(cart, item, mock_add_item_to_cart_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.update_item_quantity(99, 3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 3 WHERE item_id = 99")

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price with no items in cart
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when cart is empty
def test_list_items_empty_cart(cart, mock_print):
    mock, capsys = mock_print
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ""

# edge_case - test_empty_already_empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")

