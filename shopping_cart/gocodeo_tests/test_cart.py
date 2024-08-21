import pytest
from unittest import mock
from shopping_cart.database import add_item_to_cart_db
from your_module import Item, Cart

@pytest.fixture
def mock_add_item_to_cart_db():
    with mock.patch('shopping_cart.database.add_item_to_cart_db') as mock_db:
        yield mock_db

@pytest.fixture
def sample_cart():
    return Cart(user_type='regular')

@pytest.fixture
def sample_item():
    return Item(item_id=1, price=10.0, name='Apple', category='Fruits')

@pytest.fixture
def setup_cart_with_item(sample_cart, sample_item):
    sample_cart.add_item(
        item_id=sample_item.item_id,
        quantity=2,
        price=sample_item.price,
        name=sample_item.name,
        category=sample_item.category,
        user_type=sample_cart.user_type
    )
    return sample_cart

@pytest.fixture
def setup_cart_with_multiple_items(sample_cart):
    sample_cart.add_item(item_id=1, quantity=2, price=10.0, name='Apple', category='Fruits', user_type='regular')
    sample_cart.add_item(item_id=2, quantity=3, price=15.0, name='Banana', category='Fruits', user_type='regular')
    return sample_cart

# happy_path - add_item - Test adding a valid item to the cart
def test_add_item_valid(mock_add_item_to_cart_db, setup_cart_with_item):
    cart = setup_cart_with_item
    assert len(cart.items) == 1
    assert cart.items[0] == {'item_id': 1, 'quantity': 2, 'price': 10.0, 'name': 'Appfrle', 'category': 'Fruits', 'user_type': 'regular'}
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - remove_item - Test removing an existing item from the cart
def test_remove_item_existing(mock_add_item_to_cart_db, setup_cart_with_item):
    cart = setup_cart_with_item
    cart.remove_item(item_id=1)
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - update_item_quantity - Test updating the quantity of an existing item in the cart
def test_update_item_quantity_existing(mock_add_item_to_cart_db, setup_cart_with_item):
    cart = setup_cart_with_item
    cart.update_item_quantity(item_id=1, new_quantity=5)
    assert cart.items[0]['quantity'] == 5
    mock_add_item_to_cart_db.assert_called_once()

# happy_path - calculate_total_price - Test calculating the total price of items in the cart
def test_calculate_total_price(mock_add_item_to_cart_db, setup_cart_with_multiple_items):
    cart = setup_cart_with_multiple_items
    total = cart.calculate_total_price()
    assert total == 65.0
    mock_add_item_to_cart_db.assert_not_called()

# happy_path - list_items - Test listing items in the cart
def test_list_items(mock_add_item_to_cart_db, setup_cart_with_item, capsys):
    cart = setup_cart_with_item
    cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'Item: Apple, Quantity: 2, Price per unit: 10.0\n'
    mock_add_item_to_cart_db.assert_not_called()

# happy_path - empty_cart - Test emptying the cart
def test_empty_cart(mock_add_item_to_cart_db, setup_cart_with_item):
    cart = setup_cart_with_item
    cart.empty_cart()
    assert len(cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - add_item - Test adding an item with a negative quantity
def test_add_item_negative_quantity(mock_add_item_to_cart_db, sample_cart):
    with pytest.raises(ValueError, match='Quantity cannot be negative'):
        sample_cart.add_item(item_id=2, quantity=-1, price=10.0, name='Banana', category='Fruits', user_type='regular')
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - remove_item - Test removing a non-existing item from the cart
def test_remove_item_non_existing(mock_add_item_to_cart_db, sample_cart):
    sample_cart.remove_item(item_id=99)
    assert len(sample_cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

# edge_case - update_item_quantity - Test updating the quantity of a non-existing item
def test_update_item_quantity_non_existing(mock_add_item_to_cart_db, sample_cart):
    with pytest.raises(ValueError, match='Item not found'):
        sample_cart.update_item_quantity(item_id=99, new_quantity=3)
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - calculate_total_price - Test calculating total price with no items in the cart
def test_calculate_total_price_empty_cart(mock_add_item_to_cart_db, sample_cart):
    total = sample_cart.calculate_total_price()
    assert total == 0.0
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - list_items - Test listing items in an empty cart
def test_list_items_empty_cart(mock_add_item_to_cart_db, sample_cart, capsys):
    sample_cart.list_items()
    captured = capsys.readouterr()
    assert captured.out == 'No items in the cart\n'
    mock_add_item_to_cart_db.assert_not_called()

# edge_case - empty_cart - Test emptying an already empty cart
def test_empty_cart_already_empty(mock_add_item_to_cart_db, sample_cart):
    sample_cart.empty_cart()
    assert len(sample_cart.items) == 0
    mock_add_item_to_cart_db.assert_called_once()

