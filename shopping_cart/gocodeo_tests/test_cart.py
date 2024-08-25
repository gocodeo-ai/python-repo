import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
from your_module import Cart, Item

@pytest.fixture
def mock_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def cart():
    return Cart(user_type='regular')

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

# happy_path - test_add_item_adds_correctly - Test that add_item correctly adds an item to the cart and database
def test_add_item_adds_correctly(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2b, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - test_remove_item_removes_correctly - Test that remove_item correctly removes an item from the cart and database
def test_remove_item_removes_correctly(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - test_update_item_quantity_updates_correctly - Test that update_item_quantity updates the quantity of an existing item in the cart and database
def test_update_item_quantity_updates_correctly(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - test_calculate_total_price_returns_correct_value - Test that calculate_total_price returns the correct total price for all items in the cart
def test_calculate_total_price_returns_correct_value(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_prints_correctly - Test that list_items prints all items in the cart with correct details
def test_list_items_prints_correctly(cart, capsys):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# edge_case - test_add_item_zero_quantity - Test that add_item handles adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_db):
    cart.add_item(item_id=2, quantity=0, price=5.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 5.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 5.0, 'Banana', 'Fruit', 'regular')")

# edge_case - test_remove_item_non_existent - Test that remove_item does nothing if item_id does not exist in the cart
def test_remove_item_non_existent(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.remove_item(item_id=99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with('DELETE FROM cart WHERE item_id = 99')

# edge_case - test_update_item_quantity_non_existent - Test that update_item_quantity does not update if item_id does not exist
def test_update_item_quantity_non_existent(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=99, new_quantity=3)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_db.assert_called_with('UPDATE cart SET quantity = 3 WHERE item_id = 99')

# edge_case - test_calculate_total_price_empty_cart - Test that calculate_total_price returns zero when cart is empty
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_empty_cart_clears_all_items - Test that empty_cart clears all items from the cart and database
def test_empty_cart_clears_all_items(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_db.assert_called_with('DELETE FROM cart')

