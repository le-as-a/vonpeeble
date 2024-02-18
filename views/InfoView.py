import discord
from db.api.ability import get_abilities

class InfoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        
    @discord.ui.select(
        placeholder="What topic do you want to read about?",
        options=[
            discord.SelectOption(label="Abilities"),
            discord.SelectOption(label="Quirks"),
            discord.SelectOption(label="World")
        ],
        custom_id="topic-select"
    )
    async def topicSelect(self, topicSel, topicInter):
        if len(self.children) > 1:
            for child in self.children:
                if child.custom_id != "topic-select":
                    self.remove_item(child)
        
        topicSelected = topicSel.values[0]
        match topicSelected:
            case 'Abilities':
                callingSelect = discord.ui.Select(
                    placeholder="Pick a calling to view its abilities.",
                    options=[
                        discord.SelectOption(label="Factotum"),
                        discord.SelectOption(label="Sneak"),
                        discord.SelectOption(label="Champion"),
                        discord.SelectOption(label="Raider"),
                        discord.SelectOption(label="Battle Mage"),
                        discord.SelectOption(label="Murder Noble"),
                        discord.SelectOption(label="Sage"),
                        discord.SelectOption(label="Heretic")
                    ],
                    custom_id="calling-select"
                )
                
                callingEmbed = discord.Embed(
                    title="",
                    description="### Select a calling or pick a new topic!"
                )
                
                topicSel.placeholder = topicSelected
                async def abilityList(listInter):
                    callingSelect.placeholder = callingSelect.values[0]
                    if len(self.children) == 3:
                        for child in self.children:
                            if child.custom_id == "ability-select":
                                self.remove_item(child)
                    
                    abilities = get_abilities(callingSelect.values[0], 'All')
                    abilityOptions = [
                        discord.SelectOption(label=f"{ability[0]}", description=f"{ability[2]} Ability") for ability in abilities
                    ]
                    abilitySelect = discord.ui.Select(
                        placeholder="Choose an ability to view its details",
                        options=abilityOptions,
                        custom_id="ability-select"
                    )
                    
                    abilityListEmbed = discord.Embed(
                        title="",
                        description=f"### Select an ability to read its details."
                    )
                    
                    async def abilityInfo(abiInter):
                        abilitySelect.placeholder = abilitySelect.values[0]
                        ability = [info for info in abilities if info[0] == abilitySelect.values[0]][0]
                        embed = discord.Embed(
                            title=f"{ability[0]} [{ability[2]}]",
                            description=ability[3]
                        )
                        await abiInter.response.edit_message(embed=embed, view=self)
                        
                    abilitySelect.callback = abilityInfo
                    self.add_item(abilitySelect)
                    
                    await listInter.response.edit_message(embed=abilityListEmbed, view=self)
                    
                
                callingSelect.callback = abilityList
                self.add_item(callingSelect)
                
                await topicInter.response.edit_message(embed=callingEmbed, view=self)
            case 'Quirks':
                
                