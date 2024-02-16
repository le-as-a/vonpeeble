from sqlite3 import connect

""" CREATE TABLE quirks (
    quirk_name VARCHAR(255) NOT NULL,
    quirk_type VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
)"""

def startup():
    conn = connect("data.db")
    cur = conn.cursor()
    return (conn, cur)

def get_quirks(quirk_type):
    (conn, cur) = startup()
    quirks = cur.execute(f"SELECT * FROM quirks WHERE quirk_type = '{quirk_type}'").fetchall()
    conn.close()
    return quirks

def get_all_quirks():
    (conn, cur) = startup()
    quirks = cur.execute(f"SELECT * FROM quirks").fetchall()
    conn.close()
    return quirks