import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart_fixture():
    # Create an instance of Cart
    cart = Cart(user_type='regular')

    # Mock the database function
    with patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        mock_add_item_to_cart_db.return_value = None  # Mock return value
        yield cart, mock_add_item_to_cart_db  # Provide the cart instance and the mock

@pytest.fixture
def item_fixture():
    # Create an instance of Item
    item = Item(item_id=1, price=10.0, name='Apple', category='Fruit')
    return item

# happy_path - test_add_item_regular_user - Test that an item is added to the cart correctly for a regular user
def test_add_item_regular_user(cart_fixture, item_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_fixture.item_id, 2, item_fixture.price, item_fixture.name, item_fixture.category, 'regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - test_remove_item - Test that an item is removed from the cart correctly
def test_remove_item(cart_fixture, item_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_fixture.item_id, 2, item_fixture.price, item_fixture.name, item_fixture.category, 'regular')
    cart.remove_item(item_fixture.item_id)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - test_update_item_quantity - Test that the item quantity is updated correctly in the cart
def test_update_item_quantity(cart_fixture, item_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_fixture.item_id, 2, item_fixture.price, item_fixture.name, item_fixture.category, 'regular')
    cart.update_item_quantity(item_fixture.item_id, 5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - test_calculate_total_price - Test that the total price is calculated correctly
def test_calculate_total_price(cart_fixture, item_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_fixture.item_id, 2, item_fixture.price, item_fixture.name, item_fixture.category, 'regular')
    total_price = cart.calculate_total_price()
    assert total_price == 20.0

# happy_path - test_list_items - Test that all items in the cart are listed correctly
def test_list_items(cart_fixture, item_fixture, capsys):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_fixture.item_id, 2, item_fixture.price, item_fixture.name, item_fixture.category, 'regular')
    cart.list_items()
    captured = capsys.readouterr()
    assert "Item: Apple, Quantity: 2, Price per unit: 10.0" in captured.out

# happy_path - test_empty_cart - Test that the cart is emptied correctly
def test_empty_cart(cart_fixture, item_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_fixture.item_id, 2, item_fixture.price, item_fixture.name, item_fixture.category, 'regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart_fixture, item_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(2, 0, 15.0, 'Banana', 'Fruit', 'regular')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - test_remove_nonexistent_item - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.remove_item(99)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 99')

# edge_case - test_update_item_quantity_to_zero - Test updating the quantity of an item to zero
def test_update_item_quantity_to_zero(cart_fixture, item_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.add_item(item_fixture.item_id, 2, item_fixture.price, item_fixture.name, item_fixture.category, 'regular')
    cart.update_item_quantity(item_fixture.item_id, 0)
    assert cart.items == [{'item_id': 1, 'quantity': 0, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 0 WHERE item_id = 1')

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - test_list_items_empty_cart - Test listing items when cart is empty
def test_list_items_empty_cart(cart_fixture, capsys):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ""

# edge_case - test_empty_already_empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(cart_fixture):
    cart, mock_add_item_to_cart_db = cart_fixture
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

