import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.utils import (
    get_all_items_from_cart,
    get_item_details_from_db,
    calculate_discounted_price,
    print_cart_summary,
    save_cart_to_db
)
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
def mock_print_cart_summary(capsys):
    with patch('builtins.print') as mock:
        yield mock, capsys

@pytest.fixture
def mock_calculate_total_price():
    with patch.object(mock_cart, 'calculate_total_price', return_value=40.0) as mock:
        yield mock

# happy path - get_all_items_from_cart - Test that all items are fetched from cart with correct details.
def test_get_all_items_from_cart(mock_cart, mock_get_item_details_from_db):
    mock_cart.items = [{'item_id': 1}, {'item_id': 2}]
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}
    all_items = get_all_items_from_cart(mock_cart)
    expected_items = [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]
    assert all_items == expected_items



# happy path - get_item_details_from_db - Test that item details are fetched correctly from the database.
def test_get_item_details_from_db():
    item_details = get_item_details_from_db(1)
    expected_details = {'name': 'Item 1', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_details



# happy path - calculate_discounted_price - Test that discounted price is calculated correctly for a cart.
def test_calculate_discounted_price(mock_cart):
    mock_cart.items = [{'price': 10.0, 'quantity': 2}, {'price': 20.0, 'quantity': 1}]
    discounted_price = calculate_discounted_price(mock_cart, 0.1)
    assert discounted_price == 36.0



# happy path - print_cart_summary - Test that cart summary is printed with correct details.
def test_print_cart_summary(mock_cart, mock_print_cart_summary):
    mock_cart.items = [{'name': 'Item 1', 'category': 'general', 'quantity': 1, 'price': 10.0}, {'name': 'Item 2', 'category': 'general', 'quantity': 2, 'price': 15.0}]
    mock_cart.calculate_total_price.return_value = 40.0
    mock_print, capsys = mock_print_cart_summary
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    expected_output = "Cart Summary:\nItem: Item 1, Category: general, Quantity: 1, Price: 10.0\nItem: Item 2, Category: general, Quantity: 2, Price: 15.0\nTotal Price: 40.0\n"
    assert captured.out == expected_output



# happy path - save_cart_to_db - Test that cart items are saved to the database correctly.
def test_save_cart_to_db(mock_cart, mock_add_item_to_cart_db):
    mock_cart.items = [{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 1, 'price': 20.0}]
    save_cart_to_db(mock_cart)
    expected_calls = [
        patch('shopping_cart.database.add_item_to_cart_db').call_args_list == [
            ('INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)',),
            ('INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)',)
        ]
    ]
    assert mock_add_item_to_cart_db.call_args_list == expected_calls



# edge case - get_all_items_from_cart - Test that fetching items from an empty cart returns an empty list.
def test_get_all_items_from_empty_cart(mock_cart):
    mock_cart.items = []
    all_items = get_all_items_from_cart(mock_cart)
    assert all_items == []



# edge case - get_item_details_from_db - Test that fetching item details with invalid item_id returns default values.
def test_get_item_details_from_db_invalid_id():
    item_details = get_item_details_from_db(999)
    expected_details = {'name': 'Item 999', 'price': 10.0, 'category': 'general'}
    assert item_details == expected_details



# edge case - calculate_discounted_price - Test that calculating discounted price with zero discount returns total price.
def test_calculate_discounted_price_zero_discount(mock_cart):
    mock_cart.items = [{'price': 50.0, 'quantity': 1}]
    discounted_price = calculate_discounted_price(mock_cart, 0.0)
    assert discounted_price == 50.0



# edge case - print_cart_summary - Test that printing cart summary with no items shows only total price as zero.
def test_print_cart_summary_empty_cart(mock_cart, mock_print_cart_summary):
    mock_cart.items = []
    mock_cart.calculate_total_price.return_value = 0.0
    mock_print, capsys = mock_print_cart_summary
    print_cart_summary(mock_cart)
    captured = capsys.readouterr()
    expected_output = "Cart Summary:\nTotal Price: 0.0\n"
    assert captured.out == expected_output



# edge case - save_cart_to_db - Test that saving an empty cart to the database makes no database calls.
def test_save_empty_cart_to_db(mock_cart, mock_add_item_to_cart_db):
    mock_cart.items = []
    save_cart_to_db(mock_cart)
    assert not mock_add_item_to_cart_db.called



