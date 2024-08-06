import sqlite3
import pytest
from unittest.mock import patch, MagicMock
import json

# Code under test
def add_item_to_cart_db(query):
    """Mock function to represent interaction with the database."""
    pass  # Placeholder for database interaction logic

class ShoppingCart:
    def __init__(self):
        self.items = []

    def list_items(self):
        for item in self.items:
            print(f"Item: {item['name']}, Quantity: {item['quantity']}, Price per unit: {item['price']}")

    def empty_cart(self):
        self.items = []
        query = "DELETE FROM cart"
        add_item_to_cart_db(query)

# Load test data from JSON
with open('test_data_table.json') as f:
    test_data = json.load(f)

# Test cases
@pytest.mark.parametrize("test_case", test_data["test_list_items"])
def test_list_items(test_case, capsys):
    cart = ShoppingCart()
    cart.items = test_case["test_items"]
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == test_case["expected_output"]

@patch('sqlite3.connect')
def test_empty_cart(mock_connect):
    """Tests the empty_cart method, ensuring it clears the cart and calls the database interaction."""
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor

    cart = ShoppingCart()
    cart.items = [{'name': 'Apple', 'quantity': 2, 'price': 1.0}]  # Add some items

    cart.empty_cart()

    assert cart.items == []  # Assert cart is empty
    mock_cursor.execute.assert_called_once_with("DELETE FROM cart")
    mock_connect.return_value.commit.assert_called_once()