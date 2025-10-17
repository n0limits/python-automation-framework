import sqlite3
from threading import Lock
from typing import Optional

class DatabaseConnection:
    """Singleton database connection"""

    _instance: Optional['DatabaseConnection'] = None
    _lock: Lock = Lock()
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls):
        """Ensure only one instance exists"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize connection only once"""
        if self._connection is None:
            self._connection = sqlite3.connect(
                'test_database.db',
                check_same_thread=False
            )
            print("Database connection established")

    def get_connection(self):
        """Get database connection"""
        return self._connection

    def execute_query(self, query: str, params: tuple = ()):
        """Execute a query"""
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        self._connection.commit()
        return cursor.fetchall()

    def close(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("Database connection closed")

# Usage in tests
def test_user_exists_in_database():
    db = DatabaseConnection()  # Always returns same instance
    result = db.execute_query("SELECT * FROM users WHERE id = ?", (1,))
    assert len(result) > 0