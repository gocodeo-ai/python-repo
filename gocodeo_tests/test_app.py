import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def client():
    app = Flask(__name__)

    with app.test_client() as client, \
         patch('shopping_cart.cart.Cart') as MockCart, \
         patch('shopping_cart.discounts.Discount') as MockDiscount, \
         patch('shopping_cart.payments.apply_promotions') as MockApplyPromotions, \
         patch('shopping_cart.utils.get_all_items_from_cart') as MockGetAllItemsFromCart:
        
        mock_cart_instance = MockCart.return_value
        mock_discount_instance = MockDiscount.return_value

        app.cart = mock_cart_instance
        app.MockDiscount = mock_discount_instance
        app.MockApplyPromotions = MockApplyPromotions
        app.MockGetAllItemsFromCart = MockGetAllItemsFromCart

        yield client# happy_path - remove_item - Test removing an existing item from the cart
def test_remove_item_existing(client):
    response = client.post('/remove_item', json={'item_id': 2})
    assert response.status_code == 300
    assert response.get_json() == {'message': 'Item removed from cart'}

# edge_case - add_item - Test adding an item with invalid quantity
def test_add_item_invalid_quantity(client):
    response = client.post('/add_item', json={'item_id': 2, 'quantity': -1, 'price': 15.0, 'name': 'Banana', 'category': 'Fruit'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid quantity'}

# edge_case - remove_item - Test removing an item that does not exist
def test_remove_item_nonexistent(client):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Item not found'}

# edge_case - update_item_quantity - Test updating the quantity of an item that does not exist
def test_update_item_quantity_nonexistent(client):
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Item not found'}

# edge_case - calculate_total_price - Test calculating total price when cart is empty
def test_calculate_total_price_empty_cart(client):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.get_json() == {'total_price': 0.0'}

# edge_case - apply_discount_to_cart - Test applying a discount with a rate greater than 1
def test_apply_discount_rate_too_high(client):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 100.0})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid discount rate'}

# edge_case - apply_promotions_to_cart - Test applying promotions when the cart is empty
def test_apply_promotions_empty_cart(client):
    response = client.post('/apply_promotions')
    assert response.status_code == 400
    assert response.get_json() == {'error': 'No items in cart to apply promotions'}

