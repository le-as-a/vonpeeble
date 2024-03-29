import discord
from discord import Embed, Colour, SelectOption
from db.api.ability import get_abilities, get_ability, get_char_abilities, get_maturative_ability
from db.api.character_ability import get_entries, new_entry
from db.api.character import rank_up
from views.RankupView import RankupView
from logic import generate_stats
from protected import customized

def abilityRankupCommand(message, char_info):
    (
        user_id,
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
    ) = char_info
    (url, color) = customized(calling)
    ability_rankup = discord.ui.View(timeout=60)
    all_abilities = get_abilities(calling, "All")
    maturative_ability = get_maturative_ability(species)
    all_abilities.append(maturative_ability)
    char_abilities = [ ability[3] for ability in get_entries(user_id) ]
    ability_option_names = []
    if rank + 1 < 6:
        ability_option_names = [ ability[0] for ability in all_abilities if ability[0] not in char_abilities and ability[2] not in ['Advanced', 'Maturative'] ]
    else:
        ability_option_names = [ ability[0] for ability in all_abilities if ability[0] not in char_abilities ]
    def byNameSort(ability):
        return ability[0]
    ability_option_names.sort(key=byNameSort)
    select_ability_options = [
        SelectOption(label=f"{ability}") for ability in ability_option_names
    ]
    ability_select = discord.ui.Select(placeholder="Select an Ability",options=select_ability_options)
    ability_rankup.add_item(ability_select)
    
    async def timeout():
        ability_rankup.disable_all_items()
        embed = Embed(
            title="",
            description=f"## Rank Up for {char_name.title()} has been cancelled."
        )
        await message.edit(embed=embed, view=ability_rankup)
        return

    ability_rankup.on_timeout = timeout
    
    async def ability_info(interaction):
        ability = get_ability(ability_select.values[0])
        embed = Embed(
            title=f"{ability[0]} [{ability[2]}]",
            description=ability[3],
            color=Colour(int(color, 16))
        )
        embed.set_thumbnail(url=url)
        await interaction.response.edit_message(embed=embed)
    
    ability_select.callback = ability_info
    
    rankup_confirm = discord.ui.Button(label="Confirm Selection", style=discord.ButtonStyle.green)
    ability_rankup.add_item(rankup_confirm)
    
    async def apply_rankup(interaction):
        selected_ability = ability_select.values[0]
        ability_rankup.disable_all_items()
        embed = Embed(
            title="",
            description=f"## {char_name.title()}'s rank\n### increased to {rank+1}!\nGained a new ability: {selected_ability}",
            color=Colour(int(color, 16))
        )
        embed.set_thumbnail(url=url)
        await interaction.response.edit_message(embed=embed, view=ability_rankup)
        rank_up(user_id, might, deftness, grit, insight, aura)
        new_entry(user_id, rank+1, "Calling", f"{selected_ability}")
        return
    
    rankup_confirm.callback = apply_rankup
    
    rankup_cancel = discord.ui.Button(label="Cancel Rankup", style=discord.ButtonStyle.gray)
    ability_rankup.add_item(rankup_cancel)
    
    async def cancel_rankup(interaction):
        ability_rankup.disable_all_items()
        embed = Embed(
            title="",
            description=f"## Rank Up for {char_name.title()} has been cancelled."
        )
        await interaction.response.edit_message(embed=embed, view=ability_rankup)
        return
    
    rankup_cancel.callback = cancel_rankup
    types_allowed = "Standard or Advanced" if rank+1 >= 6 else "Standard"
    embed = Embed(
        title="",
        description=f"## Select a(n) {types_allowed} Ability to learn.",
        color=Colour(int(color, 16))
    )
    embed.set_thumbnail(url=url)
    
    return (embed, ability_rankup)

async def scoreRankupCommand(message, info):
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
    (url, color) = customized(calling)
    (next_might, next_deftness, next_grit, next_insight, next_aura) = generate_stats(calling, rank+1, species, good1, good2, bad)
    desc = f"""## {char_name.title()}'s Rank Up
### Rank {rank} Scores
{might} | {deftness} | {grit} | {insight} | {aura}
### Rank {rank+1} Scores
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

def myAbilities(message, info):
    user_id = info[0]
    char_name = info[1]
    calling = info[2]
    img_url = info[9]
    (img, color) = customized(calling)
    abilities = [ability[3] for ability in get_entries(user_id)]
    ability_info = get_char_abilities(abilities)
    view = discord.ui.View()
    select_opts = [
        SelectOption(label=f"{abi}") for abi in abilities
    ]
    select = discord.ui.Select(placeholder=f"Select one of {char_name}'s Abilities to read more.",options=select_opts,row=2)
    view.add_item(select)
    
    async def timeout():
        view.disable_all_items()
        await message.edit(view=view)
        return
    
    view.on_timeout = timeout
    
    async def selectCallback(inter):
        ability = [abi for abi in ability_info if abi[0] == select.values[0]]
        ability = ability[0]
        desc = f"""## {char_name.title()}'s Abilities
### {ability[0]} [{ability[2]}]
{ability[3]}"""
        embed = Embed(
            title="",
            description=desc,
            color=Colour(int(color, 16))
        )
        embed.set_thumbnail(url=img_url)
        await inter.response.edit_message(embed=embed)
        
    select.callback = selectCallback
    
    embed = Embed(
        title="",
        description=f"## {char_name.title()}'s Abilities",
            color=Colour(int(color, 16))
    )
    embed.set_thumbnail(url=img_url)
    
    return select_opts
    
def myProfile(info):
    (
        user_id,
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
    def rankSort(val):
        return val[1]
    abilities.sort(key=rankSort)
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
        if a[1] < 1:
            ability_names += f"**{species}:** {a[3]}\n"
        else:
            ability_names += f"**R{a[1]}:** {a[3]}\n"
    embed.add_field(name="Aptitude Scores", value=stats,inline=False)
    embed.add_field(name="Abilities", value=ability_names, inline=False)
    
    return embed