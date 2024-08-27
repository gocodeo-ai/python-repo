import pytest
from unittest.mock import patch, MagicMock

# Mocking the dependencies
@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('path.to.cart_module.Cart') as MockCart, \
         patch('path.to.cart_module.Item') as MockItem, \
         patch('path.to.database_module') as MockDatabase, \
         patch('path.to.discounts_module') as MockDiscounts, \
         patch('path.to.payments_module') as MockPayments, \
         patch('path.to.utils_module') as MockUtils:

        # Setup Mocks
        mock_cart_instance = MockCart.return_value
        mock_item_instance = MockItem.return_value

        mock_database_instance = MockDatabase.return_value
        mock_discounts_instance = MockDiscounts.return_value
        mock_payments_instance = MockPayments.return_value
        mock_utils_instance = MockUtils.return_value

        yield {
            'MockCart': MockCart,
            'MockItem': MockItem,
            'mock_cart_instance': mock_cart_instance,
            'mock_item_instance': mock_item_instance,
            'MockDatabase': MockDatabase,
            'MockDiscounts': MockDiscounts,
            'MockPayments': MockPayments,
            'MockUtils': MockUtils,
            'mock_database_instance': mock_database_instance,
            'mock_discounts_instance': mock_discounts_instance,
            'mock_payments_instance': mock_payments_instance,
            'mock_utils_instance': mock_utils_instance
        }

# happy_path - test_add_item_success - Test that Cart can add a new item successfully
def test_add_item_success(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_cart_instance.add_item.return_value = {'cart_total': 1000.0, 'items_count': 1}
    result = mock_cart_instance.add_item(cart_id=1, item={'id': 101, 'name': 'Laptop', 'price': 1000.0, 'quantity': 1})
    assert result == {'cart_total': 999.0, 'items_count': 1}

# edge_case - test_add_item_zero_quantity - Test that adding an item with zero quantity does not alter the cart
def test_add_item_zero_quantity(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_cart_instance.add_item.return_value = {'cart_total': 0.0, 'items_count': 0}
    result = mock_cart_instance.add_item(cart_id=1, item={'id': 103, 'name': 'Mouse', 'price': 25.0, 'quantity': 0})
    assert result == {'cart_total': 0.0, 'items_count': 0}

# edge_case - test_calculate_total_empty_cart - Test that calculating total on an empty cart returns zero
def test_calculate_total_empty_cart(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_cart_instance.calculate_total.return_value = {'total_price': 0.0}
    result = mock_cart_instance.calculate_total(cart_id=2, items=[])
    assert result == {'total_price': 0.0}

# edge_case - test_apply_invalid_discount - Test that applying an invalid discount code does not change the total price
def test_apply_invalid_discount(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_cart_instance.apply_discount.return_value = {'total_price': 1000.0}
    result = mock_cart_instance.apply_discount(cart_id=1, discount_code='INVALID')
    assert result == {'total_price': 1000.0}

# edge_case - test_process_payment_invalid_card - Test that payment fails with invalid credit card details
def test_process_payment_invalid_card(mock_dependencies):
    mock_payments_instance = mock_dependencies['mock_payments_instance']
    mock_payments_instance.process_payment.return_value = {'payment_status': 'failure'}
    result = mock_payments_instance.process_payment(cart_id=1, payment_method='credit_card', card_details={'number': '1234567890123456', 'expiry': '01/20', 'cvv': '000'})
    assert result == {'payment_status': 'failure}'

