import discord
from discord.ext import tasks, commands
from random import randint
from protected import TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents)
servers = [409528817179164672]