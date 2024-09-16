import pytest
from unittest.mock import patch, MagicMock
from flask import jsonify
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('app.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price.return_value = 50.0
        instance.total_price = 50.0
        yield instance

@pytest.fixture
def mock_discount():
    with patch('app.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount.return_value = None
        yield instance

@pytest.fixture
def mock_apply_promotions():
    with patch('app.apply_promotions') as mock_apply:
        mock_apply.return_value = None
        yield mock_apply

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart') as mock_get_items:
        mock_get_items.return_value = [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
        yield mock_get_items

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

@pytest.fixture(autouse=True)
def setup_mocks(mock_cart, mock_discount, mock_apply_promotions, mock_get_all_items_from_cart, mock_promotion):
    pass

# happy_path - test_add_item_success - Test that item is added to cart successfully
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.0, 'Apple', 'Fruit', 'regular')

# happy_path - test_remove_item_success - Test that item is removed from cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items_success - Test that cart items are retrieved successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]}

# happy_path - test_calculate_total_price_success - Test that total price is calculated correctly
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 50.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_success - Test that discount is applied to cart successfully
def test_apply_discount_success(client, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 50.0}
    mock_discount.assert_called_once_with(0.1, 0)
    mock_discount.return_value.apply_discount.assert_called_once()

# happy_path - test_apply_promotions_success - Test that promotions are applied to cart successfully
def test_apply_promotions_success(client, mock_apply_promotions, mock_cart):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, mock.ANY)

# edge_case - test_add_item_invalid_id - Test that adding an item with invalid ID raises an error
def test_add_item_invalid_id(client):
    response = client.post('/add_item', json={
        'item_id': 'invalid',
        'quantity': 2,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Invalid item ID'

# edge_case - test_remove_item_non_existent - Test that removing a non-existent item raises an error
def test_remove_item_non_existent(client, mock_cart):
    mock_cart.remove_item.side_effect = ValueError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'Item not found'

# edge_case - test_update_item_quantity_to_zero - Test that updating item quantity to zero removes item from cart
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)

# edge_case - test_get_cart_items_empty - Test that getting cart items when cart is empty returns empty list
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}

# edge_case - test_apply_discount_below_minimum - Test that applying a discount when total is below minimum purchase amount has no effect
def test_apply_discount_below_minimum(client, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 100})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 50.0}
    mock_discount.assert_called_once_with(0.1, 100)
    mock_discount.return_value.apply_discount.assert_called_once()

# edge_case - test_apply_promotions_no_valid - Test that applying promotions with no valid promotions returns no change
def test_apply_promotions_no_valid(client, mock_apply_promotions, mock_cart):
    mock_apply_promotions.return_value = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, mock.ANY)

