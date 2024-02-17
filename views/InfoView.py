import discord

class InfoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.select(
        placeholder="What topic do you want to read about?",
        options=[
            discord.SelectOption(label="Abilities"),
            discord.SelectOption(label="Quirks"),
            discord.SelectOption(label="World")
        ],
        custom_id="topic-select"
    )
    async def topicSelect(self, select, topicInter):
        selected = select.values[0]
        match selected:
            case 'Abilities':
                return