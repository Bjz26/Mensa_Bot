import sqlite3

DATABASE_PATH = 'subscribers.db'

def connect_db():
    return sqlite3.connect(DATABASE_PATH)

def create_subsciber_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

def subscriber_exists(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM subscribers WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def add_subscriber(user_id):
    if not subscriber_exists(user_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subscribers (user_id) VALUES (?)", (user_id,))
        conn.commit()
        conn.close()
        return 'Du hast dich erfolgreich für das tägliche Update angemeldet.'
    else:
        return 'Du bist bereits für das tägliche Update angemeldet.'

def remove_subscriber(user_id):
    if subscriber_exists(user_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscribers WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return 'Du hast dich erfolgreich vom täglichen Update abgemeldet.'
    else:
        return 'Du bist bereits vom täglichen Update abgemeldet.'
        
def get_all_subscribers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM subscribers")
    subscribers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return subscribers
