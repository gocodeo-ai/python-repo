import unittest
from unittest.mock import MagicMock, patch
from shopping_cart.utils import get_all_items_from_cart, calculate_discounted_price, print_cart_summary, save_cart_to_db
from shopping_cart.cart import Cart, Item
import time

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.cart = Cart(user_type="regular")
    def test_get_all_items_performance(self):
        self.cart.items = [{"item_id": i , "quantity": 1} for i in range(10)]

        start_time = time.time()
        get_all_items_from_cart(self.cart)
        end_time = time.time()

        threshold_time = 0.5  # in seconds

        execution_time = end_time - start_time
       
        self.assertLess(execution_time, threshold_time, f"Performance bottleneck: Execution time {execution_time} exceeds threshold {threshold_time} seconds")


   
    def test_get_all_items_from_cart(self):
        item1 = {"item_id":1, "price":50.0, "name":"Item 1", "category":"electronics", "user_type": "premium", "quantity": 2}
        item2 = {"item_id":2, "price":50.0, "name":"Item 2", "category":"electronics", "user_type": "premium", "quantity": 4}

        self.cart.items = [
           item1,
           item2
        ]

        items = get_all_items_from_cart(self.cart)
        
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'Item 1')
        self.assertEqual(items[1]['name'], 'Item 2')


    def test_calculate_discounted_price(self):
        item1 = {"item_id":1, "price":50.0, "name":"Item 1", "category":"electronics", "user_type": "premium", "quantity": 2}
        item2 = {"item_id":2, "price":50.0, "name":"Item 2", "category":"electronics", "user_type": "premium", "quantity": 4}

        self.cart.items = [
           item1,
           item2
        ]

        discount_rate = 0.1  # 10% discount
        discounted_price = calculate_discounted_price(self.cart, discount_rate)
        
        expected_price = 50.0 * 2 + 50.0 * 4  # Total without discount
        expected_discounted_price = expected_price * (1 - discount_rate)
        
        self.assertEqual(discounted_price, expected_discounted_price)

    @patch('builtins.print')
    def test_print_cart_summary(self, mock_print):
        item1 = {"item_id":1, "price":50.0, "name":"Item 1", "category":"electronics", "user_type": "premium", "quantity": 2}
        item2 = {"item_id":2, "price":50.0, "name":"Item 2", "category":"electronics", "user_type": "premium", "quantity": 4}

        self.cart.items = [
           item1,
           item2
        ]

        self.cart.calculate_total_price()
        print_cart_summary(self.cart)

        print("Cart Summary:")
        print("Item: Item 1, Category: general, Quantity: 2, Price: 50.0")
        print("Item: Item 2, Category: general, Quantity: 4, Price: 50.0")
        print("Total Price: 300.0")

    @patch('database.add_item_to_cart_db')
    def test_save_cart_to_db(self, mock_add_item_to_cart_db):
        item1 = {"item_id":1, "price":50.0, "name":"Item 1", "category":"electronics", "user_type": "premium", "quantity": 2}
        item2 = {"item_id":2, "price":50.0, "name":"Item 2", "category":"electronics", "user_type": "premium", "quantity": 4}

        self.cart.items = [
           item1,
           item2
        ]

        save_cart_to_db(self.cart)
        items = get_all_items_from_cart(self.cart)
         
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'Item 1')
        self.assertEqual(items[1]['name'], 'Item 2')



if __name__ == "__main__":
    unittest.main()
