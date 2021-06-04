import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Member
from discord.ext.commands import bot

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '>', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.command(aliases = ['wa'])
async def waifu(ctx):
    print("what")
    embed = discord.Embed(
        title = 'Sample Waifu name', 
        description = 'idk',
        colour = discord.Colour.blue()
    )
    embed.add_field(name = 'test', value = 'test', inline = False)
    embed.set_image(url='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/053b52c1-e89f-469b-aacb-972f74758f24/ddluws0-67fa36cc-0007-4e27-8bdf-46aefed76605.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzA1M2I1MmMxLWU4OWYtNDY5Yi1hYWNiLTk3MmY3NDc1OGYyNFwvZGRsdXdzMC02N2ZhMzZjYy0wMDA3LTRlMjctOGJkZi00NmFlZmVkNzY2MDUuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.pzbBFaABSy5xE-2yDGXwGZiibBLr4jcK_oh_dJ6Z-sk ')
    await ctx.send(embed=embed)

client.run(token)

#TODO: Create a caste system for waifu / husbandos
# Use ANILIST for caste


# TODO: Create a user system for collecting
# test