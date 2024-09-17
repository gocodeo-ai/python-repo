import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import get_all_items_from_cart, get_item_details_from_db, calculate_discounted_price, print_cart_summary, save_cart_to_db
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def mock_cart():
    return MagicMock()

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('shopping_cart.utils.get_item_details_from_db') as mock:
        yield mock

@pytest.fixture
def mock_calculate_total_price():
    mock_cart = MagicMock()
    mock_cart.calculate_total_price = MagicMock(return_value=40.0)
    return mock_cart

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep', return_value=None) as mock:
        yield mock

# happy_path - test_get_all_items_from_cart_returns_all_items - Test that all items are retrieved from the cart with correct details
def test_get_all_items_from_cart_returns_all_items(mock_cart, mock_get_item_details_from_db):
    mock_cart.items = [{'item_id': 1}, {'item_id': 2}]
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}

    all_items = get_all_items_from_cart(mock_cart)

    expected_result = [
        {'name': 'Item 1', 'price': 10.0, 'category': 'general'},
        {'name': 'Item 2', 'price': 10.0, 'category': 'general'}
    ]

    assert all_items == expected_result

# happy_path - test_get_item_details_from_db_returns_correct_details - Test that item details are fetched correctly from the database
def test_get_item_details_from_db_returns_correct_details(mock_time_sleep):
    item_id = 1
    expected_result = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}

    item_details = get_item_details_from_db(item_id)

    assert item_details == expected_result

# happy_path - test_calculate_discounted_price_correctly - Test that discounted price is calculated correctly
def test_calculate_discounted_price_correctly():
    cart = MagicMock()
    cart.items = [{'price': 20.0, 'quantity': 2}, {'price': 10.0, 'quantity': 1}]
    discount_rate = 0.1

    discounted_price = calculate_discounted_price(cart, discount_rate)

    assert discounted_price == 45.0

# happy_path - test_print_cart_summary_outputs_correctly - Test that cart summary is printed correctly
def test_print_cart_summary_outputs_correctly(mock_cart, capsys):
    mock_cart.items = [{'name': 'Item 1', 'category': 'general', 'quantity': 2, 'price': 20.0}]
    mock_cart.calculate_total_price.return_value = 40.0

    print_cart_summary(mock_cart)

    captured = capsys.readouterr()
    expected_output = 'Cart Summary:\nItem: Item 1, Category: general, Quantity: 2, Price: 20.0\nTotal Price: 40.0\n'

    assert captured.out == expected_output

# happy_path - test_save_cart_to_db_saves_items - Test that items are saved to the database
def test_save_cart_to_db_saves_items(mock_cart, mock_add_item_to_cart_db):
    mock_cart.items = [{'item_id': 1, 'quantity': 2, 'price': 20.0}, {'item_id': 2, 'quantity': 1, 'price': 10.0}]

    save_cart_to_db(mock_cart)

    assert mock_add_item_to_cart_db.call_count == 2

# edge_case - test_get_all_items_from_cart_with_empty_cart - Test that an empty cart returns an empty list of items
def test_get_all_items_from_cart_with_empty_cart(mock_cart):
    mock_cart.items = []

    all_items = get_all_items_from_cart(mock_cart)

    assert all_items == []

# edge_case - test_get_item_details_from_db_with_invalid_id - Test that an invalid item_id returns None or error
def test_get_item_details_from_db_with_invalid_id(mock_get_item_details_from_db):
    mock_get_item_details_from_db.side_effect = Exception('Item not found')

    with pytest.raises(Exception) as excinfo:
        get_item_details_from_db(9999)

    assert str(excinfo.value) == 'Item not found'

# edge_case - test_calculate_discounted_price_with_negative_discount - Test that a negative discount rate is handled
def test_calculate_discounted_price_with_negative_discount():
    cart = MagicMock()
    cart.items = [{'price': 20.0, 'quantity': 2}]
    discount_rate = -0.1

    with pytest.raises(ValueError) as excinfo:
        calculate_discounted_price(cart, discount_rate)

    assert str(excinfo.value) == 'Invalid discount rate'

# edge_case - test_print_cart_summary_with_empty_cart - Test that an empty cart prints a summary with zero total price
def test_print_cart_summary_with_empty_cart(mock_cart, capsys):
    mock_cart.items = []
    mock_cart.calculate_total_price.return_value = 0.0

    print_cart_summary(mock_cart)

    captured = capsys.readouterr()
    expected_output = 'Cart Summary:\nTotal Price: 0.0\n'

    assert captured.out == expected_output

# edge_case - test_save_cart_to_db_with_empty_cart - Test that saving an empty cart to the database does nothing
def test_save_cart_to_db_with_empty_cart(mock_cart, mock_add_item_to_cart_db):
    mock_cart.items = []

    save_cart_to_db(mock_cart)

    assert mock_add_item_to_cart_db.call_count == 0

