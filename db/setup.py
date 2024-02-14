from sqlite3 import connect
from helper import schemas, callings, graveyard, characters # data is private due to copyright of BREAK!! RPG system

conn = connect("data.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS callings")
cur.execute("DROP TABLE IF EXISTS characters")
cur.execute("DROP TABLE IF EXISTS graveyard")
cur.execute("DROP TABLE IF EXISTS abilities")
cur.execute("DROP TABLE IF EXISTS character_abilities")

for x in schemas:
    cur.execute(x)
    
cur.executemany("INSERT INTO callings VALUES (?,?,?,?,?,?,?)", callings)
cur.executemany("INSERT INTO graveyard VALUES (?,?,?,?,?,?)", graveyard)
cur.executemany("INSERT INTO characters VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", characters)
conn.commit()
conn.close()