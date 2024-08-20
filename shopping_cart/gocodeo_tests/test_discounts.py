import pytest
from unittest.mock import MagicMock

@pytest.fixture
def cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=100)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 2, "price": 50}
    ]
    cart.total_price = 200
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)# happy_path - apply_discount - Apply discount for a regular user with total price above min purchase amount
def test_apply_discount_regular_user(cart, discount):
    cart.user_type = 'regular'
    assert discount.apply_discount(cart) == 110.0

# happy_path - apply_bulk_discount - Apply bulk discount for items in the cart
def test_apply_bulk_discount(cart, discount):
    cart.items[0]['quantity'] = 5  # Bulk quantity
    discount.apply_bulk_discount(cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 80.0

# happy_path - apply_seasonal_discount - Apply seasonal discount for holiday season
def test_apply_seasonal_discount(cart, discount):
    assert discount.apply_seasonal_discount(cart, season='holiday', seasonal_discount_rate=0.1) == 90.0

# happy_path - apply_category_discount - Apply category discount to clothing items
def test_apply_category_discount(cart, discount):
    discount.apply_category_discount(cart, category='clothing', category_discount_rate=0.3)
    assert cart.items[1]['price'] == 35.0

# happy_path - apply_loyalty_discount - Apply loyalty discount for loyal user with more than 2 years
def test_apply_loyalty_discount(cart, discount):
    cart.user_type = 'loyal'
    assert discount.apply_loyalty_discount(cart, loyalty_years=3, loyalty_discount_rate=0.15) == 85.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount on specific items
def test_apply_flash_sale_discount(cart, discount):
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.25, items_on_sale=[1])
    assert cart.items[0]['price'] == 75.0

# edge_case - apply_discount - Apply discount when total price is below min purchase amount
def test_apply_discount_below_min_purchase(cart, discount):
    cart.calculate_total_price = MagicMock(return_value=40)
    assert discount.apply_discount(cart) == 40.0

# edge_case - apply_bulk_discount - No bulk discount applied when quantity is below bulk quantity
def test_apply_bulk_discount_no_discount(cart, discount):
    cart.items[0]['quantity'] = 2  # Below bulk quantity
    discount.apply_bulk_discount(cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert cart.items[0]['price'] == 100

# edge_case - apply_seasonal_discount - Apply seasonal discount for summer season
def test_apply_seasonal_discount_summer(cart, discount):
    assert discount.apply_seasonal_discount(cart, season='summer', seasonal_discount_rate=0.2) == 90.0

# edge_case - apply_category_discount - No category discount applied if item category does not match
def test_apply_category_discount_no_match(cart, discount):
    discount.apply_category_discount(cart, category='toys', category_discount_rate=0.3)
    assert cart.items[0]['price'] == 100

# edge_case - apply_loyalty_discount - No loyalty discount for non-loyal user
def test_apply_loyalty_discount_no_discount(cart, discount):
    cart.user_type = 'regular'
    assert discount.apply_loyalty_discount(cart, loyalty_years=1, loyalty_discount_rate=0.1) == 100

# edge_case - apply_flash_sale_discount - No flash sale discount applied if item is not on sale
def test_apply_flash_sale_discount_no_sale(cart, discount):
    discount.apply_flash_sale_discount(cart, flash_sale_rate=0.2, items_on_sale=[3])
    assert cart.items[0]['price'] == 100

