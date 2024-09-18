import pytest
from unittest import mock
from shopping_cart.cart import Cart, Item
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    """Fixture to create a Cart instance for testing."""
    return Cart(user_type='regular')

@pytest.fixture
def mock_add_item_to_cart_db():
    """Fixture to mock the add_item_to_cart_db function."""
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def item():
    """Fixture to create an Item instance for testing."""
    return Item(item_id=1, price=10.0, name='Apple', category='Fruit')

@pytest.fixture
def setup_cart_with_item(cart, mock_add_item_to_cart_db, item):
    """Fixture to set up the cart with an item."""
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    return cart

# happy_path - add_item - Test that adding an item to the cart updates the items list and database correctly
def test_add_item(cart, mock_add_item_to_cart_db, item):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 10.0, 'Apple', 'Fruit', 'regular')")

# happy_path - remove_item - Test that removing an item from the cart updates the items list and database correctly
def test_remove_item(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.remove_item(1)
    assert setup_cart_with_item.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - update_item_quantity - Test that updating item quantity changes the quantity and updates the database
def test_update_item_quantity(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.update_item_quantity(1, 5)
    assert setup_cart_with_item.items == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - calculate_total_price - Test that calculating the total price returns the correct sum
def test_calculate_total_price(setup_cart_with_item):
    total_price = setup_cart_with_item.calculate_total_price()
    assert total_price == 20.0

# happy_path - list_items - Test that listing items prints the correct format
def test_list_items(setup_cart_with_item, capsys):
    setup_cart_with_item.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'

# happy_path - empty_cart - Test that emptying the cart clears the items list and database
def test_empty_cart(setup_cart_with_item, mock_add_item_to_cart_db):
    setup_cart_with_item.empty_cart()
    assert setup_cart_with_item.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

# edge_case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_add_item_to_cart_db):
    cart.add_item(2, 0, 5.0, 'Banana', 'Fruit', 'guest')
    assert cart.items == [{'item_id': 2, 'quantity': 0, 'price': 5.0, 'name': 'Banana', 'category': 'Fruit', 'user_type': 'guest'}]
    mock_add_item_to_cart_db.assert_called_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (2, 0, 5.0, 'Banana', 'Fruit', 'guest')")

# edge_case - remove_item - Test removing an item not in the cart
def test_remove_item_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.remove_item(3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 3')

# edge_case - update_item_quantity - Test updating quantity of an item not in the cart
def test_update_item_quantity_not_in_cart(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(4, 3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 3 WHERE item_id = 4')

# edge_case - calculate_total_price - Test calculating total price with no items
def test_calculate_total_price_empty(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0.0

# edge_case - list_items - Test listing items with no items in cart
def test_list_items_empty(cart, capsys):
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ''

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_empty(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

