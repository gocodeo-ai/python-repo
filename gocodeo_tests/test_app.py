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
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock:
        yield mock

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock:
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

# Mock Cart methods
@pytest.fixture
def mock_cart_methods(mock_cart_instance):
    mock_cart_instance.add_item.return_value = None
    mock_cart_instance.remove_item.return_value = None
    mock_cart_instance.update_item_quantity.return_value = None
    mock_cart_instance.calculate_total_price.return_value = 100.0
    mock_cart_instance.total_price = 100.0
    return mock_cart_instance

# Mock Discount methods
@pytest.fixture
def mock_discount_methods(mock_discount_instance):
    mock_discount_instance.apply_discount.return_value = None
    return mock_discount_instance

# Mock Promotion methods
@pytest.fixture
def mock_promotion_methods(mock_promotion_instance):
    mock_promotion_instance.apply.return_value = None
    return mock_promotion_instance

# Mock get_all_items_from_cart function
@pytest.fixture
def mock_get_all_items_from_cart_function(mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = [
        {'id': 1, 'name': 'Test Item', 'quantity': 2, 'price': 10.99}
    ]
    return mock_get_all_items_from_cart

# Mock apply_promotions function
@pytest.fixture
def mock_apply_promotions_function(mock_apply_promotions):
    mock_apply_promotions.return_value = None
    return mock_apply_promotions

# happy path - add_item - Test successfully adding an item to the cart
def test_add_item_success(client, mock_cart_methods):
    response = client.post('/add_item', json={'item_id': 1, 'quantity': 2, 'price': 10.99, 'name': 'Test Item', 'category': 'Electronics'})
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart_methods.add_item.assert_called_once_with(1, 2, 10.99, 'Test Item', 'Electronics', 'regular')

# happy path - remove_item - Test successfully removing an item from the cart
def test_remove_item_success(client, mock_cart_methods):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart_methods.remove_item.assert_called_once_with(1)

# happy path - update_item_quantity - Test successfully updating item quantity in the cart
def test_update_item_quantity_success(client, mock_cart_methods):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 3})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart_methods.update_item_quantity.assert_called_once_with(1, 3)

# happy path - get_cart_items - Test successfully retrieving all items from the cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart_function):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'id': 1, 'name': 'Test Item', 'quantity': 2, 'price': 10.99}]}
    mock_get_all_items_from_cart_function.assert_called_once()

# happy path - calculate_total_price - Test successfully calculating total price of items in the cart
def test_calculate_total_price_success(client, mock_cart_methods):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 100.0}
    mock_cart_methods.calculate_total_price.assert_called_once()

# happy path - apply_discount_to_cart - Test successfully applying discount to the cart
def test_apply_discount_to_cart_success(client, mock_cart_methods, mock_discount_methods):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 20})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 100.0}
    mock_discount_methods.apply_discount.assert_called_once_with(mock_cart_methods)

# edge case - add_item - Test adding item with invalid input types
def test_add_item_invalid_input(client):
    response = client.post('/add_item', json={'item_id': 'abc', 'quantity': 'two', 'price': 'ten', 'name': 123, 'category': [1, 2, 3]})
    assert response.status_code == 400
    assert 'error' in response.json

# edge case - remove_item - Test removing non-existent item from the cart
def test_remove_non_existent_item(client, mock_cart_methods):
    mock_cart_methods.remove_item.side_effect = ValueError('Item not found in cart')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert 'error' in response.json

# edge case - update_item_quantity - Test updating quantity with negative value
def test_update_quantity_negative(client, mock_cart_methods):
    mock_cart_methods.update_item_quantity.side_effect = ValueError('Invalid quantity')
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': -5})
    assert response.status_code == 400
    assert 'error' in response.json

# edge case - calculate_total_price - Test calculating total price for an empty cart
def test_calculate_total_price_empty_cart(client, mock_cart_methods):
    mock_cart_methods.calculate_total_price.return_value = 0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0}

# edge case - apply_discount_to_cart - Test applying discount with invalid discount rate
def test_apply_discount_invalid_rate(client, mock_discount_methods):
    mock_discount_methods.apply_discount.side_effect = ValueError('Invalid discount rate')
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 20})
    assert response.status_code == 400
    assert 'error' in response.json

# edge case - apply_promotions_to_cart - Test applying promotions to an empty cart
def test_apply_promotions_empty_cart(client, mock_cart_methods, mock_apply_promotions_function):
    mock_cart_methods.total_price = 0
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions_function.assert_called_once()

