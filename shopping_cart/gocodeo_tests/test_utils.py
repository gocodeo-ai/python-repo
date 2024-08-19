import pytest
from unittest.mock import patch, MagicMock

# Mocking dependencies
@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock:
        yield mock

@pytest.fixture
def cart_fixture():
    class Cart:
        def __init__(self, items):
            self.items = items

        def calculate_total_price(self):
            return sum(item['price'] * item['quantity'] for item in self.items)

    return Cart

@pytest.fixture
def setup_mocks(mock_add_item_to_cart_db, mock_time_sleep, cart_fixture):
    return {
        'mock_add_item_to_cart_db': mock_add_item_to_cart_db,
        'mock_time_sleep': mock_time_sleep,
        'cart_fixture': cart_fixture
    }# happy_path - get_all_items_from_cart - Test retrieving all items from a cart with multiple items.
def test_get_all_items_from_cart(cart_fixture):
    cart = cart_fixture(items=[{'item_id': 1, 'quantity': 2}, {'item_id': 2, 'quantity': 1}])
    result = get_all_items_from_cart(cart)
    expected_result = [{'name': 'Item 1', 'price': 10.0, 'category': 'general'}, {'name': 'Item 2', 'price': 10.0, 'category': 'general'}]
    assert result == expected_result

# happy_path - get_item_details_from_db - Test retrieving item details from the database.
def test_get_item_details_from_db():
    result = get_item_details_from_db(3)
    expected_result = {'name': 'Item 3', 'price': 10.0, 'category': 'general'}
    assert result == expected_result

# happy_path - calculate_discounted_price - Test calculating discounted price for a cart.
def test_calculate_discounted_price(cart_fixture):
    cart = cart_fixture(items=[{'price': 10.0, 'quantity': 2}, {'price': 20.0, 'quantity': 1}])
    result = calculate_discounted_price(cart, 0.1)
    expected_result = 27.0
    assert result == expected_result

# happy_path - print_cart_summary - Test printing cart summary with items.
def test_print_cart_summary(cart_fixture, capsys):
    cart = cart_fixture(items=[{'name': 'Item 1', 'category': 'general', 'quantity': 1, 'price': 10.0}])
    cart.calculate_total_price = lambda: 10.0
    print_cart_summary(cart)
    captured = capsys.readouterr()
    expected_output = 'Cart Summary:\nItem: Item 1, Category: general, Quantity: 1, Price: 10.0\nTotal Price: 10.0\n'
    assert captured.out == expected_output

# happy_path - save_cart_to_db - Test saving cart to the database with valid items.
def test_save_cart_to_db(cart_fixture, mock_add_item_to_cart_db):
    cart = cart_fixture(items=[{'item_id': 1, 'quantity': 2, 'price': 10.0}, {'item_id': 2, 'quantity': 1, 'price': 20.0}])
    save_cart_to_db(cart)
    assert mock_add_item_to_cart_db.call_count == 2

# edge_case - get_all_items_from_cart - Test retrieving items from an empty cart.
def test_get_all_items_from_empty_cart(cart_fixture):
    cart = cart_fixture(items=[])
    result = get_all_items_from_cart(cart)
    expected_result = []
    assert result == expected_result

# edge_case - get_item_details_from_db - Test retrieving item details with an invalid item ID.
def test_get_item_details_from_invalid_id():
    result = get_item_details_from_db(999)
    expected_result = None
    assert result == expected_result

# edge_case - calculate_discounted_price - Test calculating discounted price with zero items in cart.
def test_calculate_discounted_price_with_empty_cart(cart_fixture):
    cart = cart_fixture(items=[])
    result = calculate_discounted_price(cart, 0.2)
    expected_result = 0.0
    assert result == expected_result

# edge_case - print_cart_summary - Test printing cart summary with no items.
def test_print_cart_summary_with_no_items(cart_fixture, capsys):
    cart = cart_fixture(items=[])
    cart.calculate_total_price = lambda: 0.0
    print_cart_summary(cart)
    captured = capsys.readouterr()
    expected_output = 'Cart Summary:\nTotal Price: 0.0\n'
    assert captured.out == expected_output

# edge_case - save_cart_to_db - Test saving an empty cart to the database.
def test_save_empty_cart_to_db(cart_fixture, mock_add_item_to_cart_db):
    cart = cart_fixture(items=[])
    save_cart_to_db(cart)
    assert mock_add_item_to_cart_db.call_count == 0

