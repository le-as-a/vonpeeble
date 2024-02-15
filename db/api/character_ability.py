from sqlite3 import connect

""" CREATE TABLE character_abilities (
    user_id INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    ability_type VARCHAR(255) NOT NULL,
    ability_name VARCHAR(255) NOT NULL
)"""

def startup():
    conn = connect("data.db")
    cur = conn.cursor()
    return (conn, cur)

def new_entry(user_id, rank, ability_type, ability_name):
    (conn, cur) = startup()
    cur.execute(f"INSERT INTO character_abilities VALUES ({user_id}, {rank}, '{ability_type}', '{ability_name}')")
    conn.commit()
    conn.close()

def get_entries(user_id):
    (conn, cur) = startup()
    entries = cur.execute(f"SELECT * FROM character_abilities WHERE user_id = {user_id}").fetchall()
    conn.close()
    return entries

def del_entries(user_id):
    (conn, cur) = startup()
    cur.execute(f"DELETE FROM character_abilities WHERE user_id = {user_id}")
    conn.commit()
    conn.close()
