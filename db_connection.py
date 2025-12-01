import sqlite3

from app.data.db import DB_PATH


def connect_database(db_path = DB_PATH):
    return sqlite3.connect(str(db_path))