import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    with patch('shopping_cart.discounts.Cart') as MockCart:
        mock_cart = MockCart.return_value
        mock_cart.calculate_total_price = Mock()
        yield mock_cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def mock_cart_items():
    return [
        {"item_id": 1, "category": "electronics", "price": 1000, "quantity": 5},
        {"item_id": 2, "category": "clothing", "price": 50, "quantity": 3},
        {"item_id": 3, "category": "home", "price": 30, "quantity": 1}
    ]

@pytest.fixture
def mock_cart_with_items(mock_cart, mock_cart_items):
    mock_cart.items = mock_cart_items
    return mock_cart

@pytest.fixture
def mock_cart_premium(mock_cart_with_items):
    mock_cart_with_items.user_type = "premium"
    return mock_cart_with_items

@pytest.fixture
def mock_cart_regular(mock_cart_with_items):
    mock_cart_with_items.user_type = "regular"
    return mock_cart_with_items

@pytest.fixture
def mock_cart_loyal(mock_cart_with_items):
    mock_cart_with_items.user_type = "loyal"
    return mock_cart_with_items

@pytest.fixture
def mock_cart_new(mock_cart_with_items):
    mock_cart_with_items.user_type = "new"
    return mock_cart_with_items

@pytest.fixture
def mock_cart_items_on_sale(mock_cart_with_items):
    mock_cart_with_items.items_on_sale = [1]
    return mock_cart_with_items

@pytest.fixture
def mock_cart_not_on_sale(mock_cart_with_items):
    mock_cart_with_items.items_on_sale = []
    return mock_cart_with_items

# happy_path - test_apply_bulk_discount - Test that bulk discount is applied when item quantity meets bulk requirement
def test_apply_bulk_discount(mock_cart_with_items, discount):
    mock_cart_with_items.items = [{'quantity': 5, 'price': 1000}]
    discount.apply_bulk_discount(mock_cart_with_items, bulk_quantity=5, bulk_discount=0.2)
    assert mock_cart_with_items.items[0]['price'] == 800

# happy_path - test_apply_seasonal_discount_holiday - Test that seasonal discount is applied during holiday season
def test_apply_seasonal_discount_holiday(mock_cart_regular, discount):
    mock_cart_regular.calculate_total_price.return_value = 200
    total_price = discount.apply_seasonal_discount(mock_cart_regular, season='christmas', seasonal_discount_rate=0.1)
    assert total_price == 180.0

# happy_path - test_apply_category_discount - Test that category discount is applied to specified category
def test_apply_category_discount(mock_cart_with_items, discount):
    discount.apply_category_discount(mock_cart_with_items, category='clothing', category_discount_rate=0.1)
    assert mock_cart_with_items.items[1]['price'] == 45.0

# happy_path - test_apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years
def test_apply_loyalty_discount(mock_cart_loyal, discount):
    mock_cart_loyal.calculate_total_price.return_value = 300
    total_price = discount.apply_loyalty_discount(mock_cart_loyal, loyalty_years=3, loyalty_discount_rate=0.15)
    assert total_price == 255.0

# edge_case - test_apply_discount_below_min_purchase - Test that no discount is applied if total price is below minimum purchase amount
def test_apply_discount_below_min_purchase(mock_cart_regular, discount):
    mock_cart_regular.calculate_total_price.return_value = 30
    total_price = discount.apply_discount(mock_cart_regular)
    assert total_price == 30.0

# edge_case - test_apply_bulk_discount_below_quantity - Test that bulk discount is not applied when item quantity is below bulk requirement
def test_apply_bulk_discount_below_quantity(mock_cart_with_items, discount):
    mock_cart_with_items.items = [{'quantity': 3, 'price': 100}]
    discount.apply_bulk_discount(mock_cart_with_items, bulk_quantity=5, bulk_discount_rate=0.2)
    assert mock_cart_with_items.items[0]['price'] == 100.0

# edge_case - test_apply_seasonal_discount_non_holiday - Test that seasonal discount is not applied during non-holiday season
def test_apply_seasonal_discount_non_holiday(mock_cart_regular, discount):
    mock_cart_regular.calculate_total_price.return_value = 200
    total_price = discount.apply_seasonal_discount(mock_cart_regular, season='spring', seasonal_discount_rate=0.1)
    assert total_price == 200.0

# edge_case - test_apply_category_discount_wrong_category - Test that category discount is not applied to items outside specified category
def test_apply_category_discount_wrong_category(mock_cart_with_items, discount):
    discount.apply_category_discount(mock_cart_with_items, category='clothing', category_discount_rate=0.1)
    assert mock_cart_with_items.items[0]['price'] == 1000.0

# edge_case - test_apply_loyalty_discount_non_loyal - Test that loyalty discount is not applied for non-loyal users
def test_apply_loyalty_discount_non_loyal(mock_cart_new, discount):
    mock_cart_new.calculate_total_price.return_value = 300
    total_price = discount.apply_loyalty_discount(mock_cart_new, loyalty_years=1, loyalty_discount_rate=0.15)
    assert total_price == 300.0

# edge_case - test_apply_flash_sale_discount_not_on_sale - Test that flash sale discount is not applied to items not on sale
def test_apply_flash_sale_discount_not_on_sale(mock_cart_not_on_sale, discount):
    discount.apply_flash_sale_discount(mock_cart_not_on_sale, flash_sale_rate=0.2, items_on_sale=[1])
    assert mock_cart_not_on_sale.items[1]['price'] == 50.0

