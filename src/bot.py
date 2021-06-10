import discord
import random
import sys
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Member
from discord.ext.commands import Bot
from discord import Status
from collection import findWaifu
from database import storeWaifu

try:
    token = sys.argv[1]
except:
    print("ERROR: Did not add evironment variable \n try doing python bot.py entertokenhere")
    quit()

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Use -help for a list of commands"))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**Command on Cooldown**, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await client.process_commands(message)



@client.command(aliases = ['wa'])
@commands.cooldown(1, 5, commands.BucketType.guild)
async def waifu(ctx):
    valid_reactions = ['👍']
    waifulol = findWaifu(30)
    rand1 = random.randint(0, 29)
    print("what")
    embed = discord.Embed(
        title = 'Unclaimed',
        description = 'Unclaimed',
        colour = discord.Colour.blue()
    )
    embed.set_image(url= waifulol[rand1].imageURL)
    embed.add_field(name = 'Name', value = f'{waifulol[rand1].name}', inline = False)
    msg = await ctx.send(embed=embed)
    await ctx.send("React with 👍 within **4** seconds to claim!")
    await msg.add_reaction('👍')
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_reactions
    reaction, user = await client.wait_for("reaction_add",timeout=4.0, check=check)

    if str(reaction.emoji) == '👍':
        embed2 = discord.Embed(
            title = 'Claimed', 
            description = f'Claimed by {user.name}',
            colour = discord.Colour.red()
        )
        embed2.set_image(url= waifulol[rand1].imageURL)
        embed2.add_field(name = 'Name', value = f'{waifulol[rand1].name}', inline = False)
        await msg.edit(embed=embed2)  
        storeWaifu(waifulol[rand1], user.id)

@client.command(aliases = ['h'])
async def help(ctx):
    embed = discord.Embed(
        title = 'Help menu for Waifu Bot', 
        description = 'Commands:',
        colour = discord.Colour.green()
    )
    embed.set_thumbnail(url = 'https://previews.123rf.com/images/aquir/aquir1311/aquir131100316/23569861-sample-grunge-red-round-stamp.jpg')
    await ctx.send(embed=embed)

@client.command(aliases = ['inv'])
@commands.cooldown(1, 2, commands.BucketType.user)
async def inventory(ctx):
    embed = discord.Embed(
        title = 'Click this link to view your inventory',
        description = 'link',
        colour = discord.Color.blurple()
    )
    await ctx.message.author.send(embed=embed)

client.run(token)

#TODO: Create a caste system for waifu / husbandos
# Use ANILIST for caste


# TODO: Create a user system for collecting
# test