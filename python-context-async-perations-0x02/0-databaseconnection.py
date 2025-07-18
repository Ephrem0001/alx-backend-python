import sqlite3

class DatabaseConnection:
    def __init__(self, db_name="users.db"):
        # Initialize with the database name or path
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open the connection and return the cursor to use inside 'with'
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the connection on exit, commit if no exception
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()

# Usage example:
if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
