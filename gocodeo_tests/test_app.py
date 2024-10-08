import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        instance = MockCart.return_value
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
        instance.calculate_total_price = MagicMock(return_value=39.98)
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
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get:
        mock_get.return_value = [{'item_id': 1, 'quantity': 2, 'price': 19.99, 'name': 'T-shirt', 'category': 'Clothing'}]
        yield mock_get

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

# happy path - add_item - Test that an item is successfully added to the cart
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 19.99,
        'name': 'T-shirt',
        'category': 'Clothing'
    })
    mock_cart.add_item.assert_called_once_with(1, 2, 19.99, 'T-shirt', 'Clothing', 'regular')
    assert response.json == {'message': 'Item added to cart'}
    assert response.status_code == 201



# happy path - remove_item - Test that an item is successfully removed from the cart
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    mock_cart.remove_item.assert_called_once_with(1)
    assert response.json == {'message': 'Item removed from cart'}
    assert response.status_code == 200



# happy path - update_item_quantity - Test that item quantity is successfully updated in the cart
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)
    assert response.json == {'message': 'Item quantity updated'}
    assert response.status_code == 200



# happy path - get_cart_items - Test that all items are retrieved from the cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    mock_get_all_items_from_cart.assert_called_once()
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 19.99, 'name': 'T-shirt', 'category': 'Clothing'}]}



# happy path - calculate_total_price - Test that total price is calculated correctly for the cart
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    mock_cart.calculate_total_price.assert_called_once()
    assert response.json == {'total_price': 39.98}



# happy path - apply_discount_to_cart - Test that discount is applied to the cart
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 50})
    mock_discount.apply_discount.assert_called_once_with(mock_cart)
    assert response.json == {'discounted_total': mock_cart.total_price}



# happy path - apply_promotions_to_cart - Test that promotions are applied to the cart
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    mock_apply_promotions.assert_called_once_with(mock_cart, mock.ANY)
    assert response.json == {'message': 'Promotions applied'}



# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 2,
        'quantity': 0,
        'price': 29.99,
        'name': 'Shoes',
        'category': 'Footwear'
    })
    mock_cart.add_item.assert_called_once_with(2, 0, 29.99, 'Shoes', 'Footwear', 'regular')
    assert response.json == {'message': 'Item added to cart'}
    assert response.status_code == 201



# edge case - remove_item - Test removing an item that does not exist in the cart
def test_remove_nonexistent_item(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 999})
    mock_cart.remove_item.assert_called_once_with(999)
    assert response.json == {'message': 'Item removed from cart'}
    assert response.status_code == 200



# edge case - update_item_quantity - Test updating item quantity to a negative number
def test_update_item_negative_quantity(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': -5})
    mock_cart.update_item_quantity.assert_called_once_with(1, -5)
    assert response.json == {'message': 'Item quantity updated'}
    assert response.status_code == 200



# edge case - calculate_total_price - Test calculating total price with an empty cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0
    response = client.get('/calculate_total_price')
    mock_cart.calculate_total_price.assert_called_once()
    assert response.json == {'total_price': 0}



# edge case - apply_discount_to_cart - Test applying discount with a negative discount rate
def test_apply_negative_discount_rate(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': -0.1, 'min_purchase_amount': 50})
    mock_discount.apply_discount.assert_called_once_with(mock_cart)
    assert response.json == {'discounted_total': mock_cart.total_price}



# edge case - apply_promotions_to_cart - Test applying promotions with an invalid promotion
def test_apply_invalid_promotion(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    mock_apply_promotions.assert_called_once_with(mock_cart, mock.ANY)
    assert response.json == {'message': 'Promotions applied'}



