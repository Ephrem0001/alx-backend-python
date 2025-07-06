import psycopg2
from psycopg2.extras import RealDictCursor

def stream_users():
    """
    Generator that yields rows from user_data table one by one as dictionaries.
    """
    # Connect to your PostgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        dbname="your_database"
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    # Execute query to fetch all rows
    cursor.execute("SELECT * FROM user_data")

    # Loop over the cursor, yield rows one by one
    for row in cursor:
        yield row

    # Cleanup
    cursor.close()
    connection.close()
