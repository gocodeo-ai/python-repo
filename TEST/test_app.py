import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.cart import Cart, Item
from shopping_cart.discounts import Discount
from shopping_cart.utils import get_all_items_from_cart
from shopping_cart.database import add_item_to_cart_db
import json

# Load test data from JSON file
with open('test_data_app.json', 'r') as f:
    test_data = json.load(f)

# Mock the database interaction
@patch('shopping_cart.cart.add_item_to_cart_db')
def test_add_item(mock_db, user_type="regular"):
    for data_point in test_data["test_add_item"]:
        item_id = data_point["item_id"]
        quantity = data_point["quantity"]
        price = data_point["price"]
        name = data_point["name"]
        category = data_point["category"]

        cart = Cart(user_type)
        cart.add_item(item_id, quantity, price, name, category, user_type)

        # Assert that the database interaction was called correctly
        mock_db.assert_called_once_with(f"INSERT INTO cart (item_id, quantity, price, name, category, user_type) VALUES ({item_id}, {quantity}, {price}, '{name}', '{category}', '{user_type}')")

        # Assert that the item was added to the cart
        assert len(cart.items) == 1
        assert cart.items[0] == {"item_id": item_id, "quantity": quantity, "price": price, "name": name, "category": category, "user_type": user_type}

@patch('shopping_cart.cart.add_item_to_cart_db')
def test_remove_item(mock_db, user_type="regular"):
    for data_point in test_data["test_remove_item"]:
        item_id = data_point["item_id"]
        quantity = data_point["quantity"]
        price = data_point["price"]
        name = data_point["name"]
        category = data_point["category"]

        cart = Cart(user_type)
        cart.add_item(item_id, quantity, price, name, category, user_type)

        cart.remove_item(item_id)

        # Assert that the database interaction was called correctly
        mock_db.assert_called_once_with(f"DELETE FROM cart WHERE item_id = {item_id}")

        # Assert that the item was removed from the cart
        assert len(cart.items) == 0

@patch('shopping_cart.cart.add_item_to_cart_db')
def test_update_item_quantity(mock_db, user_type="regular"):
    for data_point in test_data["test_update_item_quantity"]:
        item_id = data_point["item_id"]
        quantity = data_point["quantity"]
        price = data_point["price"]
        name = data_point["name"]
        category = data_point["category"]
        new_quantity = data_point["new_quantity"]

        cart = Cart(user_type)
        cart.add_item(item_id, quantity, price, name, category, user_type)

        cart.update_item_quantity(item_id, new_quantity)

        # Assert that the database interaction was called correctly
        mock_db.assert_called_once_with(f"UPDATE cart SET quantity = {new_quantity} WHERE item_id = {item_id}")

        # Assert that the item quantity was updated
        assert cart.items[0]["quantity"] == new_quantity

@patch('shopping_cart.cart.add_item_to_cart_db')
def test_calculate_total_price(mock_db, user_type="regular"):
    for data_point in test_data["test_calculate_total_price"]:
        cart = Cart(user_type)
        cart.items = data_point["cart_items"]

        total_price = cart.calculate_total_price()

        # Assert that the total price is calculated correctly
        assert total_price == data_point["expected_total_price"]

@patch('shopping_cart.utils.get_all_items_from_cart')
def test_get_cart_items(mock_get_all_items_from_cart, user_type="regular"):
    for data_point in test_data["test_get_cart_items"]:
        cart = Cart(user_type)
        mock_get_all_items_from_cart.return_value = data_point["expected_items"]

        items = get_all_items_from_cart(cart)

        # Assert that the mocked function was called with the correct argument
        mock_get_all_items_from_cart.assert_called_once_with(cart)

        # Assert that the correct items were returned
        assert items == data_point["expected_items"]

@pytest.mark.parametrize("discount_rate, min_purchase_amount, expected_total_price", test_data["test_apply_discount_to_cart"])
def test_apply_discount_to_cart(discount_rate, min_purchase_amount, expected_total_price, user_type="regular"):
    cart = Cart(user_type)
    cart.items = [
        {"item_id": 1, "quantity": 2, "price": 10.0, "name": "Item 1", "category": "Category 1", "user_type": "regular"},
        {"item_id": 2, "quantity": 1, "price": 5.0, "name": "Item 2", "category": "Category 2", "user_type": "regular"}
    ]

    discount = Discount(discount_rate, min_purchase_amount)
    discount.apply_discount(cart)

    # Assert that the total price is calculated correctly after applying the discount
    assert cart.total_price == expected_total_price


@patch('shopping_cart.cart.add_item_to_cart_db')
def test_empty_cart(mock_db, user_type="regular"):
    for data_point in test_data["test_empty_cart"]:
        cart = Cart(user_type)
        cart.items = data_point["cart_items"]

        cart.empty_cart()

        # Assert that the database interaction was called correctly
        mock_db.assert_called_once_with("DELETE FROM cart")

        # Assert that the cart is empty
        assert cart.items == []