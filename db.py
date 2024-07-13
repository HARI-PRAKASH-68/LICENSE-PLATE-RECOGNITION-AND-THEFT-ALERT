import sqlite3

# Connect to the database (creates the database if it doesn't exist)
conn = sqlite3.connect("license.db")
cursor = conn.cursor()

# Create a table named "users"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        otp TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

