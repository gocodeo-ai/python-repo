import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from demo.shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app  # Importing the Flask app

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
        instance.calculate_total_price = MagicMock(return_value=0.0)
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
    with patch('demo.shopping_cart.payments.apply_promotions') as mock_apply:
        yield mock_apply

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_items:
        yield mock_get_items

@pytest.fixture
def mock_promotion():
    with patch('demo.shopping_cart.payments.Promotion') as MockPromotion:
        instance = MockPromotion.return_value
        yield instance

@pytest.fixture(autouse=True)
def setup_mocks(mock_cart, mock_discount, mock_apply_promotions, mock_get_all_items_from_cart, mock_promotion):
    # This fixture will automatically apply all mocks for each test
    pass

# happy path - remove_item - Test that an item is removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': ' the cart state is consistent after removal
    mock_cart.remove_item.assert_called_once()


# happy path - update_item_quantity - Test that the item quantity is updated in the cart
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)


# happy path - get_cart_items - Test that all items are retrieved from the cart
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'name': 'Widget', 'quantity': 2, 'price': 10.99}]
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'name': 'Widget', 'quantity': 2, 'price': 10.99}]}
    mock_get_all_items_from_cart.assert_called_once()


# happy path - calculate_total_price - Test that the total price is calculated correctly
def test_calculate_total_price_success(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 21.98
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 21.98}
    mock_cart.calculate_total_price.assert_called_once()


# happy path - apply_discount_to_cart - Test that a discount is applied to the cart
def test_apply_discount_success(client, mock_cart, mock_discount):
    mock_cart.total_price = 19.78
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 20.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 19.78}
    mock_discount.assert_called_once_with(0.1, 20.0)
    mock_discount().apply_discount.assert_called_once_with(mock_cart)


# happy path - apply_promotions_to_cart - Test that promotions are applied to the cart
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once()


# edge case - add_item - Test adding an item with zero quantity
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={'item_id': 2, 'quantity': 0, 'price': 15.99, 'name': 'Gizmo', 'category': 'Tools'})
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(2, 0, 15.99, 'Gizmo', 'Tools')


# edge case - remove_item - Test removing an item not in the cart
def test_remove_item_not_in_cart(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 99})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(99)


# edge case - update_item_quantity - Test updating an item quantity to a negative number
def test_update_item_quantity_negative(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': -3})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, -3)


# edge case - calculate_total_price - Test calculating total price with an empty cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0.0}
    mock_cart.calculate_total_price.assert_called_once()


# edge case - apply_discount_to_cart - Test applying a discount with a rate above 1.0
def test_apply_discount_high_rate(client, mock_cart, mock_discount):
    mock_cart.total_price = 0.0
    response = client.post('/apply_discount', json={'discount_rate': 1.1, 'min_purchase_amount': 20.0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 0.0}
    mock_discount.assert_called_once_with(1.1, 20.0)
    mock_discount().apply_discount.assert_called_once_with(mock_cart)


# edge case - apply_promotions_to_cart - Test applying promotions with an empty cart
def test_apply_promotions_empty_cart(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once()


