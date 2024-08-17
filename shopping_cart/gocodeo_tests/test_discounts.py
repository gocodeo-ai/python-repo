import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.calculate_total_price = Mock(return_value=100)
    cart.user_type = "regular"
    cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 100},
        {"item_id": 2, "category": "clothing", "quantity": 2, "price": 50},
    ]
    cart.total_price = 200
    return cart

@pytest.fixture
def discount():
    return Discount(0.1, min_purchase_amount=50)

@pytest.fixture
def bulk_discount():
    return Discount(0.1)

@pytest.fixture
def seasonal_discount():
    return Discount(0.1)

@pytest.fixture
def category_discount():
    return Discount(0.1)

@pytest.fixture
def loyalty_discount():
    return Discount(0.1)

@pytest.fixture
def flash_sale_discount():
    return Discount(0.1)# happy_path - apply_discount - Apply discount for regular user with total price above minimum purchase amount
def test_apply_discount_regular_user_above_minimum(discount, mock_cart):
    mock_cart.user_type = 'regular'
    assert discount.apply_discount(mock_cart) == 110.0

# happy_path - apply_discount - Apply discount for premium user with electronics in cart
def test_apply_discount_premium_user_with_electronics(discount, mock_cart):
    mock_cart.user_type = 'premium'
    mock_cart.items[0]['category'] = 'electronics'
    assert discount.apply_discount(mock_cart) == 115.0

# happy_path - apply_bulk_discount - Apply bulk discount on items that meet quantity criteria
def test_apply_bulk_discount(discount, bulk_discount, mock_cart):
    mock_cart.items[0]['quantity'] = 10
    bulk_discount.apply_bulk_discount(mock_cart, 5, 0.2)
    assert mock_cart.items[0]['price'] == 80.0

# happy_path - apply_seasonal_discount - Apply seasonal discount during holiday season
def test_apply_seasonal_discount_holiday(seasonal_discount, mock_cart):
    assert seasonal_discount.apply_seasonal_discount(mock_cart, 'holiday', 0.2) == 80.0

# happy_path - apply_category_discount - Apply category discount to specific category items
def test_apply_category_discount(discount, category_discount, mock_cart):
    category_discount.apply_category_discount(mock_cart, 'clothing', 0.1)
    assert mock_cart.items[1]['price'] == 45.0

# happy_path - apply_loyalty_discount - Apply loyalty discount for loyal user with sufficient loyalty years
def test_apply_loyalty_discount(discount, loyalty_discount, mock_cart):
    mock_cart.user_type = 'loyal'
    assert loyalty_discount.apply_loyalty_discount(mock_cart, 3, 0.15) == 85.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount on items in the sale list
def test_apply_flash_sale_discount(flash_sale_discount, mock_cart):
    flash_sale_discount.apply_flash_sale_discount(mock_cart, 0.3, [1])
    assert mock_cart.items[0]['price'] == 70.0

# edge_case - apply_discount - Apply discount when total price is below minimum purchase amount
def test_apply_discount_below_minimum(discount, mock_cart):
    mock_cart.calculate_total_price = Mock(return_value=30)
    assert discount.apply_discount(mock_cart) == 30.0

# edge_case - apply_bulk_discount - No bulk discount applied when quantity is below criteria
def test_apply_bulk_discount_no_discount(discount, bulk_discount, mock_cart):
    mock_cart.items[0]['quantity'] = 2
    bulk_discount.apply_bulk_discount(mock_cart, 5, 0.2)
    assert mock_cart.items[0]['price'] == 100.0

# edge_case - apply_seasonal_discount - Apply seasonal discount with invalid season
def test_apply_seasonal_discount_invalid_season(seasonal_discount, mock_cart):
    assert seasonal_discount.apply_seasonal_discount(mock_cart, 'winter', 0.2) == 100.0

# edge_case - apply_category_discount - No category discount applied when category does not match
def test_apply_category_discount_no_discount(discount, category_discount, mock_cart):
    category_discount.apply_category_discount(mock_cart, 'furniture', 0.1)
    assert mock_cart.items[0]['price'] == 100.0

# edge_case - apply_loyalty_discount - No loyalty discount applied for non-loyal user
def test_apply_loyalty_discount_non_loyal_user(discount, loyalty_discount, mock_cart):
    mock_cart.user_type = 'regular'
    assert loyalty_discount.apply_loyalty_discount(mock_cart, 3, 0.15) == 100.0

# edge_case - apply_flash_sale_discount - No flash sale discount applied when item not on sale
def test_apply_flash_sale_discount_no_discount(flash_sale_discount, mock_cart):
    flash_sale_discount.apply_flash_sale_discount(mock_cart, 0.3, [3])
    assert mock_cart.items[0]['price'] == 100.0

