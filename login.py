import sqlite3

def login(username_or_email, password):
    conn = sqlite3.connect("license.db")
    cursor = conn.cursor()

    if '@' in username_or_email:
        query = "SELECT * FROM users WHERE email=? AND password=?"
    else:
        query = "SELECT * FROM users WHERE username=? AND password=?"

    cursor.execute(query, (username_or_email, password))
    user_data = cursor.fetchone()

    conn.close()

    return user_data
