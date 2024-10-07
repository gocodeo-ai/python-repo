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

    with app.app_context():
        yield app

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 20.0
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
        yield mock_apply_promotions_func

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_items:
        mock_get_items.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
        yield mock_get_items

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        yield MockPromotion

# happy_path - add_item - Test that item is added to cart successfully
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

# happy_path - remove_item - Test that item is removed from cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - update_item_quantity - Test that item quantity is updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 5
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - get_cart_items - Test that all items in cart are retrieved successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]}
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - calculate_total_price - Test that total price is calculated successfully
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 20.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - apply_discount_to_cart - Test that discount is applied successfully to cart
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 0.0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': 20.0}
    mock_discount.assert_called_once_with(0.1, 0.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - apply_promotions_to_cart - Test that promotions are applied successfully to cart
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once()
    assert mock_promotion.call_count == 2

# edge_case - add_item - Test adding item with zero quantity
def test_add_item_zero_quantity(client):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Invalid quantity'}

# edge_case - remove_item - Test removing item not in cart
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = Exception('Item not found')
    response = client.post('/remove_item', json={'item_id': 99})
    assert response.status_code == 404
    assert response.json == {'message': 'Item not found'}

# edge_case - update_item_quantity - Test updating item quantity to negative value
def test_update_item_quantity_negative(client):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': -5
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Invalid quantity'}

# edge_case - get_cart_items - Test retrieving items from empty cart
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}

# edge_case - calculate_total_price - Test calculating total price with no items in cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}

# edge_case - apply_discount_to_cart - Test applying discount with rate higher than 1
def test_apply_discount_rate_above_one(client):
    response = client.post('/apply_discount', json={
        'discount_rate': 1.5,
        'min_purchase_amount': 0.0
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Invalid discount rate'}

# edge_case - apply_promotions_to_cart - Test applying promotions with empty promotion list
def test_apply_promotions_empty_list(client, mock_apply_promotions):
    mock_apply_promotions.return_value = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No promotions applied'}

