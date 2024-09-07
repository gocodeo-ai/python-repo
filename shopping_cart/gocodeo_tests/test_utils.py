import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_dependencies():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock_get_item_details_from_db, \
         patch('shopping_cart.database.add_item_to_cart_db') as mock_add_item_to_cart_db:
        
        # Mock get_item_details_from_db
        def mock_get_item_details_from_db_side_effect(item_id):
            return {"name": f"Item {item_id}", "price": 10.0, "category": "general"}
        mock_get_item_details_from_db.side_effect = mock_get_item_details_from_db_side_effect

        # Mock add_item_to_cart_db
        mock_add_item_to_cart_db.return_value = None

        yield {
            'mock_get_item_details_from_db': mock_get_item_details_from_db,
            'mock_add_item_to_cart_db': mock_add_item_to_cart_db,
        }

# happy_path - test_get_all_items_from_cart_happy_path - Test that all items are returned with correct details from the cart
def test_get_all_items_from_cart_happy_path(mock_dependencies):
    cart = {'items': [{'item_id': 1}, {'item_id': 2}]}
    expected_result = [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]
    result = get_all_items_from_cart(cart)
    assert result == expected_result
    assert mock_dependencies['mock_get_item_details_from_db'].call_count == 2

# happy_path - test_get_item_details_from_db_happy_path - Test that item details are returned correctly from the database
def test_get_item_details_from_db_happy_path(mock_dependencies):
    item_id = 1
    expected_result = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    result = get_item_details_from_db(item_id)
    assert result == expected_result
    mock_dependencies['mock_get_item_details_from_db'].assert_called_once_with(item_id)

# happy_path - test_calculate_discounted_price_happy_path - Test that discounted price is calculated correctly for the cart
def test_calculate_discounted_price_happy_path():
    cart = {'items': [{'price': 10.0, 'quantity': 2}, {'price': 20.0, 'quantity': 1}]}
    discount_rate = 0.1
    expected_result = 45.0
    result = calculate_discounted_price(cart, discount_rate)
    assert result == expected_result

# happy_path - test_print_cart_summary_happy_path - Test that cart summary is printed correctly
def test_print_cart_summary_happy_path(capfd):
    cart = {'items': [{'name': 'Item 1', 'category': 'general', 'quantity': 2, 'price': 10.0}], 'calculate_total_price': lambda: 20.0}
    print_cart_summary(cart)
    captured = capfd.readouterr()
    expected_output = "Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 10.0\nTotal Price: 20.0\n"
    assert captured.out == expected_output

# happy_path - test_save_cart_to_db_happy_path - Test that all items are saved to the database correctly
def test_save_cart_to_db_happy_path(mock_dependencies):
    cart = {'items': [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 1, 'price': 20.0}]}
    save_cart_to_db(cart)
    expected_queries = [
        'INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)',
        'INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)'
    ]
    for query in expected_queries:
        mock_dependencies['mock_add_item_to_cart_db'].assert_any_call(query)
    assert mock_dependencies['mock_add_item_to_cart_db'].call_count == 2

# edge_case - test_get_all_items_from_cart_edge_case_empty_cart - Test that an empty cart returns an empty list of items
def test_get_all_items_from_cart_edge_case_empty_cart():
    cart = {'items': []}
    expected_result = []
    result = get_all_items_from_cart(cart)
    assert result == expected_result

# edge_case - test_get_item_details_from_db_edge_case_non_existent_item - Test that item details are returned with default values for a non-existent item
def test_get_item_details_from_db_edge_case_non_existent_item(mock_dependencies):
    item_id = 999
    expected_result = {'name': 'Item 999', 'price': 10.0, 'category': 'general'}
    result = get_item_details_from_db(item_id)
    assert result == expected_result
    mock_dependencies['mock_get_item_details_from_db'].assert_called_once_with(item_id)

# edge_case - test_calculate_discounted_price_edge_case_zero_discount - Test that discounted price calculation handles zero discount rate
def test_calculate_discounted_price_edge_case_zero_discount():
    cart = {'items': [{'price': 10.0, 'quantity': 2}, {'price': 20.0, 'quantity': 1}]}
    discount_rate = 0.0
    expected_result = 40.0
    result = calculate_discounted_price(cart, discount_rate)
    assert result == expected_result

# edge_case - test_print_cart_summary_edge_case_empty_cart - Test that cart summary handles an empty cart
def test_print_cart_summary_edge_case_empty_cart(capfd):
    cart = {'items': [], 'calculate_total_price': lambda: 0.0}
    print_cart_summary(cart)
    captured = capfd.readouterr()
    expected_output = "Cart Summary:\nTotal Price: 0.0\n"
    assert captured.out == expected_output

# edge_case - test_save_cart_to_db_edge_case_empty_cart - Test that saving an empty cart to the database results in no queries
def test_save_cart_to_db_edge_case_empty_cart(mock_dependencies):
    cart = {'items': []}
    save_cart_to_db(cart)
    mock_dependencies['mock_add_item_to_cart_db'].assert_not_called()

