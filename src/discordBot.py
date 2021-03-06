import discord
from discord.cogs.claimWaifu import claimWaifu
from discord.cogs.inventory import inventory
from discord.ext import commands
from data.database import databaseSetup
import os

from discord.cogs.bot import bot
from discord.cogs.leaderboard import leaderboard


databaseSetup()
token = os.getenv("DISCORD_BOT_TOKEN")
if (token is None):
    token = open("/run/secrets/DISCORD_BOT_TOKEN").read()
backendURL = os.getenv("BOT_URL")
if (backendURL is None):
    backendURL = "127.0.0.1:5200"
 
intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)
client.config = {}
client.config["backendURL"] = backendURL
client.remove_command('help')

client.add_cog(claimWaifu(client))
client.add_cog(inventory(client))
client.add_cog(bot(client))
client.add_cog(leaderboard(client))


client.run(token)
