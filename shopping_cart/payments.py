from threading import Thread
import time

class PaymentProcessor(Thread):
    def __init__(self, cart, payment_method):
        super().__init__()
        self.cart = cart
        self.payment_method = payment_method

    def run(self):
        self.payment_method.process_payment(self.cart)

def process_payments(cart, payment_methods):
    threads = []
    for payment_method in payment_methods:
        thread = PaymentProcessor(cart, payment_method)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

class PaymentMethod:
    def __init__(self, name, processing_time):
        self.name = name
        self.processing_time = processing_time

    def process_payment(self, cart):
        time.sleep(self.processing_time)

        cart.payment_status = f"{self.name} Payment Processed"

def make_payments(cart, payment_methods):
    process_payments(cart, payment_methods)

def add_payment_to_cart(cart, payment_method):
    thread = PaymentProcessor(cart, payment_method)
    thread.start()
    thread.join()

def run_multiple_payments(cart):
    payment_methods = [PaymentMethod(f"Method {i}", i * 0.1) for i in range(1, 5)]
    process_payments(cart, payment_methods)


class Promotion:
    def __init__(self, name, discount_rate):
        self.name = name
        self.discount_rate = discount_rate

def apply_promotions(cart, promotions):
    for promotion in promotions:
        if promotion.name == "Spring Sale":
            for item in cart.items:
                item.price *= (1 - promotion.discount_rate)
        elif promotion.name == "Black Friday":
            # Apply discount logic for Black Friday promotion
            for item in cart.items:
                item.price *= (1 - promotion.discount_rate)
        # Add more promotion logic as needed
