import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_cart():
    mock_cart = Mock()
    mock_cart.calculate_total_price = Mock(return_value=100)
    mock_cart.user_type = "regular"
    mock_cart.items = [
        {"item_id": 1, "category": "electronics", "quantity": 1, "price": 50},
        {"item_id": 2, "category": "clothing", "quantity": 2, "price": 25},
    ]
    mock_cart.total_price = 100
    return mock_cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

# happy_path - test_apply_discount_regular_user - Test apply_discount method for a regular user with total price above min_purchase_amount.
def test_apply_discount_regular_user(mock_cart, discount):
    result = discount.apply_discount(mock_cart)
    assert result == 110.0

# happy_path - test_apply_bulk_discount - Test apply_bulk_discount method where item quantity meets bulk quantity requirement.
def test_apply_bulk_discount(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=2, bulk_discount_rate=0.2)
    assert mock_cart.items[1]['price'] == 20.0

# happy_path - test_apply_seasonal_discount_holiday - Test apply_seasonal_discount method during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    result = discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.15)
    assert result == 85.0

# happy_path - test_apply_category_discount_electronics - Test apply_category_discount method for electronics category.
def test_apply_category_discount_electronics(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='electronics', category_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 45.0

# happy_path - test_apply_loyalty_discount - Test apply_loyalty_discount method for loyal user with more than 2 loyalty years.
def test_apply_loyalty_discount(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    result = discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert result == 90.0

# edge_case - test_apply_discount_below_min_purchase - Test apply_discount method for total price below min_purchase_amount.
def test_apply_discount_below_min_purchase(mock_cart, discount):
    mock_cart.calculate_total_price = Mock(return_value=40)
    result = discount.apply_discount(mock_cart)
    assert result == 40.0

# edge_case - test_apply_bulk_discount_no_qualifying_items - Test apply_bulk_discount method where no item quantity meets bulk quantity requirement.
def test_apply_bulk_discount_no_qualifying_items(mock_cart, discount):
    discount.apply_bulk_discount(mock_cart, bulk_quantity=3, bulk_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 50.0

# edge_case - test_apply_seasonal_discount_non_holiday - Test apply_seasonal_discount method during non-holiday season.
def test_apply_seasonal_discount_non_holiday(mock_cart, discount):
    result = discount.apply_seasonal_discount(mock_cart, season='winter', seasonal_discount_rate=0.15)
    assert result == 100.0

# edge_case - test_apply_category_discount_non_existing_category - Test apply_category_discount method for a non-existing category.
def test_apply_category_discount_non_existing_category(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='toys', category_discount_rate=0.2)
    assert mock_cart.items[0]['price'] == 50.0

# edge_case - test_apply_flash_sale_discount_no_items_on_sale - Test apply_flash_sale_discount method where no items are on sale.
def test_apply_flash_sale_discount_no_items_on_sale(mock_cart, discount):
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.3, items_on_sale=[3])
    assert mock_cart.items[0]['price'] == 50.0

