import pytest
from unittest.mock import Mock, patch
from flask import Flask, jsonify
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_cart():
    with patch('app.Cart') as mock_cart_class:
        mock_cart = Mock()
        mock_cart_class.return_value = mock_cart
        yield mock_cart

@pytest.fixture
def mock_discount():
    with patch('app.Discount') as mock_discount_class:
        mock_discount = Mock()
        mock_discount_class.return_value = mock_discount
        yield mock_discount

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion') as mock_promotion_class:
        mock_promotion = Mock()
        mock_promotion_class.return_value = mock_promotion
        yield mock_promotion

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart') as mock_get_items:
        yield mock_get_items

@pytest.fixture
def mock_apply_promotions():
    with patch('app.apply_promotions') as mock_apply_promo:
        yield mock_apply_promo

@pytest.fixture
def mock_jsonify():
    with patch('app.jsonify') as mock_json:
        mock_json.side_effect = lambda x: x
        yield mock_json

# happy path - add_item - Test adding an item to the cart successfully
def test_add_item_success(client, mock_cart, mock_jsonify):
    response = client.post('/add_item', json={'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics'})
    mock_cart.add_item.assert_called_once_with(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')
    mock_jsonify.assert_called_once_with({'message': 'Item added to cart'})
    assert response.status_code == 201

# happy path - remove_item - Test removing an item from the cart successfully
def test_remove_item_success(client, mock_cart, mock_jsonify):
    response = client.post('/remove_item', json={'item_id': 1})
    mock_cart.remove_item.assert_called_once_with(1)
    mock_jsonify.assert_called_once_with({'message': 'Item removed from cart'})
    assert response.status_code == 200

# happy path - update_item_quantity - Test updating item quantity in the cart successfully
def test_update_item_quantity_success(client, mock_cart, mock_jsonify):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 3})
    mock_cart.update_item_quantity.assert_called_once_with(1, 3)
    mock_jsonify.assert_called_once_with({'message': 'Item quantity updated'})
    assert response.status_code == 200

# happy path - get_cart_items - Test getting all items from the cart successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart, mock_jsonify):
    mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics'}]
    response = client.get('/get_cart_items')
    mock_get_all_items_from_cart.assert_called_once()
    mock_jsonify.assert_called_once_with({'items': [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics'}]})
    assert response.status_code == 200

# happy path - calculate_total_price - Test calculating total price of the cart successfully
def test_calculate_total_price_success(client, mock_cart, mock_jsonify):
    mock_cart.calculate_total_price.return_value = 21.98
    response = client.get('/calculate_total_price')
    mock_cart.calculate_total_price.assert_called_once()
    mock_jsonify.assert_called_once_with({'total_price': 21.98})
    assert response.status_code == 200

# happy path - apply_discount_to_cart - Test applying discount to the cart successfully
def test_apply_discount_to_cart_success(client, mock_cart, mock_discount, mock_jsonify):
    mock_cart.total_price = 19.782
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 20})
    mock_discount.assert_called_once_with(0.1, 20)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)
    mock_jsonify.assert_called_once_with({'discounted_total': 19.782})
    assert response.status_code == 200

# edge case - add_item - Test adding an item with invalid input
def test_add_item_invalid_input(client, mock_cart, mock_jsonify):
    response = client.post('/add_item', json={'item_id': 'abc', 'quantity': -1, 'price': 'invalid', 'name': '', 'category': ''})
    mock_cart.add_item.assert_not_called()
    mock_jsonify.assert_called_once_with({'error': 'Invalid input'})
    assert response.status_code == 400

# edge case - remove_item - Test removing a non-existent item from the cart
def test_remove_nonexistent_item(client, mock_cart, mock_jsonify):
    mock_cart.remove_item.side_effect = ValueError('Item not found in cart')
    response = client.post('/remove_item', json={'item_id': 999})
    mock_cart.remove_item.assert_called_once_with(999)
    mock_jsonify.assert_called_once_with({'error': 'Item not found in cart'})
    assert response.status_code == 404

# edge case - update_item_quantity - Test updating quantity of a non-existent item
def test_update_nonexistent_item_quantity(client, mock_cart, mock_jsonify):
    mock_cart.update_item_quantity.side_effect = ValueError('Item not found in cart')
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    mock_cart.update_item_quantity.assert_called_once_with(999, 5)
    mock_jsonify.assert_called_once_with({'error': 'Item not found in cart'})
    assert response.status_code == 404

# edge case - get_cart_items - Test getting items from an empty cart
def test_get_empty_cart_items(client, mock_get_all_items_from_cart, mock_jsonify):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    mock_get_all_items_from_cart.assert_called_once()
    mock_jsonify.assert_called_once_with({'items': []})
    assert response.status_code == 200

# edge case - calculate_total_price - Test calculating total price of an empty cart
def test_calculate_empty_cart_total_price(client, mock_cart, mock_jsonify):
    mock_cart.calculate_total_price.return_value = 0
    response = client.get('/calculate_total_price')
    mock_cart.calculate_total_price.assert_called_once()
    mock_jsonify.assert_called_once_with({'total_price': 0})
    assert response.status_code == 200

# edge case - apply_discount_to_cart - Test applying discount with invalid discount rate
def test_apply_invalid_discount_rate(client, mock_cart, mock_discount, mock_jsonify):
    response = client.post('/apply_discount', json={'discount_rate': -0.1, 'min_purchase_amount': 20})
    mock_discount.assert_called_once_with(-0.1, 20)
    mock_discount.return_value.apply_discount.side_effect = ValueError('Invalid discount rate')
    mock_jsonify.assert_called_once_with({'error': 'Invalid discount rate'})
    assert response.status_code == 400

