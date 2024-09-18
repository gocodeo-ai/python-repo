import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item:
        mock_add_item.return_value = None
        cart_instance = Cart(user_type='regular')
        yield cart_instance

@pytest.fixture
def item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def mock_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_db_instance:
        yield mock_db_instance

# happy_path - add_item - Test that add_item adds a valid item to the cart
def test_add_item_valid(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    assert cart.items == [{'item_id': item.item_id, 'quantity': 2, 'price': item.price, 'name': item.name, 'category': item.category, 'user_type': cart.user_type}]

# happy_path - remove_item - Test that remove_item removes an existing item from the cart
def test_remove_item_existing(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.remove_item(item.item_id)
    assert cart.items == []

# happy_path - update_item_quantity - Test that update_item_quantity updates the quantity of an existing item
def test_update_item_quantity_existing(cart, item, mock_db):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    cart.update_item_quantity(item.item_id, 5)
    assert cart.items == [{'item_id': item.item_id, 'quantity': 5, 'price': item.price, 'name': item.name, 'category': item.category, 'user_type': cart.user_type}]

# happy_path - calculate_total_price - Test that calculate_total_price calculates the total price correctly
def test_calculate_total_price_correct(cart, item, mock_db):
    cart.add_item(item.item_id, 5, item.price, item.name, item.category, cart.user_type)
    total_price = cart.calculate_total_price()
    assert total_price == 50.0

# happy_path - list_items - Test that list_items lists all items in the cart
def test_list_items(cart, item, mock_db, capsys):
    cart.add_item(item.item_id, 5, item.price, item.name, item.category, cart.user_type)
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 5, Price per unit: 10.0\n'

# happy_path - empty_cart - Test that empty_cart removes all items from the cart
def test_empty_cart(cart, item, mock_db):
    cart.add_item(item.item_id, 5, item.price, item.name, item.category, cart.user_type)
    cart.empty_cart()
    assert cart.items == []

# edge_case - add_item - Test that add_item handles adding an item with zero quantity
def test_add_item_zero_quantity(cart, item, mock_db):
    cart.add_item(item.item_id, 5, item.price, item.name, item.category, cart.user_type)
    cart.add_item(2, 0, 15.0, 'Banana', 'Fruit', 'regular')
    assert cart.items == [{'item_id': item.item_id, 'quantity': 5, 'price': item.price, 'name': item.name, 'category': item.category, 'user_type': cart.user_type}]

# edge_case - remove_item - Test that remove_item handles removing a non-existent item
def test_remove_item_non_existent(cart, item, mock_db):
    cart.add_item(item.item_id, 5, item.price, item.name, item.category, cart.user_type)
    cart.remove_item(3)
    assert cart.items == [{'item_id': item.item_id, 'quantity': 5, 'price': item.price, 'name': item.name, 'category': item.category, 'user_type': cart.user_type}]

# edge_case - update_item_quantity - Test that update_item_quantity handles updating a non-existent item
def test_update_item_quantity_non_existent(cart, item, mock_db):
    cart.add_item(item.item_id, 5, item.price, item.name, item.category, cart.user_type)
    cart.update_item_quantity(4, 10)
    assert cart.items == [{'item_id': item.item_id, 'quantity': 5, 'price': item.price, 'name': item.name, 'category': item.category, 'user_type': cart.user_type}]

# edge_case - calculate_total_price - Test that calculate_total_price handles an empty cart
def test_calculate_total_price_empty(cart, mock_db):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - list_items - Test that list_items handles an empty cart
def test_list_items_empty(cart, mock_db, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - empty_cart - Test that empty_cart handles an already empty cart
def test_empty_cart_already_empty(cart, mock_db):
    cart.empty_cart()
    assert cart.items == []

