from app.data.db import connect_database

def create_user_table(conn):
    """create users table if it doenst exists """
    cursor = conn.cursor()
    #create sql table
    create_table_sql =
    cursor.execute(create_table_sql)
    conn.commit()
    print("User Table Created")


def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def insert_user(username, password_hash, role='user'):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()