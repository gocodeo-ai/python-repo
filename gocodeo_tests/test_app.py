import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion', autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart', autospec=True) as mock:
        yield mock

@pytest.fixture
def client(app, mock_cart, mock_discount, mock_apply_promotions, mock_promotion, mock_get_all_items_from_cart):
    with app.test_client() as client:
        yield client

# happy_path - test_add_item_success - Test that add_item successfully adds an item to the cart
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 9.99,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.return_value.add_item.assert_called_once_with(1, 2, 9.99, 'Apple', 'Fruit', 'regular')

# happy_path - test_remove_item_success - Test that remove_item successfully removes an item from the cart
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.return_value.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that update_item_quantity successfully updates item quantity in the cart
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.return_value.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items_success - Test that get_cart_items retrieves all items from the cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'quantity': 2, 'price': 9.99, 'name': 'Apple', 'category': 'Fruit'}]
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 9.99, 'name': 'Apple', 'category': 'Fruit'}]}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart.return_value)

# happy_path - test_calculate_total_price_success - Test that calculate_total_price returns the total price of items in the cart
def test_calculate_total_price_success(client, mock_cart):
    mock_cart.return_value.calculate_total_price.return_value = 19.98
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 19.98}
    mock_cart.return_value.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_to_cart_success - Test that apply_discount_to_cart applies discount to the total price
def test_apply_discount_to_cart_success(client, mock_cart, mock_discount):
    mock_cart.return_value.total_price = 19.98
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 17.98}
    mock_discount.assert_called_once_with(0.1, 0.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart.return_value)

# happy_path - test_apply_promotions_to_cart_success - Test that apply_promotions_to_cart applies promotions to the cart
def test_apply_promotions_to_cart_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once()
    mock_promotion.assert_any_call("Spring Sale", 0.10)
    mock_promotion.assert_any_call("Black Friday", 0.25)

# edge_case - test_add_item_invalid_item_id - Test that add_item handles invalid item_id
def test_add_item_invalid_item_id(client):
    response = client.post('/add_item', json={
        'item_id': 'invalid',
        'quantity': 2,
        'price': 9.99,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Invalid item_id'

# edge_case - test_remove_item_non_existent - Test that remove_item handles non-existent item_id
def test_remove_item_non_existent(client, mock_cart):
    mock_cart.return_value.remove_item.side_effect = KeyError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == 'Item not found'

# edge_case - test_update_item_quantity_zero - Test that update_item_quantity handles zero quantity
def test_update_item_quantity_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Quantity must be greater than zero'

# edge_case - test_get_cart_items_empty - Test that get_cart_items handles empty cart
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart.return_value)

# edge_case - test_calculate_total_price_empty_cart - Test that calculate_total_price handles cart with no items
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.return_value.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}
    mock_cart.return_value.calculate_total_price.assert_called_once()

# edge_case - test_apply_discount_to_cart_excessive_discount - Test that apply_discount_to_cart handles discount greater than total price
def test_apply_discount_to_cart_excessive_discount(client, mock_cart, mock_discount):
    mock_cart.return_value.total_price = 19.98
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 0.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 0.0}
    mock_discount.assert_called_once_with(1.5, 0.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart.return_value)

