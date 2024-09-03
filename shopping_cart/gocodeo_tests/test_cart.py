import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def cart():
    return Cart(user_type='regular')

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Orange', category='Fruit')

@pytest.fixture
def mock_database_operations():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

# happy_path - add_item - Test that add_item adds a single item to the cart correctly.
def test_add_single_item(cart, mock_database_operations):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_database_operations.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - remove_item - Test that remove_item removes an item from the cart correctly.
def test_remove_item(cart, mock_database_operations):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_database_operations.assert_called_once_with("DELETE FROM cart WHERE item_id = 1")

# happy_path - update_item_quantity - Test that update_item_quantity updates the quantity of an item correctly.
def test_update_item_quantity(cart, mock_database_operations):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_database_operations.assert_called_once_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")

# happy_path - calculate_total_price - Test that calculate_total_price calculates the total price correctly for multiple items.
def test_calculate_total_price(cart):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 3, 'price': 5.0}]
    total_price = cart.calculate_total_price()
    assert total_price == 35.0

# happy_path - list_items - Test that list_items lists all items currently in the cart.
def test_list_items(cart, capsys):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple'}]
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == "Item: Apple, Quantity: 2, Price per unit: 10.0\n"

# happy_path - empty_cart - Test that empty_cart removes all items from the cart.
def test_empty_cart(cart, mock_database_operations):
    cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    cart.empty_cart()
    assert cart.items == []
    mock_database_operations.assert_called_once_with("DELETE FROM cart")

# edge_case - add_item - Test that add_item handles adding an item with zero quantity.
def test_add_item_zero_quantity(cart, mock_database_operations):
    cart.add_item(item_id=1, quantity=0, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 0, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_database_operations.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 0, 10.0, 'Apple', 'Fruit', 'regular')")

# edge_case - remove_item - Test that remove_item does nothing if the item does not exist in the cart.
def test_remove_nonexistent_item(cart, mock_database_operations):
    cart.items = []
    cart.remove_item(item_id=999)
    assert cart.items == []
    mock_database_operations.assert_called_once_with("DELETE FROM cart WHERE item_id = 999")

# edge_case - update_item_quantity - Test that update_item_quantity handles updating a non-existent item gracefully.
def test_update_nonexistent_item_quantity(cart, mock_database_operations):
    cart.items = []
    cart.update_item_quantity(item_id=999, new_quantity=5)
    assert cart.items == []
    mock_database_operations.assert_called_once_with("UPDATE cart SET quantity = 5 WHERE item_id = 999")

# edge_case - calculate_total_price - Test that calculate_total_price returns zero when the cart is empty.
def test_calculate_total_price_empty_cart(cart):
    cart.items = []
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - list_items - Test that list_items outputs nothing when the cart is empty.
def test_list_items_empty_cart(cart, capsys):
    cart.items = []
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == "null"

