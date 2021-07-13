import discord
import time
from discord.cogs.ClaimWaifu import ClaimWaifu
from discord.ext import commands
from data.database import databaseSetup
import os 


databaseSetup()
token = os.getenv("DISCORD_BOT_TOKEN")  
if (token is None):
    token = open(f"/run/secrets/DISCORD_BOT_TOKEN").read()
backendURL = os.getenv("BOT_URL")
if (backendURL is None ):
    backendURL = "127.0.0.1:5200"

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '-', intents=intents)
client.remove_command('help')

client.add_cog(ClaimWaifu)

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


@client.command(aliases = ['h'])
async def help(ctx):
    embed = discord.Embed(
        title = 'Help',
        description = 'List of commands for Waifu Bot',
        colour = discord.Colour.green()
    )
    embed.set_thumbnail(url = f'{client.user.avatar_url}')
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
        url = f"http://{backendURL}/inventory/{ctx.message.author.id}",
        colour = discord.Color.blurple()
    )
    await ctx.message.author.send(embed=embed)
    msg = await ctx.send(f"Sent an inventory link to {ctx.message.author.mention}")
    time.sleep(2)
    await msg.delete()


@client.command()
@commands.has_permissions(manage_guild = True)
async def setlb(ctx, channel):
    await ctx.send(f'Set the leaderboard to {channel}')
    channel = getnum(str(channel))
    channel = int(channel)
    channel = client.get_channel(channel)
    embed = discord.Embed(
        title = 'Help',
        description = 'List of commands for Waifu Bot',
        colour = discord.Colour.blue()
    )
    await channel.send("test")

@setlb.error
async def setlb_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**You dont have permission to do that!**")
client.run(token)

