import pytest
from unittest.mock import MagicMock, patch
from shopping_cart.discounts import Discount

@pytest.fixture
def mock_cart():
    cart = MagicMock()
    cart.items = [{'category': 'books', 'price': 20, 'quantity': 1, 'item_id': 1}]
    cart.user_type = 'regular'
    cart.total_price = 0
    
    def mock_calculate_total_price():
        return sum(item['price'] * item['quantity'] for item in cart.items)

    cart.calculate_total_price = MagicMock(side_effect=mock_calculate_total_price)
    return cart

@pytest.fixture
def discount():
    return Discount(discount_rate=0.1, min_purchase_amount=50)

@pytest.fixture
def mock_cart_with_premium_user():
    cart = MagicMock()
    cart.items = [{'category': 'electronics', 'price': 150, 'quantity': 1, 'item_id': 2}]
    cart.user_type = 'premium'
    cart.total_price = 0
    
    def mock_calculate_total_price():
        return sum(item['price'] * item['quantity'] for item in cart.items)

    cart.calculate_total_price = MagicMock(side_effect=mock_calculate_total_price)
    return cart

@pytest.fixture
def mock_cart_with_bulk_items():
    cart = MagicMock()
    cart.items = [{'category': 'books', 'price': 20, 'quantity': 10}]
    
    def mock_calculate_total_price():
        return sum(item['price'] * item['quantity'] for item in cart.items)

    cart.calculate_total_price = MagicMock(side_effect=mock_calculate_total_price)
    return cart

# happy path - apply_discount - Test that discount is applied correctly when total price is above minimum purchase amount for a regular user.
def test_apply_discount_regular_user(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 100
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 110


# happy path - apply_discount - Test that discount is applied correctly with increased rate for premium users with electronics in their cart.
def test_apply_discount_premium_user_with_electronics(mock_cart_with_premium_user, discount):
    mock_cart_with_premium_user.calculate_total_price.return_value = 200
    discount.apply_discount(mock_cart_with_premium_user)
    assert mock_cart_with_premium_user.total_price == 230


# happy path - apply_bulk_discount - Test that bulk discount is applied to items with quantity above the bulk quantity threshold.
def test_apply_bulk_discount(mock_cart_with_bulk_items, discount):
    discount.apply_bulk_discount(mock_cart_with_bulk_items, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart_with_bulk_items.items[0]['price'] == 18


# happy path - apply_seasonal_discount - Test that seasonal discount is applied during holiday season.
def test_apply_seasonal_discount_holiday(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 300
    discount.apply_seasonal_discount(mock_cart, season='holiday', seasonal_discount_rate=0.2)
    assert mock_cart.total_price == 240


# happy path - apply_category_discount - Test that category discount is applied to items of specified category.
def test_apply_category_discount(mock_cart, discount):
    discount.apply_category_discount(mock_cart, category='books', category_discount_rate=0.15)
    assert mock_cart.items[0]['price'] == 17


# happy path - apply_loyalty_discount - Test that loyalty discount is applied for loyal users with more than 2 years of loyalty.
def test_apply_loyalty_discount(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    mock_cart.calculate_total_price.return_value = 150
    discount.apply_loyalty_discount(mock_cart, loyalty_years=3, loyalty_discount_rate=0.05)
    assert mock_cart.total_price == 142.5


# edge case - apply_discount - Test that no discount is applied when total price is below minimum purchase amount.
def test_apply_discount_below_minimum_purchase(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 50
    discount.apply_discount(mock_cart)
    assert mock_cart.total_price == 50


# edge case - apply_bulk_discount - Test that no bulk discount is applied when item quantity is below the bulk quantity threshold.
def test_apply_bulk_discount_below_threshold(mock_cart, discount):
    mock_cart.items = [{'quantity': 3, 'price': 20}]
    discount.apply_bulk_discount(mock_cart, bulk_quantity=5, bulk_discount_rate=0.1)
    assert mock_cart.items[0]['price'] == 20


# edge case - apply_seasonal_discount - Test that no seasonal discount is applied outside of holiday or summer seasons.
def test_apply_seasonal_discount_no_discount(mock_cart, discount):
    mock_cart.calculate_total_price.return_value = 400
    discount.apply_seasonal_discount(mock_cart, season='winter', seasonal_discount_rate=0.2)
    assert mock_cart.total_price == 400


# edge case - apply_category_discount - Test that no category discount is applied to items not in the specified category.
def test_apply_category_discount_no_discount(mock_cart, discount):
    mock_cart.items = [{'category': 'electronics', 'price': 100}]
    discount.apply_category_discount(mock_cart, category='clothing', category_discount_rate=0.15)
    assert mock_cart.items[0]['price'] == 100


# edge case - apply_loyalty_discount - Test that no loyalty discount is applied for users with less than 3 years of loyalty.
def test_apply_loyalty_discount_below_threshold(mock_cart, discount):
    mock_cart.user_type = 'loyal'
    mock_cart.calculate_total_price.return_value = 200
    discount.apply_loyalty_discount(mock_cart, loyalty_years=2, loyalty_discount_rate=0.05)
    assert mock_cart.total_price == 200


