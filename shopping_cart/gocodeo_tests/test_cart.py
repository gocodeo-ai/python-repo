import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db', autospec=True) as mock_db:
        yield mock_db

@pytest.fixture
def cart():
    return Cart(user_type='Regular')

@pytest.fixture
def mock_item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def populated_cart(cart, mock_item):
    cart.add_item(mock_item.item_id, 2, mock_item.price, mock_item.name, mock_item.category, cart.user_type)
    return cart

@pytest.fixture
def empty_cart(cart):
    cart.empty_cart()
    return cart

# happy_path - test_add_item_success - Test that item is added successfully to the cart with correct details
def test_add_item_success(cart, mock_item, mock_add_item_to_cart_db):
    cart.add_item(mock_item.item_id, 2, mock_item.price, mock_item.name, mock_item.category, cart.user_type)
    assert cart.items == [{'item_id': mock_item.item_id, 'quantity': 2, 'price': mock_item.price, 'name': mock_item.name, 'category': mock_item.category, 'user_type': cart.user_type}]

# happy_path - test_remove_item_success - Test that item is removed successfully from the cart
def test_remove_item_success(populated_cart, mock_add_item_to_cart_db):
    populated_cart.remove_item(1)
    assert populated_cart.items == []

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully in the cart
def test_update_item_quantity_success(populated_cart, mock_add_item_to_cart_db):
    populated_cart.update_item_quantity(1, 5)
    assert populated_cart.items[0]['quantity'] == 5

# happy_path - test_calculate_total_price_success - Test that total price is calculated correctly
def test_calculate_total_price_success(populated_cart):
    total_price = populated_cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items_success - Test that items are listed correctly from the cart
def test_list_items_success(populated_cart, capsys):
    populated_cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - test_empty_cart_success - Test that cart is emptied successfully
def test_empty_cart_success(populated_cart, mock_add_item_to_cart_db):
    populated_cart.empty_cart()
    assert populated_cart.items == []

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity does not add item
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(2, 0, 10.0, 'Banana', 'Fruit', cart.user_type)
    assert cart.items == []

# edge_case - test_remove_item_not_exist - Test removing an item that does not exist in the cart
def test_remove_item_not_exist(cart, mock_add_item_to_cart_db):
    cart.remove_item(99)
    assert cart.items == []

# edge_case - test_update_item_quantity_not_exist - Test updating quantity of an item not in the cart
def test_update_item_quantity_not_exist(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(99, 10)
    assert cart.items == []

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price when cart is empty
def test_calculate_total_price_empty_cart(empty_cart):
    total_price = empty_cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when cart is empty
def test_list_items_empty_cart(empty_cart, capsys):
    empty_cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - test_empty_cart_already_empty - Test emptying an already empty cart
def test_empty_cart_already_empty(empty_cart, mock_add_item_to_cart_db):
    empty_cart.empty_cart()
    assert empty_cart.items == []

