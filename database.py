import sqlite3
import os

class DatabaseConnection:
    def __init__(self, db_path):
        self.connection = None  
        self.db_path = db_path  

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    def execute(self, query, params=None):
        if params is None:
            params = []
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        

    def fetchone(self, query, params=None):
        if params is None:
            params = []
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()

        return result

    def fetchall(self, query, params=None):
        if params is None:
            params = []
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "shopping_cart.db")
database_connection = DatabaseConnection(db_path)


def add_item_to_cart_db(query, params=None):
    
    if params is None:
        params = []
    database_connection.connect()
    database_connection.execute(query, params)
    database_connection.commit()
    database_connection.close()
