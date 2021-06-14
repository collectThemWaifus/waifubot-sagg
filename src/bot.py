import discord
import random
import sys
from discord.ext import commands
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

def getnum(str):
    ret = ''
    for i in range(len(str)):
        if str[i].isdigit():
            ret += str[i]
    return(ret)

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

#key is MessageID, and Value is Waifu
unclaimedWaifus = {}
@client.event
async def on_reaction_add(reaction, user):
    if (user.bot): 
        return
    global unclaimedWaifus
    try: #check if waifu exsits
        messageWaifu = unclaimedWaifus.get(str(reaction.message.id))
    except:
        return
    if str(reaction.emoji) == '👍':
        embed2 = discord.Embed(
            title = 'Claimed', 
            description = f'Claimed by {user.name}',
            colour = discord.Colour.red()
        )
        embed2.set_image(url= messageWaifu.imageURL)
        embed2.add_field(name = 'Name', value = f'{messageWaifu.name}', inline = False)
        await reaction.message.edit(embed=embed2)  
        storeWaifu(messageWaifu, user.id)


@client.command(aliases = ['wa'])
async def waifu(ctx : commands.Context):
    valid_reactions = ['👍']
    listOfRandomWaifu = findWaifu(30)
    randomNum = random.randint(0, 29)
    randomWaifu = listOfRandomWaifu[randomNum]
    print("what")
    embed = discord.Embed(
        title = 'Unclaimed',
        description = 'Unclaimed',
        colour = discord.Colour.blue()
    )
    embed.set_image(url= randomWaifu.imageURL)
    embed.add_field(name = 'Name', value = f'{randomWaifu.name}', inline = False)
    msg = await ctx.send(embed=embed)
    unclaimedWaifus[str(msg.id)] =randomWaifu

    #await ctx.send("React with 👍 within **4** seconds to claim!")
    await msg.add_reaction('👍')

@client.command(aliases = ['h'])
async def help(ctx):
    embed = discord.Embed(
        title = 'Help',
        description = 'List of commands for Waifu Bot',
        colour = discord.Colour.green()
    )
    #embed.set_thumbnail(url = 'https://previews.123rf.com/images/aquir/aquir1311/aquir131100316/23569861-sample-grunge-red-round-stamp.jpg')
    embed.add_field(name = 'waifu (wa)', value = 'Displays a random waifu, react to claim.', inline = False)
    embed.add_field(name = 'inventory (inv)', value = 'Sends you a link to a website containing your inventory', inline = False)
    embed.add_field(name = 'help (h)', value = 'Displays this message!', inline = False)
    embed.add_field(name = 'setlb [channel]', value = 'Set a specific channel to display the leaderboard', inline = False)
    embed.set_footer(text="This bot is still in development!")
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


@client.command()
@commands.has_permissions(manage_guild = True)
async def setlb(ctx, channel):
    await ctx.send(f'Set the leaderboard to {channel}')
    channel = getnum(str(channel))
    channel = int(channel)
    channel = client.get_channel(channel)
    await channel.send("test")

@setlb.error
async def setlb_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**You dont have permission to do that!**")
client.run(token)

#TODO: Create a caste system for waifu / husbandos
# Use ANILIST for caste


# TODO: Create a user system for collecting
# test