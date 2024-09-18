import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price = MagicMock(return_value=100)
        yield mock_cart_instance

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def bulk_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'quantity': 10, 'price': 20}]
        yield mock_cart_instance

@pytest.fixture
def seasonal_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.calculate_total_price = MagicMock(return_value=200)
        yield mock_cart_instance

@pytest.fixture
def category_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'category': 'clothing', 'price': 50}]
        yield mock_cart_instance

@pytest.fixture
def loyalty_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.user_type = 'loyal'
        mock_cart_instance.calculate_total_price = MagicMock(return_value=200)
        yield mock_cart_instance

@pytest.fixture
def flash_sale_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'item_id': 1, 'price': 100}]
        yield mock_cart_instance

# happy_path - test_apply_discount_premium_user_with_electronics - Test that discount is applied correctly for a premium user with electronics in cart
def test_apply_discount_premium_user_with_electronics(mock_cart, discount):
    mock_cart.user_type = 'premium'
    mock_cart.items = [{'category': 'electronics', 'price': 100}]
    mock_cart.calculate_total_price.return_value = 100
    result = discount.apply_discount(mock_cart)
    assert result == 115.0

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied when quantity meets the bulk requirement
def test_apply_bulk_discount(bulk_cart, discount):
    discount.apply_bulk_discount(bulk_cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert bulk_cart.items[0]['price'] == 16.0

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season
def test_apply_seasonal_discount_holiday(seasonal_cart, discount):
    result = discount.apply_seasonal_discount(seasonal_cart, season='holiday', seasonal_discount_rate=0.3)
    assert result == 140.0

# happy_path - test_apply_category_discount - Test that category discount is applied to items in the specified category
def test_apply_category_discount(category_cart, discount):
    discount.apply_category_discount(category_cart, category='clothing', category_discount_rate=0.1)
    assert category_cart.items[0]['price'] == 45.0

# happy_path - test_apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years
def test_apply_loyalty_discount(loyalty_cart, discount):
    result = discount.apply_loyalty_discount(loyalty_cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert result == 180.0

# happy_path - test_apply_flash_sale_discount - Test that flash sale discount is applied to items on sale
def test_apply_flash_sale_discount(flash_sale_cart, discount):
    discount.apply_flash_sale_discount(flash_sale_cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert flash_sale_cart.items[0]['price'] == 80.0

# edge_case - test_apply_discount_below_min_purchase - Test that no discount is applied if total price is below minimum purchase amount
def test_apply_discount_below_min_purchase(mock_cart, discount):
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'category': 'book', 'price': 30}]
    mock_cart.calculate_total_price.return_value = 30
    result = discount.apply_discount(mock_cart)
    assert result == 30.0

# edge_case - test_apply_bulk_discount_quantity_below - Test that bulk discount is not applied if quantity is below the bulk requirement
def test_apply_bulk_discount_quantity_below(bulk_cart, discount):
    bulk_cart.items = [{'quantity': 3, 'price': 20}]
    discount.apply_bulk_discount(bulk_cart, bulk_quantity=5, bulk_discount_rate=0.2)
    assert bulk_cart.items[0]['price'] == 20.0

# edge_case - test_apply_seasonal_discount_non_season - Test that no seasonal discount is applied if season is not holiday or summer
def test_apply_seasonal_discount_non_season(seasonal_cart, discount):
    result = discount.apply_seasonal_discount(seasonal_cart, season='winter', seasonal_discount_rate=0.3)
    assert result == 200.0

# edge_case - test_apply_category_discount_wrong_category - Test that no category discount is applied to items not in the specified category
def test_apply_category_discount_wrong_category(category_cart, discount):
    category_cart.items = [{'category': 'electronics', 'price': 50}]
    discount.apply_category_discount(category_cart, category='clothing', category_discount_rate=0.1)
    assert category_cart.items[0]['price'] == 50.0

# edge_case - test_apply_loyalty_discount_non_loyal_user - Test that no loyalty discount is applied for non-loyal users
def test_apply_loyalty_discount_non_loyal_user(mock_cart, discount):
    mock_cart.user_type = 'regular'
    mock_cart.calculate_total_price.return_value = 200
    result = discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.1)
    assert result == 200.0

# edge_case - test_apply_flash_sale_discount_item_not_on_sale - Test that no flash sale discount is applied to items not on sale
def test_apply_flash_sale_discount_item_not_on_sale(flash_sale_cart, discount):
    flash_sale_cart.items = [{'item_id': 2, 'price': 100}]
    discount.apply_flash_sale_discount(flash_sale_cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert flash_sale_cart.items[0]['price'] == 100.0

