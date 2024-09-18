import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price = MagicMock(return_value=150)
        mock_cart_instance.user_type = 'regular'
        mock_cart_instance.items = [{'category': 'books'}]
        yield mock_cart_instance

@pytest.fixture
def mock_cart_premium():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price = MagicMock(return_value=150)
        mock_cart_instance.user_type = 'premium'
        mock_cart_instance.items = [{'category': 'electronics'}]
        yield mock_cart_instance

@pytest.fixture
def mock_cart_bulk_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'quantity': 6, 'price': 100}]
        yield mock_cart_instance

@pytest.fixture
def mock_cart_seasonal_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price = MagicMock(return_value=200)
        yield mock_cart_instance

@pytest.fixture
def mock_cart_category_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'category': 'clothing', 'price': 50}]
        yield mock_cart_instance

@pytest.fixture
def mock_cart_loyalty_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price = MagicMock(return_value=100)
        mock_cart_instance.user_type = 'loyal'
        yield mock_cart_instance

@pytest.fixture
def mock_cart_flash_sale_discount():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'item_id': 101, 'price': 100}]
        yield mock_cart_instance

# happy_path - test_apply_discount_above_minimum - Test that a discount is applied when total price is above minimum purchase amount.
def test_apply_discount_above_minimum(mock_cart):
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    total_price = discount.apply_discount(mock_cart)
    assert total_price == 165

# happy_path - test_apply_discount_premium_electronics - Test that the discount is increased by 1.5 times for premium users with electronics in cart.
def test_apply_discount_premium_electronics(mock_cart_premium):
    discount = Discount(discount_rate=0.1, min_purchase_amount=100)
    total_price = discount.apply_discount(mock_cart_premium)
    assert total_price == 165

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied to items with quantity above bulk quantity.
def test_apply_bulk_discount(mock_cart_bulk_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(mock_cart_bulk_discount, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_bulk_discount.items[0]['price'] == 80

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart_seasonal_discount):
    discount = Discount(discount_rate=0.1)
    total_price = discount.apply_seasonal_discount(mock_cart_seasonal_discount, season='holiday', seasonal_discount_rate=0.25)
    assert total_price == 150

# happy_path - test_apply_category_discount - Test that category discount is applied to items in specific category.
def test_apply_category_discount(mock_cart_category_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_category_discount(mock_cart_category_discount, category='clothing', category_discount_rate=0.15)
    assert mock_cart_category_discount.items[0]['price'] == 42.5

# happy_path - test_apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years.
def test_apply_loyalty_discount(mock_cart_loyalty_discount):
    discount = Discount(discount_rate=0.1)
    total_price = discount.apply_loyalty_discount(mock_cart_loyalty_discount, loyalty_years=3, loyalty_discount_rate=0.1)
    assert total_price == 90

# happy_path - test_apply_flash_sale_discount - Test that flash sale discount is applied to items on sale.
def test_apply_flash_sale_discount(mock_cart_flash_sale_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_flash_sale_discount(mock_cart_flash_sale_discount, flash_sale_rate=0.3, items_on_sale=[101])
    assert mock_cart_flash_sale_discount.items[0]['price'] == 70

# edge_case - test_no_discount_below_minimum - Test that no discount is applied when total price is below minimum purchase amount.
def test_no_discount_below_minimum(mock_cart):
    discount = Discount(discount_rate=0.1, min_purchase_amount=200)
    total_price = discount.apply_discount(mock_cart)
    assert total_price == 150

# edge_case - test_no_bulk_discount - Test that no bulk discount is applied to items with quantity below bulk quantity.
def test_no_bulk_discount(mock_cart_bulk_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_bulk_discount(mock_cart_bulk_discount, bulk_quantity=10, bulk_discount_rate=0.2)
    assert mock_cart_bulk_discount.items[0]['price'] == 100

# edge_case - test_no_seasonal_discount_non_holiday - Test that no seasonal discount is applied during non-holiday season.
def test_no_seasonal_discount_non_holiday(mock_cart_seasonal_discount):
    discount = Discount(discount_rate=0.1)
    total_price = discount.apply_seasonal_discount(mock_cart_seasonal_discount, season='winter', seasonal_discount_rate=0.25)
    assert total_price == 200

# edge_case - test_no_category_discount - Test that no category discount is applied to items not in specified category.
def test_no_category_discount(mock_cart_category_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_category_discount(mock_cart_category_discount, category='electronics', category_discount_rate=0.15)
    assert mock_cart_category_discount.items[0]['price'] == 50

# edge_case - test_no_loyalty_discount_non_loyal - Test that no loyalty discount is applied for non-loyal users.
def test_no_loyalty_discount_non_loyal(mock_cart_loyalty_discount):
    mock_cart_loyalty_discount.user_type = 'regular'
    discount = Discount(discount_rate=0.1)
    total_price = discount.apply_loyalty_discount(mock_cart_loyalty_discount, loyalty_years=1, loyalty_discount_rate=0.1)
    assert total_price == 100

# edge_case - test_no_flash_sale_discount - Test that no flash sale discount is applied to items not on sale.
def test_no_flash_sale_discount(mock_cart_flash_sale_discount):
    discount = Discount(discount_rate=0.1)
    discount.apply_flash_sale_discount(mock_cart_flash_sale_discount, flash_sale_rate=0.3, items_on_sale=[102])
    assert mock_cart_flash_sale_discount.items[0]['price'] == 100

