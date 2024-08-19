import unittest
from shopping_cart import Cart, Item

class TestCart(unittest.TestCase):

    def setUp(self):
        self.cart = Cart(user_type="regular")

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
     

    def test_remove_item(self):
        item_id = 1
        quantity = 2
        price = 50.0
        name = "Phone"
        category = "electronics"
        user_type = "premium"
        self.cart.add_item(item_id, quantity, price, name, category, user_type)
        
        self.cart.remove_item(item_id)
        
        self.assertEqual(len(self.cart.items), 0)
        
        

    def test_update_item_quantity(self):
        item_id = 1
        quantity = 2
        new_quantity = 5
        price = 50.0
        name = "Phone"
        category = "electronics"
        user_type = "premium"
        self.cart.add_item(item_id, quantity, price, name, category, user_type)
        
        self.cart.update_item_quantity(item_id, new_quantity)
        
        self.assertEqual(self.cart.items[0]['quantity'], new_quantity)
   

    def test_calculate_total_price(self):
        item1 = {"item_id":1, "price":50.0, "name":"Phone", "category":"electronics", "user_type": "premium", "quantity": 2}
        item2 = {"item_id":2, "price":30.0, "name":"Book", "category":"Books", "user_type": "premium", "quantity": 1}

        self.cart.items = [
           item1,
           item2
        ]
        
        total_price = self.cart.calculate_total_price()
        
        expected_total = (50.0 * 2) + 30.0
        self.assertEqual(total_price, expected_total)

  
    def test_empty_cart(self):
        item1 = {"item_id":1, "price":50.0, "name":"Phone", "category":"electronics", "user_type": "premium", "quantity": 2}

        self.cart.items = [
            item1
        ]
        
        self.cart.empty_cart()
        
        self.assertEqual(len(self.cart.items), 0)
        
      
    def test_add_item_sql_injection_error(self):
        # Simulate SQL injection by providing malicious input
        malicious_input = "1; DROP TABLE cart; --"

        item_id = malicious_input
        quantity = 2
        price = 10.0
        name = f"Test Item" 
        category = "general"
        user_type="premium"
         # Call add_item method with malicious input and assert exception
        with self.assertRaises(Exception) as context:
             self.cart.add_item(item_id, quantity, price, name, category, user_type)
        
       
        # Check if the expected error message is in the raised exception
        self.assertIn("SQL injection detected", str(context.exception))
       
                 
     

if __name__ == '__main__':
    unittest.main()
