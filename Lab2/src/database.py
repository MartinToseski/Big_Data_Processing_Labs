import sqlite3
from pathlib import Path

DB_PATH = Path('db/lab2.db')

def init_db() :
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        !!! SQL CODE HERE !!!
        """)

    connection.commit()
    connection.close()