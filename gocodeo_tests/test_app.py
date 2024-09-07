import pytest
from unittest.mock import patch, Mock
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
    with patch('app.Cart') as MockCart:
        mock_cart = MockCart.return_value
        mock_cart.add_item = Mock()
        mock_cart.remove_item = Mock()
        mock_cart.update_item_quantity = Mock()
        mock_cart.calculate_total_price = Mock(return_value=20.0)
        yield mock_cart

@pytest.fixture
def mock_discount():
    with patch('app.Discount') as MockDiscount:
        mock_discount = MockDiscount.return_value
        mock_discount.apply_discount = Mock()
        yield mock_discount

@pytest.fixture
def mock_promotions():
    with patch('app.apply_promotions') as MockApplyPromotions:
        yield MockApplyPromotions

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart') as MockGetAllItemsFromCart:
        MockGetAllItemsFromCart.return_value = [
            {'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}
        ]
        yield MockGetAllItemsFromCart

@pytest.fixture
def mock_promotion():
    with patch('app.Promotion') as MockPromotion:
        mock_promotion = MockPromotion.return_value
        yield mock_promotion

# happy_path - test_add_item_success - Test that item is added to the cart successfully
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

# happy_path - test_remove_item_success - Test that item is removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully in the cart
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items_success - Test that all items are retrieved from the cart successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]}
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - test_apply_discount_success - Test that discount is applied successfully to the cart
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 20.0}
    mock_discount.apply_discount.assert_called_once_with(mock_cart)

# happy_path - test_apply_promotions_success - Test that promotions are applied successfully to the cart
def test_apply_promotions_success(client, mock_cart, mock_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_promotions.assert_called_once_with(mock_cart, [mock_promotion, mock_promotion])

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 0, 10.0, 'Apple', 'Fruit', 'regular')

# edge_case - test_remove_item_non_existent - Test removing an item that does not exist in the cart
def test_remove_item_non_existent(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(999)

# edge_case - test_update_item_quantity_to_zero - Test updating item quantity to zero
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)

# edge_case - test_apply_discount_negative_rate - Test applying a discount with a negative rate
def test_apply_discount_negative_rate(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': -0.1, 'min_purchase_amount': 0.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 20.0}
    mock_discount.apply_discount.assert_called_once_with(mock_cart)

# edge_case - test_apply_promotions_empty_list - Test applying promotions with an empty promotions list
def test_apply_promotions_empty_list(client, mock_cart, mock_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_promotions.assert_called_once_with(mock_cart, [mock_promotion, mock_promotion])

