from sqlite3 import connect
from helper import schemas, callings, graveyard, abilities, species_abilities, quirks # data is private due to copyright of BREAK!! RPG system

conn = connect("data.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS callings")
cur.execute("DROP TABLE IF EXISTS characters")
cur.execute("DROP TABLE IF EXISTS graveyard")
cur.execute("DROP TABLE IF EXISTS abilities")
cur.execute("DROP TABLE IF EXISTS character_abilities")
cur.execute("DROP TABLE IF EXISTS quirks")
cur.execute("DROP TABLE IF EXISTS character_quirk")
cur.execute("DROP TABLE IF EXISTS game_mechs")

for x in schemas:
    cur.execute(x)
    
cur.executemany("INSERT INTO callings VALUES (?,?,?,?,?,?,?)", callings)
cur.executemany("INSERT INTO graveyard VALUES (?,?,?,?,?,?)", graveyard)
# cur.executemany("INSERT INTO characters VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", characters)
cur.executemany("INSERT INTO abilities VALUES (?,?,?,?)", abilities)
cur.executemany("INSERT INTO abilities VALUES (?,?,?,?)", species_abilities)
# cur.executemany("INSERT INTO character_abilities VALUES (?,?,?,?)", char_abilities)
cur.executemany("INSERT INTO quirks VALUES(?,?,?)", quirks)
conn.commit()
conn.close()