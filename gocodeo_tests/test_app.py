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
        instance.calculate_total_price.return_value = 50.0
        instance.total_price = 50.0
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
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
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_all_items:
        mock_get_all_items.return_value = [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'item1', 'category': 'category1'}]
        yield mock_get_all_items

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

# happy_path - add_item - Test that adding an item to the cart returns a success message.
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'item1', 'category': 'category1'})
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.0, 'item1', 'category1', 'regular')

# happy_path - remove_item - Test that removing an item from the cart returns a success message.
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - update_item_quantity - Test that updating an item quantity in the cart returns a success message.
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - get_cart_items - Test that getting all items from the cart returns the correct item list.
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'item1', 'category': 'category1'}]}

# happy_path - calculate_total_price - Test that calculating the total price returns the correct total.
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 50.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - apply_discount_to_cart - Test that applying a discount returns the correct discounted total.
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 50.0}
    mock_discount.assert_called_once_with(0.1, 0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - apply_promotions_to_cart - Test that applying promotions returns a success message.
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_cart.promotion1, mock_cart.promotion2])

# edge_case - add_item - Test that adding an item with zero quantity returns an error message.
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={'item_id': 2, 'quantity': 0, 'price': 10.0, 'name': 'item2', 'category': 'category2'})
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}
    mock_cart.add_item.assert_not_called()

# edge_case - remove_item - Test that removing an item not in the cart returns an error message.
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = KeyError('Item not found in cart')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found in cart'}

# edge_case - update_item_quantity - Test that updating an item quantity to zero removes it from the cart.
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)

# edge_case - get_cart_items - Test that getting items from an empty cart returns an empty list.
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}

# edge_case - calculate_total_price - Test that calculating the total price of an empty cart returns zero.
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}

# edge_case - apply_discount_to_cart - Test that applying a discount with a higher minimum purchase amount than the cart total returns no discount.
def test_apply_discount_min_purchase_not_met(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 100})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 50.0}
    mock_discount.assert_called_once_with(0.1, 100)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# edge_case - apply_promotions_to_cart - Test that applying promotions when no promotions are available returns a no promotions applied message.
def test_apply_promotions_none_available(client, mock_cart, mock_apply_promotions):
    mock_apply_promotions.return_value = 'No promotions applied'
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No promotions applied'}

