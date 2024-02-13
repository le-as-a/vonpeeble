from discord import Intents, Option, Embed, Colour, User
from discord.ext import commands
from random import randint
from datetime import datetime
import calendar
from protected import TOKEN, servers
from logic import generate_stats, customized
from db.api.character import new_char, get_char, get_aptitude, rank_up, edit_char, del_char
from db.api.graveyard import new_death, view_graveyard
from views.RankupView import RankupView
from views.DeleteView import DeleteView

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents)

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
    char_name: Option(str, required=True), # type: ignore
    calling: Option(str, required=True, choices=[
        'Factotum',
        'Sneak',
        'Champion',
        'Raider',
        'Battle Mage',
        'Murder Noble',
        'Sage',
        'Heretic'    
    ]), # type: ignore
    rank: Option(int, required=True, min_value=1, max_value=10), # type: ignore
    species: Option(str, required=True, choices=[
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
        'Bio-Mechaonoid'  
    ]), # type: ignore
    good_trait_1: Option(str, required=True, choices=[
        'Might', 'Deftness', 'Grit', 'Insight', 'Aura'    
    ]), # type: ignore
    good_trait_2: Option(str, required=True, choices=[
        'Might', 'Deftness', 'Grit', 'Insight', 'Aura'    
    ]), # type: ignore
    bad_trait: Option(str, required=True, choices=[
        'Might', 'Deftness', 'Grit', 'Insight', 'Aura'    
    ]), # type: ignore
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
    
    if status:
        response = f"{char_name} was successfully created! Use `/profile` to view them."
    else:
        response = f"There was an error creating this character. Are you sure you don't already have one?"
    await message.respond(response)
    return

@bot.slash_command(
    guild_ids=servers,
    name="profile",
    description="View your BREAK!! RPG character."                   
)
async def profile(message):
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
    (calling_url, calling_color) = customized(calling)
    embed = Embed(
        title="",
        description=f"# {char_name.title()}\n## {species} {calling}, Rank {rank}",
        color=Colour(int(calling_color, 16))
    )
    embed.set_image(url=img_url)
    embed.set_thumbnail(url=calling_url)
    stats = f"""**Might** {might}   
    **Deftness** {deftness}     
    **Grit** {grit}
    **Insight** {insight}   
    **Aura** {aura}"""
    embed.add_field(name="Aptitude Scores", value=stats,inline=False)
    await message.respond(embed=embed)
    return

@bot.slash_command(
    guild_ids=servers,
    name="check",
    description="Roll an aptitude check!"
)
async def check(
    message,
    aptitude: Option(str, required=True, choices=['Might', 'Deftness', 'Grit', 'Insight', 'Aura']), #type:ignore
    reroll: Option(str, required=False, choices=['Edge', 'Snag']), #type: ignore
    bonus: Option(str, required=False, choices=['Minor Bonus', 'Minor Penalty', 'Major Bonus', 'Major Penalty']) #type:ignore
):
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
    
    user_id = message.author.id
    
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
    desc = f"""## {aptitude} check
    {altered_roll}\n# {total if bonus and result != f"## Special Success for {char_name}!" else chosen} `vs` {score}\n{result}
    """
    embed = Embed(
        title="",
        description=desc
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
    bonus: Option(int, required=False, min_value=-5, max_value=15), #type:ignore
    reroll: Option(str, required=False, choices=['Edge', 'Snag']) #type:ignore
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
        chosen = roll1 if roll1 < roll2 else roll2
        rejected = roll2 if chosen == roll1 else roll1
        altered_roll += f"... with an **Edge** ({rejected}).\n"
    elif reroll and reroll == 'Snag':
        chosen = roll1 if roll1 > roll2 else roll2
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
    if rank == 10:
        await message.respond("Your character is at the max rank already!")
        return
    (next_might, next_deftness, next_grit, next_insight, next_aura) = generate_stats(calling, rank+1, species, good1, good2, bad)
    (url, color) = customized(calling)
    desc = f"""## {char_name.title()}'s Rank Up
### Current Scores
{might} | {deftness} | {grit} | {insight} | {aura}
### Next Scores
{next_might} | {next_deftness} | {next_grit} | {next_insight} | {next_aura}"""
    embed = Embed(
        title="",
        description=desc,
        color=Colour(int(color, 16))
    )
    embed.set_thumbnail(url=url)
    await message.respond(embed=embed, view=RankupView(
        message, 
        userId, 
        char_name, 
        rank, 
        next_might, 
        next_deftness, 
        next_grit, 
        next_insight, 
        next_aura, 
        url, 
        color
    ))

@bot.slash_command(
    guild_ids=servers,
    name="delete",
    description="Delete your character..."
)
async def delete(message, reason: Option(str, choices=['Character died.', 'Remaking them.', 'Other'], required=True)): #type:ignore
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
        dt_obj = datetime.strptime(date, f'%Y-%m-%d')
        epoch = calendar.timegm(dt_obj.timetuple())
        user = await bot.fetch_user(userId)
        embed.add_field(
            name=f"{char_name} died <t:{epoch}:D>",
            value=f"{calling}, Rank {rank}\nPlayed by {user.display_name}",
            inline=False
        )
    await message.respond(embed=embed)
    return


bot.run(TOKEN)