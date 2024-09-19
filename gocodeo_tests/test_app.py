import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def client():
    app = Flask(__name__)
    with app.test_client() as client:
        yield client

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
        mock_discount_instance.apply_discount = MagicMock()
        yield mock_discount_instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock_apply_promotions_func:
        mock_apply_promotions_func.return_value = None
        yield mock_apply_promotions_func

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_items_func:
        mock_get_items_func.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Sample Item', 'category': 'Electronics'}]
        yield mock_get_items_func

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        mock_promotion_instance = MockPromotion.return_value
        yield mock_promotion_instance

# happy_path - test_add_item_success - Test that adding an item to the cart returns a success message
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Sample Item',
        'category': 'Electronics'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.0, 'Sample Item', 'Electronics', 'regular')

# happy_path - test_remove_item_success - Test that removing an item from the cart returns a success message
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that updating item quantity in the cart returns a success message
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items - Test that getting cart items returns the correct items
def test_get_cart_items(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Sample Item', 'category': 'Electronics'}]}
    mock_get_all_items_from_cart.assert_called_once()

# happy_path - test_calculate_total_price - Test that calculating total price returns the correct total
def test_calculate_total_price(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 20.0}
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_success - Test that applying a discount updates the total price accordingly
def test_apply_discount_success(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 20.0}
    mock_discount.apply_discount.assert_called_once_with(mock_cart)

# happy_path - test_apply_promotions_success - Test that applying promotions returns a success message
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock.ANY, mock.ANY])

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity returns an error
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.0,
        'name': 'Sample Item',
        'category': 'Electronics'
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Invalid quantity'}

# edge_case - test_remove_item_not_in_cart - Test that removing an item not in the cart returns an error
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = KeyError('Item not found')
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'message': 'Item not found'}

# edge_case - test_update_item_quantity_not_in_cart - Test that updating quantity of an item not in the cart returns an error
def test_update_item_quantity_not_in_cart(client, mock_cart):
    mock_cart.update_item_quantity.side_effect = KeyError('Item not found')
    response = client.post('/update_item_quantity', json={'item_id': 999, 'new_quantity': 5})
    assert response.status_code == 404
    assert response.json == {'message': 'Item not found'}

# edge_case - test_get_cart_items_empty - Test that getting cart items when cart is empty returns an empty list
def test_get_cart_items_empty(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}

# edge_case - test_apply_discount_invalid_rate - Test that applying a discount with a rate greater than 100% returns an error
def test_apply_discount_invalid_rate(client, mock_cart, mock_discount):
    mock_discount.apply_discount.side_effect = ValueError('Invalid discount rate')
    response = client.post('/apply_discount', json={'discount_rate': 1.5, 'min_purchase_amount': 0})
    assert response.status_code == 400
    assert response.json == {'message': 'Invalid discount rate'}

# edge_case - test_apply_promotions_no_applicable - Test that applying promotions with no applicable promotions returns no change
def test_apply_promotions_no_applicable(client, mock_cart, mock_apply_promotions):
    mock_apply_promotions.return_value = False
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'No applicable promotions'}

