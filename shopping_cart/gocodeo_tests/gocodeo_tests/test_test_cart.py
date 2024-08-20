import unittest
from unittest.mock import patch, MagicMock
from shopping_cart import Cart, Item

class TestCart(unittest.TestCase):

    @patch('shopping_cart.Database')
    def setUp(self, mock_db):
        # Mock the database connection
        self.mock_db_instance = mock_db.return_value
        self.mock_db_instance.connect.return_value = MagicMock()
        self.mock_db_instance.execute.return_value = MagicMock()
        self.mock_db_instance.commit.return_value = MagicMock()

        # Mock the Cart class
        self.cart = Cart(user_type="regular")
        self.cart.db = self.mock_db_instance

        # Mock Item class if required
        self.mock_item = MagicMock(spec=Item)# happy_path - test_add_item - Add an item to the cart and verify it is added correctly
def test_add_item(self):
        item_id = 1
        quantity = 2
        price = 50.0
        name = "Phone"
        category = "electronics"
        user_type = "premium"
        self.cart.add_item(item_id, quantity, price, name, category, user_type)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0]['item_id'], item_id)
        self.assertEqual(self.cart.items[0]['quantity'], quantity)
        self.assertEqual(self.cart.items[0]['price'], price)
        self.assertEqual(self.cart.items[0]['name'], name)
        self.assertEqual(self.cart.items[0]['category'], category)
        self.assertEqual(self.cart.items[0]['user_type'], user_type)

# edge_case - test_add_item_sql_injection_error - Test adding an item with SQL injection input
def test_add_item_sql_injection_error(self):
        malicious_input = "1; DROP TABLE cart; --"
        item_id = malicious_input
        quantity = 2
        price = 10.0
        name = f"Test Item"
        category = "general"
        user_type="premium"
        with self.assertRaises(Exception) as context:
            self.cart.add_item(item_id, quantity, price, name, category, user_type)
        self.assertIn("SQL injection detected", str(context.exception))

