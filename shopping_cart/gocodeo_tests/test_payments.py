import unittest
from shopping_cart.payments import  PaymentMethod, PaymentProcessor, process_payments
from shopping_cart.cart import Cart,Item

class TestPayments(unittest.TestCase):
    def test_concurrency_issue(self):
     
        cart = Cart('premium')

        payment_methods = [PaymentMethod(name="Method1", processing_time=0.1), PaymentMethod(name="Method2", processing_time=0.2)]

        process_payments(cart, payment_methods)

        self.assertEqual(cart.payment_status, "Method1 Payment Processed")
    
    def test_failed_payment_processing(self):
        
        cart = Cart('premium')

        cart.total_price = 50 

        process_payments(cart, "InvalidMethod") 

        self.assertEqual(cart.payment_status, "Payment Processing Failed")
        
    
    def test_successful_payment_processing(self):
        cart = Cart('premium')
        cart.total_price = 100

        payment_methods = [
            PaymentMethod(name="CreditCard", processing_time=0.5),
            PaymentMethod(name="PayPal", processing_time=0.8)
        ]

        process_payments(cart, payment_methods)

        self.assertEqual(cart.payment_status, "PayPal Payment Processed")
       


if __name__ == "__main__":
    unittest.main()


