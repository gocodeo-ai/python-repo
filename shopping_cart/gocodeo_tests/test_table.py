import pytest
from unittest.mock import patch, MagicMock
import sqlite3

@pytest.fixture
def mock_sqlite():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Mock the connection object
        mock_connect.return_value = mock_conn
        
        # Mock the cursor object
        mock_conn.cursor.return_value = mock_cursor
        
        yield {
            'mock_connect': mock_connect,
            'mock_conn': mock_conn,
            'mock_cursor': mock_cursor
        }

        # Ensure connection is closed
        mock_conn.close.assert_called_once()

@pytest.fixture
def mock_commit_failure():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Mock the connection object
        mock_connect.return_value = mock_conn
        
        # Mock the cursor object
        mock_conn.cursor.return_value = mock_cursor
        
        # Simulate a commit failure
        mock_conn.commit.side_effect = sqlite3.Error("Commit failed")
        
        yield {
            'mock_connect': mock_connect,
            'mock_conn': mock_conn,
            'mock_cursor': mock_cursor
        }

        # Ensure connection is closed
        mock_conn.close.assert_called_once()

@pytest.fixture
def mock_cursor_execution_failure():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Mock the connection object
        mock_connect.return_value = mock_conn
        
        # Mock the cursor object
        mock_conn.cursor.return_value = mock_cursor
        
        # Simulate a cursor execution failure
        mock_cursor.execute.side_effect = sqlite3.Error("Execution failed")
        
        yield {
            'mock_connect': mock_connect,
            'mock_conn': mock_conn,
            'mock_cursor': mock_cursor
        }

        # Ensure connection is closed
        mock_conn.close.assert_called_once()

@pytest.fixture
def mock_connection_close_failure():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Mock the connection object
        mock_connect.return_value = mock_conn
        
        # Mock the cursor object
        mock_conn.cursor.return_value = mock_cursor
        
        # Simulate a connection close failure
        mock_conn.close.side_effect = sqlite3.Error("Close failed")
        
        yield {
            'mock_connect': mock_connect,
            'mock_conn': mock_conn,
            'mock_cursor': mock_cursor
        }

        # Ensure connection close was attempted
        mock_conn.close.assert_called_once()

# happy_path - test_create_cart_table - Test that the 'cart' table is dropped if it exists and then created successfully.
def test_create_cart_table(mock_sqlite):
    from shopping_cart.table import execute
    
    # Arrange
    mock_data = mock_sqlite
    
    # Act
    execute('CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status)')
    
    # Assert
    mock_data['mock_cursor'].execute.assert_any_call('DROP TABLE IF EXISTS cart;')
    mock_data['mock_cursor'].execute.assert_any_call('CREATE TABLE cart (id INTEGER PRIMARY KEY, item_id INTEGER, name TEXT, price REAL, quantity INTEGER, category TEXT, user_type TEXT, payment_status)')
    print("Table 'cart' recreated successfully.")

# happy_path - test_database_connection - Test that the database connection is established to 'shopping_cart.db'.
def test_database_connection(mock_sqlite):
    from shopping_cart.table import connect
    
    # Arrange
    mock_data = mock_sqlite
    
    # Act
    connect('shopping_cart.db')
    
    # Assert
    mock_data['mock_connect'].assert_called_once_with('shopping_cart.db')
    print('Database connection established successfully.')

# happy_path - test_drop_table_query - Test that the SQL command to drop the table is executed without error.
def test_drop_table_query(mock_sqlite):
    from shopping_cart.table import execute
    
    # Arrange
    mock_data = mock_sqlite
    
    # Act
    execute('DROP TABLE IF EXISTS cart;')
    
    # Assert
    mock_data['mock_cursor'].execute.assert_called_once_with('DROP TABLE IF EXISTS cart;')
    print('Drop table query executed successfully.')

# happy_path - test_commit_transaction - Test that the transaction is committed after table creation.
def test_commit_transaction(mock_sqlite):
    from shopping_cart.table import commit
    
    # Arrange
    mock_data = mock_sqlite
    
    # Act
    commit()
    
    # Assert
    mock_data['mock_conn'].commit.assert_called_once()
    print('Transaction committed successfully.')

# happy_path - test_create_cursor - Test that the cursor is successfully created from the connection.
def test_create_cursor(mock_sqlite):
    from shopping_cart.table import cursor
    
    # Arrange
    mock_data = mock_sqlite
    
    # Act
    cursor()
    
    # Assert
    mock_data['mock_conn'].cursor.assert_called_once()
    print('Cursor created successfully.')

# edge_case - test_database_file_access_error - Test that an error is handled gracefully if the database file is not accessible.
def test_database_file_access_error():
    with patch('sqlite3.connect', side_effect=sqlite3.Error('Database file not accessible')) as mock_connect:
        from shopping_cart.table import connect
        
        # Act & Assert
        try:
            connect('non_existent.db')
        except sqlite3.Error as e:
            assert str(e) == 'Database file not accessible'
        print('Database file access error handled successfully.')

# edge_case - test_sql_syntax_error - Test that an error is handled if the SQL syntax for table creation is incorrect.
def test_sql_syntax_error(mock_cursor_execution_failure):
    from shopping_cart.table import execute
    
    # Arrange
    mock_data = mock_cursor_execution_failure
    
    # Act & Assert
    try:
        execute('CREATE TABLE cart (id INTEGER PRIMARY KEY, name TEXT price REAL);')
    except sqlite3.Error as e:
        assert str(e) == 'Execution failed'
    print('SQL syntax error handled successfully.')

# edge_case - test_commit_failure - Test that an error is handled if the connection commit fails.
def test_commit_failure(mock_commit_failure):
    from shopping_cart.table import commit
    
    # Arrange
    mock_data = mock_commit_failure
    
    # Act & Assert
    try:
        commit()
    except sqlite3.Error as e:
        assert str(e) == 'Commit failed'
    print('Commit failure handled successfully.')

# edge_case - test_cursor_execution_failure - Test that an error is handled if the cursor execution fails.
def test_cursor_execution_failure(mock_cursor_execution_failure):
    from shopping_cart.table import execute
    
    # Arrange
    mock_data = mock_cursor_execution_failure
    
    # Act & Assert
    try:
        execute('INVALID SQL')
    except sqlite3.Error as e:
        assert str(e) == 'Execution failed'
    print('Cursor execution failure handled successfully.')

# edge_case - test_connection_close_failure - Test that an error is handled if the connection closure fails.
def test_connection_close_failure(mock_connection_close_failure):
    from shopping_cart.table import close
    
    # Arrange
    mock_data = mock_connection_close_failure
    
    # Act & Assert
    try:
        close()
    except sqlite3.Error as e:
        assert str(e) == 'Close failed'
    print('Connection close failure handled successfully.')

