import pytest
from unittest.mock import MagicMock

@pytest.fixture
def cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=1000)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 2, "price": 50},
    ]
    cart.total_price = 1000
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=500)

@pytest.fixture
def bulk_discount_cart():
    cart = MagicMock()
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 5, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 10, "price": 50},
    ]
    return cart

@pytest.fixture
def seasonal_discount_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=2000)
    cart.total_price = 2000
    return cart

@pytest.fixture
def category_discount_cart():
    cart = MagicMock()
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 2, "price": 50},
    ]
    return cart

@pytest.fixture
def loyalty_discount_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=1500)
    cart.user_type = "loyal"
    cart.total_price = 1500
    return cart

@pytest.fixture
def flash_sale_cart():
    cart = MagicMock()
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 2, "price": 50},
    ]
    return cart# happy_path - apply_discount - Apply discount to a regular user with total price above minimum purchase amount
def test_apply_discount_regular(cart, discount):
    cart.user_type = 'regular'
    total = discount.apply_discount(cart)
    assert total == 1100.0

# happy_path - apply_discount - Apply discount to a premium user with electronics in cart
def test_apply_discount_premium(cart, discount):
    cart.user_type = 'premium'
    cart.items[0]['category'] = 'electronics'
    total = discount.apply_discount(cart)
    assert total == 1150.0

# happy_path - apply_bulk_discount - Apply bulk discount to items in cart
def test_apply_bulk_discount(bulk_discount_cart, discount):
    discount.apply_bulk_discount(bulk_discount_cart, 5, 0.2)
    assert bulk_discount_cart.items[0]['price'] == 80.0
    assert bulk_discount_cart.items[1]['price'] == 50

# happy_path - apply_seasonal_discount - Apply holiday seasonal discount
def test_apply_seasonal_discount(seasonal_discount_cart, discount):
    total = discount.apply_seasonal_discount(seasonal_discount_cart, 'holiday', 0.1)
    assert total == 1800.0

# happy_path - apply_category_discount - Apply category discount to electronics
def test_apply_category_discount(category_discount_cart, discount):
    discount.apply_category_discount(category_discount_cart, 'electronics', 0.2)
    assert category_discount_cart.items[0]['price'] == 80.0

# happy_path - apply_loyalty_discount - Apply loyalty discount for a loyal user
def test_apply_loyalty_discount(loyalty_discount_cart, discount):
    total = discount.apply_loyalty_discount(loyalty_discount_cart, 3, 0.15)
    assert total == 1275.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount to items on sale
def test_apply_flash_sale_discount(flash_sale_cart, discount):
    discount.apply_flash_sale_discount(flash_sale_cart, 0.3, [1])
    assert flash_sale_cart.items[0]['price'] == 70.0

# happy_path - apply_flash_sale_discount - No flash sale discount applied to items not on sale
def test_apply_flash_sale_discount_no_discount(flash_sale_cart, discount):
    discount.apply_flash_sale_discount(flash_sale_cart, 0.3, [3])
    assert flash_sale_cart.items[0]['price'] == 100.0

