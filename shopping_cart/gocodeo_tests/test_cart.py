import pytest
from unittest import mock
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    """Fixture to create a Cart instance for testing."""
    return Cart(user_type='regular')

@pytest.fixture
def mock_add_item_to_cart_db():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def mock_item():
    with mock.patch('shopping_cart.cart.Item') as mock_item_class:
        yield mock_item_class

@pytest.fixture
def mock_print(monkeypatch):
    """Mock print to capture printed output."""
    mock_print_func = mock.Mock()
    monkeypatch.setattr("builtins.print", mock_print_func)
    yield mock_print_func

# happy_path - add_item - Test that adding an item to the cart updates the items list and database correctly.
def test_add_item_updates_items_and_db(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=2, price=100, name='Laptop', category='Electronics', user_type='regular')
    assert cart.items == [{'item_id': 1, 'quantity': 2, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_once_with("INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES (1, 2, 100, 'Laptop', 'Electronics', 'regular')")

# happy_path - remove_item - Test that removing an item from the cart updates the items list and database correctly.
def test_remove_item_updates_items_and_db(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=1, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.remove_item(item_id=1)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart WHERE item_id = 1')

# happy_path - update_item_quantity - Test that updating item quantity in the cart updates the items list and database correctly.
def test_update_item_quantity_updates_items_and_db(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=1, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items == [{'item_id': 1, 'quantity': 5, 'price': 100, 'name': 'Laptop', 'category': 'Electronics', 'user_type': 'regular'}]
    mock_add_item_to_cart_db.assert_called_with('UPDATE cart SET quantity = 5 WHERE item_id = 1')

# happy_path - calculate_total_price - Test that calculating total price returns the correct total based on items in the cart.
def test_calculate_total_price_returns_correct_total(cart):
    cart.add_item(item_id=1, quantity=5, price=100, name='Laptop', category='Electronics', user_type='regular')
    total_price = cart.calculate_total_price()
    assert total_price == 500

# happy_path - list_items - Test that listing items prints correct item details.
def test_list_items_prints_correct_details(cart, mock_print):
    cart.add_item(item_id=1, quantity=5, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.list_items()
    mock_print.assert_called_with('Item: Laptop, Quantity: 5, Price per unit: 100')

# happy_path - empty_cart - Test that emptying the cart clears the items list and database correctly.
def test_empty_cart_clears_items_and_db(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=1, quantity=1, price=100, name='Laptop', category='Electronics', user_type='regular')
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

# edge_case - add_item - Test that adding an item with zero quantity does not update the cart or database.
def test_add_item_with_zero_quantity_does_not_update(cart, mock_add_item_to_cart_db):
    cart.add_item(item_id=2, quantity=0, price=50, name='Mouse', category='Electronics', user_type='regular')
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - remove_item - Test that removing an item not in the cart does not affect the cart or database.
def test_remove_nonexistent_item_does_not_update(cart, mock_add_item_to_cart_db):
    cart.remove_item(item_id=999)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - update_item_quantity - Test that updating quantity of an item not in the cart does not affect the cart or database.
def test_update_quantity_of_nonexistent_item_does_not_update(cart, mock_add_item_to_cart_db):
    cart.update_item_quantity(item_id=999, new_quantity=3)
    assert cart.items == []
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - calculate_total_price - Test that calculating total price for an empty cart returns zero.
def test_calculate_total_price_for_empty_cart_returns_zero(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0

# edge_case - list_items - Test that listing items in an empty cart prints nothing.
def test_list_items_for_empty_cart_prints_nothing(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge_case - empty_cart - Test that emptying an already empty cart does not cause errors.
def test_empty_already_empty_cart_does_not_cause_errors(cart, mock_add_item_to_cart_db):
    cart.empty_cart()
    assert cart.items == []
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

