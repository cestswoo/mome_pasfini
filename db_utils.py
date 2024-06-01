# db_utils.py
import sqlite3

DATABASE = 'momE.db'

def get_connection():
    return sqlite3.connect(DATABASE, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # userstable 초기화
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
    # poststable 초기화
    c.execute('CREATE TABLE IF NOT EXISTS poststable(username TEXT, image BLOB, post TEXT, timestamp TEXT, is_public INTEGER)')
    # likestable 초기화
    c.execute('CREATE TABLE IF NOT EXISTS likestable(post_id INTEGER, username TEXT)')
    # self_diagnosis 초기화
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
    # schedules 초기화
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
    # diary 초기화
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
    conn.commit()
    conn.close()

# Initialize database
init_db()
