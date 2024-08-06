from shopping_cart.database import add_item_to_cart_db
import time
import json

def get_all_items_from_cart(cart):
    all_items = []
    for item in cart.items:
        item_details = get_item_details_from_db(item['item_id'])
        all_items.append(item_details)
    return all_items

def get_item_details_from_db(item_id):
    time.sleep(1)
    return {"name": f"Item {item_id}", "price": 10.0, "category": "general"}

def calculate_discounted_price(cart, discount_rate):
    total_price = 0
    for item in cart.items:
        total_price += item["price"] * item["quantity"]
    discounted_price = total_price * (1 - discount_rate)
    return discounted_price

def print_cart_summary(cart):
    print("Cart Summary:")
    for item in cart.items:
        print(f"Item: {item['name']}, Category: {item['category']}, Quantity: {item['quantity']}, Price: {item['price']}")
    print(f"Total Price: {cart.calculate_total_price()}")

def save_cart_to_db(cart):
    for item in cart.items:
        query = f"INSERT INTO cart (item_id, quantity, price) VALUES ({item['item_id']}, {item['quantity']}, {item['price']})"
        add_item_to_cart_db(query)

import io
import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.database import add_item_to_cart_db
import time
from shopping_cart.utils import save_cart_to_db,get_all_items_from_cart,print_cart_summary,calculate_discounted_price


class Cart:
    def __init__(self):
        self.items = [
            {"item_id": 1, "quantity": 2, "price": 10.0},
            {"item_id": 2, "quantity": 1, "price": 20.0}
        ]

    def calculate_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item["price"] * item["quantity"]
        return total_price

# Fixture for creating a cart instance
@pytest.fixture
def cart():
    return Cart()

# Load test data from JSON file
def load_test_data():
    with open("test_data_utils.json", "r") as f:
        return json.load(f)


# Parameterized test for discounted price calculation
@pytest.mark.parametrize("discount_rate, expected_price", load_test_data()["test_calculate_discounted_price"])
def test_calculate_discounted_price(discount_rate, expected_price, cart):
    """Tests calculating discounted price for different discount rates."""
    discounted_price = calculate_discounted_price(cart, discount_rate)
    assert discounted_price == expected_price

# Example cart class for testing


# Example test for print_cart_summary
# @patch("sys.stdout", new_callable=io.StringIO)
# def test_print_cart_summary(mock_stdout, cart):
#     """Tests printing cart summary."""
#     print_cart_summary(cart)
#     expected_output = "Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 10.0\nItem: Item 2, Category: general, Quantity: 1, Price: 20.0\nTotal Price: 40.0"
#     assert mock_stdout.getvalue() == expected_output

