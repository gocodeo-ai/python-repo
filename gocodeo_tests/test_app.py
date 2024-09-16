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
    
    # Mocking the Cart class
    with patch('shopping_cart.cart.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price.return_value = 20.0
        mock_cart_instance.total_price = 20.0
        mock_cart_instance.add_item = MagicMock()
        mock_cart_instance.remove_item = MagicMock()
        mock_cart_instance.update_item_quantity = MagicMock()
        
        # Mocking the Discount class
        with patch('shopping_cart.discounts.Discount') as MockDiscount:
            mock_discount_instance = MockDiscount.return_value
            mock_discount_instance.apply_discount = MagicMock()

            # Mocking the apply_promotions function
            with patch('shopping_cart.payments.apply_promotions') as mock_apply_promotions:
                mock_apply_promotions.return_value = None

                # Mocking the Promotion class
                with patch('shopping_cart.payments.Promotion') as MockPromotion:
                    mock_promotion_instance = MockPromotion.return_value
                    mock_promotion_instance.name = "Spring Sale"
                    mock_promotion_instance.discount = 0.10
                    
                    # Mocking the get_all_items_from_cart function
                    with patch('shopping_cart.utils.get_all_items_from_cart') as mock_get_all_items_from_cart:
                        mock_get_all_items_from_cart.return_value = [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Test Item', 'category': 'Electronics'}]
                        
                        yield app

def test_add_item_success(client, app):
    # Test implementation will go here
    pass

def test_remove_item_success(client, app):
    # Test implementation will go here
    pass

def test_update_item_quantity_success(client, app):
    # Test implementation will go here
    pass

def test_get_cart_items_success(client, app):
    # Test implementation will go here
    pass

def test_calculate_total_price_success(client, app):
    # Test implementation will go here
    pass

def test_apply_discount_success(client, app):
    # Test implementation will go here
    pass

def test_apply_promotions_success(client, app):
    # Test implementation will go here
    pass

# happy_path - test_add_item_success - Test that an item is added to the cart successfully.
def test_add_item_success(client, app):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 2,
        'price': 10.0,
        'name': 'Test Item',
        'category': 'Electronics'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Item added to cart'}

# happy_path - test_remove_item_success - Test that an item is removed from the cart successfully.
def test_remove_item_success(client, app):
    response = client.post('/remove_item', json={'item_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Item removed from cart'}

# happy_path - test_update_item_quantity_success - Test that the item quantity is updated successfully in the cart.
def test_update_item_quantity_success(client, app):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 5
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Item quantity updated'}

# happy_path - test_get_cart_items_success - Test that all items in the cart are retrieved successfully.
def test_get_cart_items_success(client, app):
    response = client.get('/get_cart_items')
    assert response.status_code == 200
    assert response.json == {
        'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Test Item', 'category': 'Electronics'}]
    }

# happy_path - test_calculate_total_price_success - Test that the total price of the cart is calculated correctly.
def test_calculate_total_price_success(client, app):
    response = client.get('/calculate_total_price')
    assert response.status_code == 200
    assert response.json == {'total_price': 20.0}

# happy_path - test_apply_discount_success - Test that a discount is applied to the cart successfully.
def test_apply_discount_success(client, app):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 0.0
    })
    assert response.status_code == 200
    assert response.json == {'discounted_total': 18.0}

# happy_path - test_apply_promotions_success - Test that promotions are applied to the cart successfully.
def test_apply_promotions_success(client, app):
    response = client.post('/apply_promotions')
    assert response.status_code == 200
    assert response.json == {'message': 'Promotions applied'}

# edge_case - test_add_item_zero_quantity - Test adding an item with zero quantity to the cart.
def test_add_item_zero_quantity(client, app):
    response = client.post('/add_item', json={
        'item_id': 1,
        'quantity': 0,
        'price': 10.0,
        'name': 'Test Item',
        'category': 'Electronics'
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}

# edge_case - test_remove_nonexistent_item - Test removing an item that is not in the cart.
def test_remove_nonexistent_item(client, app):
    response = client.post('/remove_item', json={'item_id': 999})
    assert response.status_code == 404
    assert response.json == {'error': 'Item not found in cart'}

# edge_case - test_update_item_quantity_to_zero - Test updating item quantity to zero in the cart.
def test_update_item_quantity_to_zero(client, app):
    response = client.post('/update_item_quantity', json={
        'item_id': 1,
        'new_quantity': 0
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Quantity must be greater than zero'}

# edge_case - test_get_cart_items_empty_cart - Test retrieving items from an empty cart.
def test_get_cart_items_empty_cart(client, app):
    with patch('shopping_cart.utils.get_all_items_from_cart', return_value=[]):
        response = client.get('/get_cart_items')
        assert response.status_code == 200
        assert response.json == {'items': []}

# edge_case - test_calculate_total_price_empty_cart - Test calculating total price of an empty cart.
def test_calculate_total_price_empty_cart(client, app):
    with patch('shopping_cart.cart.Cart.calculate_total_price', return_value=0.0):
        response = client.get('/calculate_total_price')
        assert response.status_code == 200
        assert response.json == {'total_price': 0.0}

# edge_case - test_apply_discount_high_minimum - Test applying a discount with a higher minimum purchase amount than the cart total.
def test_apply_discount_high_minimum(client, app):
    response = client.post('/apply_discount', json={
        'discount_rate': 0.1,
        'min_purchase_amount': 100.0
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Minimum purchase amount not reached'}

# edge_case - test_apply_promotions_no_applicable - Test applying promotions when no applicable promotions exist.
def test_apply_promotions_no_applicable(client, app):
    with patch('shopping_cart.payments.apply_promotions', return_value=None):
        response = client.post('/apply_promotions')
        assert response.status_code == 200
        assert response.json == {'message': 'No applicable promotions'}

