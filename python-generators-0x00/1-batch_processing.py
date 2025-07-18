import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows (as lists of dicts)
    """
    connection = psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        dbname=os.getenv("PGDATABASE")
    )
    # Use server-side named cursor to avoid loading all rows into memory
    cursor = connection.cursor(name="batch_cursor", cursor_factory=RealDictCursor)
    cursor.itersize = batch_size

    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch and prints users over age 25
    """
    for batch in stream_users_in_batches(batch_size):
        for row in batch:
            if row["age"] > 25:
                print(row)
