import psycopg2
from psycopg2 import Error
import csv
import uuid
from dotenv import load_dotenv
import os

# Load variables from .env into environment
load_dotenv()


def connect_db():
    """Connects to PostgreSQL server."""
    try:
        connection = psycopg2.connect(
            host=os.getenv("PGHOST"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            dbname=os.getenv("PGDATABASE")
        )
        print("Connected to PostgreSQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
    return None

def create_database(connection):
    """Creates ALX_prodev database if not exists."""
    try:
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{os.getenv('PGDATABASE')}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {os.getenv('PGDATABASE')}")
            print("Database created successfully")
        else:
            print("Database already exists")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = psycopg2.connect(
            host=os.getenv("PGHOST"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            dbname=os.getenv("PGDATABASE")
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def create_table(connection):
    """Creates the user_data table if not exists."""
    try:
        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age NUMERIC NOT NULL
            );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Inserts data into user_data table from a CSV file."""
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Generate UUID if not in CSV
                user_id = row.get('user_id') or str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                # Check if user already exists
                cursor.execute(
                    "SELECT user_id FROM user_data WHERE user_id = %s",
                    (user_id,)
                )
                result = cursor.fetchone()
                if result:
                    continue  # Skip existing
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(insert_query, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    connection = connect_db()
    if connection:
        create_table(connection)
        # Use the correct path to your CSV file
        insert_data(connection, 'data/user_data.csv')
        connection.close()