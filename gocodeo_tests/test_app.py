import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
import app  # Import the Flask app

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('app.Cart') as MockCart:
        instance = MockCart.return_value
        instance.add_item = MagicMock()
        instance.remove_item = MagicMock()
        instance.update_item_quantity = MagicMock()
        instance.calculate_total_price = MagicMock(return_value=100.0)
        instance.total_price = 90.0
        yield instance

@pytest.fixture
def mock_discount():
    with patch('app.Discount') as MockDiscount:
        instance = MockDiscount.return_value
        instance.apply_discount = MagicMock()
        yield instance

@pytest.fixture
def mock_promotions():
    with patch('app.apply_promotions') as MockApplyPromotions:
        MockApplyPromotions.return_value = None
        yield MockApplyPromotions

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('app.get_all_items_from_cart') as MockGetAllItems:
        MockGetAllItems.return_value = [{'item_id': 1, 'quantity': 2, 'price': 19.99, 'name': 'Widget', 'category': 'Gadgets'}]
        yield MockGetAllItems

# happy_path - test_add_item_success - Test that an item is added to the cart successfully
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 19.99,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 19.99, 'Widget', 'Gadgets', 'regular')

# happy_path - test_remove_item_success - Test that an item is removed from the cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that the item quantity is updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items_success - Test that all items in the cart are retrieved successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.get_json() == {'items': [{'item_id': 1, 'quantity': 2, 'price': 19.99, 'name': 'Widget', 'category': 'Gadgets'}]}
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - test_calculate_total_price_success - Test that the total price is calculated correctly
def test_calculate_total_price_success(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.get_json() == {'total_price': 100.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_success - Test that a discount is applied to the cart successfully
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 20.0})
    assert response.status_code == 200
    assert response.get_json() == {'discounted_total': 90.0}
    mock_discount.assert_called_once_with(0.1, 20.0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - test_apply_promotions_success - Test that promotions are applied to the cart successfully
def test_apply_promotions_success(client, mock_cart, mock_promotions):
    response = client.post('/apply_promotions', json={})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Promotions applied'}
    mock_promotions.assert_called_once_with(mock_cart, [Promotion("Spring Sale", 0.10), Promotion("Black Friday", 0.25)])

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 2,
        'quantity': 0,
        'price': 19.99,
        'name': 'Widget',
        'category': 'Gadgets'
    })
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Invalid quantity'}

# edge_case - test_remove_item_non_existent - Test removing an item that does not exist in the cart
def test_remove_item_non_existent(client, mock_cart):
    mock_cart.remove_item.side_effect = ValueError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Item not found'}
    mock_cart.remove_item.assert_called_once_with(999)

# edge_case - test_update_item_quantity_to_zero - Test updating item quantity to zero
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Invalid quantity'}

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price for an empty cart
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.get_json() == {'total_price': 0.0}
    mock_cart.calculate_total_price.assert_called_once()

# edge_case - test_apply_discount_rate_greater_than_one - Test applying a discount with a rate greater than 1
def test_apply_discount_rate_greater_than_one(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 20.0})
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Invalid discount rate'}

# edge_case - test_apply_promotions_empty_cart - Test applying promotions when cart is empty
def test_apply_promotions_empty_cart(client, mock_cart, mock_promotions):
    mock_cart.calculate_total_price.return_value = 0.0
    response = client.post('/apply_promotions', json={})
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Cart is empty'}
    mock_promotions.assert_not_called()

