import discord
import time
from discord.cogs.ClaimWaifu import ClaimWaifu
from discord.cogs.inventory import inventory
from discord.ext import commands
from data.database import databaseSetup
import os

from discord.cogs.bot import bot 


databaseSetup()
token = os.getenv("DISCORD_BOT_TOKEN")  
if (token is None):
    token = open(f"/run/secrets/DISCORD_BOT_TOKEN").read()
backendURL = os.getenv("BOT_URL")
if (backendURL is None ):
    backendURL = "127.0.0.1:5200"

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.config = {}
client.config["backendURL"] = backendURL
client.remove_command('help')

client.add_cog(ClaimWaifu)
client.add_cog(inventory)
client.add_cog(bot)


client.run(token)

