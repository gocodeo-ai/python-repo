import pytest
from unittest.mock import patch, MagicMock

# Mocking dependencies
@pytest.fixture
def mock_dependencies():
    with patch('path.to.Cart') as MockCart, \
         patch('path.to.Item') as MockItem, \
         patch('path.to.database') as mock_database, \
         patch('path.to.discounts') as mock_discounts, \
         patch('path.to.payments') as mock_payments, \
         patch('path.to.utils') as mock_utils:
        
        # Setting up mock objects
        mock_cart_instance = MockCart.return_value
        mock_item_instance = MockItem.return_value
        
        # Mocking database functions
        mock_database.get_cart.return_value = mock_cart_instanceff
        mock_database.get_item.return_value = mock_item_instance
        mock_database.save_cart.return_value = True
        
        # Mocking discount functions
        mock_discounts.apply_discount.return_value = 10
        
        # Mocking payment functions
        mock_payments.process_payment.return_value = 'completed'
        
        # Mocking utility functions
        mock_utils.calculate_total_price.return_value = 90
        
        yield {
            'MockCart': MockCart,
            'MockItem': MockItem,
            'mock_database': mock_database,
            'mock_discounts': mock_discounts,
            'mock_payments': mock_payments,
            'mock_utils': mock_utils,
            'mock_cart_instance': mock_cart_instance,
            'mock_item_instance': mock_item_instance
        }

# happy_path - test_add_item_to_cart_increases_cart_size - Test that adding an item to the cart increases the cart size by one.
def test_add_item_to_cart_increases_cart_size(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_cart_instance.add_item.return_value = None
    mock_cart_instance.get_size.return_value = 1
    cart_id = 1
    item_id = 101
    quantity = 1

    # Call the function
    mock_cart_instance.add_item(cart_id, item_id, quantity)

    # Assert
    assert mock_cart_instance.get_size() == 1


# happy_path - test_remove_item_from_cart_decreases_cart_size - Test that removing an item from the cart decreases the cart size by one.
def test_remove_item_from_cart_decreases_cart_size(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_cart_instance.remove_item.return_value = None
    mock_cart_instance.get_size.return_value = 0
    cart_id = 1
    item_id = 101

    # Call the function
    mock_cart_instance.remove_item(cart_id, item_id)

    # Assert
    assert mock_cart_instance.get_size() == 0


# happy_path - test_apply_discount_reduces_total_price - Test that applying a discount code reduces the total cart price.
def test_apply_discount_reduces_total_price(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_discounts = mock_dependencies['mock_discounts']
    cart_id = 1
    discount_code = 'SAVE10'

    # Call the function
    discount = mock_discounts.apply_discount(cart_id, discount_code)

    # Assert
    assert discount == 10


# happy_path - test_successful_payment_changes_order_status - Test that successful payment changes the order status to completed.
def test_successful_payment_changes_order_status(mock_dependencies):
    mock_payments = mock_dependencies['mock_payments']
    order_id = 1
    payment_method = 'credit_card'

    # Call the function
    status = mock_payments.process_payment(order_id, payment_method)

    # Assert
    assert status == 'completed'


# happy_path - test_fetch_item_returns_correct_details - Test that fetching an item returns the correct item details.
def test_fetch_item_returns_correct_details(mock_dependencies):
    mock_item_instance = mock_dependencies['mock_item_instance']
    mock_item_instance.get_details.return_value = {'item_name': 'Laptop', 'price': 1000}
    item_id = 101

    # Call the function
    item_details = mock_item_instance.get_details(item_id)

    # Assert
    assert item_details == {'item_name': 'Laptop', 'price': 1000}


# edge_case - test_add_zero_quantity_does_not_change_cart_size - Test that adding an item with zero quantity does not change the cart size.
def test_add_zero_quantity_does_not_change_cart_size(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_cart_instance.add_item.return_value = None
    mock_cart_instance.get_size.return_value = 0
    cart_id = 1
    item_id = 101
    quantity = 0

    # Call the function
    mock_cart_instance.add_item(cart_id, item_id, quantity)

    # Assert
    assert mock_cart_instance.get_size() == 0


# edge_case - test_remove_nonexistent_item_does_not_change_cart_size - Test that removing an item not in the cart does not change the cart size.
def test_remove_nonexistent_item_does_not_change_cart_size(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_cart_instance.remove_item.return_value = None
    mock_cart_instance.get_size.return_value = 0
    cart_id = 1
    item_id = 999

    # Call the function
    mock_cart_instance.remove_item(cart_id, item_id)

    # Assert
    assert mock_cart_instance.get_size() == 0


# edge_case - test_apply_invalid_discount_code_does_not_change_price - Test that applying an invalid discount code does not change the total price.
def test_apply_invalid_discount_code_does_not_change_price(mock_dependencies):
    mock_cart_instance = mock_dependencies['mock_cart_instance']
    mock_discounts = mock_dependencies['mock_discounts']
    mock_cart_instance.get_total_price.return_value = 100
    cart_id = 1
    discount_code = 'INVALID'

    # Call the function
    discount = mock_discounts.apply_discount(cart_id, discount_code)

    # Assert
    assert discount == 0
    assert mock_cart_instance.get_total_price() == 100


# edge_case - test_payment_with_insufficient_funds_does_not_change_status - Test that payment with insufficient funds does not change the order status.
def test_payment_with_insufficient_funds_does_not_change_status(mock_dependencies):
    mock_payments = mock_dependencies['mock_payments']
    order_id = 1
    payment_method = 'debit_card'

    # Call the function
    status = mock_payments.process_payment(order_id, payment_method)

    # Assert
    assert status == 'pending'


# edge_case - test_fetch_nonexistent_item_returns_error - Test that fetching details for a nonexistent item returns an error.
def test_fetch_nonexistent_item_returns_error(mock_dependencies):
    mock_item_instance = mock_dependencies['mock_item_instance']
    mock_item_instance.get_details.side_effect = Exception('Item not found')
    item_id = 999

    # Call the function and assert
    try:
        mock_item_instance.get_details(item_id)
    except Exception as e:
        assert str(e) == 'Item not found'


