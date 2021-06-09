import discord
import random
import os
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Member
from discord.ext.commands import Bot
from discord import Status

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
    print("what")
    embed = discord.Embed(
        title = 'Sample Waifu name',
        description = 'Unclaimed',
        colour = discord.Colour.blue()
    )
    embed.set_image(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/053b52c1-e89f-469b-aacb-972f74758f24/ddluws0-67fa36cc-0007-4e27-8bdf-46aefed76605.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzA1M2I1MmMxLWU4OWYtNDY5Yi1hYWNiLTk3MmY3NDc1OGYyNFwvZGRsdXdzMC02N2ZhMzZjYy0wMDA3LTRlMjctOGJkZi00NmFlZmVkNzY2MDUuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.pzbBFaABSy5xE-2yDGXwGZiibBLr4jcK_oh_dJ6Z-sk ')
    embed.add_field(name = 'Name', value = 'name', inline = False)
    embed.add_field(name = 'Age', value = 'age', inline = False)
    embed.add_field(name = 'Gender', value = 'female', inline = False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('👍')
    await ctx.send("React with 👍 to claim!")
    reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: reaction.emoji == '👍')

    embed2 = discord.Embed(
        title = 'Claimed', 
        description = 'Claimed',
        colour = discord.Colour.red()
    )
    embed2.set_image(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/053b52c1-e89f-469b-aacb-972f74758f24/ddluws0-67fa36cc-0007-4e27-8bdf-46aefed76605.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzA1M2I1MmMxLWU4OWYtNDY5Yi1hYWNiLTk3MmY3NDc1OGYyNFwvZGRsdXdzMC02N2ZhMzZjYy0wMDA3LTRlMjctOGJkZi00NmFlZmVkNzY2MDUuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.pzbBFaABSy5xE-2yDGXwGZiibBLr4jcK_oh_dJ6Z-sk ')
    embed2.add_field(name = 'Name', value = 'name', inline = False)
    embed2.add_field(name = 'Age', value = 'age', inline = False)
    embed2.add_field(name = 'Gender', value = 'female', inline = False)

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

client.run('ODQyODMyODc4NTU0MzE2ODM3.YJ7DSQ.xMx2ddZCWmKg6aihGeb2esDGKYQ')

#TODO: Create a caste system for waifu / husbandos
# Use ANILIST for caste


# TODO: Create a user system for collecting
# test