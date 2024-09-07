import pytest
from unittest.mock import Mock, patch
from shopping_cart.cart import Item, Cart
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.cart.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def cart():
    return Cart("Regular")

@pytest.fixture
def item():
    return Item(1, 10.99, "Test Item", "Electronics")

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock_print:
        yield mock_print

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_cart = MockCart.return_value
        mock_cart.items = []
        mock_cart.user_type = "Regular"
        mock_cart.payment_status = ""
        mock_cart.total_price = 0
        
        def add_item(item_id, quantity, price, name, category, user_type):
            mock_cart.items.append({"item_id": item_id, "quantity": quantity, "price": price, "name": name, "category": category, "user_type": user_type})
        
        def remove_item(item_id):
            mock_cart.items = [item for item in mock_cart.items if item["item_id"] != item_id]
        
        def update_item_quantity(item_id, new_quantity):
            for item in mock_cart.items:
                if item["item_id"] == item_id:
                    item["quantity"] = new_quantity
        
        def calculate_total_price():
            total_price = sum(item["price"] * item["quantity"] for item in mock_cart.items)
            mock_cart.total_price = total_price
            return total_price
        
        def list_items():
            for item in mock_cart.items:
                print(f"Item: {item['name']}, Quantity: {item['quantity']}, Price per unit: {item['price']}")
        
        def empty_cart():
            mock_cart.items = []
        
        mock_cart.add_item = add_item
        mock_cart.remove_item = remove_item
        mock_cart.update_item_quantity = update_item_quantity
        mock_cart.calculate_total_price = calculate_total_price
        mock_cart.list_items = list_items
        mock_cart.empty_cart = empty_cart
        
        yield mock_cart

@pytest.fixture
def mock_item():
    with patch('shopping_cart.cart.Item') as MockItem:
        mock_item = MockItem.return_value
        mock_item.item_id = 1
        mock_item.price = 10.99
        mock_item.name = "Test Item"
        mock_item.category = "Electronics"
        yield mock_item

# happy path - add_item - Test adding an item to the cart
def test_add_item_to_cart(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'Regular')
    assert len(mock_cart.items) == 1
    assert mock_cart.items[0] == {'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics', 'user_type': 'Regular'}
    mock_add_item_to_cart_db.assert_called_once()

# happy path - remove_item - Test removing an item from the cart
def test_remove_item_from_cart(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'Regular')
    mock_cart.remove_item(1)
    assert len(mock_cart.items) == 0
    mock_add_item_to_cart_db.assert_called()

# happy path - update_item_quantity - Test updating item quantity in the cart
def test_update_item_quantity(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'Regular')
    mock_cart.update_item_quantity(1, 5)
    assert mock_cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called()

# happy path - calculate_total_price - Test calculating total price of items in the cart
def test_calculate_total_price(mock_cart):
    mock_cart.add_item(1, 2, 10.99, 'Test Item 1', 'Electronics', 'Regular')
    mock_cart.add_item(2, 1, 5.99, 'Test Item 2', 'Books', 'Regular')
    total_price = mock_cart.calculate_total_price()
    assert total_price == 27.97

# happy path - list_items - Test listing items in the cart
def test_list_items(mock_cart, mock_print):
    mock_cart.add_item(1, 2, 10.99, 'Test Item 1', 'Electronics', 'Regular')
    mock_cart.add_item(2, 1, 5.99, 'Test Item 2', 'Books', 'Regular')
    mock_cart.list_items()
    mock_print.assert_any_call('Item: Test Item 1, Quantity: 2, Price per unit: 10.99')
    mock_print.assert_any_call('Item: Test Item 2, Quantity: 1, Price per unit: 5.99')

# happy path - empty_cart - Test emptying the cart
def test_empty_cart(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'Regular')
    mock_cart.empty_cart()
    assert len(mock_cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 0, 10.99, 'Test Item', 'Electronics', 'Regular')
    assert len(mock_cart.items) == 1
    assert mock_cart.items[0]['quantity'] == 0
    mock_add_item_to_cart_db.assert_called_once()

# edge case - remove_item - Test removing a non-existent item
def test_remove_non_existent_item(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'Regular')
    initial_length = len(mock_cart.items)
    mock_cart.remove_item(999)
    assert len(mock_cart.items) == initial_length
    mock_add_item_to_cart_db.assert_called()

# edge case - update_item_quantity - Test updating quantity of a non-existent item
def test_update_non_existent_item_quantity(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'Regular')
    initial_items = mock_cart.items.copy()
    mock_cart.update_item_quantity(999, 5)
    assert mock_cart.items == initial_items
    mock_add_item_to_cart_db.assert_called()

# edge case - calculate_total_price - Test calculating total price for an empty cart
def test_calculate_total_price_empty_cart(mock_cart):
    total_price = mock_cart.calculate_total_price()
    assert total_price == 0

# edge case - list_items - Test listing items for an empty cart
def test_list_items_empty_cart(mock_cart, mock_print):
    mock_cart.list_items()
    mock_print.assert_not_called()

# edge case - empty_cart - Test emptying an already empty cart
def test_empty_already_empty_cart(mock_cart, mock_add_item_to_cart_db):
    mock_cart.empty_cart()
    assert len(mock_cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with('DELETE FROM cart')

