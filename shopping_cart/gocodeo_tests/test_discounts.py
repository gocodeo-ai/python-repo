import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=100)
        yield instance

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=100)

@pytest.fixture
def mock_cart_with_items():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=100)
        instance.items = [{'category': 'electronics', 'price': 100, 'quantity': 1, 'item_id': 1}]
        yield instance

@pytest.fixture
def mock_cart_with_bulk_items():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=100)
        instance.items = [{'category': 'electronics', 'price': 100, 'quantity': 10}]
        yield instance

@pytest.fixture
def mock_cart_with_loyal_user():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=100)
        instance.user_type = 'loyal'
        yield instance

@pytest.fixture
def mock_cart_with_non_loyal_user():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=100)
        instance.user_type = 'regular'
        yield instance

@pytest.fixture
def mock_cart_with_flash_sale_items():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        instance = MockCart.return_value
        instance.calculate_total_price = MagicMock(return_value=100)
        instance.items = [{'item_id': 2, 'price': 100}]
        yield instance

# happy path - apply_discount - apply discount to a premium user with electronics in cart
def test_apply_discount_premium_user_electronics(mock_cart_with_items, discount):
    mock_cart_with_items.user_type = 'premium'
    result = discount.apply_discount(mock_cart_with_items)
    assert result == 151.5
    assert mock_cart_with_items.total_price == 151.5


# happy path - apply_bulk_discount - apply bulk discount to items with sufficient quantity
def test_apply_bulk_discount_sufficient_quantity(mock_cart_with_bulk_items, discount):
    discount.apply_bulk_discount(mock_cart_with_bulk_items, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart_with_bulk_items.items[0]['price'] == 90.0


# happy path - apply_seasonal_discount - apply seasonal discount during holiday season
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    result = discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.2)
    assert result == 80.0
    assert mock_cart.total_price == 80.0


# happy path - apply_category_discount - apply category discount to electronics
def test_apply_category_discount_electronics(mock_cart_with_items, discount):
    discount.apply_category_discount(mock_cart_with_items, category='electronics', category_discount_rate=0.1)
    assert mock_cart_with_items.items[0]['price'] == 90.0


# happy path - apply_loyalty_discount - apply loyalty discount to loyal user with more than 2 years
def test_apply_loyalty_discount_loyal_user(mock_cart_with_loyal_user, discount):
    result = discount.apply_loyalty_discount(mock_cart_with_loyal_user, loyalty_years=3, loyalty_discount_rate=0.1)
    assert result == 90.0
    assert mock_cart_with_loyal_user.total_price == 90.0


# happy path - apply_flash_sale_discount - apply flash sale discount to items on sale
def test_apply_flash_sale_discount_items_on_sale(mock_cart_with_items, discount):
    discount.apply_flash_sale_discount(mock_cart_with_items, flash_sale_rate=0.2, items_on_sale=[1])
    assert mock_cart_with_items.items[0]['price'] == 80.0


# edge case - apply_discount - apply discount with total price less than minimum purchase amount
def test_apply_discount_below_minimum_purchase(mock_cart_with_non_loyal_user, discount):
    mock_cart_with_non_loyal_user.calculate_total_price = MagicMock(return_value=50)
    result = discount.apply_discount(mock_cart_with_non_loyal_user)
    assert result == 50
    assert mock_cart_with_non_loyal_user.total_price == 50


# edge case - apply_bulk_discount - apply bulk discount with insufficient quantity
def test_apply_bulk_discount_insufficient_quantity(mock_cart_with_items, discount):
    mock_cart_with_items.items[0]['quantity'] = 3
    discount.apply_bulk_discount(mock_cart_with_items, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart_with_items.items[0]['price'] == 100.0


# edge case - apply_seasonal_discount - apply seasonal discount during non-discount season
def test_apply_seasonal_discount_non_discount_season(mock_cart, discount):
    result = discount.apply_seasonal_discount(mock_cart, season='winter', seasonal_discount_rate=0.2)
    assert result == 100.0
    assert mock_cart.total_price == 100.0


# edge case - apply_category_discount - apply category discount to non-matching category
def test_apply_category_discount_non_matching_category(mock_cart_with_items, discount):
    discount.apply_category_discount(mock_cart_with_items, category='books', category_discount_rate=0.1)
    assert mock_cart_with_items.items[0]['price'] == 100.0


# edge case - apply_loyalty_discount - apply loyalty discount to non-loyal user
def test_apply_loyalty_discount_non_loyal_user(mock_cart_with_non_loyal_user, discount):
    result = discount.apply_loyalty_discount(mock_cart_with_non_loyal_user, loyalty_years=3, loyalty_discount_rate=0.1)
    assert result == 100.0
    assert mock_cart_with_non_loyal_user.total_price == 100.0


# edge case - apply_flash_sale_discount - apply flash sale discount to items not on sale
def test_apply_flash_sale_discount_items_not_on_sale(mock_cart_with_flash_sale_items, discount):
    discount.apply_flash_sale_discount(mock_cart_with_flash_sale_items, flash_sale_rate=0.2, items_on_sale=[1])
    assert mock_cart_with_flash_sale_items.items[0]['price'] == 100.0


