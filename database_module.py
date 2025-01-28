import sqlite3

DATABASE = 'crawl_database.db'

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_data(username):
    """Fetches user data by username."""
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user_data

from werkzeug.security import check_password_hash

def validate_password(stored_password_hash, password):
    """Validates password with the stored hash."""
    # Ensure the stored password hash is a string, not bytes
    if isinstance(stored_password_hash, bytes):
        stored_password_hash = stored_password_hash.decode('utf-8')
    return check_password_hash(stored_password_hash, password)

