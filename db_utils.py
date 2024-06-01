# db_utils.py
import sqlite3

def get_connection():
    return sqlite3.connect('data.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS userstable (
            username TEXT,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS self_diagnosis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            date TEXT,
            q1 INTEGER,
            q2 INTEGER,
            q3 INTEGER,
            q4 INTEGER,
            q5 INTEGER,
            q6 INTEGER,
            q7 INTEGER,
            q8 INTEGER,
            q9 INTEGER,
            q10 INTEGER,
            total_score INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            diary TEXT,
            sentiment TEXT,
            message TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS poststable (
            username TEXT,
            image BLOB,
            post TEXT,
            timestamp TEXT,
            is_public INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS likestable (
            post_id INTEGER,
            username TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date TEXT,
            time TEXT,
            task TEXT,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()
