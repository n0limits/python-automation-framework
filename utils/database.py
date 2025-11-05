import sqlite3
from threading import Lock
from typing import Optional

class DatabaseConnection:
    """
    Singleton Pattern for managing database connections.
    Ensures only one database connection exists throughout test execution,
    preventing connection pool exhaustion and ensuring consistent database state.

    Benefits:
    - Single database connection shared across all tests
    - Thread-safe for parallel test execution
    - Automatic connection management
    - Prevents connection leaks

    Important Note:
    - SQLite connection uses check_same_thread=False for pytest-xdist compatibility
    - For production databases, use connection pooling instead

    Example:
        db = DatabaseConnection()  # Always returns same instance
        result = db.execute_query("SELECT * FROM users WHERE id = ?", (1,))
    """

    _instance: Optional['DatabaseConnection'] = None
    _lock: Lock = Lock()
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls):
        """
        Ensure only one instance exists -Singleton patetrn
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize database connection only once.
        Connection Details:
        - Database: test_database.db (SQLite)
        - check_same_thread=False: Allows pytest-xdist parallel execution
        """
        if self._connection is None:
            self._connection = sqlite3.connect(
                'test_database.db',
                check_same_thread=False
            )
            print("Database connection established")

    def get_connection(self):
        """
        Get the underlying database connection.
        Returns:            sqlite3.Connection instance
        """
        return self._connection

    def execute_query(self, query: str, params: tuple = ()):
        """
        Execute a SQL query with parameter.

        Automatically commits the transaction and returns results.
        Uses parameterized queries to prevent SQL injection.
        Args:
            query: SQL query with ? placeholders
        Returns:
            List of result rows (empty list for INSERT/UPDATE/DELETE)
        Example:
            # SELECT query
            users = db.execute_query("SELECT * FROM users WHERE name = ?", ("Victor",))
        """
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        self._connection.commit()
        return cursor.fetchall()

    def close(self):
        """
        Close the database connection.
        Should be called in test teardown/cleanup to free resources.
        Resets the connection to None, allowing a new connection to be created
        if DatabaseConnection is used again.
        """
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Database connection closed")

# Usage in tests
def test_user_exists_in_database():
    db = DatabaseConnection()  # Always returns same instance
    result = db.execute_query("SELECT * FROM users WHERE id = ?", (1,))
    assert len(result) > 0