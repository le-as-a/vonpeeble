from sqlite3 import connect

""" CREATE TABLE callings (
    name VARCHAR(255) NOT NULL,
    rank INTEGER NOT NULL,
    might INTEGER,
    deftness INTEGER,
    grit INTEGER,
    insight INTEGER,
    aura INTEGER
)"""

def startup():
    conn = connect("data.db")
    cur = conn.cursor()
    return (conn, cur)

def get_calling(calling, rank):
    (conn, cur) = startup()
    info = cur.execute(f"SELECT might, deftness, grit, insight, aura FROM callings WHERE name = '{calling}' AND rank = {rank}").fetchone()
    conn.close()
    return info