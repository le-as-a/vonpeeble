from discord import Intents, Option, Embed, Colour, SelectOption
import discord
from discord.ext import commands
from random import randint
from datetime import datetime
import time
from protected import TOKEN, servers
from logic import generate_stats, customized
from db.api.character import new_char, get_char, get_aptitude, edit_char
from db.api.graveyard import view_graveyard
from db.api.ability import get_abilities, get_ability
from db.api.character_ability import get_entries, new_entry
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
    char_name: Option(
        str, required=True,
        description="Name your shiny new character."
    ), # type: ignore
    calling: Option(str, required=True, choices=[
        'Factotum',
        'Sneak',
        'Champion',
        'Raider',
        'Battle Mage',
        'Murder Noble',
        'Sage',
        'Heretic'    
    ],
    description="Pick a calling from the list provided."), # type: ignore
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
    ],
    description="Pick a species to play from the list provided."), # type: ignore
    good_trait_1: Option(str, required=True, choices=[
        'Might', 'Deftness', 'Grit', 'Insight', 'Aura'    
    ],
    description="Add a +1 to which trait?"), # type: ignore
    good_trait_2: Option(str, required=True, choices=[
        'Might', 'Deftness', 'Grit', 'Insight', 'Aura'    
    ],
    description="Add a +1 to which trait?"), # type: ignore
    bad_trait: Option(str, required=True, choices=[
        'Might', 'Deftness', 'Grit', 'Insight', 'Aura'    
    ],
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
    
    starter_abilities = [ability[0] for ability in get_abilities(calling, "Default")]
    for x in starter_abilities:
        new_entry(user_id, 1, "Calling", x)
    
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
    abilities = get_entries(user_id)
    (calling_url, calling_color) = customized(calling)
    embed = Embed(
        title="",
        description=f"# {char_name.title()}\n## {calling}, Rank {rank}",
        color=Colour(int(calling_color, 16))
    )
    embed.set_image(url=img_url)
    embed.set_thumbnail(url=calling_url)
    stats = f"""**Might** {might}   
    **Deftness** {deftness}     
    **Grit** {grit}
    **Insight** {insight}   
    **Aura** {aura}"""
    ability_names = ""
    for a in abilities:
        ability_names += f"**R{a[1]}:** {a[3]}\n"
    embed.add_field(name="Aptitude Scores", value=stats,inline=False)
    embed.add_field(name="Abilities", value=ability_names, inline=False)
    await message.respond(embed=embed)
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
        choices=['Might', 'Deftness', 'Grit', 'Insight', 'Aura'],
        description="Choose an aptitude to compare to this check!"
    ), #type:ignore
    reroll: Option(
        str, required=False, 
        choices=['Edge', 'Snag'],
        description="Optionally include an Edge/Snag."
    ), #type: ignore
    bonus: Option(
        str, required=False, 
        choices=['Minor Bonus', 'Minor Penalty', 'Major Bonus', 'Major Penalty'],
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
    bonus: Option(
        int, required=False, min_value=-5, max_value=15,
        description="Choose an aptitude to compare to this check!"
    ), #type:ignore
    reroll: Option(
        str, required=False, 
        choices=['Edge', 'Snag'],
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
    name="abilities",
    description="View information on abilities for a certain calling."
)
async def abilities(
    message,
    calling: Option(str, choices=[
        'Factotum',
        'Sneak',
        'Champion',
        'Raider',
        'Battle Mage',
        'Murder Noble',
        'Sage',
        'Heretic'    
    ]), #type:ignore
    ability_type: Option(str, choices=[
        'Starter',
        'Standard',
        'Advanced'
    ]) #type:ignore
):
    ability_type = "Default" if ability_type == 'Starter' else ability_type
    (img, color) = customized(calling)
    abilities = get_abilities(calling, ability_type)
    ability_options = [
        SelectOption(label=f"{ability[0]}") for ability in abilities
    ]
    ability_select = discord.ui.Select(placeholder="Select an Ability",options=ability_options)
    ability_view = discord.ui.View(timeout=180)
    ability_view.add_item(ability_select)
    
    async def timeout():
        ability_select.disabled = True
        await message.edit(view=ability_view)
        return
    
    ability_view.on_timeout = timeout
    
    async def ability_info(interaction):
        ability = get_ability(ability_select.values[0])
        aType = "Starter" if ability[2] == "Default" else ability[2]
        embed = Embed(
            title=f"{ability[0]} [{aType}]",
            description=ability[3],
            color=Colour(int(color, 16))
        )
        embed.set_thumbnail(url=img)
        await interaction.response.edit_message(embed=embed)
    
    ability_select.callback = ability_info
    embed = Embed(
        title="Choose an Ability to read about it below!",
        color=Colour(int(color, 16))
    )
    embed.set_thumbnail(url=img)
    
    await message.respond(embed=embed, view=ability_view)
    
    

# ============================

bot.run(TOKEN)