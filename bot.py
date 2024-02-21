from discord import Intents, Option, Embed, Colour
import discord
from discord.ext import commands
from random import randint
from datetime import datetime
import time
from protected import TOKEN, servers
from logic import generate_stats, apt_check, injury_table, specRoll
from commands import abilityRankupCommand, scoreRankupCommand, myProfile
from db.api.character import new_char, get_char, get_aptitude, edit_char
from db.api.graveyard import view_graveyard
from db.api.ability import get_abilities, get_species_abilities
from db.api.character_ability import new_entry
from views.DeleteView import DeleteView
from views.ProfileView import ProfileView
from views.CreateView import CreateView
from views.InfoView import InfoView

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents)

# global information used across multiple commands
callings = [
    'Factotum',
    'Sneak',
    'Champion',
    'Raider',
    'Battle Mage',
    'Murder Noble',
    'Sage',
    'Heretic'
]
apt_desc = {
    "Might": "Smash, crush, lift",
    "Deftness": "Dodge, sneak, leap",
    "Grit": "Cling, persist, press on",
    "Insight": "Notice, know, remember",
    "Aura": "Persuade, inspire, terrify"
}
aptitude_list = ['Might', 'Deftness', 'Grit', 'Insight', 'Aura']
bonuses = ['Minor Bonus', 'Major Bonus', 'Minor Penalty', 'Major Penalty']
reroll_type = ['Edge', 'Snag']
species_list = [
    'Human',
    'Dimensional Stray',
    'Chib',
    'Tenebrate',
    'Rai-Neko',
    'Promethean',
    'Gruun',
    'Goblin',
    'Dwarf',
    'Elf',
    'Bio-Mechanoid'
]

@bot.event
async def on_ready():
    print("Ready to play BREAK!! RPG.")
    
@bot.slash_command(
    guild_ids=servers,
    name="create",
    description="Create a new character!"
)
async def create(
    message,
    char_name: Option(
        str, required=True,
        description="Name your shiny new character."
    ), # type: ignore
    calling: Option(str, required=True, choices=callings,
    description="Pick a calling from the list provided."), # type: ignore
    rank: Option(int, required=True, min_value=1, max_value=10), # type: ignore
    species: Option(str, required=True, choices=species_list,
    description="Pick a species to play from the list provided."), # type: ignore
    good_trait_1: Option(str, required=True, choices=aptitude_list,
    description="Add a +1 to which trait?"), # type: ignore
    good_trait_2: Option(str, required=True, choices=aptitude_list,
    description="Add a +1 to which trait?"), # type: ignore
    bad_trait: Option(str, required=True, choices=aptitude_list,
    description="Add a -1 to which trait?"), # type: ignore
    image: Option(str, required=False) # type: ignore
):
    user_id = message.author.id
    (
        might, 
        deftness, 
        grit, 
        insight, 
        aura
    ) = generate_stats(
        calling, 
        rank, 
        species, 
        good_trait_1, 
        good_trait_2, 
        bad_trait
    )
    size = 'Small' if species in ['Chib', 'Goblin'] else 'Large' if species in ['Gruun', 'Promethean'] else 'Medium'
    
    if not image or not image.startswith("https://"):
        image = "https://i.pinimg.com/736x/ef/8a/6e/ef8a6e9f16c80279e9ea3ed19fbe8df0.jpg"
    
    response = ''
    status = new_char(
        user_id,
        char_name,
        calling,
        rank,
        species,
        size,
        good_trait_1,
        good_trait_2,
        bad_trait,
        image,
        might,
        deftness,
        grit,
        insight,
        aura
    )
    
    species_abilities = [ability[0] for ability in get_species_abilities(species)]
    for x in species_abilities:
        new_entry(user_id, 0, "Species", x)
    
    starter_abilities = [ability[0] for ability in get_abilities(calling, "Default")]
    for x in starter_abilities:
        new_entry(user_id, 1, "Calling", x)
    
    if status:
        embed = Embed(
            title="Choose your Quirk.",
            description="Select a Quirk type to view more."
        )
        await message.respond(embed=embed, view=CreateView(user_id, char_name), ephemeral=True)
    else:
        response = f"There was an error creating this character. Are you sure you don't already have one?"
        await message.respond(response)
    return

@bot.slash_command(
    guild_ids=servers,
    name="profile",
    description="View your BREAK!! RPG character."                   
)
async def profile(
    message,
    user: Option(discord.User, required=False) #type:ignore
):
    user_id = 0
    error_msg = ""
    if user:
        user_id = user.id
        error_msg = "This user doesn't have a character!"
    else:
        user_id = message.author.id
        error_msg = "There was an error finding your character. Try creating one with `/create`!"
    info = get_char(user_id)
    if not info:
        await message.respond(error_msg)
        return
    embed = myProfile(info)
    await message.respond(embed=embed, view=ProfileView(message, info))
    return

@bot.slash_command(
    guild_ids=servers,
    name="check",
    description="Roll an aptitude check!"
)
async def check(
    message,
    aptitude: Option(
        str, required=True, 
        choices=aptitude_list,
        description="Choose an aptitude to compare to this check!"
    ), #type:ignore
    reroll: Option(
        str, required=False, 
        choices=reroll_type,
        description="Optionally include an Edge/Snag."
    ), #type: ignore
    bonus: Option(
        str, required=False, 
        choices=bonuses,
        description="Optionally include a bonus/penalty."
    ) #type:ignore
):
    user_id = message.author.id
    info = get_aptitude(user_id, aptitude)
    if not info:
        await message.respond("There was an error finding your character. Try creating one with `/create`!")
        return
    (char_name, img_url, score) = info
    roll1 = randint(1, 20)
    roll2 = randint(1, 20)
    chosen = roll1
    rejected = roll2
    total_chosen = roll1
    total_rejected = roll2

    altered_roll = ""
    
    if reroll and reroll == 'Edge':
        chosen = roll1 if roll1 < roll2 else roll2
        rejected = roll2 if chosen == roll1 else roll1
        total_chosen = chosen
        total_rejected = rejected
        altered_roll += f"- with an **Edge** ({rejected})\n"
    elif reroll and reroll == 'Snag':
        chosen = roll1 if roll1 > roll2 else roll2
        rejected = roll2 if chosen == roll1 else roll1
        total_chosen = chosen
        total_rejected = rejected
        altered_roll += f"- with a **Snag** ({rejected})\n"
    else:
        altered_roll += "- no Edge/Snag \n"
    
    if bonus:
        match bonus:
            case 'Minor Bonus':
                total_chosen -= 2
                total_rejected -= 2
                altered_roll += f"- **{bonus}** (-2)"
            case 'Major Bonus':
                total_chosen -= 4
                total_rejected -= 4
                altered_roll += f"- **{bonus}** (-4)"
            case 'Minor Penalty':
                total_chosen += 2
                total_rejected += 2
                altered_roll += f"- **{bonus}** (+2)"
            case 'Major Penalty':
                total_chosen += 4
                total_rejected += 4
                altered_roll += f"- **{bonus}** (+4)"
    else:
        altered_roll += "- no Bonus/Penalty"
    
    result = f"## Special Success for {char_name}!" if chosen == score else f"## {char_name} succeeded!" if total_chosen <= score else "... Failure."
    total = f"{total_chosen} ({chosen} - 2)" if bonus == 'Minor Bonus' else f"{total_chosen} ({chosen} - 4)" if bonus == 'Major Bonus' else f"{total_chosen} ({chosen} + 2)" if bonus == 'Minor Penalty' else f"{total_chosen} ({chosen} + 4)"
    desc = f"""## {aptitude} check\n{apt_desc[aptitude]}
---
{altered_roll}\n# {total if bonus and result != f"## Special Success for {char_name}!" else chosen} `vs` {score}\n{result}
"""
    color = apt_check(aptitude)
    embed = Embed(
        title="",
        description=desc,
        color=Colour(int(color, 16))
    )
    embed.set_thumbnail(url=img_url)
    await message.respond(embed=embed)
    return

@bot.slash_command(
    guild_ids=servers,
    name="attack",
    description="Roll to attack."
)
async def attack(
    message,
    bonus: Option(
        int, required=False, min_value=-5, max_value=15,
        description="Choose an aptitude to compare to this check!"
    ), #type:ignore
    reroll: Option(
        str, required=False, 
        choices=reroll_type,
        description="Optionally include a bonus/penalty."
    ) #type:ignore
):
    user_id = message.author.id
    info = get_char(user_id)
    if not info:
        await message.respond("There was an error finding your character. Try creating one with `/create`!")
        return
    
    roll1 = randint(1, 20)
    roll2 = randint(1, 20)
    chosen = roll1
    rejected = roll2
    
    char_name = info[1]
    img_url = info[9]
    
    altered_roll = ""
    result = ""
    
    if reroll and reroll == 'Edge':
        chosen = roll1 if roll1 > roll2 else roll2
        rejected = roll2 if chosen == roll1 else roll1
        altered_roll += f"... with an **Edge** ({rejected}).\n"
    elif reroll and reroll == 'Snag':
        chosen = roll1 if roll1 < roll2 else roll2
        rejected = roll2 if chosen == roll1 else roll1
        altered_roll += f"... with a **Snag** ({rejected}).\n"
    
    if bonus and bonus > 0:
        result = f"{chosen+bonus} ({chosen} + {bonus})"
    elif bonus and bonus < 0:
        result = f"{chosen+bonus} ({chosen} - {-bonus})"
    else:
        result = f"{chosen}"
    
    desc = f"## {char_name.title()} is attacking!\n{altered_roll}# {result}"
    embed = Embed(
        title="",
        description=desc
    )
    embed.set_thumbnail(url=img_url)
    await message.respond(embed=embed)
    return

@bot.slash_command(
    guild_ids=servers,
    name="rankup",
    description="Rank up your character's calling."
)
async def rankup(message):
    user_id = message.author.id
    info = get_char(user_id)
    if not info:
        await message.respond("There was an error finding your character. Try creating one with `/create`!")
        return
    rank = info[3]
    if rank == 10:
        await message.respond("Your character is at the max rank already!")
        return
    elif (rank + 1) % 2 == 0:
        (embed, ability_rankup) = abilityRankupCommand(message, info)
        await message.respond(embed=embed, view=ability_rankup)
        
    else:
        await scoreRankupCommand(message, info)

@bot.slash_command(
    guild_ids=servers,
    name="edit",
    description="Edit your character name or image."
)
async def edit(
    message,
    option: Option(
        str, required=True, 
        choices=['Name', 'Image URL'],
        description="What part of your character profile do you want to edit?"
    ), #type:ignore
    input: Option(
        str, required=True,
        description="Input the change you want to make to your chosen option."
    ) #type:ignore
):
    user_id = message.author.id
    info = get_char(user_id)
    if not info:
        await message.respond("There was an error finding your character. Try creating one with `/create`!")
        return
    
    edit_char(user_id, option, input)
    await message.respond(f"{info[1]} successfully edited.")
    return

@bot.slash_command(
    guild_ids=servers,
    name="delete",
    description="Delete your character..."
)
async def delete(
    message, 
    reason: Option(str, required=True,
        choices=['Character died.', 'Remaking them.', 'Other'],
        description="Why are you deleting your character?"
    ) #type:ignore
): 
    user_id = message.author.id
    info = get_char(user_id)
    if not info:
        await message.respond("There was an error finding your character. Try creating one with `/create`!")
        return
    (
        userId,
        char_name,
        calling,
        rank,
        species,
        size,
        good1,
        good2,
        bad,
        img_url,
        might,
        deftness,
        grit,
        insight,
        aura
    ) = info
    desc = f"## Are you sure you want to delete \n# {char_name}?"
    embed = Embed(
        title="",
        description=desc
    )
    embed.set_thumbnail(url=img_url)
    await message.respond(embed=embed, view=DeleteView(
        message,
        userId,
        char_name,
        calling,
        rank,
        img_url,
        reason
    ))

@bot.slash_command(
    guild_ids=servers,
    name="graveyard",
    description="View all the characters that have died."
)
async def graveyard(message):
    deaths = view_graveyard()
    embed = Embed(
        title="",
        description=f"## Gone but not forgotten."
    )
    embed.set_image(url="https://i.imgur.com/qonze34.gif")
    for char in deaths:
        (
            userId,
            char_name,
            calling,
            rank,
            img,
            date
        ) = char
        dt_obj = datetime.strptime(date, f'%Y-%m-%d %H:%M:%S.%f%z')
        epoch = time.mktime(dt_obj.timetuple())
        user = await bot.fetch_user(userId)
        embed.add_field(
            name=f"{char_name} died \n<t:{int(epoch)}:D>",
            value=f"{calling}, Rank {rank}\nPlayed by {user.display_name}",
            inline=True
        )
    await message.respond(embed=embed)
    return

@bot.slash_command(
    guild_ids=servers,
    name="info",
    description="Get information on various topics from BREAK!! RPG rulebook."
)
async def info(message):
    embed = Embed(
        title="",
        description="### Select a topic to read about."
    )
    await message.respond(embed=embed, view=InfoView())
    return

@bot.slash_command(
    guild_ids=servers,
    name="injury",
    description="Choose a severity level for injury and roll on the injury table."
)
async def injury(
    message,
    severity: Option(int, required=True, min_value=1, max_value=3) #type:ignore
):
    roll = randint(1, 20)
    (injury, special_roll, img) = injury_table(severity, roll)
    if special_roll:
        injury += specRoll(special_roll)
    severity_type = "First" if severity == 1 else "Second" if severity == 2 else "Third"
    color = '7cd606' if severity == 1 else 'd67806' if severity == 2 else 'd60606'
    embed = Embed(
        title="",
        description=f"""## INJURY ROLL [{severity_type} offense]\n{injury}""",
        color=Colour(int(color, 16))
    )
    embed.set_thumbnail(url=img)
    await message.respond(embed=embed)

# ============================

bot.run(TOKEN)