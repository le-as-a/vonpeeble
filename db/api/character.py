from sqlite3 import connect

""" CREATE TABLE characters (
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    calling VARCHAR(255) NOT NULL,
    rank INTEGER NOT NULL,
    species VARCHAR(255) NOT NULL,
    size VARCHAR(255) NOT NULL,
    good1 VARCHAR(255) NOT NULL,
    good2 VARCHAR(255) NOT NULL,
    bad VARCHAR(255) NOT NULL,
    img_url VARCHAR(255) NOT NULL,
    might INTEGER,
    deftness INTEGER,
    grit INTEGER,
    insight INTEGER,
    aura INTEGER
)"""

def startup(user_id):
    conn = connect("data.db")
    cur = conn.cursor()
    char = cur.execute(f"SELECT * FROM characters WHERE user_id = {user_id}").fetchone()
    return (conn, cur, char)

def new_char(
    user_id, # 0
    char_name, # 1
    calling, # 2
    rank, # 3
    species, # 4
    size, # 5
    good1, # 6
    good2, # 7
    bad, # 8
    img_url, # 9 
    might, # 10
    deftness, # 11
    grit, # 12
    insight, # 13
    aura): #14
    (conn, cur, char) = startup(user_id)
    if char:
        conn.close()
        return False
    cur.execute(f"INSERT INTO characters VALUES ({user_id}, '{char_name}', '{calling}', '{rank}', '{species}', '{size}', '{good1}', '{good2}', '{bad}', '{img_url}', {might}, {deftness}, {grit}, {insight}, {aura})")
    conn.commit()
    conn.close()
    return True
    
def get_char(user_id):
    (conn, cur, char) = startup(user_id)
    conn.close()
    return char

def get_aptitude(user_id, aptitude):
    (conn, cur, char) = startup(user_id)
    conn.close()
    score = 0
    if not char:
        return False
    match aptitude:
        case 'Might':
            score = char[10]
        case 'Deftness':
            score = char[11]
        case 'Grit':
            score = char[12]
        case 'Insight':
            score = char[13]
        case 'Aura':
            score = char[14]
    return (char[1], char[9], score)

def rank_up(user_id, might, deftness, grit, insight, aura):
    (conn, cur, char) = startup(user_id)
    if not char:
        conn.close()
        return False
    cur.execute(f"UPDATE characters SET rank = rank + 1, might = {might}, deftness = {deftness}, grit = {grit}, insight = {insight}, aura = {aura} WHERE user_id = {user_id}")
    conn.commit()
    conn.close()
    return True

def edit_char(user_id, option, data):
    (conn, cur, char) = startup(user_id)
    opt = ''
    if not char:
        conn.close()
        return False
    match option:
        case 'Name':
            opt = 'name'
        case 'Image URL':
            opt = 'img_url'
    cur.execute(f"UPDATE characters SET {opt} = '{data}' WHERE user_id = {user_id}")
    conn.commit()
    conn.close()
    return True

def del_char(user_id):
    (conn, cur, char) = startup(user_id)
    if not char:
        conn.close()
        return False
    cur.execute(f"DELETE FROM characters WHERE user_id = {user_id}")
    conn.commit()
    conn.close()
    return True