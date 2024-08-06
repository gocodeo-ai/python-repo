import pytest
from unittest.mock import MagicMock
from shopping_cart.discounts import Discount
import json

class Cart:
    def __init__(self, items, user_type="regular"):
        self.items = items
        self.user_type = user_type
        self.total_price = 0

    def calculate_total_price(self):
        total = 0
        for item in self.items:
            total += item["price"] * item["quantity"]
        return total

@pytest.fixture
def cart():
    return Cart(items=[
        {"item_id": 1, "category": "electronics", "price": 100, "quantity": 2},
        {"item_id": 2, "category": "clothes", "price": 50, "quantity": 1},
    ])

@pytest.fixture
def test_data():
    with open("test_data_discount.json", "r") as f:
        return json.load(f)

def test_apply_discount(cart, test_data):
    for data_point in test_data["test_apply_discount"]:
        discount_rate = data_point["discount_rate"]
        min_purchase_amount = data_point["min_purchase_amount"]
        expected_price = data_point["expected_price"]
        discount = Discount(discount_rate, min_purchase_amount)
        cart.total_price = 0  # Reset total price
        assert discount.apply_discount(cart) == expected_price

def test_apply_bulk_discount(cart, test_data):
    for data_point in test_data["test_apply_bulk_discount"]:
        bulk_quantity = data_point["bulk_quantity"]
        bulk_discount_rate = data_point["bulk_discount_rate"]
        expected_prices = data_point["expected_prices"]
        discount = Discount(0.1)
        discount.apply_bulk_discount(cart, bulk_quantity, bulk_discount_rate)
        assert cart.items[0]["price"] == expected_prices[0]
        assert cart.items[1]["price"] == expected_prices[1]

def test_apply_seasonal_discount(cart, test_data):
    for data_point in test_data["test_apply_seasonal_discount"]:
        season = data_point["season"]
        seasonal_discount_rate = data_point["seasonal_discount_rate"]
        expected_price = data_point["expected_price"]
        discount = Discount(0.1)
        cart.total_price = 0  # Reset total price
        assert discount.apply_seasonal_discount(cart, season, seasonal_discount_rate) == expected_price

def test_apply_category_discount(cart, test_data):
    for data_point in test_data["test_apply_category_discount"]:
        category = data_point["category"]
        category_discount_rate = data_point["category_discount_rate"]
        expected_prices = data_point["expected_prices"]
        discount = Discount(0.1)
        discount.apply_category_discount(cart, category, category_discount_rate)
        assert cart.items[0]["price"] == expected_prices[0]
        assert cart.items[1]["price"] == expected_prices[1]

def test_apply_loyalty_discount(cart, test_data):
    for data_point in test_data["test_apply_loyalty_discount"]:
        loyalty_years = data_point["loyalty_years"]
        loyalty_discount_rate = data_point["loyalty_discount_rate"]
        expected_price = data_point["expected_price"]
        cart.user_type = "loyal"  # Set user type to loyal
        discount = Discount(0.1)
        cart.total_price = 0  # Reset total price
        assert discount.apply_loyalty_discount(cart, loyalty_years, loyalty_discount_rate) == expected_price

def test_apply_flash_sale_discount(cart, test_data):
    for data_point in test_data["test_apply_flash_sale_discount"]:
        flash_sale_rate = data_point["flash_sale_rate"]
        items_on_sale = data_point["items_on_sale"]
        expected_prices = data_point["expected_prices"]
        discount = Discount(0.1)
        discount.apply_flash_sale_discount(cart, flash_sale_rate, items_on_sale)
        assert cart.items[0]["price"] == expected_prices[0]
        assert cart.items[1]["price"] == expected_prices[1]