import discord
import random
import os
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Member
from discord.ext.commands import Bot
from discord import Status

from collection import findWaifu

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Use -help for a list of commands"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await client.process_commands(message)



@client.command(aliases = ['wa'])
async def waifu(ctx):
    waifulol = findWaifu(30)
    rand1 = random.randint(0, 30)
    print("what")
    embed = discord.Embed(
        title = 'Unclaimed',
        description = 'Unclaimed',
        colour = discord.Colour.blue()
    )
    embed.set_image(url= waifulol[rand1].imageURL)
    embed.add_field(name = 'Name', value = f'{waifulol[rand1].name}', inline = False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('👍')
    await ctx.send("React with 👍 to claim!")
    reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: reaction.emoji == '👍')

    embed2 = discord.Embed(
        title = 'Claimed', 
        description = 'Claimed',
        colour = discord.Colour.red()
    )
    embed2.set_image(url= waifulol[rand1].imageURL)
    embed2.add_field(name = 'Name', value = f'{waifulol[rand1].name}', inline = False)

    await ctx.send(f"Claimed by {user.name}")
    await msg.edit(embed=embed2)



    #stores the user.name and the name of waifu and the image here

@client.command(aliases = ['helpme'])
async def help(ctx):
    embed = discord.Embed(
        title = 'Help menu for Waifu Bot', 
        description = 'Commands:',
        colour = discord.Colour.green()
    )
    embed.set_thumbnail(url = 'https://previews.123rf.com/images/aquir/aquir1311/aquir131100316/23569861-sample-grunge-red-round-stamp.jpg')
    await ctx.send(embed=embed)

client.run(token)

#TODO: Create a caste system for waifu / husbandos
# Use ANILIST for caste


# TODO: Create a user system for collecting
# test