import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=150)
    cart.user_type = "regular"
    cart.items = [{'category': 'books', 'price': 50}, {'category': 'clothing', 'price': 100}]
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=100)

@pytest.fixture
def mock_cart_bulk():
    cart_bulk = MagicMock()
    cart_bulk.items = [{'quantity': 10, 'price': 20}, {'quantity': 5, 'price': 15}]
    return cart_bulk

@pytest.fixture
def mock_cart_seasonal():
    cart_seasonal = MagicMock()
    cart_seasonal.calculate_total_price = MagicMock(return_value=200)
    return cart_seasonal

@pytest.fixture
def mock_cart_category():
    cart_category = MagicMock()
    cart_category.items = [{'category': 'electronics', 'price': 100}, {'category': 'books', 'price': 50}]
    return cart_category

@pytest.fixture
def mock_cart_loyalty():
    cart_loyalty = MagicMock()
    cart_loyalty.calculate_total_price = MagicMock(return_value=300)
    cart_loyalty.user_type = "loyal"
    return cart_loyalty

@pytest.fixture
def mock_cart_flash_sale():
    cart_flash_sale = MagicMock()
    cart_flash_sale.items = [{'item_id': 1, 'price': 100}, {'item_id': 2, 'price': 200}]
    return cart_flash_sale

# happy path - apply_discount - Test that discount is applied correctly when total price is above minimum purchase amount.
def test_apply_discount_above_min_purchase(mock_cart, discount):
    result = discount.apply_discount(mock_cart)
    assert result == 165.0
    assert mock_cart.total_price == 165.0


# happy path - apply_bulk_discount - Test that bulk discount is applied to items meeting the quantity threshold.
def test_apply_bulk_discount(mock_cart_bulk, discount):
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=10, bulk_discount_rate=0.2)
    assert mock_cart_bulk.items[0]['price'] == 16.0
    assert mock_cart_bulk.items[1]['price'] == 15


# happy path - apply_seasonal_discount - Test that seasonal discount is applied during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart_seasonal, discount):
    result = discount.apply_seasonal_discount(mock_cart_seasonal, season='holiday', seasonal_discount_rate=0.25)
    assert result == 150.0
    assert mock_cart_seasonal.total_price == 150.0


# happy path - apply_category_discount - Test that category discount is applied to electronics.
def test_apply_category_discount_electronics(mock_cart_category, discount):
    discount.apply_category_discount(mock_cart_category, category='electronics', category_discount_rate=0.1)
    assert mock_cart_category.items[0]['price'] == 90.0
    assert mock_cart_category.items[1]['price'] == 50


# happy path - apply_loyalty_discount - Test that loyalty discount is applied to loyal users with more than 2 years.
def test_apply_loyalty_discount(mock_cart_loyalty, discount):
    result = discount.apply_loyalty_discount(mock_cart_loyalty, loyalty_years=3, loyalty_discount_rate=0.15)
    assert result == 255.0
    assert mock_cart_loyalty.total_price == 255.0


# happy path - apply_flash_sale_discount - Test that flash sale discount is applied to specific items on sale.
def test_apply_flash_sale_discount(mock_cart_flash_sale, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.3, items_on_sale=[1])
    assert mock_cart_flash_sale.items[0]['price'] == 70.0
    assert mock_cart_flash_sale.items[1]['price'] == 200


# edge case - apply_discount - Test that no discount is applied when total price is below minimum purchase amount.
def test_apply_discount_below_min_purchase(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 50
    result = discount.apply_discount(mock_cart)
    assert result == 50.0
    assert mock_cart.total_price == 50.0


# edge case - apply_bulk_discount - Test that no bulk discount is applied if quantity is just below threshold.
def test_apply_bulk_discount_below_threshold(mock_cart_bulk, discount):
    mock_cart_bulk.items = [{'quantity': 9, 'price': 20}]
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=10, bulk_discount_rate=0.2)
    assert mock_cart_bulk.items[0]['price'] == 20.0


# edge case - apply_seasonal_discount - Test that seasonal discount is not applied during non-holiday season.
def test_apply_seasonal_discount_non_holiday(mock_cart_seasonal, discount):
    result = discount.apply_seasonal_discount(mock_cart_seasonal, season='winter', seasonal_discount_rate=0.25)
    assert result == 200.0
    assert mock_cart_seasonal.total_price == 200.0


# edge case - apply_category_discount - Test that category discount is not applied to non-target category.
def test_apply_category_discount_non_target_category(mock_cart_category, discount):
    discount.apply_category_discount(mock_cart_category, category='electronics', category_discount_rate=0.1)
    assert mock_cart_category.items[0]['price'] == 90.0
    assert mock_cart_category.items[1]['price'] == 50


# edge case - apply_loyalty_discount - Test that loyalty discount is not applied to loyal users with less than 3 years.
def test_apply_loyalty_discount_below_years(mock_cart_loyalty, discount):
    result = discount.apply_loyalty_discount(mock_cart_loyalty, loyalty_years=2, loyalty_discount_rate=0.15)
    assert result == 300.0
    assert mock_cart_loyalty.total_price == 300.0


# edge case - apply_flash_sale_discount - Test that flash sale discount is not applied to items not on sale.
def test_apply_flash_sale_discount_not_on_sale(mock_cart_flash_sale, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.3, items_on_sale=[2])
    assert mock_cart_flash_sale.items[0]['price'] == 100.0
    assert mock_cart_flash_sale.items[1]['price'] == 200


