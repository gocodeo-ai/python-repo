import pytest
from unittest.mock import patch, MagicMock
from flask import json
from app import app
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 99.95
        mock_cart_instance.add_item.return_value = None
        mock_cart_instance.remove_item.return_value = None
        mock_cart_instance.update_item_quantity.return_value = None
        mock_cart_instance.total_price = 99.95
        yield mock_cart_instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        mock_discount_instance = MockDiscount.return_value
        mock_discount_instance.apply_discount.return_value = None
        yield mock_discount_instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock_apply_promotions_func:
        mock_apply_promotions_func.return_value = None
        yield mock_apply_promotions_func

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        mock_promotion_instance = MockPromotion.return_value
        yield mock_promotion_instance

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_items:
        mock_get_items.return_value = [{'item_id': 1, 'quantity': 5, 'price': 19.99, 'name': 'Test Item', 'category': 'Books'}]
        yield mock_get_items

# happy_path - test_add_item_success - Test that adding a valid item to the cart returns success message
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 19.99,
        'name': 'Test Item',
        'category': 'Books'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}

# happy_path - test_remove_item_success - Test that removing a valid item from the cart returns success message
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}

# happy_path - test_update_item_quantity_success - Test that updating item quantity in the cart returns success message
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}

# happy_path - test_get_cart_items_success - Test that fetching all items from the cart returns the correct items
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 5, 'price': 19.99, 'name': 'Test Item', 'category': 'Books'}]}

# happy_path - test_calculate_total_price_success - Test that calculating total price returns the correct total price
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 99.95}

# happy_path - test_apply_discount_success - Test that applying a valid discount returns the correct discounted total
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 50})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 89.95}

# happy_path - test_apply_promotions_success - Test that applying promotions returns success message
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity returns an error
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 2,
        'quantity': 0,
        'price': 19.99,
        'name': 'Test Item',
        'category': 'Books'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}

# edge_case - test_remove_non_existent_item - Test that removing a non-existent item returns an error
def test_remove_non_existent_item(client, mock_cart):
    mock_cart.remove_item.side_effect = KeyError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}

# edge_case - test_update_non_existent_item_quantity - Test that updating quantity for a non-existent item returns an error
def test_update_non_existent_item_quantity(client, mock_cart):
    mock_cart.update_item_quantity.side_effect = KeyError('Item not found')
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}

# edge_case - test_get_cart_items_empty_cart - Test that fetching items from an empty cart returns an empty list
def test_get_cart_items_empty_cart(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}

# edge_case - test_apply_high_min_purchase_discount - Test that applying a discount with a higher min purchase amount returns no discount
def test_apply_high_min_purchase_discount(client, mock_cart, mock_discount):
    mock_discount.apply_discount.side_effect = None
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 200})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 99.95}

# edge_case - test_apply_no_applicable_promotions - Test that applying promotions with no applicable promotions returns no change
def test_apply_no_applicable_promotions(client, mock_cart, mock_apply_promotions):
    mock_apply_promotions.side_effect = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No applicable promotions'}

