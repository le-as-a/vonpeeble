from sqlite3 import connect

""" CREATE TABLE character_quirk (
    user_id INTEGER NOT NULL,
    quirk_name VARCHAR(255) NOT NULL,
    quirk_type VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
)"""

def startup():
    conn = connect("data.db")
    cur = conn.cursor()
    return (conn, cur)

def new_char_quirk(user_id, quirk_name, quirk_type, description):
    (conn, cur) = startup()
    cur.execute("INSERT INTO character_quirk VALUES (?,?,?,?)", (user_id, quirk_name, quirk_type, description))
    conn.commit()
    conn.close()
    
def del_char_quirk(user_id):
    (conn, cur) = startup()
    cur.execute(f"DELETE FROM character_quirk WHERE user_id = {user_id}")
    conn.commit()
    conn.close()
    
def get_char_quirk(user_id):
    (conn, cur) = startup()
    quirk = cur.execute(f"SELECT * FROM character_quirk WHERE user_id = {user_id}").fetchone()
    conn.close()
    return quirk