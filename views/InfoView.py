import discord
from db.api.ability import get_abilities, get_all_species_abilities
from db.api.quirk import get_all_quirks
from logic import customized, qColor, qImg

class InfoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        
    @discord.ui.select(
        placeholder="What topic do you want to read about?",
        options=[
            discord.SelectOption(label="Calling Abilities"),
            discord.SelectOption(label="Species Abilities"),
            discord.SelectOption(label="Character Quirks")
        ],
        custom_id="topic-select"
    )
    async def topicSelect(self, topicSel, topicInter):
        topicSelected = topicSel.placeholder = topicSel.values[0]
        for child in self.children[::-1]:
            if child.custom_id != "topic-select":
                self.remove_item(child)
        
        topicEmbed = discord.Embed(
            title="",
            description=f"## You chose to view info on {topicSelected}!\n### Use the dropdown options to learn more."
        )
        
        match topicSelected:
            case 'Calling Abilities':
                callingSelect = discord.ui.Select(
                    placeholder="Select a calling.",
                    options=[
                        discord.SelectOption(
                            label="Factotum",
                            emoji="<:factotum:1208699303271342141>"
                        ),
                        discord.SelectOption(
                            label="Sneak",
                            emoji="<:sneak:1208699307277164564>"
                        ),
                        discord.SelectOption(
                            label="Champion",
                            emoji="<:champion:1208699298406203453>"
                        ),
                        discord.SelectOption(
                            label="Raider",
                            emoji="<:raider:1208699297235865620>"
                        ),
                        discord.SelectOption(
                            label="Battle Mage",
                            emoji="<:battlemage:1208699305817546803>"
                        ),
                        discord.SelectOption(
                            label="Murder Noble",
                            emoji="<:murdernoble:1208699300109094932>"
                        ),
                        discord.SelectOption(
                            label="Sage",
                            emoji="<:sage:1208699304446001152>"
                        ),
                        discord.SelectOption(
                            label="Heretic",
                            emoji="<:heretic:1208699302059311114>"
                        )
                    ],
                    custom_id="calling-select"
                )
                self.add_item(callingSelect)
                
                async def callingSelected(callingInter):
                    calling = callingSelect.placeholder = callingSelect.values[0]
                    abilities = get_abilities(calling, 'All')
                    (img, color) = customized(calling)
                    
                    if len(self.children) == 3:
                        for child in self.children:
                            if child.custom_id == "ability-select":
                                self.remove_item(child)
                                
                    abilitySelect = discord.ui.Select(
                        placeholder="Select an Ability.",
                        options=[
                            discord.SelectOption(
                                label=f"{ability[0]}",
                                description=f"{ability[2]}"
                            ) for ability in abilities
                        ],
                        custom_id="ability-select"
                    )
                    self.add_item(abilitySelect)
                    
                    callingEmbed = discord.Embed(
                        title="",
                        description=f"## You selected {calling}!\n### Choose an ability to learn more.",
                        color=discord.Colour(int(color, 16))
                    )
                    callingEmbed.set_thumbnail(url=img)
                    
                    async def abilitySelected(abilityInter):
                        abilitySelect.placeholder = abilitySelect.values[0]
                        ability = [abi for abi in abilities if abi[0] == abilitySelect.values[0]][0]
                        
                        abilityEmbed = discord.Embed(
                            title=f"{ability[0]} [{ability[2]}]",
                            description=ability[3],
                            color=discord.Colour(int(color, 16))
                        )
                        abilityEmbed.set_thumbnail(url=img)
                        
                        await abilityInter.response.edit_message(embed=abilityEmbed, view=self)
                    abilitySelect.callback = abilitySelected
                    
                    await callingInter.response.edit_message(embed=callingEmbed, view=self)
                callingSelect.callback = callingSelected
                
                await topicInter.response.edit_message(embed=topicEmbed, view=self)
            case 'Species Abilities':
                abilities = get_all_species_abilities()
                speciesSelect = discord.ui.Select(
                    placeholder="Select a species.",
                    options=[
                        discord.SelectOption(label="Human"),
                        discord.SelectOption(label="Dimensional Stray"),
                        discord.SelectOption(label="Chib"),
                        discord.SelectOption(label="Tenebrate"),
                        discord.SelectOption(label="Rai-Neko"),
                        discord.SelectOption(label="Promethean"),
                        discord.SelectOption(label="Gruun"),
                        discord.SelectOption(label="Goblin"),
                        discord.SelectOption(label="Dwarf"),
                        discord.SelectOption(label="Elf"),
                        discord.SelectOption(label="Bio-Mechanoid")
                    ],
                    custom_id="species-select"
                )
                self.add_item(speciesSelect)
                
                async def speciesSelected(speciesInter):
                    species = speciesSelect.placeholder = speciesSelect.values[0]
                    if len(self.children) == 3:
                        for child in self.children:
                            if child.custom_id == "ability-select":
                                self.remove_item(child)
                    
                    abilitySelect = discord.ui.Select(
                        placeholder="Select an ability.",
                        options=[
                            discord.SelectOption(
                                label=f"{ability[0]}",
                                description=f"{ability[2]}"
                            ) for ability in abilities if ability[1] == species    
                        ],
                        custom_id="ability-select"
                    )
                    self.add_item(abilitySelect)
                    
                    speciesEmbed = discord.Embed(
                        title="",
                        description=f"## You selected {species}!\n### Choose an ability to learn more."
                    )
                    
                    async def abilitySelected(abilityInter):
                        abilitySelect.placeholder = abilitySelect.values[0]
                        ability = [abi for abi in abilities if abi[0] == abilitySelect.values[0]][0]
                        
                        abilityEmbed = discord.Embed(
                            title=f"{ability[0]} [{ability[2]}]",
                            description=ability[3]
                        )
                        
                        await abilityInter.response.edit_message(embed=abilityEmbed, view=self)
                    abilitySelect.callback = abilitySelected
                
                    await speciesInter.response.edit_message(embed=speciesEmbed, view=self)
                speciesSelect.callback = speciesSelected
                
                await topicInter.response.edit_message(embed=topicEmbed, view=self)
            case 'Character Quirks':
                quirks = get_all_quirks()
                typeSelect = discord.ui.Select(
                    placeholder="Select a Quirk type.",
                    options=[
                        discord.SelectOption(label="Spirit"),
                        discord.SelectOption(label="Physiology"),
                        discord.SelectOption(label="Fate"),
                        discord.SelectOption(label="Eldritch"),
                        discord.SelectOption(label="Robotic")
                    ],
                    custom_id="type-select"
                )
                self.add_item(typeSelect)
                
                async def typeSelected(typeInter):
                    qType = typeSelect.placeholder = typeSelect.values[0]
                    color = qColor(qType)
                    
                    if len(self.children) == 3:
                        for child in self.children:
                            if child.custom_id == "quirk-select":
                                self.remove_item(child)
                    
                    quirkSelect = discord.ui.Select(
                        placeholder="Select a quirk.",
                        options=[
                            discord.SelectOption(
                                label=f"{quirk[0]}"
                            ) for quirk in quirks if qType == quirk[1]
                        ],
                        custom_id="quirk-select"
                    )
                    self.add_item(quirkSelect)
                    
                    typeEmbed = discord.Embed(
                        title="",
                        description=f"## You selected {qType}!\n### Choose a quirk to learn more.",
                        color=discord.Colour(int(color, 16))
                    )
                    
                    async def quirkSelected(quirkInter):
                        quirkSelect.placeholder = quirkSelect.values[0]
                        quirk = [
                            q for q in quirks if q[0] == quirkSelect.values[0]
                        ][0]
                        img = qImg(quirk[0])
                        quirkEmbed = discord.Embed(
                            title=f"{quirk[0]}",
                            description=quirk[2],
                            color=discord.Colour(int(color, 16))
                        )
                        quirkEmbed.set_thumbnail(url=img)
                        
                        await quirkInter.response.edit_message(embed=quirkEmbed, view=self)
                    quirkSelect.callback = quirkSelected
                    
                    await typeInter.response.edit_message(embed=typeEmbed, view=self)
                typeSelect.callback = typeSelected
                
                await topicInter.response.edit_message(embed=topicEmbed, view=self)
                        
                    