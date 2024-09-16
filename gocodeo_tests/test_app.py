import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart
from app import app  # Assuming your Flask app is in app.py

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_instance = MockCart.return_value
        mock_instance.calculate_total_price.return_value = 50.0
        mock_instance.add_item = MagicMock()
        mock_instance.remove_item = MagicMock()
        mock_instance.update_item_quantity = MagicMock()
        mock_instance.total_price = 50.0
        yield mock_instance

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount') as MockDiscount:
        mock_instance = MockDiscount.return_value
        mock_instance.apply_discount = MagicMock()
        yield mock_instance

@pytest.fixture
def mock_apply_promotions():
    with patch('shopping_cart.payments.apply_promotions') as mock_apply:
        yield mock_apply

@pytest.fixture
def mock_get_all_items_from_cart():
    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_all:
        mock_get_all.return_value = [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
        yield mock_get_all

@pytest.fixture(autouse=True)
def setup_mocks(mock_cart, mock_discount, mock_apply_promotions, mock_get_all_items_from_cart):
    # This fixture will automatically apply the mocks to all tests
    pass

# happy_path - test_add_item_success - Test that item is added to cart successfully
def test_add_item_success(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Item added to cart'
    mock_cart.add_item.assert_called_once_with(1, 2, 10.0, 'Apple', 'Fruit', 'regular')

# happy_path - test_remove_item_success - Test that item is removed from cart successfully
def test_remove_item_success(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json['message'] == 'Item removed from cart'
    mock_cart.remove_item.assert_called_once_with(1)

# happy_path - test_update_item_quantity_success - Test that item quantity is updated successfully
def test_update_item_quantity_success(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 5})
    assert response.status_code == 200
    assert response.json['message'] == 'Item quantity updated'
    mock_cart.update_item_quantity.assert_called_once_with(1, 5)

# happy_path - test_get_cart_items - Test that all items are retrieved from cart
def test_get_cart_items(client, mock_get_all_items_from_cart):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json['items'] == [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
    mock_get_all_items_from_cart.assert_called_once_with(mock_cart)

# happy_path - test_calculate_total_price - Test that total price is calculated correctly
def test_calculate_total_price(client, mock_cart):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json['total_price'] == 50.0
    mock_cart.calculate_total_price.assert_called_once()

# happy_path - test_apply_discount_to_cart - Test that discount is applied to the cart
def test_apply_discount_to_cart(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.1, 'min_purchase_amount': 20.0})
    assert response.status_code == 200
    assert response.json['discounted_total'] == 50.0  # Assuming mock_cart.total_price is mocked to 50.0
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# happy_path - test_apply_promotions_to_cart - Test that promotions are applied to the cart
def test_apply_promotions_to_cart(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json['message'] == 'Promotions applied'
    mock_apply_promotions.assert_called_once_with(mock_cart, [Promotion('Spring Sale', 0.10), Promotion('Black Friday', 0.25)])

# edge_case - test_add_item_zero_quantity - Test adding item with zero quantity
def test_add_item_zero_quantity(client, mock_cart):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Item added to cart'
    mock_cart.add_item.assert_called_once_with(1, 0, 10.0, 'Apple', 'Fruit', 'regular')

# edge_case - test_remove_nonexistent_item - Test removing item not in cart
def test_remove_nonexistent_item(client, mock_cart):
    response = client.post('/remove_item', json={'item_id': 99})
    assert response.status_code == 200
    assert response.json['message'] == 'Item removed from cart'
    mock_cart.remove_item.assert_called_once_with(99)

# edge_case - test_update_item_quantity_to_zero - Test updating item quantity to zero
def test_update_item_quantity_to_zero(client, mock_cart):
    response = client.post('/update_item_quantity', json={'item_id': 1, 'new_quantity': 0})
    assert response.status_code == 200
    assert response.json['message'] == 'Item quantity updated'
    mock_cart.update_item_quantity.assert_called_once_with(1, 0)

# edge_case - test_apply_zero_discount - Test applying discount with zero rate
def test_apply_zero_discount(client, mock_cart, mock_discount):
    response = client.post('/apply_discount', json={'discount_rate': 0.0, 'min_purchase_amount': 20.0})
    assert response.status_code == 200
    assert response.json['discounted_total'] == 50.0  # Assuming mock_cart.total_price is mocked to 50.0
    mock_discount.return_value.apply_discount.assert_called_once_with(mock_cart)

# edge_case - test_apply_no_promotions - Test applying promotions with no active promotions
def test_apply_no_promotions(client, mock_cart, mock_apply_promotions):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json['message'] == 'Promotions applied'
    mock_apply_promotions.assert_called_once_with(mock_cart, [Promotion('Spring Sale', 0.10), Promotion('Black Friday', 0.25)])

