import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from demo.shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app  # Importing the Flask app from your source code

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price.return_value = 0.0
        instance.total_price = 0.0
        yield instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount = MagicMock()
        yield instance

@pytest.fixture
def mock_apply_promotions():
    with patch('demo.shopping_cart.payments.apply_promotions') as mock_apply_promotions:
        yield mock_apply_promotions

@pytest.fixture
def mock_promotion():
    with patch('demo.shopping_cart.payments.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_all_items:
        mock_get_all_items.return_value = []
        yield mock_get_all_items

# happy path - add_item - Test that an item is added to the cart successfully with valid data
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Test Item',
        'category': 'Test Category'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.0, 'Test Item', 'Test Category')


# happy path - remove_item - Test that an item is removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)


# happy path - update_item_quantity - Test that the item quantity is updated successfully in the cart
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that all items are retrieved from the cart successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart)


# happy path - calculate_total_price - Test that the total price is calculated correctly
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}
    mock_cart.calculate_total_price.assert_called_once()


# happy path - apply_discount_to_cart - Test that a discount is applied successfully to the cart
def test_apply_discount_success(client, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 0.0}
    mock_discount.apply_discount.assert_called_once_with(mock_cart)


# happy path - apply_promotions_to_cart - Test that promotions are applied successfully to the cart
def test_apply_promotions_success(client, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion, mock_promotion])


# edge case - add_item - Test adding an item with zero quantity to the cart
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 2,
        'quantity': 0,
        'price': 10.0,
        'name': 'Zero Quantity Item',
        'category': 'Test Category'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(2, 0, 10.0, 'Zero Quantity Item', 'Test Category')


# edge case - remove_item - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(999)


# edge case - update_item_quantity - Test updating item quantity to zero
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)


# edge case - get_cart_items - Test retrieving items from an empty cart
def test_get_items_from_empty_cart(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart)


# edge case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}
    mock_cart.calculate_total_price.assert_called_once()


# edge case - apply_discount_to_cart - Test applying a discount with a rate higher than 1
def test_apply_discount_invalid_rate(client, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 0.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 0.0}
    mock_discount.apply_discount.assert_called_once_with(mock_cart)


# edge case - apply_promotions_to_cart - Test applying promotions with no promotions available
def test_apply_no_promotions(client, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion, mock_promotion])


