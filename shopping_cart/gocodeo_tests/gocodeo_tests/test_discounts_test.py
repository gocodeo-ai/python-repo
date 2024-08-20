import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.total_price = 120.0
    cart.items = [{'price': 50.0}, {'price': 25.0}]
    cart.user_type = 'regular'
    return cart

@pytest.fixture
def discount():
    discount = MagicMock()
    discount.apply_discount = MagicMock()
    discount.apply_bulk_discount = MagicMock()
    discount.apply_seasonal_discount = MagicMock()
    discount.apply_category_discount = MagicMock()
    discount.apply_loyalty_discount = MagicMock()
    discount.apply_flash_sale_discount = MagicMock()
    return discount# happy_path - apply_discount - Apply discount for a regular user with total price above minimum purchase amount
def test_apply_discount_regular_user(mock_cart, discount):
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 110.0

# happy_path - apply_bulk_discount - Apply bulk discount for items that meet the quantity requirement
def test_apply_bulk_discount(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=1, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 40.0
    assert mock_cart.items[1]['price'] == 25

# happy_path - apply_seasonal_discount - Apply seasonal discount during holiday season
def test_apply_seasonal_discount(mock_cart, discount):
    total_price = discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.1)
    assert total_price == 90.0

# happy_path - apply_category_discount - Apply category discount to clothing items
def test_apply_category_discount(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='clothing', category_discount_rate=0.1)
    assert mock_cart.items[1]['price'] == 22.5

# happy_path - apply_loyalty_discount - Apply loyalty discount for a loyal user with more than 2 years loyalty
def test_apply_loyalty_discount(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    total_price = discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.15)
    assert total_price == 85.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount to items on sale
def test_apply_flash_sale_discount(mock_cart, discount):
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=[1])
    assert mock_cart.items[0]['price'] == 35.0

# edge_case - apply_discount - Apply discount when total price is below minimum purchase amount
def test_apply_discount_below_minimum(mock_cart, discount):
    mock_cart.calculate_total_price = MagicMock(return_value=40)
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 100.0

# edge_case - apply_bulk_discount - Apply bulk discount when no items meet the quantity requirement
def test_apply_bulk_discount_no_items(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=10, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 50

# edge_case - apply_seasonal_discount - Apply seasonal discount with invalid season
def test_apply_seasonal_discount_invalid_season(mock_cart, discount):
    total_price = discount.apply_seasonal_discount(mock_cart, season='winter', seasonal_discount_rate=0.1)
    assert total_price == 100.0

# edge_case - apply_category_discount - Apply category discount when no items match the category
def test_apply_category_discount_no_match(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='toys', category_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 50

# edge_case - apply_loyalty_discount - Apply loyalty discount for a user not meeting loyalty years requirement
def test_apply_loyalty_discount_not_loyal(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    total_price = discount.apply_loyalty_discount(mock_cart, loyalty_years=1, loyalty_discount_rate=0.15)
    assert total_price == 100.0

# edge_case - apply_flash_sale_discount - Apply flash sale discount when no items are on sale
def test_apply_flash_sale_discount_no_sale_items(mock_cart, discount):
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=[])
    assert mock_cart.items[0]['price'] == 50

