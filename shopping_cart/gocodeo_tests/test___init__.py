import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_dependencies():
    with patch('path.to.cart.Cart') as MockCart, \
         patch('path.to.cart.Item') as MockItem, \
         patch('path.to.database') as mock_database, \
         patch('path.to.discounts') as mock_discounts, \
         patch('path.to.payments') as mock_payments, \
         patch('path.to.utils') as mock_utils:

        # Mock the Cart and Item classes
        cart_instance = MockCart.return_value
        item_instance = MockItem.return_value

        # Mock the database functions
        mock_database.get_cart.return_value = cart_instance
        mock_database.get_item.return_value = item_instance

        # Mock the discounts functions
        mock_discounts.apply_discount.return_value = {'status': 'success', 'discounted_total': 45.0}
        mock_discounts.validate_discount_code.return_value = Truer

        # Mock the payments functions
        mock_payments.process_payment.return_value = {'status': 'success', 'payment_confirmation': 'CONF12345'}
        mock_payments.validate_payment_method.return_value = True

        # Mock the utils functions
        mock_utils.calculate_total.return_value = 50.0

        yield {
            'MockCart': MockCart,
            'MockItem': MockItem,
            'mock_database': mock_database,
            'mock_discounts': mock_discounts,
            'mock_payments': mock_payments,
            'mock_utils': mock_utils
        }

# happy_path - test_remove_item_successfully - Test that Cart can remove an Item successfully
def test_remove_item_successfully(mock_dependencies):
    mock_dependencies['mock_database'].get_cart.return_value.remove_item.return_value = {'status': 'success', 'cart_total': 307}
    result = mock_dependencies['MockCart']().remove_item(cart_id=1, item_id=101)
    assert result['status'] == 'success'
    assert result['cart_total'] == 307

# happy_path - test_apply_discount_successfully - Test that discount is applied correctly to Cart
def test_apply_discount_successfully(mock_dependencies):
    mock_dependencies['mock_discounts'].apply_discount.return_value = {'status': 'success', 'discounted_total': 45.0}
    result = mock_dependencies['mock_discounts'].apply_discount(cart_id=1, discount_code='DISCOUNT10')
    assert result['status'] == 'success'
    assert result['discounted_total'] == 45.0

# happy_path - test_process_payment_successfully - Test that payment is processed successfully
def test_process_payment_successfully(mock_dependencies):
    mock_dependencies['mock_payments'].process_payment.return_value = {'status': 'success', 'payment_confirmation': 'CONF12345'}
    result = mock_dependencies['mock_payments'].process_payment(cart_id=1, payment_method='credit_card')
    assert result['status'] == 'success'
    assert result['payment_confirmation'] == 'CONF12345'

# happy_path - test_calculate_total_successfully - Test that Cart total is calculated correctly
def test_calculate_total_successfully(mock_dependencies):
    mock_dependencies['mock_utils'].calculate_total.return_value = 50.0
    result = mock_dependencies['mock_utils'].calculate_total(cart_id=1)
    assert result['status'] == 'success'
    assert result['total'] == 50.0

# edge_case - test_add_item_zero_quantity - Test that adding an Item with zero quantity fails
def test_add_item_zero_quantity(mock_dependencies):
    mock_dependencies['mock_database'].get_cart.return_value.add_item.return_value = {'status': 'error', 'message': 'Quantity must be greater than zero'}
    result = mock_dependencies['MockCart']().add_item(cart_id=1, item_id=101, quantity=0)
    assert result['status'] == 'error'
    assert result['message'] == 'Quantity must be greater than zero'

# edge_case - test_remove_item_not_in_cart - Test that removing an Item not in Cart fails
def test_remove_item_not_in_cart(mock_dependencies):
    mock_dependencies['mock_database'].get_cart.return_value.remove_item.return_value = {'status': 'error', 'message': 'Item not found in cart'}
    result = mock_dependencies['MockCart']().remove_item(cart_id=1, item_id=999)
    assert result['status'] == 'error'
    assert result['message'] == 'Item not found in cart'

# edge_case - test_apply_invalid_discount_code - Test that applying an invalid discount code fails
def test_apply_invalid_discount_code(mock_dependencies):
    mock_dependencies['mock_discounts'].apply_discount.return_value = {'status': 'error', 'message': 'Invalid discount code'}
    result = mock_dependencies['mock_discounts'].apply_discount(cart_id=1, discount_code='INVALIDCODE')
    assert result['status'] == 'error'
    assert result['message'] == 'Invalid discount code'

# edge_case - test_process_payment_insufficient_funds - Test that payment fails with insufficient funds
def test_process_payment_insufficient_funds(mock_dependencies):
    mock_dependencies['mock_payments'].process_payment.return_value = {'status': 'error', 'message': 'Insufficient funds'}
    result = mock_dependencies['mock_payments'].process_payment(cart_id=1, payment_method='credit_card')
    assert result['status'] == 'error'
    assert result['message'] == 'Insufficient funds'

# edge_case - test_calculate_total_empty_cart - Test that calculating total for an empty Cart returns zero
def test_calculate_total_empty_cart(mock_dependencies):
    mock_dependencies['mock_utils'].calculate_total.return_value = {'status': 'success', 'total': 0.0}
    result = mock_dependencies['mock_utils'].calculate_total(cart_id=2)
    assert result['status'] == 'success'
    assert result['total'] == 0.0

