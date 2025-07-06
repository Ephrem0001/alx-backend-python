import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def stream_user_ages():
    """
    Generator that yields ages one by one.
    """
    connection = psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        dbname=os.getenv("PGDATABASE")
    )
    cursor = connection.cursor(name="age_cursor", cursor_factory=RealDictCursor)

    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row["age"]

    cursor.close()
    connection.close()

def calculate_average_age():
    """
    Calculates and prints the average age.
    """
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average}")

# Uncomment to run directly:
# if __name__ == "__main__":
#     calculate_average_age()
