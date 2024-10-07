import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from shopping_cart.cart import Cart
from shopping_cart.discounts import Discount
from shopping_cart.payments import apply_promotions, Promotion
from shopping_cart.utils import get_all_items_from_cart

@pytest.fixture
def app():
    app = Flask(__name__)

    # Mock the Cart class
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 50.0
        mock_cart_instance.total_price = 50.0
        mock_cart_instance.add_item.return_value = None
        mock_cart_instance.remove_item.return_value = None
        mock_cart_instance.update_item_quantity.return_value = None
        
        # Mock the Discount class
        with patch('shopping_cart.discounts.Discount') as MockDiscount:
            mock_discount_instance = MockDiscount.return_value
            mock_discount_instance.apply_discount.return_value = None
            
            # Mock the apply_promotions function
            with patch('shopping_cart.payments.apply_promotions') as mock_apply_promotions:
                mock_apply_promotions.return_value = None
                
                # Mock the Promotion class
                with patch('shopping_cart.payments.Promotion') as MockPromotion:
                    mock_promotion_instance = MockPromotion.return_value
                    mock_promotion_instance.name = "Spring Sale"
                    mock_promotion_instance.discount_rate = 0.10
                    
                    # Mock the get_all_items_from_cart function
                    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_all_items:
                        mock_get_all_items.return_value = [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]
                        
                        yield app

@pytest.fixture
def client(app):
    return app.test_client()

# happy_path - add_item - Test that an item is added to the cart with valid data.
def test_add_item_success(client):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Apple',
        'category': 'Fruit'
    })
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Item added to cart'}

# happy_path - remove_item - Test that an item is removed from the cart successfully.
def test_remove_item_success(client):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item removed from cart'}

# happy_path - update_item_quantity - Test that the item quantity is updated successfully in the cart.
def test_update_item_quantity_success(client):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 5
    })
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Item quantity updated'}

# happy_path - get_cart_items - Test that all items in the cart are retrieved successfully.
def test_get_cart_items_success(client):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.get_json() == {'items': [{'item_id': 1, 'quantity': 5, 'price': 10.0, 'name': 'Apple', 'category': 'Fruit'}]}

# happy_path - calculate_total_price - Test that the total price of the cart is calculated correctly.
def test_calculate_total_price_success(client):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.get_json() == {'total_price': 50.0}

# happy_path - apply_discount_to_cart - Test that a discount is applied correctly to the cart.
def test_apply_discount_success(client):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 0
    })
    assert response.status_code == 200
    assert response.get_json() == {'discounted_total': 45.0}

# happy_path - apply_promotions_to_cart - Test that promotions are applied correctly to the cart.
def test_apply_promotions_success(client):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Promotions applied'}

# edge_case - add_item - Test that adding an item with zero quantity fails.
def test_add_item_zero_quantity(client):
    response = client.post('/add_item', json={
        'item_id': 2,
        'quantity': 0,
        'price': 5.0,
        'name': 'Banana',
        'category': 'Fruit'
    })
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Invalid quantity'}

# edge_case - remove_item - Test that removing a non-existent item from the cart fails.
def test_remove_non_existent_item(client):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Item not found'}

# edge_case - update_item_quantity - Test that updating the quantity of a non-existent item fails.
def test_update_quantity_non_existent_item(client):
    response = client.post('/update_item_quantity', json={
        'item_id': 999,
        'new_quantity': 3
    })
    assert response.status_code == 404
    assert response.get_json() == {'message': 'Item not found'}

# edge_case - get_cart_items - Test that retrieving items from an empty cart returns an empty list.
def test_get_cart_items_empty_cart(client):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.get_json() == {'items': []}

# edge_case - calculate_total_price - Test that calculating the total price of an empty cart returns zero.
def test_calculate_total_price_empty_cart(client):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.get_json() == {'total_price': 0.0}

# edge_case - apply_discount_to_cart - Test that applying a discount with a negative rate fails.
def test_apply_negative_discount_rate(client):
    response = client.post('/apply_discount', json={
        'discount_rate': -0.1,
        'min_purchase_amount': 0
    })
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Invalid discount rate'}

