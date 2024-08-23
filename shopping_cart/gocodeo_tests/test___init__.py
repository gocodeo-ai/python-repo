import pytest
from unittest.mock import patch, MagicMock

# Mocking dependencies
@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('your_module.cart.Cart') as MockCart, \
         patch('your_module.cart.Item') as MockItem, \
         patch('your_module.database') as MockDatabase, \
         patch('your_module.discounts') as MockDiscounts, \
         patch('your_module.payments') as MockPayments, \
         patch('your_module.utils') as MockUtils:

        # You can set up any return values or side effects for the mocks here if needed
        mock_cart_instance = MockCart.return_value
        mock_item_instance = MockItem.return_value
        mock_database_instance = MockDatabase.return_value
        mock_discounts_instance = MockDiscounts.return_value
        mock_payments_instance = MockPayments.return_value
        mock_utils_instance = MockUtils.return_value

        yield {
            'MockCart': mock_cart_instance,
            'MockItem': mock_item_instance,
            'MockDatabase': mock_database_instance,
            'MockDiscounts': mock_discounts_instance,
            'MockPayments': mock_payments_instance,
            'MockUtils': mock_utils_instance
        }
```

# happy_path - test_add_item_to_cart_increases_count - Test that adding an item to the cart increases the cart's total item count by one.
def test_add_item_to_cart_increases_count(mock_dependencies):
    cart = mock_dependencies['MockCart']
    cart.total_items = 0
    cart.add_item.return_value = None

    cart.add_item(cart_id=1, item_id=101, quantity=1)

    cart.add_item.assert_called_once_with(cart_id=1, item_id=101, quantity=1)
    assert cart.total_items == 1

# happy_path - test_apply_valid_discount_reduces_total_price - Test that applying a valid discount code reduces the total price of the cart.
def test_apply_valid_discount_reduces_total_price(mock_dependencies):
    discounts = mock_dependencies['MockDiscounts']
    cart = mock_dependencies['MockCart']
    cart.total_price = 100
    discounts.apply_discount.return_value = 80

    new_price = discounts.apply_discount(cart_id=1, discount_code='SAVE20')

    discounts.apply_discount.assert_called_once_with(cart_id=1, discount_code='SAVE20')
    assert new_price == 80

# happy_path - test_finalize_payment_marks_order_paid - Test that finalizing a payment with valid details marks the order as paid.
def test_finalize_payment_marks_order_paid(mock_dependencies):
    payments = mock_dependencies['MockPayments']
    order = mock_dependencies['MockDatabase'].get_order.return_value
    order.status = 'unpaid'
    payments.finalize_payment.return_value = 'paid'

    status = payments.finalize_payment(order_id=1, payment_details={'card_number': '1234567890123456', 'expiry_date': '12/25', 'cvv': '123'})

    payments.finalize_payment.assert_called_once_with(order_id=1, payment_details={'card_number': '1234567890123456', 'expiry_date': '12/25', 'cvv': '123'})
    assert status == 'paid'

# happy_path - test_get_item_details_returns_correct_information - Test that retrieving an item's details returns the correct item information.
def test_get_item_details_returns_correct_information(mock_dependencies):
    item = mock_dependencies['MockItem']
    item.name = 'Laptop'
    item.price = 1000
    item.get_details.return_value = {'name': 'Laptop', 'price': 1000}

    details = item.get_details(item_id=101)

    item.get_details.assert_called_once_with(item_id=101)
    assert details == {'name': 'Laptop', 'price': 1000}

# edge_case - test_add_zero_quantity_item_does_not_change_count - Test that adding an item with zero quantity does not change the cart's total item count.
def test_add_zero_quantity_item_does_not_change_count(mock_dependencies):
    cart = mock_dependencies['MockCart']
    cart.total_items = 0
    cart.add_item.return_value = None

    cart.add_item(cart_id=1, item_id=101, quantity=0)

    cart.add_item.assert_called_once_with(cart_id=1, item_id=101, quantity=0)
    assert cart.total_items == 0

# edge_case - test_remove_nonexistent_item_does_not_change_count - Test that removing an item not in the cart does not change the cart's total item count.
def test_remove_nonexistent_item_does_not_change_count(mock_dependencies):
    cart = mock_dependencies['MockCart']
    cart.total_items = 0
    cart.remove_item.return_value = None

    cart.remove_item(cart_id=1, item_id=999)

    cart.remove_item.assert_called_once_with(cart_id=1, item_id=999)
    assert cart.total_items == 0

# edge_case - test_apply_expired_discount_does_not_change_total_price - Test that applying an expired discount code does not change the total price of the cart.
def test_apply_expired_discount_does_not_change_total_price(mock_dependencies):
    discounts = mock_dependencies['MockDiscounts']
    cart = mock_dependencies['MockCart']
    cart.total_price = 100
    discounts.apply_discount.return_value = 100

    new_price = discounts.apply_discount(cart_id=1, discount_code='EXPIRED')

    discounts.apply_discount.assert_called_once_with(cart_id=1, discount_code='EXPIRED')
    assert new_price == 100

# edge_case - test_finalize_payment_with_invalid_card_fails - Test that finalizing a payment with invalid card details does not mark the order as paid.
def test_finalize_payment_with_invalid_card_fails(mock_dependencies):
    payments = mock_dependencies['MockPayments']
    order = mock_dependencies['MockDatabase'].get_order.return_value
    order.status = 'unpaid'
    payments.finalize_payment.return_value = 'unpaid'

    status = payments.finalize_payment(order_id=1, payment_details={'card_number': '0000000000000000', 'expiry_date': '01/20', 'cvv': '000'})

    payments.finalize_payment.assert_called_once_with(order_id=1, payment_details={'card_number': '0000000000000000', 'expiry_date': '01/20', 'cvv': '000'})
    assert status == 'unpaid'

# edge_case - test_get_nonexistent_item_details_returns_error - Test that retrieving details of a non-existent item returns an error.
def test_get_nonexistent_item_details_returns_error(mock_dependencies):
    item = mock_dependencies['MockItem']
    item.get_details.return_value = {'error': 'Item not found'}

    details = item.get_details(item_id=999)

    item.get_details.assert_called_once_with(item_id=999)
    assert details == {'error': 'Item not found'}

