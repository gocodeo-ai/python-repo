import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db

@pytest.fixture
def cart():
    class Cart:
        def __init__(self):
            self.items = [
                {"item_id": 1, "name": "Item 1", "category": "general", "quantity": 2, "price": 10.0},
                {"item_id": 2, "name": "Item 2", "category": "general", "quantity": 1, "price": 20.0}
            ]

        def calculate_total_price(self):
            return sum(item['price'] * item['quantity'] for item in self.items)

    return Cart()

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('your_module.get_item_details_from_db') as mock:
        yield mock

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock:
        yield mock

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock# happy_path - get_all_items_from_cart - Retrieve all items from the cart and their details
def test_get_all_items_from_cart(cart, mock_get_item_details_from_db):
    mock_get_item_details_from_db.side_effect = lambda item_id: {'name': f'Item {item_id}', 'price': 10.0, 'category': 'general'}
    items = get_all_items_from_cart(cart)
    assert len(items) == 2
    assert items[0]['name'] == 'Item 1'
    assert items[1]['name'] == 'Item 2'

# happy_path - calculate_discounted_price - Calculate the discounted price of items in the cart
def test_calculate_discounted_price(cart):
    discounted_price = calculate_discounted_price(cart, 0.1)
    assert discounted_price == 36.0

# happy_path - print_cart_summary - Print the summary of the cart items
def test_print_cart_summary(cart, capsys):
    print_cart_summary(cart)
    captured = capsys.readouterr()
    assert 'Cart Summary:' in captured.out
    assert 'Item: Item 1' in captured.out
    assert 'Total Price: 40.0' in captured.out

# happy_path - save_cart_to_db - Save the cart items to the database
def test_save_cart_to_db(cart, mock_add_item_to_cart_db):
    save_cart_to_db(cart)
    assert mock_add_item_to_cart_db.call_count == 2
    mock_add_item_to_cart_db.assert_any_call('INSERT INTO cart (item_id, quantity, price) VALUES (1, 2, 10.0)')
    mock_add_item_to_cart_db.assert_any_call('INSERT INTO cart (item_id, quantity, price) VALUES (2, 1, 20.0)')

