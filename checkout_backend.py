import sqlite3


def connect():
    conn = sqlite3.connect('Equipment_Users.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name text, email text, phone text, total_co integer)')
    conn.commit()
    conn.close()
    
    
def insert(name, email, phone):
    total_co = 0
    conn = sqlite3.connect('Equipment_Users.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO user VALUES (NULL, ?, ?, ?, ?)', (name, email, phone, total_co))
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect('Equipment_Users.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user')
    rows = cur.fetchall()
    conn.close()
    return rows


def view_by_id(id_num):
    conn = sqlite3.connect('Equipment_Users.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user WHERE id=?', (id_num,))
    rows = cur.fetchall()
    conn.close()
    return rows


def search(name='', email='', phone=''):
    conn = sqlite3.connect('Equipment_Users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE name=? OR email=? OR phone=?", (name, email, phone))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete(id_num):
    conn = sqlite3.connect('Equipment_Users.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM user WHERE id=?', (id_num,))
    conn.commit()
    conn.close()


def update(id_num, name, email, phone):
    conn = sqlite3.connect('Equipment_Users.db')
    cur = conn.cursor()
    cur.execute('UPDATE user SET name=?, email=?, phone=? WHERE id=?', (name, email, phone, id_num))
    conn.commit()
    conn.close()


def update_total_co(id_num, total_co):
    total_co += 1
    conn = sqlite3.connect('Equipment_Users.db')
    cur = conn.cursor()
    cur.execute('UPDATE user SET total_co=? WHERE id=?', (total_co, id_num))
    conn.commit()
    conn.close()


connect()
