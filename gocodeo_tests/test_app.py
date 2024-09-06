import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with patch('app.cart', new=MagicMock(spec=Cart)) as mock_cart:
            yield client, mock_cart

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount', autospec=True) as mock_discount_class:
        mock_discount_instance = mock_discount_class.return_value
        mock_discount_instance.apply_discount.return_value = None
        yield mock_discount_instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions', autospec=True) as mock_promotion:
        yield mock_apply_promotions_func

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart', autospec=True) as mock_get_items_func:
        yield mock_get_items_func

# happy_path - add_item - Test that an item is successfully added to the cart
def test_add_item_success(client):
    client, mock_cart = client
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10,
        'name': 'Tablet',
        'category': 'Electronics'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.0, 'Sample Item', 'Electronics', 'regular')

# happy_path - remove_item - Test that an item is successfully removed from the cart
def test_remove_item_success(client):
    client, mock_cart = client
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - update_item_quantity - Test that item quantity is successfully updated in the cart
def test_update_item_quantity_success(client):
    client, mock_cart = client
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - calculate_total_price - Test that total price is calculated correctly for the cart
def test_calculate_total_price_success(client, mock_get_all_items_from_cart):
    client, mock_cart = client
    mock_cart.calculate_total_price.return_value = 20.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 20.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - apply_discount_to_cart - Test that discount is applied correctly to the cart
def test_apply_discount_success(client, mock_discount):
    client, mock_cart = client
    mock_cart.total_price = 18.0
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 18.0}
    mock_discount.apply_discount.assert_called_once_with(mock_cart)

# happy_path - apply_promotions_to_cart - Test that promotions are applied successfully to the cart
def test_apply_promotions_success(client, mock_apply_promotions):
    client, mock_cart = client
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [Promotion("Spring Sale", 0.10), Promotion("Black Friday", 0.25)])

# edge_case - remove_item - Test removing an item not present in the cart
def test_remove_item_not_in_cart(client):
    client, mock_cart = client
    mock_cart.remove_item.side_effect = KeyError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}
    mock_cart.remove_item.assert_called_once_with(999)

# edge_case - update_item_quantity - Test updating quantity of an item not in the cart
def test_update_item_quantity_not_in_cart(client):
    client, mock_cart = client
    mock_cart.update_item_quantity.side_effect = KeyError('Item not found')
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found'}
    mock_cart.update_item_quantity.assert_called_once_with(999, 5)

# edge_case - apply_discount_to_cart - Test applying discount with rate greater than 1
def test_apply_discount_rate_greater_than_one(client):
    client, mock_cart = client
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 0})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid discount rate'}

# edge_case - apply_promotions_to_cart - Test applying promotions with an empty list
def test_apply_promotions_empty(client, mock_apply_promotions):
    client, mock_cart = client
    mock_apply_promotions.return_value = None
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [])

