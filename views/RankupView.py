import discord
from db.api.character import rank_up

class RankupView(discord.ui.View):
    def __init__(self, user_id, char_name):
        super().__init__(timeout=30)
        self.user_id = user_id
        self.char_name = char_name
        
    @discord.ui.button(
        label="Confirm Rankup",
        style=discord.ButtonStyle.greem
    )
    async def confirmRankup(self, btn, interaction):
        