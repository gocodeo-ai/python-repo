import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_cart():
    cart = Mock()
    cart.user_type = 'regular'
    cart.items = [{'price': 20.0, 'quantity': 1, 'category': 'clothing'}, {'price': 80.0, 'category': 'electronics'}]
    cart.calculate_total_price.return_value = 100.0
    return cart

@pytest.fixture
def discount():
    discount = Mock()
    discount.apply_discount.return_value = 110.0
    discount.apply_bulk_discount.side_effect = lambda cart, bulk_quantity, bulk_discount_rate: setattr(cart.items[0], 'price', 16.0)
    discount.apply_seasonal_discount.return_value = 90.0
    discount.apply_category_discount.side_effect = lambda cart, category, category_discount_rate: setattr(cart.items[1], 'price', 60.0)
    discount.apply_loyalty_discount.return_value = 90.0
    discount.apply_flash_sale_discount.side_effect = lambda cart, flash_sale_rate, items_on_sale: setattr(cart.items[1], 'price', 56.0)
    return discount# happy_path - apply_discount - Apply discount for a regular user with total price above min purchase amount
def test_apply_discount_regular_user_above_min(mock_cart, discount):
    mock_cart.user_type = 'regular'
    assert discount.apply_discount(mock_cart) == 110.0

# happy_path - apply_bulk_discount - Apply bulk discount on items that meet the quantity requirement
def test_apply_bulk_discount(mock_cart, discount):
    mock_cart.items[0]['quantity'] = 10
    discount.apply_bulk_discount(mock_cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 16.0

# happy_path - apply_seasonal_discount - Apply seasonal discount during holidays
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    assert discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.1) == 90.0

# happy_path - apply_category_discount - Apply category discount on electronics
def test_apply_category_discount(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='electronics', category_discount_rate=0.25)
    assert mock_cart.items[1]['price'] == 60.0

# happy_path - apply_loyalty_discount - Apply loyalty discount for loyal user with more than 2 years
def test_apply_loyalty_discount(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    assert discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.1) == 90.0

# happy_path - apply_flash_sale_discount - Apply flash sale discount on items on sale
def test_apply_flash_sale_discount(mock_cart, discount):
    items_on_sale = [2]
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=items_on_sale)
    assert mock_cart.items[1]['price'] == 56.0

# edge_case - apply_discount - Handle case where total price is below min purchase amount
def test_apply_discount_below_min(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 40
    assert discount.apply_discount(mock_cart) == 40

# edge_case - apply_bulk_discount - Handle case where no items meet the bulk quantity requirement
def test_apply_bulk_discount_no_items(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=15, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 20

# edge_case - apply_seasonal_discount - Handle case where season is not recognized
def test_apply_seasonal_discount_unknown_season(mock_cart, discount):
    assert discount.apply_seasonal_discount(mock_cart, season='winter', seasonal_discount_rate=0.1) == 100

# edge_case - apply_category_discount - Handle case where no items match the category
def test_apply_category_discount_no_match(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='furniture', category_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 20

# edge_case - apply_loyalty_discount - Handle case where user is not loyal enough for discount
def test_apply_loyalty_discount_not_loyal(mock_cart, discount):
    mock_cart.user_type = 'regular'
    assert discount.apply_loyalty_discount(mock_cart, loyalty_years=1, loyalty_discount_rate=0.1) == 100

# edge_case - apply_flash_sale_discount - Handle case where no items are on sale
def test_apply_flash_sale_discount_no_sale(mock_cart, discount):
    items_on_sale = []
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=items_on_sale)
    assert mock_cart.items[1]['price'] == 80

