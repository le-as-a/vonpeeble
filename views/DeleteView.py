import discord
from datetime import datetime
import time
from db.api.character import del_char
from db.api.graveyard import new_death

class DeleteView(discord.ui.View):
    def __init__(self, msg, user_id, char_name, calling, rank, img, reason):
        super().__init__(timeout=10)
        self.msg = msg
        self.user_id = user_id
        self.char_name = char_name
        self.calling = calling
        self.rank = rank
        self.img = img
        self.reason = reason
        self.pressed = False
        
    @discord.ui.button(
        label="Confirm Deletion",
        style=discord.ButtonStyle.red
    )
    async def confirmDelete(self, btn, inter):
        self.pressed = True
        self.disable_all_items()
        msg = ""
        if self.reason == "Character died.":
            time_of_death = new_death(self.user_id, self.char_name, self.calling, self.rank, self.img)
            dt_obj = datetime.strptime(time_of_death, f'%Y-%m-%d %H:%M:%S.%f%z')
            epoch = time.mktime(dt_obj.timetuple())
            msg = f"### {self.char_name} was buried in the graveyard \n### on <t:{int(epoch)}:D>.\nView the dead with `/graveyard`."
        else:
            msg = f"{self.char_name} has been deleted."
        embed = discord.Embed(
            title="",
            description=msg
        )
        embed.set_thumbnail(url=self.img)
        await inter.response.edit_message(embed=embed, view=self)
        del_char(self.user_id)
        return
    
    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.gray
    )
    async def cancelDelete(self, btn, inter):
        self.pressed = True
        self.disable_all_items()
        embed = discord.Embed(
            title="",
            description=f"### {self.char_name}'s deletion was cancelled.\nView your character with `/profile`."
        )
        embed.set_thumbnail(url=self.img)
        await inter.response.edit_message(embed=embed, view=self)
        return
    
    async def interaction_check(self, interaction):
        if interaction.user != self.msg.author:
            await interaction.response.send_message("This isn't your character!", ephemeral=True)
            return False
        return True
    
    async def on_timeout(self):
        if not self.pressed:
            self.disable_all_items()
            embed = discord.Embed(
                title="",
                description=f"### {self.char_name}'s deletion was cancelled.\nView your character with `/profile`."
            )
            embed.set_thumbnail(url=self.img)
            await self.message.edit(embed=embed, view=self)
        return
        
        
    