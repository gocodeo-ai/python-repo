import pytest
from unittest.mock import patch
from shopping_cart.database import add_item_to_cart_db
from shopping_cart.cart import Cart, Item

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        cart_instance = Cart(user_type='regular')
        yield cart_instance, mock_db

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def another_item():
    return Item(item_id=2, price=159999999.0, name='Banana', category='Fruit')# happy_path - add_item - Test adding a valid item to the cart
def test_add_item_valid(cart, item):
    cart[0].add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    assert cart[0].items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# happy_path - add_item - Test adding multiple valid items to the cart
def test_add_multiple_items(cart, item, another_item):
    cart[0].add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart[0].add_item(2, 1, 15.0, 'Banana', 'Fruit', 'regular')
    assert cart[0].items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}, {'item_id': 2, 'quantity': 1, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Test calculating total price of items in the cart
def test_calculate_total_price(cart, item, another_item):
    cart[0].add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart[0].add_item(2, 1, 15.0, 'Banana', 'Fruit', 'regular')
    total = cart[0].calculate_total_price()
    assert total == 35.0

# happy_path - list_items - Test listing items in the cart
def test_list_items(cart, item, another_item, capsys):
    cart[0].add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart[0].add_item(2, 1, 15.0, 'Banana', 'Fruit', 'regular')
    cart[0].list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\nItem: Banana, Quantity: 1, Price per unit: 15.0\n'

# happy_path - empty_cart - Test emptying the cart
def test_empty_cart(cart, item, another_item):
    cart[0].add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart[0].empty_cart()
    assert cart[0].items == []

# edge_case - add_item - Test adding an item with a negative quantity
def test_add_item_negative_quantity(cart):
    with pytest.raises(ValueError, match='Quantity cannot be negative'):
        cart[0].add_item(3, -1, 5.0, 'Orange', 'Fruit', 'regular')

# edge_case - remove_item - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item(cart):
    cart[0].add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart[0].add_item(2, 1, 15.0, 'Banana', 'Fruit', 'regular')
    cart[0].remove_item(99)
    assert cart[0].items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}, {'item_id': 2, 'quantity': 1, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]

# edge_case - update_item_quantity - Test updating quantity of an item that does not exist
def test_update_nonexistent_item_quantity(cart):
    with pytest.raises(ValueError, match='Item not found'):
        cart[0].update_item_quantity(99, 5)

# edge_case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart):
    total = cart[0].calculate_total_price()
    assert total == 0.0

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart):
    cart[0].empty_cart()
    assert cart[0].items == []

