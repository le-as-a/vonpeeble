from sqlite3 import connect
from helper import schemas, callings # data is private due to copyright of BREAK!! RPG system

conn = connect("data.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS callings")
cur.execute("DROP TABLE IF EXISTS characters")

for x in schemas:
    cur.execute(x)
    
cur.executemany("INSERT INTO callings VALUES (?,?,?,?,?,?,?)", callings)
conn.commit()
conn.close()