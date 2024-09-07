import pytest
from unittest.mock import Mock, patch
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def mock_cart():
    return Mock(spec=Cart)

@pytest.fixture
def mock_discount():
    return Mock(spec=Discount)

@pytest.fixture
def mock_promotion():
    return Mock(spec=Promotion)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart') as mock:
        yield mock

@pytest.fixture
def mock_apply_promotions():
    with patch('app.apply_promotions') as mock:
        yield mock

@pytest.fixture
def mock_cart_instance(mock_cart):
    with patch('app.Cart', return_value=mock_cart):
        yield mock_cart

@pytest.fixture
def mock_discount_instance(mock_discount):
    with patch('app.Discount', return_value=mock_discount):
        yield mock_discount

@pytest.fixture
def mock_promotion_instance(mock_promotion):
    with patch('app.Promotion', return_value=mock_promotion):
        yield mock_promotion

@pytest.fixture
def mock_flask_request():
    with patch('app.request') as mock_request:
        yield mock_request

@pytest.fixture
def mock_flask_jsonify():
    with patch('app.jsonify') as mock_jsonify:
        yield mock_jsonify

# happy path - add_item - Generate test cases on successful item addition to cart
def test_add_item_success(client, mock_cart_instance, mock_flask_request, mock_flask_jsonify):
    mock_flask_request.json = {'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics'}
    mock_flask_jsonify.return_value = {'message': 'Item added to cart'}, 201
    response = client.post('/add_item')
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart_instance.add_item.assert_called_once_with(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')

# happy path - remove_item - Generate test cases on successful item removal from cart
def test_remove_item_success(client, mock_cart_instance, mock_flask_request, mock_flask_jsonify):
    mock_flask_request.json = {'item_id': 1}
    mock_flask_jsonify.return_value = {'message': 'Item removed from cart'}, 200
    response = client.post('/remove_item')
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart_instance.remove_item.assert_called_once_with(1)

# happy path - update_item_quantity - Generate test cases on successful item quantity update
def test_update_item_quantity_success(client, mock_cart_instance, mock_flask_request, mock_flask_jsonify):
    mock_flask_request.json = {'item_id': 1, 'new_quantity': 5}
    mock_flask_jsonify.return_value = {'message': 'Item quantity updated'}, 200
    response = client.post('/update_item_quantity')
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart_instance.update_item_quantity.assert_called_once_with(1, 5)

# happy path - get_cart_items - Generate test cases on successful retrieval of cart items
def test_get_cart_items_success(client, mock_cart_instance, mock_get_all_items_from_cart, mock_flask_jsonify):
    mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics'}]
    mock_flask_jsonify.return_value = {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics'}]}
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics'}]}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart_instance)

# happy path - calculate_total_price - Generate test cases on successful calculation of total price
def test_calculate_total_price_success(client, mock_cart_instance, mock_flask_jsonify):
    mock_cart_instance.calculate_total_price.return_value = 21.98
    mock_flask_jsonify.return_value = {'total_price': 21.98}
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 21.98}
    mock_cart_instance.calculate_total_price.assert_called_once()

# happy path - apply_discount_to_cart - Generate test cases on successful application of discount
def test_apply_discount_success(client, mock_cart_instance, mock_discount_instance, mock_flask_request, mock_flask_jsonify):
    mock_flask_request.json = {'discount_rate': 0.1, 'min_purchase_amount': 20}
    mock_cart_instance.total_price = 19.782
    mock_flask_jsonify.return_value = {'discounted_total': 19.782}
    response = client.post('/apply_discount')
    assert response.status_code == 200
    assert response.json == {'discounted_total': 19.782}
    mock_discount_instance.apply_discount.assert_called_once_with(mock_cart_instance)

# edge case - add_item - Generate test cases on adding item with invalid input
def test_add_item_invalid_input(client, mock_cart_instance, mock_flask_request, mock_flask_jsonify):
    mock_flask_request.json = {'item_id': 'abc', 'quantity': -1, 'price': 'invalid', 'name': '', 'category': None}
    mock_flask_jsonify.return_value = {'error': 'Invalid input'}, 400
    response = client.post('/add_item')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid input'}
    mock_cart_instance.add_item.assert_not_called()

# edge case - remove_item - Generate test cases on removing non-existent item
def test_remove_nonexistent_item(client, mock_cart_instance, mock_flask_request, mock_flask_jsonify):
    mock_flask_request.json = {'item_id': 999}
    mock_cart_instance.remove_item.side_effect = KeyError('Item not found')
    mock_flask_jsonify.return_value = {'error': 'Item not found in cart'}, 404
    response = client.post('/remove_item')
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found in cart'}
    mock_cart_instance.remove_item.assert_called_once_with(999)

# edge case - update_item_quantity - Generate test cases on updating quantity with invalid value
def test_update_quantity_invalid(client, mock_cart_instance, mock_flask_request, mock_flask_jsonify):
    mock_flask_request.json = {'item_id': 1, 'new_quantity': -5}
    mock_flask_jsonify.return_value = {'error': 'Invalid quantity'}, 400
    response = client.post('/update_item_quantity')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid quantity'}
    mock_cart_instance.update_item_quantity.assert_not_called()

# edge case - calculate_total_price - Generate test cases on calculating total price for empty cart
def test_calculate_total_price_empty_cart(client, mock_cart_instance, mock_flask_jsonify):
    mock_cart_instance.calculate_total_price.return_value = 0
    mock_flask_jsonify.return_value = {'total_price': 0}
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0}
    mock_cart_instance.calculate_total_price.assert_called_once()

# edge case - apply_discount_to_cart - Generate test cases on applying discount with invalid rate
def test_apply_discount_invalid_rate(client, mock_cart_instance, mock_discount_instance, mock_flask_request, mock_flask_jsonify):
    mock_flask_request.json = {'discount_rate': -0.5, 'min_purchase_amount': 0}
    mock_discount_instance.apply_discount.side_effect = ValueError('Invalid discount rate')
    mock_flask_jsonify.return_value = {'error': 'Invalid discount rate'}, 400
    response = client.post('/apply_discount')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid discount rate'}
    mock_discount_instance.apply_discount.assert_called_once_with(mock_cart_instance)

# edge case - apply_promotions_to_cart - Generate test cases on applying promotions to empty cart
def test_apply_promotions_empty_cart(client, mock_cart_instance, mock_apply_promotions, mock_flask_jsonify):
    mock_cart_instance.total_price = 0
    mock_flask_jsonify.return_value = {'message': 'Promotions applied', 'total_price': 0}
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied', 'total_price': 0}
    mock_apply_promotions.assert_called_once()

