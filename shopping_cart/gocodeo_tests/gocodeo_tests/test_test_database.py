import unittest
from unittest.mock import patch, MagicMock
import os
import sqlite3
from memory_profiler import memory_usage

class TestMemoryLeak(unittest.TestCase):
    @patch('shopping_cart.database.DatabaseConnection')
    @patch('shopping_cart.database.add_item_to_cart_db')
    def setUp(self, mock_add_item_to_cart_db, mock_DatabaseConnection):
        self.mock_db_connection = MagicMock()
        mock_DatabaseConnection.return_value = self.mock_db_connection
        
        self.db_path = "shopping_cart.db"
        self.db_connection = mock_DatabaseConnection(self.db_path)
        self.db_connection.connect()
        self.init_database()

    def tearDown(self):
        if os.path.exists(self.db_path):
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

if __name__ == "__main__":
    unittest.main()# happy_path - test_connection - Test if the database connection is established and closed properly
def test_connection(self):
        self.db_connection.connect()
        self.assertIsNotNone(self.db_connection.connection)
        self.db_connection.close()
        self.assertIsNone(self.db_connection.connection)

# edge_case - test_invalid_query - Test handling of an invalid SQL query
def test_invalid_query(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db_connection.execute("INVALID SQL QUERY")

