import unittest
import os
import psutil
from memory_profiler import memory_usage
from shopping_cart.database import DatabaseConnection, add_item_to_cart_db
import sqlite3

class TestMemoryLeak(unittest.TestCase):
    def setUp(self):
        self.db_path = "shopping_cart.db"
        self.db_connection = DatabaseConnection(self.db_path)
        self.db_connection.connect()
        self.init_database()

    def tearDown(self):
        os.remove(self.db_path)

    def init_database(self):
        create_table_query = '''
                                CREATE TABLE IF NOT EXISTS  cart (
                                    id INTEGER PRIMARY KEY,
                                    item_id INTEGER ,
                                    name TEXT,
                                    price REAL,
                                    quantity INTEGER,
                                    category TEXT,
                                    user_type TEXT,
                                    payment_status
                                );
                             '''
         
        self.db_connection.execute(create_table_query, None)
        self.db_connection.commit()


    def test_connection(self):
        self.db_connection.connect()
        self.assertIsNotNone(self.db_connection.connection)
        self.db_connection.close()
        self.assertIsNone(self.db_connection.connection)

    def test_execute_insert(self):
        insert_query = "INSERT INTO cart (item_id, name, price, quantity, category, user_type, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params = (1, "Item 1", 10.0, 1, "general", "regular", "pending")
        self.db_connection.execute(insert_query, params)
        self.db_connection.commit()

        select_query = "SELECT * FROM cart WHERE item_id = ?"
        result = self.db_connection.fetchone(select_query, (1,))
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 1)

    def test_execute_update(self):
        self.test_execute_insert()
        update_query = "UPDATE cart SET price = ? WHERE item_id = ?"
        self.db_connection.execute(update_query, (20.0, 1))
        self.db_connection.commit()

        select_query = "SELECT price FROM cart WHERE item_id = ?"
        result = self.db_connection.fetchone(select_query, (1,))
        self.assertEqual(result[0], 20.0)

    def test_execute_delete(self):
        self.test_execute_insert()
        delete_query = "DELETE FROM cart WHERE item_id = ?"
        self.db_connection.execute(delete_query, (1,))
        self.db_connection.commit()

        select_query = "SELECT * FROM cart WHERE item_id = ?"
        result = self.db_connection.fetchone(select_query, (1,))
        self.assertIsNone(result)

    def test_fetchone(self):
        self.test_execute_insert()
        select_query = "SELECT * FROM cart WHERE item_id = ?"
        result = self.db_connection.fetchone(select_query, (1,))
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 1)

    def test_fetchall(self):
        self.test_execute_insert()
        insert_query = "INSERT INTO cart (item_id, name, price, quantity, category, user_type, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.db_connection.execute(insert_query, (2, "Item 2", 15.0, 2, "general", "regular", "pending"))
        self.db_connection.commit()

        select_query = "SELECT * FROM cart"
        results = self.db_connection.fetchall(select_query)
        self.assertEqual(len(results), 2)

    def test_invalid_query(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db_connection.execute("INVALID SQL QUERY")

    def test_memory_leak(self):
        mem_usage_before = memory_usage()
        
        for _ in range(10000):
            query = "INSERT INTO cart (item_id) VALUES (1)"
            add_item_to_cart_db(query, params=None)

        mem_usage_after = memory_usage()
       
        max_memory_increase = 0.1  # in MB
        for mem_before, mem_after in zip(mem_usage_before, mem_usage_after):
            memory_increase = mem_after - mem_before
            self.assertLess(memory_increase, max_memory_increase, f"Memory Leak: Memory Increase {memory_increase} exceeds threshold {max_memory_increase}")

if __name__ == "__main__":
    unittest.main()
