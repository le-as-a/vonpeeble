from sqlite3 import connect
from datetime import datetime, timezone

""" CREATE TABLE graveyard (
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    calling VARCHAR(255) NOT NULL,
    rank INTEGER NOT NULL,
    img VARCHAR(255) NOT NULL,
    date VARCHAR(255) NOT NULL
)"""

def startup():
    conn = connect("data.db")
    cur = conn.cursor()
    return (conn, cur)

def new_death(user_id, char_name, calling, rank, img):
    time_of_death = str(datetime.now())
    time_of_death += "-0600"
    (conn, cur) = startup()
    cur.execute(f"INSERT INTO graveyard VALUES ({user_id}, '{char_name}', '{calling}', {rank}, '{img}', '{time_of_death}')")
    conn.commit()
    conn.close()
    return time_of_death

def view_graveyard():
    (conn, cur) = startup()
    deaths = cur.execute(f"SELECT * FROM graveyard").fetchall()
    conn.close()
    return deaths

def del_death(user_id, char_name):
    (conn, cur) = startup()
    char = cur.execute(f"SELECT * FROM graveyard WHERE user_id = {user_id} AND name = '{char_name}'").fetchone()
    if not char:
        return False
    cur.execute(f"DELETE FROM graveyard WHERE user_id = {user_id} AND name = '{char_name}'")
    conn.commit()
    conn.close()
    return char[1]
