import discord
from db.api.character import rank_up

class RankupView(discord.ui.View):
    def __init__(self, msg, user_id, char_name, rank, might, deftness, grit, insight, aura, url, color):
        super().__init__(timeout=30)
        self.msg = msg
        self.user_id = user_id
        self.char_name = char_name
        self.rank = rank
        self.might = might
        self.deftness = deftness
        self.grit = grit
        self.insight = insight
        self.aura = aura
        self.url = url
        self.color = color
        self.pressed = False
        
    @discord.ui.button(
        label="Confirm Rankup",
        style=discord.ButtonStyle.green
    )
    async def confirmRankup(self, btn, interaction):
        btn.disabled = True
        self.pressed = True
        embed = discord.Embed(
            title="",
            description=f"## {self.char_name}'s rank \n### increased to {self.rank+1}!",
            color=discord.Colour(int(self.color, 16))
        )
        embed.set_thumbnail(url=self.url)
        await interaction.response.edit_message(embed=embed, view=self)
        rank_up(self.user_id, self.might, self.deftness, self.grit, self.insight, self.aura)
        return
        
    async def interaction_check(self, interaction):
        if interaction.user != self.msg.author:
            await interaction.response.send_message("This isn't your character!", ephemeral=True)
            return False
        return True
    
    async def on_timeout(self):
        if not self.pressed:
            embed = discord.Embed(
                title="",
                description=f"## {self.char_name}'s rank up has been cancelled."
            )
            self.disable_all_items()
            await self.message.edit(embed=embed, view=self)
        return