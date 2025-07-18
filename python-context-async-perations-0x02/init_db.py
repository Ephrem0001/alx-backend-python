# init_db.py
import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')

# Insert some sample users
cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Alice", "alice@example.com", 30))
cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Bob", "bob@example.com", 45))
cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Charlie", "charlie@example.com", 50))

conn.commit()
conn.close()

print("Database initialized with sample users.")
