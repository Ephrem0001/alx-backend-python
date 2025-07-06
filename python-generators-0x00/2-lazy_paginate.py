import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def paginate_users(page_size, offset):
    """
    Helper function to fetch a page of users from the database.
    """
    connection = psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        dbname=os.getenv("PGDATABASE")
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
    )
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that yields pages of user data lazily.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
