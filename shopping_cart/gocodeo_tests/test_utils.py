import pytest
from unittest.mock import patch, MagicMock
from shopping_cart.database import add_item_to_cart_db
import time

@pytest.fixture
def cart():
    class Cart:
        def __init__(self):
            self.items = [
                {"item_id": 1, "name": "Item 1", "category": "general", "quantity": 2, "price": 10.0},
                {"item_id": 2, "name": "Item 2", "category": "general", "quantity": 1, "price": 20.0}
            ]
        
        def calculate_total_price(self):
            return sum(item["price"] * item["quantity"] for item in self.items)
    
    return Cart()

@pytest.fixture
def mock_add_item_to_cart_db():
    with patch('shopping_cart.database.add_item_to_cart_db') as mock:
        yield mock

@pytest.fixture
def mock_time_sleep():
    with patch('time.sleep') as mock:
        yield mock

@pytest.fixture
def mock_get_item_details_from_db():
    with patch('__main__.get_item_details_from_db') as mock:
        mock.side_effect = lambda item_id: {"name": f"Item {item_id}", "price": 10.0, "category": "general"}
        yield mock

@pytest.fixture
def setup_all_mocks(mock_add_item_to_cart_db, mock_time_sleep, mock_get_item_details_from_db):
    pass# happy_path - get_all_items_from_cart - Test getting all items from cart returns correct item details
def test_get_all_items_from_cart(cart, setup_all_mocks):
    all_items = get_all_items_from_cart(cart)
    assert len(all_items) == 2
    assert all_items[0]['name'] == 'Item 1'
    assert all_items[1]['name'] == 'Item 2'

# happy_path - calculate_discounted_price - Test calculating discounted price for the cart
def test_calculate_discounted_price(cart):
    discounted_price = calculate_discounted_price(cart, 0.1)
    assert discounted_price == 36.0

# happy_path - print_cart_summary - Test print cart summary does not raise exceptions
def test_print_cart_summary(cart, capsys):
    print_cart_summary(cart)
    captured = capsys.readouterr()
    assert 'Cart Summary:' in captured.out
    assert 'Item: Item 1' in captured.out
    assert 'Total Price:' in captured.out

# happy_path - save_cart_to_db - Test saving cart to database calls add_item_to_cart_db for each item
def test_save_cart_to_db(cart, mock_add_item_to_cart_db):
    save_cart_to_db(cart)
    assert mock_add_item_to_cart_db.call_count == 2

# edge_case - get_all_items_from_cart - Test getting all items from an empty cart returns an empty list
def test_get_all_items_from_empty_cart():
    class EmptyCart:
        items = []
        def calculate_total_price(self):
            return 0
    empty_cart = EmptyCart()
    all_items = get_all_items_from_cart(empty_cart)
    assert all_items == []

# edge_case - calculate_discounted_price - Test calculating discounted price with a discount rate of 0
def test_calculate_discounted_price_zero_discount(cart):
    discounted_price = calculate_discounted_price(cart, 0)
    assert discounted_price == 40.0

# edge_case - calculate_discounted_price - Test calculating discounted price with a discount rate greater than 1
def test_calculate_discounted_price_high_discount(cart):
    discounted_price = calculate_discounted_price(cart, 1.5)
    assert discounted_price == 0.0

# edge_case - save_cart_to_db - Test saving an empty cart to database does not call add_item_to_cart_db
def test_save_empty_cart_to_db(mock_add_item_to_cart_db):
    class EmptyCart:
        items = []
        def calculate_total_price(self):
            return 0
    empty_cart = EmptyCart()
    save_cart_to_db(empty_cart)
    assert mock_add_item_to_cart_db.call_count == 0

