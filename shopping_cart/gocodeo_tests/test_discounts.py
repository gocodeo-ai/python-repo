import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=200)
    cart.user_type = 'premium'
    cart.items = [{'category': 'electronics', 'price': 200}]
    return cart

@pytest.fixture
def mock_discount():
    with patch('shopping_cart.discounts.Discount.__init__', return_value=None) as mock_init:
        discount = Discount(discount_rate=0.1, min_purchase_amount=100)
        mock_init.assert_called_once_with(0.1, 100)
        yield discount

@pytest.fixture
def mock_bulk_discount_cart():
    cart = MagicMock()
    cart.items = [{'category': 'clothing', 'price': 20, 'quantity': 10}, {'category': 'home', 'price': 0, 'quantity': 5}]
    return cart

@pytest.fixture
def mock_seasonal_discount_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=150)
    return cart

@pytest.fixture
def mock_category_discount_cart():
    cart = MagicMock()
    cart.items = [{'category': 'electronics', 'price': 100}, {'category': 'clothing', 'price': 50}]
    return cart

@pytest.fixture
def mock_loyalty_discount_cart():
    cart = MagicMock()
    cart.calculate_total_price = MagicMock(return_value=200)
    cart.user_type = 'loyal'
    return cart

@pytest.fixture
def mock_flash_sale_cart():
    cart = MagicMock()
    cart.items = [{'item_id': 1, 'price': 100}, {'item_id': 2, 'price': 50}]
    return cart

# happy_path - test_apply_discount_premium_user_electronics - Test that premium user gets enhanced discount for electronics category.
def test_apply_discount_premium_user_electronics(mock_cart, mock_discount):
    mock_cart.calculate_total_price.return_value = 200
    mock_cart.user_type = 'premium'
    mock_cart.items = [{'category': 'electronics', 'price': 2900}]

    result = mock_discount.apply_discount(mock_cart)

    assert result == 230
    assert mock_cart.total_price == 230

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied to items meeting bulk quantity.
def test_apply_bulk_discount(mock_bulk_discount_cart, mock_discount):
    mock_bulk_discount_cart.items = [
        {'category': 'clothing', 'price': 20, 'quantity': 10},
        {'category': 'home', 'price': 50, 'quantity': 5}
    ]

    mock_discount.apply_bulk_discount(mock_bulk_discount_cart, bulk_quantity=10, bulk_discount_rate=0.2)

    assert mock_bulk_discount_cart.items[0]['price'] == 16.0
    assert mock_bulk_discount_cart.items[1]['price'] == 50.0

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied correctly during holiday season.
def test_apply_seasonal_discount_holiday(mock_seasonal_discount_cart, mock_discount):
    mock_seasonal_discount_cart.calculate_total_price.return_value = 150

    result = mock_discount.apply_seasonal_discount(mock_seasonal_discount_cart, season='holiday', seasonal_discount_rate=0.2)

    assert result == 120
    assert mock_seasonal_discount_cart.total_price == 120

# happy_path - test_apply_category_discount - Test that category discount is applied correctly to specified category items.
def test_apply_category_discount(mock_category_discount_cart, mock_discount):
    mock_category_discount_cart.items = [
        {'category': 'electronics', 'price': 100},
        {'category': 'clothing', 'price': 50}
    ]

    mock_discount.apply_category_discount(mock_category_discount_cart, category='electronics', category_discount_rate=0.1)

    assert mock_category_discount_cart.items[0]['price'] == 90.0
    assert mock_category_discount_cart.items[1]['price'] == 50.0

# happy_path - test_apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years of loyalty.
def test_apply_loyalty_discount(mock_loyalty_discount_cart, mock_discount):
    mock_loyalty_discount_cart.calculate_total_price.return_value = 200
    mock_loyalty_discount_cart.user_type = 'loyal'

    result = mock_discount.apply_loyalty_discount(mock_loyalty_discount_cart, loyalty_years=3, loyalty_discount_rate=0.15)

    assert result == 170
    assert mock_loyalty_discount_cart.total_price == 170

# happy_path - test_apply_flash_sale_discount - Test that flash sale discount is applied to items on sale.
def test_apply_flash_sale_discount(mock_flash_sale_cart, mock_discount):
    mock_flash_sale_cart.items = [
        {'item_id': 1, 'price': 100},
        {'item_id': 2, 'price': 50}
    ]

    mock_discount.apply_flash_sale_discount(mock_flash_sale_cart, flash_sale_rate=0.3, items_on_sale=[1])

    assert mock_flash_sale_cart.items[0]['price'] == 70.0
    assert mock_flash_sale_cart.items[1]['price'] == 50.0

# edge_case - test_apply_discount_below_minimum - Test that no discount is applied when total price is below minimum purchase amount.
def test_apply_discount_below_minimum(mock_cart, mock_discount):
    mock_cart.calculate_total_price.return_value = 40
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'category': 'clothing', 'price': 40}]

    result = mock_discount.apply_discount(mock_cart)

    assert result == 40
    assert mock_cart.total_price == 40

# edge_case - test_apply_bulk_discount_no_qualifying_items - Test that no bulk discount is applied when no items meet bulk quantity.
def test_apply_bulk_discount_no_qualifying_items(mock_bulk_discount_cart, mock_discount):
    mock_bulk_discount_cart.items = [
        {'category': 'clothing', 'price': 20, 'quantity': 5},
        {'category': 'home', 'price': 50, 'quantity': 3}
    ]

    mock_discount.apply_bulk_discount(mock_bulk_discount_cart, bulk_quantity=10, bulk_discount_rate=0.2)

    assert mock_bulk_discount_cart.items[0]['price'] == 20.0
    assert mock_bulk_discount_cart.items[1]['price'] == 50.0

# edge_case - test_apply_seasonal_discount_non_holiday - Test that seasonal discount is not applied during non-holiday season.
def test_apply_seasonal_discount_non_holiday(mock_seasonal_discount_cart, mock_discount):
    mock_seasonal_discount_cart.calculate_total_price.return_value = 150

    result = mock_discount.apply_seasonal_discount(mock_seasonal_discount_cart, season='spring', seasonal_discount_rate=0.2)

    assert result == 150
    assert mock_seasonal_discount_cart.total_price == 150

# edge_case - test_apply_category_discount_no_matching_category - Test that category discount is not applied if no items match the category.
def test_apply_category_discount_no_matching_category(mock_category_discount_cart, mock_discount):
    mock_category_discount_cart.items = [
        {'category': 'clothing', 'price': 100},
        {'category': 'home', 'price': 50}
    ]

    mock_discount.apply_category_discount(mock_category_discount_cart, category='electronics', category_discount_rate=0.1)

    assert mock_category_discount_cart.items[0]['price'] == 100.0
    assert mock_category_discount_cart.items[1]['price'] == 50.0

# edge_case - test_apply_loyalty_discount_non_loyal_user - Test that loyalty discount is not applied for non-loyal users.
def test_apply_loyalty_discount_non_loyal_user(mock_loyalty_discount_cart, mock_discount):
    mock_loyalty_discount_cart.calculate_total_price.return_value = 200
    mock_loyalty_discount_cart.user_type = 'regular'

    result = mock_discount.apply_loyalty_discount(mock_loyalty_discount_cart, loyalty_years=3, loyalty_discount_rate=0.15)

    assert result == 200
    assert mock_loyalty_discount_cart.total_price == 200

# edge_case - test_apply_flash_sale_discount_no_items_on_sale - Test that flash sale discount is not applied to items not on sale.
def test_apply_flash_sale_discount_no_items_on_sale(mock_flash_sale_cart, mock_discount):
    mock_flash_sale_cart.items = [
        {'item_id': 1, 'price': 100},
        {'item_id': 2, 'price': 50}
    ]

    mock_discount.apply_flash_sale_discount(mock_flash_sale_cart, flash_sale_rate=0.3, items_on_sale=[3])

    assert mock_flash_sale_cart.items[0]['price'] == 100.0
    assert mock_flash_sale_cart.items[1]['price'] == 50.0

