import pytest
from unittest.mock import Mock, patch
from shopping_cart.cart import Cart, Item

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.cart.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def cart():
    return Cart('regular')

@pytest.fixture
def item():
    return Item(1, 10.99, 'Test Item', 'Electronics')

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as mock_cart:
        mock_instance = mock_cart.return_value
        mock_instance.items = []
        mock_instance.user_type = 'regular'
        mock_instance.payment_status = ''
        mock_instance.total_price = 0
        
        def add_item(item_id, quantity, price, name, category, user_type):
            mock_instance.items.append({
                "item_id": item_id,
                "quantity": quantity,
                "price": price,
                "name": name,
                "category": category,
                "user_type": user_type
            })

        def remove_item(item_id):
            mock_instance.items = [item for item in mock_instance.items if item["item_id"] != item_id]

        def update_item_quantity(item_id, new_quantity):
            for item in mock_instance.items:
                if item["item_id"] == item_id:
                    item["quantity"] = new_quantity

        def calculate_total_price():
            total_price = sum(item["price"] * item["quantity"] for item in mock_instance.items)
            mock_instance.total_price = total_price
            return total_price

        def list_items():
            for item in mock_instance.items:
                print(f"Item: {item['name']}, Quantity: {item['quantity']}, Price per unit: {item['price']}")

        def empty_cart():
            mock_instance.items = []

        mock_instance.add_item = Mock(side_effect=add_item)
        mock_instance.remove_item = Mock(side_effect=remove_item)
        mock_instance.update_item_quantity = Mock(side_effect=update_item_quantity)
        mock_instance.calculate_total_price = Mock(side_effect=calculate_total_price)
        mock_instance.list_items = Mock(side_effect=list_items)
        mock_instance.empty_cart = Mock(side_effect=empty_cart)
        
        yield mock_instance

@pytest.fixture
def mock_item():
    with patch('shopping_cart.cart.Item') as mock_item:
        mock_instance = mock_item.return_value
        mock_instance.item_id = 1
        mock_instance.price = 10.99
        mock_instance.name = 'Test Item'
        mock_instance.category = 'Electronics'
        yield mock_instance

# happy path - add_item - Generate test cases on adding an item to the cart successfully
def test_add_item_success(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')
    assert len(mock_cart.items) == 1
    assert mock_cart.items[0]['item_id'] == 1
    assert mock_cart.items[0]['quantity'] == 2
    assert mock_cart.items[0]['price'] == 10.99
    assert mock_cart.items[0]['name'] == 'Test Item'
    assert mock_cart.items[0]['category'] == 'Electronics'
    assert mock_cart.items[0]['user_type'] == 'regular'
    mock_add_item_to_cart_db.assert_called_once()

# happy path - remove_item - Generate test cases on removing an item from the cart successfully
def test_remove_item_success(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')
    mock_cart.remove_item(1)
    assert len(mock_cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 1")

# happy path - update_item_quantity - Generate test cases on updating item quantity successfully
def test_update_item_quantity_success(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')
    mock_cart.update_item_quantity(1, 5)
    assert mock_cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 1")

# happy path - calculate_total_price - Generate test cases on calculating total price correctly
def test_calculate_total_price(mock_cart):
    mock_cart.add_item(1, 2, 10.99, 'Test Item 1', 'Electronics', 'regular')
    mock_cart.add_item(2, 1, 5.99, 'Test Item 2', 'Books', 'regular')
    total_price = mock_cart.calculate_total_price()
    assert total_price == 27.97
    assert mock_cart.total_price == 27.97

# happy path - list_items - Generate test cases on listing items in the cart
def test_list_items(mock_cart, capsys):
    mock_cart.add_item(1, 2, 10.99, 'Test Item 1', 'Electronics', 'regular')
    mock_cart.add_item(2, 1, 5.99, 'Test Item 2', 'Books', 'regular')
    mock_cart.list_items()
    captured = capsys.readouterr()
    assert "Item: Test Item 1, Quantity: 2, Price per unit: 10.99" in captured.out
    assert "Item: Test Item 2, Quantity: 1, Price per unit: 5.99" in captured.out

# happy path - empty_cart - Generate test cases on emptying the cart successfully
def test_empty_cart(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')
    mock_cart.empty_cart()
    assert len(mock_cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")

# edge case - add_item - Generate test cases on adding an item with zero quantity
def test_add_item_zero_quantity(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 0, 10.99, 'Test Item', 'Electronics', 'regular')
    assert len(mock_cart.items) == 1
    assert mock_cart.items[0]['quantity'] == 0
    mock_add_item_to_cart_db.assert_called_once()

# edge case - remove_item - Generate test cases on removing a non-existent item from the cart
def test_remove_nonexistent_item(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')
    mock_cart.remove_item(999)
    assert len(mock_cart.items) == 1
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart WHERE item_id = 999")

# edge case - update_item_quantity - Generate test cases on updating quantity of a non-existent item
def test_update_nonexistent_item_quantity(mock_cart, mock_add_item_to_cart_db):
    mock_cart.add_item(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')
    mock_cart.update_item_quantity(999, 5)
    assert len(mock_cart.items) == 1
    assert mock_cart.items[0]['quantity'] == 2
    mock_add_item_to_cart_db.assert_called_with("UPDATE cart SET quantity = 5 WHERE item_id = 999")

# edge case - calculate_total_price - Generate test cases on calculating total price for an empty cart
def test_calculate_total_price_empty_cart(mock_cart):
    total_price = mock_cart.calculate_total_price()
    assert total_price == 0
    assert mock_cart.total_price == 0

# edge case - list_items - Generate test cases on listing items for an empty cart
def test_list_items_empty_cart(mock_cart, capsys):
    mock_cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == ""

# edge case - empty_cart - Generate test cases on emptying an already empty cart
def test_empty_already_empty_cart(mock_cart, mock_add_item_to_cart_db):
    mock_cart.empty_cart()
    assert len(mock_cart.items) == 0
    mock_add_item_to_cart_db.assert_called_with("DELETE FROM cart")

