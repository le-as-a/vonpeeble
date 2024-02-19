import discord
from db.api.quirk import get_all_quirks
from db.api.character_quirk import new_char_quirk
from db.api.character import del_char
from db.api.character_ability import del_entries
from logic import qColor, qImg

class CreateView(discord.ui.View):
    def __init__(self, user_id, char_name):
        super().__init__(timeout=500)
        self.user_id = user_id
        self.char_name = char_name
        self.quirk_type = ""
        self.all_quirks = get_all_quirks()
        self.selected_quirk = ()
        
    async def on_timeout(self):
        self.disable_all_items()
        embed = discord.Embed(
            title="Character creation cancelled!"
        )
        del_char(self.user_id)
        del_entries(self.user_id)
        await self.message.edit(embed=embed, view=self)
        
    @discord.ui.button(
        label="Confirm Quirk",
        style=discord.ButtonStyle.green,
        disabled=True,
        row=3,
        custom_id="confirm-btn"
    )
    async def confirmQuirk(self, btn, inter):
        (quirk_name, quirk_type, desc) = self.selected_quirk
        new_char_quirk(self.user_id, quirk_name, quirk_type, desc)
        self.disable_all_items()
        embed = discord.Embed(
            title="",
            description=f"## {self.char_name.title()}'s Quirk Saved!\n- Added quirk: {quirk_name}"
        )
        
        await inter.response.edit_message(embed=embed, view=self)
        return
            
            
    @discord.ui.select(row=1, custom_id="type-select", placeholder="Select a Quirk Type", options=[
        discord.SelectOption(label="Spirit"),
        discord.SelectOption(label="Physiology"),
        discord.SelectOption(label="Fate"),
        discord.SelectOption(label="Eldritch"),
        discord.SelectOption(label="Robotic")
    ])
    async def quirkTypeSelect(self, select, inter):
        self.quirk_type = select.values[0]
        opts = [
            discord.SelectOption(label=f"{quirk[0]}") for quirk in self.all_quirks if quirk[1] == self.quirk_type
        ]
        if len(self.children) == 3:
            for child in self.children:
                if child.custom_id == "quirk-select":
                    self.remove_item(child)
        
        quirkSelect = discord.ui.Select(
            placeholder="Select a Quirk.",
            options=opts,
            row=2,
            custom_id="quirk-select"
        )
        self.add_item(quirkSelect)
        
        embed = discord.Embed(
            title="Choose your Quirk.",
            description=f"You selected {self.quirk_type}! Now select a Quirk from the second menu and click confirm."
        )
            
        async def quirkSelectCallback(interaction):
            for child in self.children:
                if child.custom_id == "confirm-btn":
                    child.disabled = False
            self.quirk_type = select.values[0]
            quirk = [ q for q in self.all_quirks if q[0] == quirkSelect.values[0] ][0]
            self.selected_quirk = quirk
            color = qColor(quirk[1])
            img = qImg(quirk[0])
            embed = discord.Embed(
                title=f"{quirk[0]} [{quirk[1]}]",
                description=f"{quirk[2]}",
                color=discord.Colour(int(color, 16))
            )
            embed.set_thumbnail(url=img)
            await interaction.response.edit_message(embed=embed, view=self)
        quirkSelect.callback = quirkSelectCallback
        select.placeholder = select.values[0]
        await inter.response.edit_message(embed=embed, view=self)
        
            
        