import pytest
from unittest.mock import patch
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
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')# happy_path - add_item - Test adding a valid item to the cart
def test_add_item_valid(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# happy_path - calculate_total_price - Test calculating total price with multiple items
def test_calculate_total_price_multiple_items(cart):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.add_item(2, 3, 5.0, 'Banana', 'Fruit', 'regular')
    assert cart.calculate_total_price() == 50.0

# happy_path - remove_item - Test removing an existing item from the cart
def test_remove_item_existing(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.remove_item(1)
    assert cart.items == []

# happy_path - update_item_quantity - Test updating item quantity in the cart
def test_update_item_quantity_valid(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.update_item_quantity(1, 5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]

# happy_path - list_items - Test listing items in the cart
def test_list_items(cart, capsys):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Item: Apple, Quantity: 2, Price per unit: 10.0'

# happy_path - empty_cart - Test emptying the cart
def test_empty_cart(cart, mock_add_item_to_cart_db):
    cart.add_item(1, 2, 10.0, 'Apple', 'Fruit', 'regular')
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(2, 0, 15.0, 'Banana', 'Fruit', 'regular')
    assert cart.items == []

# edge_case - remove_item - Test removing a non-existing item from the cart
def test_remove_item_non_existing(cart, mock_add_item_to_cart_db):
    cart.remove_item(99)
    assert cart.items == []

# edge_case - update_item_quantity - Test updating quantity of a non-existing item
def test_update_item_quantity_non_existing(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(99, 3)
    assert cart.items == []

# edge_case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_no_items(cart):
    assert cart.calculate_total_price() == 0.0

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Test adding an item with negative price
def test_add_item_negative_price(cart, mock_add_item_to_cart_db):
    cart.add_item(3, 1, -5.0, 'Orange', 'Fruit', 'regular')
    assert cart.items == []

