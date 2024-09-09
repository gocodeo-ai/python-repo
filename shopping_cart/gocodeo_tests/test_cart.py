import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None
        cart_instance = Cart(user_type='regular')
        yield cart_instance

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

# happy_path - add_item - Test that adding an item to the cart works correctly
def test_add_item_to_cart(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# happy_path - add_item - Test that multiple items can be added to the cart
def test_add_multiple_items_to_cart(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=20.0, name='Banana', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}, {'item_id': 2, 'quantity': 1, 'price': 20.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Test that total price is calculated correctly after adding items
def test_calculate_total_price(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=20.0, name='Banana', category='Fruit', user_type='regular')
    total = cart.calculate_total_price()
    assert total == 30.0

# happy_path - list_items - Test that items can be listed correctly
def test_list_items(cart, capsys):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=20.0, name='Banana', category='Fruit', user_type='regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\nItem: Banana, Quantity: 1, Price per unit: 20.0\n'

# happy_path - empty_cart - Test that the cart can be emptied
def test_empty_cart(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - remove_item - Test that removing an item not in the cart does not change the cart
def test_remove_nonexistent_item(cart, mock_db):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=20.0, name='Banana', category='Fruit', user_type='regular')
    cart.remove_item(item_id=99)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}, {'item_id': 2, 'quantity': 1, 'price': 20.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]

# edge_case - update_item_quantity - Test that updating quantity of an item not in the cart does not change the cart
def test_update_quantity_nonexistent_item(cart):
    cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruit', user_type='regular')
    cart.add_item(item_id=2, quantity=1, price=20.0, name='Banana', category='Fruit', user_type='regular')
    cart.update_item_quantity(item_id=99, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}, {'item_id': 2, 'quantity': 1, 'price': 20.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]

# edge_case - calculate_total_price - Test that calculating total price of an empty cart returns 0
def test_calculate_total_price_empty_cart(cart):
    total = cart.calculate_total_price()
    assert total == 0.0

# edge_case - add_item - Test that adding an item with zero quantity does not add it to the cart
def test_add_item_zero_quantity(cart):
    cart.add_item(item_id=3, quantity=0, price=15.0, name='Orange', category='Fruit', user_type='regular')
    assert cart.items == []

# edge_case - add_item - Test that the cart can handle maximum integer quantity
def test_add_item_max_quantity(cart):
    cart.add_item(item_id=4, quantity=2147483647, price=5.0, name='Grapes', category='Fruit', user_type='regular')
    assert cart.items == [{'item_id': 4, 'quantity': 2147483647, 'price': 5.0, 'name': 'Grapes', 'category': 'Fruit', 'user_type': 'regular'}]

