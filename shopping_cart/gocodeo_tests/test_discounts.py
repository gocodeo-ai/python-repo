import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.items = []
    cart.user_type = 'regular'
    cart.total_price = 0

    def calculate_total_price():
        return sum(item['price'] * item.get('quantity', 1) for item in cart.items)

    cart.calculate_total_price = MagicMock(side_effect=calculate_total_price)
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.5, min_purchase_amount=100)

@patch('shopping_cart.discounts.Cart', autospec=True)
def test_discount_with_mock_cart(mock_cart):
    cart = mock_cart
    cart.user_type = 'premium'
    cart.items = [{'category': 'electronics', 'price': 100}]
    cart.total_price = 100

    discount_instance = discount
    result = discount_instance.apply_discount(cart)
    assert result == 250  # Example assertion, adjust based on your test case needs

# happy path - apply_seasonal_discount - Test that seasonal discount is applied during holiday season
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 700
    result = discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.2)
    assert result == 160


# happy path - apply_category_discount - Test that category discount is applied to all items in the specified category
def test_apply_category_discount(mock_cart, discount):
    mock_cart.items = [{'category': 'books', 'price': 50}, {'category': 'books', 'price': 30}]
    discount.apply_category_discount(mock_cart, category='books', category_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 45
    assert mock_cart.items[1]['price'] == 27


# happy path - apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years of loyalty
def test_apply_loyalty_discount(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    mock_cart.calculate_total_price.return_value = 300
    result = discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.15)
    assert result == 255


# happy path - apply_flash_sale_discount - Test that flash sale discount is applied to items on sale
def test_apply_flash_sale_discount(mock_cart, discount):
    mock_cart.items = [{'item_id': 1, 'price': 100}, {'item_id': 2, 'price': 150}]
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.2, items_on_sale=[1])
    assert mock_cart.items[0]['price'] == 80
    assert mock_cart.items[1]['price'] == 150


# edge case - apply_discount - Test that discount is not applied when total price is below minimum purchase amount
def test_apply_discount_below_min_purchase(mock_cart, discount):
    mock_cart.user_type = 'regular'
    mock_cart.items = [{'category': 'clothing', 'price': 50}]
    mock_cart.calculate_total_price.return_value = 50
    result = discount.apply_discount(mock_cart)
    assert result == 50


# edge case - apply_bulk_discount - Test that bulk discount is not applied when quantity is below the threshold
def test_apply_bulk_discount_below_threshold(mock_cart, discount):
    mock_cart.items = [{'quantity': 3, 'price': 100}]
    discount.apply_bulk_discount(mock_cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 100


# edge case - apply_seasonal_discount - Test that seasonal discount is not applied for non-holiday seasons
def test_apply_seasonal_discount_non_holiday(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 200
    result = discount.apply_seasonal_discount(mock_cart, season='fall', seasonal_discount_rate=0.2)
    assert result == 200


# edge case - apply_category_discount - Test that category discount is not applied to items outside the specified category
def test_apply_category_discount_non_matching_category(mock_cart, discount):
    mock_cart.items = [{'category': 'toys', 'price': 50}]
    discount.apply_category_discount(mock_cart, category='books', category_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 50


# edge case - apply_loyalty_discount - Test that loyalty discount is not applied for users with less than 3 years of loyalty
def test_apply_loyalty_discount_insufficient_years(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    mock_cart.calculate_total_price.return_value = 300
    result = discount.apply_loyalty_discount(mock_cart, loyalty_years=2, loyalty_discount_rate=0.15)
    assert result == 300


# edge case - apply_flash_sale_discount - Test that flash sale discount is not applied to items not on sale
def test_apply_flash_sale_discount_no_sale_items(mock_cart, discount):
    mock_cart.items = [{'item_id': 1, 'price': 100}, {'item_id': 2, 'price': 150}]
    discount.apply_flash_sale_discount(mock_cart, flash_sale_rate=0.2, items_on_sale=[3])
    assert mock_cart.items[0]['price'] == 100
    assert mock_cart.items[1]['price'] == 150


