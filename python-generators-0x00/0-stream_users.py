import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load variables from .env into environment
load_dotenv()


def stream_users():
    """
    Generator that yields rows from user_data table one by one as dictionaries.
    """
    connection = None
    cursor = None
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            dbname=os.getenv("PGDATABASE")
        )
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Execute query to fetch all rows
        cursor.execute("SELECT * FROM user_data")

        # Loop over the cursor, yield rows one by one
        for row in cursor:
            yield row
    except Exception as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
