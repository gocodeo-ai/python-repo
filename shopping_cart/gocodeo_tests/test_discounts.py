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
def mock_cart_with_items():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'category': 'books', 'price': 100, 'quantity': 1}]
        mock_cart_instance.calculate_total_price = MagicMock(return_value=100)
        yield mock_cart_instance

@pytest.fixture
def mock_cart_premium():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.user_type = 'premium'
        mock_cart_instance.items = [{'category': 'electronics', 'price': 200, 'quantity': 1}]
        mock_cart_instance.calculate_total_price = MagicMock(return_value=200)
        yield mock_cart_instance

@pytest.fixture
def mock_cart_loyal():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.user_type = 'loyal'
        mock_cart_instance.items = [{'category': 'books', 'price': 100, 'quantity': 1}]
        mock_cart_instance.calculate_total_price = MagicMock(return_value=100)
        yield mock_cart_instance

@pytest.fixture
def mock_cart_bulk():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'category': 'books', 'price': 100, 'quantity': 10}]
        mock_cart_instance.calculate_total_price = MagicMock(return_value=1000)
        yield mock_cart_instance

@pytest.fixture
def mock_cart_flash_sale():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart_instance = MockCart.return_value
        mock_cart_instance.items = [{'item_id': 1, 'price': 100, 'quantity': 1}]
        mock_cart_instance.calculate_total_price = MagicMock(return_value=100)
        yield mock_cart_instance

# happy path - apply_discount - Test that discount is applied correctly when total price is above minimum purchase amount for regular users.
def test_apply_discount_regular_user_above_minimum(mock_cart, discount):
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'category': 'books', 'price': 100, 'quantity': 1}]
    mock_cart.calculate_total_price.return_value = 100
    total_price = discount.apply_discount(mock_cart)
    assert total_price == 110
    assert mock_cart.total_price == 110


# happy path - apply_discount - Test that premium user gets additional discount on electronics.
def test_apply_discount_premium_user_on_electronics(mock_cart_premium, discount):
    total_price = discount.apply_discount(mock_cart_premium)
    assert total_price == 230
    assert mock_cart_premium.total_price == 230


# happy path - apply_bulk_discount - Test that bulk discount is applied correctly for items meeting the bulk quantity.
def test_apply_bulk_discount(mock_cart_bulk, discount):
    discount.apply_bulk_discount(mock_cart_bulk, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_bulk.items[0]['price'] == 80


# happy path - apply_seasonal_discount - Test that seasonal discount is applied correctly during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart_with_items, discount):
    total_price = discount.apply_seasonal_discount(mock_cart_with_items, season='holiday', seasonal_discount_rate=0.2)
    assert total_price == 80
    assert mock_cart_with_items.total_price == 80


# happy path - apply_category_discount - Test that category discount is applied correctly for specified category.
def test_apply_category_discount(mock_cart_with_items, discount):
    discount.apply_category_discount(mock_cart_with_items, category='books', category_discount_rate=0.15)
    assert mock_cart_with_items.items[0]['price'] == 85


# happy path - apply_loyalty_discount - Test that loyalty discount is applied correctly for loyal users with more than 2 years.
def test_apply_loyalty_discount(mock_cart_loyal, discount):
    total_price = discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=3, loyalty_discount_rate=0.1)
    assert total_price == 90
    assert mock_cart_loyal.total_price == 90


# happy path - apply_flash_sale_discount - Test that flash sale discount is applied correctly to items on sale.
def test_apply_flash_sale_discount(mock_cart_flash_sale, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.25, items_on_sale=[1])
    assert mock_cart_flash_sale.items[0]['price'] == 75


# edge case - apply_discount - Test that no discount is applied when total price is below minimum purchase amount.
def test_apply_discount_below_minimum(mock_cart, discount):
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'category': 'books', 'price': 40, 'quantity': 1}]
    mock_cart.calculate_total_price.return_value = 40
    total_price = discount.apply_discount(mock_cart)
    assert total_price == 40
    assert mock_cart.total_price == 40


# edge case - apply_discount - Test that no additional discount is applied for premium user without electronics.
def test_apply_discount_premium_user_no_electronics(mock_cart_premium, discount):
    mock_cart_premium.items = [{'category': 'books', 'price': 200, 'quantity': 1}]
    mock_cart_premium.calculate_total_price.return_value = 200
    total_price = discount.apply_discount(mock_cart_premium)
    assert total_price == 220
    assert mock_cart_premium.total_price == 220


# edge case - apply_bulk_discount - Test that bulk discount is not applied for items below bulk quantity.
def test_apply_bulk_discount_below_quantity(mock_cart_with_items, discount):
    mock_cart_with_items.items[0]['quantity'] = 4
    discount.apply_bulk_discount(mock_cart_with_items, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_with_items.items[0]['price'] == 100


# edge case - apply_seasonal_discount - Test that seasonal discount is not applied during non-holiday season.
def test_apply_seasonal_discount_non_holiday(mock_cart_with_items, discount):
    total_price = discount.apply_seasonal_discount(mock_cart_with_items, season='winter', seasonal_discount_rate=0.2)
    assert total_price == 100
    assert mock_cart_with_items.total_price == 100


# edge case - apply_category_discount - Test that category discount is not applied for different category.
def test_apply_category_discount_different_category(mock_cart_with_items, discount):
    discount.apply_category_discount(mock_cart_with_items, category='electronics', category_discount_rate=0.15)
    assert mock_cart_with_items.items[0]['price'] == 100


# edge case - apply_loyalty_discount - Test that loyalty discount is not applied for non-loyal users or loyalty years less than 3.
def test_apply_loyalty_discount_non_loyal_user(mock_cart, discount):
    mock_cart.user_type = 'regular'
    total_price = discount.apply_loyalty_discount(mock_cart, loyalty_years=2, loyalty_discount_rate=0.1)
    assert total_price == 100
    assert mock_cart.total_price == 100


# edge case - apply_flash_sale_discount - Test that flash sale discount is not applied to items not on sale.
def test_apply_flash_sale_discount_item_not_on_sale(mock_cart_flash_sale, discount):
    discount.apply_flash_sale_discount(mock_cart_flash_sale, flash_sale_rate=0.25, items_on_sale=[2])
    assert mock_cart_flash_sale.items[0]['price'] == 100


