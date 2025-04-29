import sqlite3
from sqlite3 import Error
from typing import Optional

def create_connection(db_file: str) -> Optional[sqlite3.Connection]:
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_tables(conn: sqlite3.Connection) -> None:
    """Create database tables if they don't exist"""
    sql_create_history_table = """CREATE TABLE IF NOT EXISTS history (
                                    id integer PRIMARY KEY,
                                    timestamp integer NOT NULL,
                                    price real NOT NULL,
                                    volume real NOT NULL,
                                    signal_type text NOT NULL,
                                    signal_strength real NOT NULL
                                );"""
    
    try:
        c = conn.cursor()
        c.execute(sql_create_history_table)
    except Error as e:
        print(e)

def save_history(conn: sqlite3.Connection, data: dict) -> None:
    """Save trading history to database"""
    sql = '''INSERT INTO history(timestamp, price, volume, signal_type, signal_strength)
             VALUES(?,?,?,?,?)'''
    try:
        c = conn.cursor()
        c.execute(sql, (data['timestamp'], data['price'], data['volume'], 
                        data['signal_type'], data['signal_strength']))
        conn.commit()
    except Error as e:
        print(e)

def get_history(conn: sqlite3.Connection, limit: int = 100) -> list:
    """Get trading history from database"""
    sql = '''SELECT * FROM history ORDER BY timestamp DESC LIMIT ?'''
    try:
        c = conn.cursor()
        c.execute(sql, (limit,))
        return c.fetchall()
    except Error as e:
        print(e)
        return []
