import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('shopping_cart.db')

try:
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Define the SQL command to drop the cart table if it exists
    drop_table_query = '''
    DROP TABLE IF EXISTS cart;
    '''

    # Execute the SQL command to drop the table
    cursor.execute(drop_table_query)

    # Define the SQL command to create the cart table
    create_table_query = '''
    CREATE TABLE cart (
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

    # Execute the SQL command to create the table
    cursor.execute(create_table_query)

    # Commit the transaction
    conn.commit()

    print("Table 'cart' recreated successfully.")

except sqlite3.Error as e:
    print("Error occurred:", e)

finally:
    # Close the connection
    conn.close()
