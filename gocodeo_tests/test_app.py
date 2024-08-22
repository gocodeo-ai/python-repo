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
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        yield mock_cart_instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        mock_discount_instance = MockDiscount.return_value
        yield mock_discount_instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as MockApplyPromotions:
        yield MockApplyPromotions

@pytest.fixture
def mock_promotion():
    with patch('shopping_cart.payments.Promotion') as MockPromotion:
        mock_promotion_instance = MockPromotion.return_value
        yield mock_promotion_instance

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as MockGetAllItemsFromCart:
        yield MockGetAllItemsFromCart

# happy_path - add_item - Test that item is added to cart successfully with valid input data
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.5,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}
    mock_cart.add_item.assert_called_once_with(1, 2, 10.5, 'Apple', 'Fruit', 'regular')

# happy_path - remove_item - Test that item is removed from cart successfully with valid item_id
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - update_item_quantity - Test that item quantity is updated successfully with valid item_id and new_quantity
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - get_cart_items - Test that cart items are retrieved successfully
def test_get_cart_items_success(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.5, 'name': 'Apple', 'category': 'Fruit'}]
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.5, 'name': 'Apple', 'category': 'Fruit'}]}

# happy_path - calculate_total_price - Test that total price is calculated correctly for items in cart
def test_calculate_total_price_success(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 21.0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 21.0}

# happy_path - apply_discount_to_cart - Test that discount is applied successfully when conditions are met
def test_apply_discount_success(client, mock_cart, mock_discount):
    mock_cart.total_price = 21.0
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 0})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 18.9}
    mock_discount.assert_called_once_with(0.1, 0)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - apply_promotions_to_cart - Test that promotions are applied successfully to the cart
def test_apply_promotions_success(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion('Spring Sale', 0.10), mock_promotion('Black Friday', 0.25)])

# edge_case - add_item - Test that adding an item with zero quantity returns an error
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.5,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 400
    assert response.json == {'message': 'Quantity must be greater than zero'}
    mock_cart.add_item.assert_not_called()

# edge_case - remove_item - Test that removing an item not in cart returns an error
def test_remove_item_not_in_cart(client, mock_cart):
    mock_cart.remove_item.side_effect = KeyError('Item not found in cart')
    response = client.post('/remove_item', json={'item_id': 99})
    assert response.status_code == 404
    assert response.json == {'message': 'Item not found in cart'}

# edge_case - update_item_quantity - Test that updating item quantity to zero removes it from cart
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)

# edge_case - get_cart_items - Test that getting cart items returns empty list when cart is empty
def test_get_cart_items_empty_cart(client, mock_get_all_items_from_cart):
    mock_get_all_items_from_cart.return_value = []
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {'items': []}

# edge_case - calculate_total_price - Test that calculating total price returns zero when cart is empty
def test_calculate_total_price_empty_cart(client, mock_cart):
    mock_cart.calculate_total_price.return_value = 0
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 0}

# edge_case - apply_discount_to_cart - Test that applying discount with high min_purchase_amount returns no discount
def test_apply_discount_high_min_purchase(client, mock_cart, mock_discount):
    mock_cart.total_price = 21.0
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 1000})
    assert response.status_code == 200
    assert response.json == {'discounted_total': 21.0}
    mock_discount.assert_called_once_with(0.1, 1000)
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# edge_case - apply_promotions_to_cart - Test that applying conflicting promotions resolves correctly
def test_apply_conflicting_promotions(client, mock_cart, mock_apply_promotions, mock_promotion):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}
    mock_apply_promotions.assert_called_once_with(mock_cart, [mock_promotion('Spring Sale', 0.10), mock_promotion('Black Friday', 0.25)])

