import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=100)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 2, "price": 50}
    ]
    cart.total_price = 100
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def mock_cart_premium():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=150)
    cart.user_type = "premium"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 150},
        {"item_id": 2, "category": "clothing", "quantity": 3, "price": 50}
    ]
    cart.total_price = 150
    return cart

@pytest.fixture
def mock_cart_loyal():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=200)
    cart.user_type = "loyal"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 2, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 4, "price": 25}
    ]
    cart.total_price = 200
    return cart

@pytest.fixture
def mock_cart_bulk():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=300)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 10, "price": 30},
        {"item_id": 2, "category": "clothing", "quantity": 5, "price": 20}
    ]
    cart.total_price = 300
    return cart

@pytest.fixture
def mock_cart_flash_sale():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=400)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 4, "price": 75}
    ]
    cart.total_price = 400
    return cart

@pytest.fixture
def mock_cart_seasonal():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=500)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 2, "price": 200},
        {"item_id": 2, "category": "clothing", "quantity": 6, "price": 50}
    ]
    cart.total_price = 500
    return cart

@pytest.fixture
def mock_cart_category():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=600)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 3, "price": 150},
        {"item_id": 2, "category": "clothing", "quantity": 8, "price": 75}
    ]
    cart.total_price = 600
    return cart# happy_path - apply_discount - Apply discount to a regular user with total price above min purchase amount
def test_apply_discount_regular(mock_cart, discount):
    assert discount.apply_discount(mock_cart) == 110.0

# happy_path - apply_discount - Apply discount to a premium user with electronics in cart
def test_apply_discount_premium(mock_cart_premium, discount):
    assert discount.apply_discount(mock_cart_premium) == 225.0

# happy_path - apply_bulk_discount - Apply bulk discount to items in cart
def test_apply_bulk_discount(mock_cart_bulk, discount):
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_bulk.items[0]['price'] == 24.0
    assert mock_cart_bulk.items[1]['price'] == 20

# happy_path - apply_seasonal_discount - Apply seasonal discount for holiday
def test_apply_seasonal_discount(mock_cart_seasonal, discount):
    assert discount.apply_seasonal_discount(mock_cart_seasonal, season='holiday', seasonal_discount_rate=0.1) == 450.0

# happy_path - apply_category_discount - Apply category discount to electronics category
def test_apply_category_discount(mock_cart_category, discount):
    discount.apply_category_discount(mock_cart_category, category='electronics', category_discount_rate=0.1)
    assert mock_cart_category.items[0]['price'] == 135.0

# happy_path - apply_loyalty_discount - Apply loyalty discount for loyal user with more than 2 years
def test_apply_loyalty_discount(mock_cart_loyal, discount):
    assert discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=3, loyalty_discount_rate=0.15) == 170.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount on specific items
def test_apply_flash_sale_discount(mock_cart_flash_sale, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.25, items_on_sale=[1])
    assert mock_cart_flash_sale.items[0]['price'] == 75.0

# edge_case - apply_discount - Apply discount with total price below min purchase amount
def test_apply_discount_below_min_purchase(mock_cart, discount):
    cart = mock_cart
    cart.calculate_total_price = Mock(return_value=40)
    assert discount.apply_discount(cart) == 40

# edge_case - apply_bulk_discount - Apply bulk discount with no items meeting bulk quantity
def test_apply_bulk_discount_no_items(mock_cart_bulk, discount):
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=20, bulk_discount_rate=0.2)
    assert mock_cart_bulk.items[0]['price'] == 30
    assert mock_cart_bulk.items[1]['price'] == 20

# edge_case - apply_seasonal_discount - Apply seasonal discount with invalid season
def test_apply_seasonal_discount_invalid_season(mock_cart_seasonal, discount):
    assert discount.apply_seasonal_discount(mock_cart_seasonal, season='winter', seasonal_discount_rate=0.1) == 500

# edge_case - apply_category_discount - Apply category discount with no matching category
def test_apply_category_discount_no_match(mock_cart_category, discount):
    discount.apply_category_discount(mock_cart_category, category='toys', category_discount_rate=0.1)
    assert mock_cart_category.items[0]['price'] == 150
    assert mock_cart_category.items[1]['price'] == 75

# edge_case - apply_loyalty_discount - Apply loyalty discount for loyal user with less than 2 years
def test_apply_loyalty_discount_not_eligible(mock_cart_loyal, discount):
    assert discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=1, loyalty_discount_rate=0.15) == 200

# edge_case - apply_flash_sale_discount - Apply flash sale discount with no items on sale
def test_apply_flash_sale_discount_no_items_on_sale(mock_cart_flash_sale, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.25, items_on_sale=[]) 
    assert mock_cart_flash_sale.items[0]['price'] == 100
    assert mock_cart_flash_sale.items[1]['price'] == 75

