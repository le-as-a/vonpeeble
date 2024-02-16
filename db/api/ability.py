from sqlite3 import connect

""" CREATE TABLE abilities (
    ability_name VARCHAR(255) NOT NULL,
    source VARCHAR(255) NOT NULL,
    ability_type VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
)"""

def startup():
    conn = connect("data.db")
    cur = conn.cursor()
    return (conn, cur)

def get_abilities(calling, ability_type):
    (conn, cur) = startup()
    cmd = ""
    if ability_type == "All":
        cmd = f"SELECT * FROM abilities WHERE source = '{calling}' AND NOT ability_type = 'Default'"
    else:
        cmd = f"SELECT * FROM abilities WHERE source = '{calling}' AND ability_type = '{ability_type}'"
    abilities = cur.execute(cmd).fetchall()
    conn.close()
    return abilities

def get_ability(ability_name):
    (conn, cur) = startup()
    ability = cur.execute(f"SELECT * FROM abilities WHERE ability_name = '{ability_name}'").fetchone()
    conn.close()
    return ability

def get_char_abilities(abilities):
    (conn, cur) = startup()
    char_abilities = []
    for n in abilities:
        ability = cur.execute(f"SELECT * FROM abilities WHERE ability_name = '{n}'").fetchone()
        char_abilities.append(ability)
    conn.close()
    return char_abilities

def get_species_abilities(species):
    (conn, cur) = startup()
    abilities = cur.execute(f"SELECT * FROM abilities WHERE source = '{species}' AND ability_type = 'Innate'").fetchall()
    conn.close()
    return abilities

def get_maturative_ability(species):
    (conn, cur) = startup()
    maturative_ability = cur.execute(f"SELECT * FROM abilities WHERE source = '{species}' AND ability_type = 'Maturative'").fetchone()
    conn.close()
    return maturative_ability