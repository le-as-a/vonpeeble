import discord
from discord import Embed, Colour, SelectOption
from commands import myProfile, myAbilities
from logic import customized, quirk_decor
from db.api.character_ability import get_entries
from db.api.ability import get_char_abilities
from db.api.character_quirk import get_char_quirk

class ProfileView(discord.ui.View):
    def __init__(self, msg, info):
        super().__init__()
        self.msg = msg
        self.info = info
        self.select_opts = myAbilities(msg, info)
        
        select = discord.ui.Select(
            placeholder="Select an Ability to learn more.",
            options=self.select_opts,
            custom_id="select"
        )
        self.add_item(select)
        
        async def selectCallback(inter):
            user_id = self.info[0]
            char_name = self.info[1]
            calling = self.info[2]
            species = self.info[4]
            img_url = self.info[9]
            (img, color) = customized(calling)
            abilities = [ability[3] for ability in get_entries(user_id)]
            ability_info = get_char_abilities(abilities)
            ability = [abi for abi in ability_info if abi[0] == select.values[0]][0]
            desc = f"## {char_name.title()}'s Abilities"
            if ability[1] == species:
                desc += f"\n### {ability[0]} [{species}]\n{ability[3]}"
            else:
                desc += f"\n### {ability[0]} [{ability[2]}]\n{ability[3]}"
            embed = Embed(
                title="",
                description=desc,
                color=Colour(int(color, 16))
            )
            embed.set_thumbnail(url=img_url)
            for child in self.children:
                if child.custom_id == "basics" or child.custom_id == "quirk":
                    child.disabled = False
            await inter.response.edit_message(embed=embed, view=self)
        select.callback = selectCallback
            
        
    @discord.ui.button(
        label="Basics",
        style=discord.ButtonStyle.blurple,
        custom_id="basics",
        disabled=True,
        row=2
    )
    async def viewBasics(self, btn, inter):
        embed = myProfile(self.info)
        btn.disabled = True
        for child in self.children:
            if child.custom_id == "quirk":
                child.disabled = False
        await inter.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(
        label="Quirk",
        style=discord.ButtonStyle.green,
        custom_id="quirk",
        row=2
    )
    async def viewQuirk(self, btn, inter):
        btn.disabled = True
        user_id = self.info[0]
        quirk = get_char_quirk(user_id)
        (color, img) = quirk_decor(quirk[2], quirk[1])
        embed = Embed(
            title="",
            description=f"## {quirk[1]} [{quirk[2]}]\n{quirk[3]}",
            color=Colour(int(color, 16))
        )
        embed.set_thumbnail(url=img)
        for child in self.children:
            if child.custom_id == "basics" and child.disabled == True:
                child.disabled = False
        await inter.response.edit_message(embed=embed, view=self)
        
    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(view=self)
        return
    
        
        
        