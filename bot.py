from discord import Intents, Option
from discord.ext import commands
from random import randint
from protected import TOKEN, servers
from logic import generate_stats
from db.api.character import new_char, get_char, get_aptitude, rank_up, edit_char, del_char

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
    
    if not image:
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
        await message.respond("There was an error viewing your character. You can create one using `/create`!")
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
    
    

bot.run(TOKEN)