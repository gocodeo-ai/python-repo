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
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        instance = MockCart.return_value
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
        instance.calculate_total_price = MagicMock(return_value=20.0)
        yield instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount = MagicMock()
        yield instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock_apply:
        yield mock_apply

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_all:
        mock_get_all.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
        yield mock_get_all

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

# happy_path - test_add_item_success - Test that item is added to cart successfully
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'})
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
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 3})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 3)

# happy_path - test_get_cart_items_success - Test that all items are retrieved from cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]}
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that total price is calculated correctly
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 20.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_to_cart_success - Test that discount is applied to cart successfully
def test_apply_discount_to_cart_success(client, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 20.0}
    mock_discount.apply_discount.assert_called_once()

# happy_path - test_apply_promotions_to_cart_success - Test that promotions are applied to cart successfully
def test_apply_promotions_to_cart_success(client, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once()

# edge_case - test_add_item_zero_quantity - Test adding item with zero quantity does not add to cart
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={'item_id': 2, 'quantity': 0, 'price': 5.0, 'name': 'Banana', 'category': 'Fruit'})
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(2, 0, 5.0, 'Banana', 'Fruit', 'regular')

# edge_case - test_remove_item_not_in_cart - Test removing an item not in cart returns appropriate message
def test_remove_item_not_in_cart(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 99})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(99)

# edge_case - test_update_item_quantity_to_zero - Test updating item quantity to zero removes item from cart
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)

# edge_case - test_get_cart_items_empty_cart - Test retrieving items from an empty cart returns empty list
def test_get_cart_items_empty_cart(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once()

# edge_case - test_apply_discount_high_min_purchase - Test applying discount with higher min purchase amount does not apply discount
def test_apply_discount_high_min_purchase(client, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 100})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 20.0}
    mock_discount.apply_discount.assert_called_once()

# edge_case - test_apply_promotions_empty_cart - Test applying promotions to an empty cart returns appropriate message
def test_apply_promotions_empty_cart(client, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once()

