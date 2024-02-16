from sqlite3 import connect

""" CREATE TABLE character_quirk (
    user_id INTEGER NOT NULL,
    quirk_name VARCHAR(255) NOT NULL
)"""

def startup():
    conn = connect("data.db")
    cur = conn.cursor()
    return (conn, cur)

def new_char_quirk(user_id, quirk_name):
    (conn, cur) = startup()
    cur.execute(f"INSERT INTO character_quirk VALUES ({user_id}, '{quirk_name}')")
    conn.commit()
    conn.close()
    
def del_char_quirk(user_id):
    (conn, cur) = startup()
    cur.execute(f"DELETE FROM character_quirk WHERE user_id = {user_id}")
    conn.commit()
    conn.close()
    
def get_char_quirk(user_id):
    (conn, cur) = startup()
    (quirk_name) = cur.execute(f"SELECT quirk_name FROM character_quirk WHERE user_id = {user_id}").fetchone()
    quirk = cur.execute(f"SELECT * FROM quirks WHERE quirk_name = '{quirk_name}'").fetchone()
    conn.close()
    return quirk