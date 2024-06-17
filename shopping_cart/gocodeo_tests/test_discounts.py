import unittest
from unittest.mock import MagicMock
from shopping_cart.cart import Cart,Item
from shopping_cart.discounts import Discount


class TestDiscount(unittest.TestCase):
    def setUp(self):
        self.cart = Cart(user_type="regular")
        self.cart.user_type = "regular"
        item1 = {"item_id":1, "price":50.0, "name":"Phone", "category":"electronics", "user_type": "premium", "quantity": 2}
        item2 = {"item_id":2, "price":50.0, "name":"Tab", "category":"electronics", "user_type": "premium", "quantity": 4}

        self.cart.items = [
           item1,
           item2
        ]

    def test_apply_discount_logic_error(self):
        self.cart.user_type = "premium"
        discount = Discount(0.1, 50)
        total_price = discount.apply_discount(self.cart)
        self.assertAlmostEqual(total_price, 85.0, places=2, msg="Both values should be equal")

    def test_apply_bulk_discount(self):
        bulk_discount_rate = 0.20
        bulk_quantity = 3
        discount = Discount(0.1, 50)
        discount.apply_bulk_discount(self.cart, bulk_quantity, bulk_discount_rate)
        self.assertAlmostEqual(self.cart.items[1]["price"], 50 * 0.8, places=2, msg="Both values should be equal")

    def test_apply_seasonal_discount_holiday(self):
        seasonal_discount_rate = 0.20
        season = "holiday"
        discount = Discount(0.1, 50)
        discount.apply_seasonal_discount(self.cart, season, seasonal_discount_rate)
        self.assertAlmostEqual(self.cart.total_price, (2 * 50 + 4 * 50) * 0.8, places=2, msg="Both values should be equal")

    def test_apply_category_discount(self):
        category_discount_rate = 0.25
        category = "electronics"
        discount = Discount(0.1, 50)
        discount.apply_category_discount(self.cart, category, category_discount_rate)
        self.assertAlmostEqual(self.cart.items[1]["price"], 50 * 0.75, places=2, msg="Both values should be equal")

    def test_apply_loyalty_discount(self):
        loyalty_discount_rate = 0.05
        loyalty_years = 3
        self.cart.user_type = "loyal"
        discount = Discount(0.1, 50)
        discount.apply_loyalty_discount(self.cart, loyalty_years, loyalty_discount_rate)
        self.assertAlmostEqual(self.cart.total_price, (2 * 50 + 4 * 50) * 0.95, places=2, msg="Both values should be equal")

    def test_apply_flash_sale_discount(self):
        flash_sale_rate = 0.30
        items_on_sale = [1, 2]
        discount = Discount(0.1, 50)
        discount.apply_flash_sale_discount(self.cart, flash_sale_rate, items_on_sale)
        self.assertAlmostEqual(self.cart.items[0]["price"], 50 * 0.7, places=2, msg="Both values should be equal")
        self.assertAlmostEqual(self.cart.items[1]["price"], 50 * 0.7, places=2, msg="Both values should be equal")

if __name__ == '__main__':
    unittest.main()
