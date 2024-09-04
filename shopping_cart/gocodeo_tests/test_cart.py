import pytest
from unittest.mock import Mock, patch
from shopping_cart.cart import Item, Cart

# Mock the add_item_to_cart_db function
@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def cart():
    return Cart(user_type="Regular")

@pytest.fixture
def item():
    return Item(item_id=1, price=10.99, name="Test Item", category="Electronics")

@pytest.fixture
def mock_database():
    with patch('shopping_cart.database') as mock_db:
        mock_db.add_item_to_cart_db = Mock()
        yield mock_db

@pytest.fixture
def setup_cart(cart, item, mock_database):
    cart.add_item(item.item_id, 2, item.price, item.name, item.category, cart.user_type)
    return cart

@pytest.fixture(autouse=True)
def mock_print(monkeypatch):
    mock_print = Mock()
    monkeypatch.setattr("builtins.print", mock_print)
    return mock_print

# happy path - add_item - Test adding an item to the cart
def test_add_item(cart, mock_database):
    cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'Regular')
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == 1
    assert cart.items[0]['quantity'] == 2
    mock_database.add_item_to_cart_db.assert_called_once()

# happy path - remove_item - Test removing an item from the cart
def test_remove_item(setup_cart, mock_database):
    setup_cart.remove_item(1)
    assert len(setup_cart.items) == 0
    mock_database.add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")

# happy path - update_item_quantity - Test updating item quantity in the cart
def test_update_item_quantity(setup_cart, mock_database):
    setup_cart.update_item_quantity(1, 3)
    assert setup_cart.items[0]['quantity'] == 3
    mock_database.add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 3 WHERE item_id = 1")

# happy path - calculate_total_price - Test calculating total price of items in the cart
def test_calculate_total_price(setup_cart):
    total_price = setup_cart.calculate_total_price()
    assert total_price == 21.98

# happy path - list_items - Test listing items in the cart
def test_list_items(setup_cart, mock_print):
    setup_cart.list_items()
    mock_print.assert_called_with('Item: Test Item, Quantity: 2, Price per unit: 10.99')

# happy path - empty_cart - Test emptying the cart
def test_empty_cart(setup_cart, mock_database):
    setup_cart.empty_cart()
    assert len(setup_cart.items) == 0
    mock_database.add_item_to_cart_db.assert_called_with("DELETE FROM cart")

# happy path - add_item - Test adding an item to the cart successfully
def test_add_item_success(cart, mock_database):
    cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'Regular')
    assert len(cart.items) == 1
    assert cart.items[0]['item_id'] == 1
    assert cart.items[0]['quantity'] == 2
    mock_database.add_item_to_cart_db.assert_called_once()

# happy path - remove_item - Test removing an item from the cart
def test_remove_item(setup_cart, mock_database):
    setup_cart.remove_item(1)
    assert len(setup_cart.items) == 0
    mock_database.add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")

# happy path - update_item_quantity - Test updating item quantity in the cart
def test_update_item_quantity(setup_cart, mock_database):
    setup_cart.update_item_quantity(1, 3)
    assert setup_cart.items[0]['quantity'] == 3
    mock_database.add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 3 WHERE item_id = 1")

# happy path - calculate_total_price - Test calculating total price of items in the cart
def test_calculate_total_price(setup_cart):
    total_price = setup_cart.calculate_total_price()
    assert total_price == 21.98
    assert setup_cart.total_price == 21.98

# happy path - list_items - Test listing items in the cart
def test_list_items(setup_cart, mock_print):
    setup_cart.list_items()
    mock_print.assert_called_with('Item: Test Item, Quantity: 2, Price per unit: 10.99')

# happy path - empty_cart - Test emptying the cart
def test_empty_cart(setup_cart, mock_database):
    setup_cart.empty_cart()
    assert len(setup_cart.items) == 0
    mock_database.add_item_to_cart_db.assert_called_with("DELETE FROM cart")

# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_database):
    cart.add_item(1, 0, 10.99, 'Test Item', 'Electronics', 'Regular')
    assert len(cart.items) == 0
    mock_database.add_item_to_cart_db.assert_not_called()

# edge case - remove_item - Test removing a non-existent item
def test_remove_non_existent_item(cart, mock_database):
    cart.remove_item(999)
    assert len(cart.items) == 0
    mock_database.add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 999")

# edge case - update_item_quantity - Test updating quantity to a negative value
def test_update_quantity_negative(setup_cart, mock_database):
    setup_cart.update_item_quantity(1, -2)
    assert setup_cart.items[0]['quantity'] == -2
    mock_database.add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = -2 WHERE item_id = 1")

# edge case - calculate_total_price - Test calculating total price with an empty cart
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0

# edge case - list_items - Test listing items in an empty cart
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge case - empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(cart, mock_database):
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_database.add_item_to_cart_db.assert_called_with("DELETE FROM cart")

# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(cart, mock_database):
    cart.add_item(1, 0, 10.99, 'Test Item', 'Electronics', 'Regular')
    assert len(cart.items) == 0
    mock_database.add_item_to_cart_db.assert_not_called()

# edge case - remove_item - Test removing a non-existent item from the cart
def test_remove_nonexistent_item(cart, mock_database):
    cart.remove_item(999)
    assert len(cart.items) == 0
    mock_database.add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 999")

# edge case - update_item_quantity - Test updating quantity to a negative value
def test_update_quantity_negative(setup_cart, mock_database):
    setup_cart.update_item_quantity(1, -1)
    assert setup_cart.items[0]['quantity'] == -1
    mock_database.add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = -1 WHERE item_id = 1")

# edge case - calculate_total_price - Test calculating total price with an empty cart
def test_calculate_total_price_empty_cart(cart):
    total_price = cart.calculate_total_price()
    assert total_price == 0
    assert cart.total_price == 0

# edge case - list_items - Test listing items in an empty cart
def test_list_items_empty_cart(cart, mock_print):
    cart.list_items()
    mock_print.assert_not_called()

# edge case - empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(cart, mock_database):
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_database.add_item_to_cart_db.assert_called_with("DELETE FROM cart")

