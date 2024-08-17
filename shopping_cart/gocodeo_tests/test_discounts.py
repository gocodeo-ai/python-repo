import pytest
from unittest.mock import Mock

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
    return Discount(discount_rate=0.1, min_purchase_amount=50)# happy_path - apply_discount - Apply discount to a regular user with total price above minimum purchase amount
def test_apply_discount_regular_user_above_minimum(discount, mock_cart):
    mock_cart.user_type = 'regular'
    total = discount.apply_discount(mock_cart)
    assert total == 110.0  # 100 * (1 + 0.1)

# happy_path - apply_discount - Apply discount to a premium user with electronics in the cart
def test_apply_discount_premium_user_with_electronics(discount, mock_cart):
    mock_cart.user_type = 'premium'
    total = discount.apply_discount(mock_cart)
    assert total == 115.0  # 100 + (0.1 * 1.5) 

# happy_path - apply_bulk_discount - Apply bulk discount to items in the cart
def test_apply_bulk_discount(discount, mock_cart):
    mock_cart.items = [
        {'item_id': 1, 'category': 'electronics', 'quantity': 5, 'price': 100},
        {'item_id': 2, 'category': 'clothing', 'quantity': 2, 'price': 50}
    ]
    discount.apply_bulk_discount(mock_cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 80.0  # 100 * (1 - 0.2)

# happy_path - apply_seasonal_discount - Apply holiday seasonal discount to the cart
def test_apply_seasonal_discount_holiday(discount, mock_cart):
    total = discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.1)
    assert total == 90.0  # 100 * (1 - 0.1)

# happy_path - apply_category_discount - Apply category discount to clothing items in the cart
def test_apply_category_discount(discount, mock_cart):
    discount.apply_category_discount(mock_cart, category='clothing', category_discount_rate=0.15)
    assert mock_cart.items[1]['price'] == 42.5  # 50 * (1 - 0.15)

# happy_path - apply_loyalty_discount - Apply loyalty discount for a loyal user with more than 2 years of loyalty
def test_apply_loyalty_discount(discount, mock_cart):
    mock_cart.user_type = 'loyal'
    total = discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert total == 90.0  # 100 * (1 - 0.1)

# happy_path - apply_flash_sale_discount - Apply flash sale discount to items on sale
def test_apply_flash_sale_discount(discount, mock_cart):
    mock_cart.items = [
        {'item_id': 1, 'category': 'electronics', 'quantity': 1, 'price': 100},
        {'item_id': 2, 'category': 'clothing', 'quantity': 2, 'price': 50}
    ]
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=[1])
    assert mock_cart.items[0]['price'] == 70.0  # 100 * (1 - 0.3)

# edge_case - apply_discount - Apply discount when total price is below minimum purchase amount
def test_apply_discount_below_minimum(discount, mock_cart):
    mock_cart.calculate_total_price = Mock(return_value=40)
    total = discount.apply_discount(mock_cart)
    assert total == 40.0  # No discount applied

# edge_case - apply_bulk_discount - No bulk discount applied when quantity is below bulk quantity
def test_apply_bulk_discount_below_quantity(discount, mock_cart):
    mock_cart.items = [
        {'item_id': 1, 'category': 'electronics', 'quantity': 3, 'price': 100},
    ]
    discount.apply_bulk_discount(mock_cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 100.0  # No discount applied

# edge_case - apply_seasonal_discount - Apply seasonal discount during summer
def test_apply_seasonal_discount_summer(discount, mock_cart):
    total = discount.apply_seasonal_discount(mock_cart, season='summer', seasonal_discount_rate=0.2)
    assert total == 90.0  # 100 * (1 - 0.1)

# edge_case - apply_category_discount - No category discount applied when category does not match
def test_apply_category_discount_no_match(discount, mock_cart):
    discount.apply_category_discount(mock_cart, category='toys', category_discount_rate=0.2)
    assert mock_cart.items[1]['price'] == 50.0  # No discount applied

# edge_case - apply_loyalty_discount - No loyalty discount applied for non-loyal user
def test_apply_loyalty_discount_non_loyal(discount, mock_cart):
    mock_cart.user_type = 'regular'
    total = discount.apply_loyalty_discount(mock_cart, loyalty_years=1, loyalty_discount_rate=0.1)
    assert total == 100.0  # No discount applied

# edge_case - apply_flash_sale_discount - No flash sale discount applied when item is not on sale
def test_apply_flash_sale_discount_no_sale(discount, mock_cart):
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=[3])
    assert mock_cart.items[0]['price'] == 100.0  # No discount applied

