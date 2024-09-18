import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=100)
        instance.user_type = 'regular'
        instance.items = [{'category': 'books', 'price': 10}]
        yield instance

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def mock_cart_premium():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=200)
        instance.user_type = 'premium'
        instance.items = [{'category': 'electronics', 'price': 100}]
        yield instance

@pytest.fixture
def mock_cart_bulk():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.items = [{'quantity': 10, 'price': 100}]
        yield instance

@pytest.fixture
def mock_cart_seasonal():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=200)
        yield instance

@pytest.fixture
def mock_cart_category():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.items = [{'category': 'books', 'price': 100}]
        yield instance

@pytest.fixture
def mock_cart_loyalty():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=300)
        instance.user_type = 'loyal'
        yield instance

@pytest.fixture
def mock_cart_flash_sale():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.items = [{'item_id': 1, 'price': 100}]
        yield instance

# happy_path - test_apply_discount_regular_user - Test that discount is applied correctly when total price exceeds minimum purchase amount for regular users.
def test_apply_discount_regular_user(discount, mock_cart):
    expected_total_price = 110  # 100 + 10% of 100
    result = discount.apply_discount(mock_cart)
    assert result == expected_total_price

# happy_path - test_apply_discount_premium_user_electronics - Test that premium users receive enhanced discount on electronics.
def test_apply_discount_premium_user_electronics(discount, mock_cart_premium):
    expected_total_price = 300  # 200 + 1.5 * 10% of 200
    result = discount.apply_discount(mock_cart_premium)
    assert result == expected_total_price

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied correctly when quantity meets bulk requirement.
def test_apply_bulk_discount(discount, mock_cart_bulk):
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=5, bulk_discount_rate=0.1)
    expected_price = 90  # 100 - 10% of 100
    assert mock_cart_bulk.items[0]['price'] == expected_price

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season.
def test_apply_seasonal_discount_holiday(discount, mock_cart_seasonal):
    expected_total_price = 160  # 200 - 20% of 200
    result = discount.apply_seasonal_discount(mock_cart_seasonal, season='holiday', seasonal_discount_rate=0.2)
    assert result == expected_total_price

# happy_path - test_apply_category_discount - Test that category discount is applied to specified category items.
def test_apply_category_discount(discount, mock_cart_category):
    discount.apply_category_discount(mock_cart_category, category='books', category_discount_rate=0.1)
    expected_price = 90  # 100 - 10% of 100
    assert mock_cart_category.items[0]['price'] == expected_price

# happy_path - test_apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years.
def test_apply_loyalty_discount(discount, mock_cart_loyalty):
    expected_total_price = 255  # 300 - 15% of 300
    result = discount.apply_loyalty_discount(mock_cart_loyalty, loyalty_years=3, loyalty_discount_rate=0.15)
    assert result == expected_total_price

# happy_path - test_apply_flash_sale_discount - Test that flash sale discount is applied to items on sale.
def test_apply_flash_sale_discount(discount, mock_cart_flash_sale):
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.2, items_on_sale=[1])
    expected_price = 80  # 100 - 20% of 100
    assert mock_cart_flash_sale.items[0]['price'] == expected_price

# edge_case - test_apply_discount_below_min_purchase - Test that discount is not applied when total price is below minimum purchase amount.
def test_apply_discount_below_min_purchase(discount, mock_cart):
    mock_cart.calculate_total_price.return_value = 50
    expected_total_price = 50
    result = discount.apply_discount(mock_cart)
    assert result == expected_total_price

# edge_case - test_apply_bulk_discount_below_quantity - Test that no bulk discount is applied when quantity is below bulk requirement.
def test_apply_bulk_discount_below_quantity(discount, mock_cart_bulk):
    mock_cart_bulk.items = [{'quantity': 3, 'price': 100}]
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=5, bulk_discount_rate=0.1)
    expected_price = 100
    assert mock_cart_bulk.items[0]['price'] == expected_price

# edge_case - test_apply_seasonal_discount_non_holiday - Test that seasonal discount is not applied for non-holiday season.
def test_apply_seasonal_discount_non_holiday(discount, mock_cart_seasonal):
    expected_total_price = 200
    result = discount.apply_seasonal_discount(mock_cart_seasonal, season='winter', seasonal_discount_rate=0.2)
    assert result == expected_total_price

# edge_case - test_apply_category_discount_non_matching_category - Test that category discount is not applied to unspecified category items.
def test_apply_category_discount_non_matching_category(discount, mock_cart_category):
    mock_cart_category.items = [{'category': 'electronics', 'price': 100}]
    discount.apply_category_discount(mock_cart_category, category='books', category_discount_rate=0.1)
    expected_price = 100
    assert mock_cart_category.items[0]['price'] == expected_price

# edge_case - test_apply_loyalty_discount_insufficient_years - Test that loyalty discount is not applied for users with less than 3 years.
def test_apply_loyalty_discount_insufficient_years(discount, mock_cart_loyalty):
    expected_total_price = 300
    result = discount.apply_loyalty_discount(mock_cart_loyalty, loyalty_years=1, loyalty_discount_rate=0.15)
    assert result == expected_total_price

# edge_case - test_apply_flash_sale_discount_not_on_sale - Test that flash sale discount is not applied to items not on sale.
def test_apply_flash_sale_discount_not_on_sale(discount, mock_cart_flash_sale):
    mock_cart_flash_sale.items = [{'item_id': 2, 'price': 100}]
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.2, items_on_sale=[1])
    expected_price = 100
    assert mock_cart_flash_sale.items[0]['price'] == expected_price

