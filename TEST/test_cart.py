import pytest
from shopping_cart import Cart, Item
from unittest.mock import MagicMock, patch
import json

# Mock the database interaction 
add_item_to_cart_db = MagicMock()

def load_test_data(filename="test_data_cart.json"):
    """Loads test data from the specified JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

test_data = load_test_data()

# Add item test cases
@pytest.mark.parametrize(
    "item_id, quantity, price, name, category, user_type, expected_items",
    [(data["item_id"], data["quantity"], data["price"], data["name"], data["category"], data["user_type"], 
     [{"item_id": data["item_id"], "quantity": data["quantity"], "price": data["price"], "name": data["name"], "category": data["category"], "user_type": data["user_type"]}] )
     for data in test_data["test_data_add_item"]]
)
def test_add_item(item_id, quantity, price, name, category, user_type, expected_items):
    cart = Cart("Guest")
    cart.add_item(item_id, quantity, price, name, category, user_type)
    assert cart.items == expected_items
    add_item_to_cart_db.assert_called_once_with(f"INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES ({item_id}, {quantity}, {price}, '{name}', '{category}', '{user_type}')")

# Remove item test cases
@pytest.mark.parametrize(
    "item_id, initial_items, expected_items",
    [(data["item_id"], 
     [{"item_id": 1, "quantity": 2, "price": 10.0, "name": "Apple", "category": "Fruit", "user_type": "Guest"}], 
     [{"item_id": 1, "quantity": 2, "price": 10.0, "name": "Apple", "category": "Fruit", "user_type": "Guest"}] if data["item_id"] == 10 
     else [], 
     )
     for data in test_data["test_data_remove_item"]]
)
def test_remove_item(item_id, initial_items, expected_items):
    cart = Cart("Guest")
    cart.items = initial_items
    cart.remove_item(item_id)
    assert cart.items == expected_items
    add_item_to_cart_db.assert_called_once_with(f"DELETE FROM cart WHERE item_id = {item_id}")

# Update item quantity test cases
@pytest.mark.parametrize(
    "item_id, new_quantity, initial_items, expected_items",
    [(data["item_id"], data["new_quantity"], 
     [{"item_id": 1, "quantity": 2, "price": 10.0, "name": "Apple", "category": "Fruit", "user_type": "Guest"}],
     [{"item_id": 1, "quantity": 3, "price": 10.0, "name": "Apple", "category": "Fruit", "user_type": "Guest"}] if data["item_id"] == 1
     else [{"item_id": 1, "quantity": 2, "price": 10.0, "name": "Apple", "category": "Fruit", "user_type": "Guest"}],
     )
     for data in test_data["test_data_update_item_quantity"]]
)
def test_update_item_quantity(item_id, new_quantity, initial_items, expected_items):
    cart = Cart("Guest")
    cart.items = initial_items
    cart.update_item_quantity(item_id, new_quantity)
    assert cart.items == expected_items
    add_item_to_cart_db.assert_called_once_with(f"UPDATE cart SET quantity = {new_quantity} WHERE item_id = {item_id}")

# Calculate total price test cases
@pytest.mark.parametrize(
    "items, expected_total_price",
    [(data["items"], data["expected_total_price"]) for data in test_data["test_data_calculate_total_price"]]
)
def test_calculate_total_price(items, expected_total_price):
    cart = Cart("Guest")
    cart.items = items
    assert cart.calculate_total_price() == expected_total_price

@patch('shopping_cart.database.DatabaseConnection')
def test_empty_cart(mock_connection):
    cart = Cart("Guest")
    cart.items = [{"item_id": 1, "quantity": 2, "price": 10.0, "name": "Apple", "category": "Fruit", "user_type": "Guest"}]
    cart.empty_cart()
    assert cart.items == []
    mock_connection.return_value.execute.assert_called_once_with("DELETE FROM cart", [])