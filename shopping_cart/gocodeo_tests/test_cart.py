import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    return Cart(user_type='regular')

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.cart.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def mock_item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def populated_cart(cart, mock_item):
    cart.add_item(mock_item.item_id, 5, mock_item.price, mock_item.name, mock_item.category, cart.user_type)
    return cart

@pytest.fixture
def empty_cart(cart):
    cart.empty_cart()
    return cart

# happy_path - add_item - Test that an item is added to the cart correctly
def test_add_item_success(cart, mock_add_item_to_cart_db, mock_item):
    cart.add_item(mock_item.item_id, 2, mock_item.price, mock_item.name, mock_item.category, cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - remove_item - Test that an item is removed from the cart correctly
def test_remove_item_success(populated_cart, mock_add_item_to_cart_db):
    populated_cart.remove_item(1)
    assert populated_cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - update_item_quantity - Test that the item quantity is updated correctly in the cart
def test_update_item_quantity_success(populated_cart, mock_add_item_to_cart_db):
    populated_cart.update_item_quantity(1, 5)
    assert populated_cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - calculate_total_price - Test that total price is calculated correctly for items in cart
def test_calculate_total_price_success(populated_cart):
    total_price = populated_cart.calculate_total_price()
    assert total_price == 50.0

# happy_path - list_items - Test that items are listed correctly from the cart
def test_list_items_success(populated_cart, capsys):
    populated_cart.list_items()
    captured = capsys.readouterr()
    assert 'Item: Apple, Quantity: 5, Price per unit: 10.0' in captured.out

# happy_path - empty_cart - Test that the cart is emptied correctly
def test_empty_cart_success(populated_cart, mock_add_item_to_cart_db):
    populated_cart.empty_cart()
    assert populated_cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(populated_cart, mock_add_item_to_cart_db):
    populated_cart.add_item(2, 0, 5.0, 'Banana', 'Fruit', 'regular')
    assert populated_cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - remove_item - Test removing an item not in the cart
def test_remove_item_not_in_cart(populated_cart, mock_add_item_to_cart_db):
    populated_cart.remove_item(99)
    assert populated_cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - update_item_quantity - Test updating quantity of an item not in the cart
def test_update_item_quantity_not_in_cart(populated_cart, mock_add_item_to_cart_db):
    populated_cart.update_item_quantity(99, 3)
    assert populated_cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - calculate_total_price - Test calculating total price with no items in cart
def test_calculate_total_price_empty_cart(empty_cart):
    total_price = empty_cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - list_items - Test listing items when cart is empty
def test_list_items_empty_cart(empty_cart, capsys):
    empty_cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(empty_cart, mock_add_item_to_cart_db):
    empty_cart.empty_cart()
    assert empty_cart.items == []
    mock_add_item_to_cart_db.assert_called_once()

