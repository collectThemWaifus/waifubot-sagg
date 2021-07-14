from typing import Collection
from discord import Embed
from discord import Colour
from discord.ext import commands
from discord import client
from discord import Status
from discord import Game
class bot( commands.Cog ):
    def __init__(self, bot: client) -> None:
        self.bot = bot

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
        await client.change_presence(status=Status.online, activity=Game("Use -help for a list of commands"))

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
        embed = Embed(
            title = 'Help',
            description = 'List of commands for Waifu Bot',
            colour = Colour.green()
        )
        embed.set_thumbnail(url = f'{client.user.avatar_url}')
        embed.add_field(name = 'waifu (wa)', value = 'Displays a random waifu, react to claim.', inline = False)
        embed.add_field(name = 'inventory (inv)', value = 'Sends you a link to a website containing your inventory', inline = False)
        embed.add_field(name = 'help (h)', value = 'Displays this message!', inline = False)
        embed.add_field(name = 'setlb [channel]', value = 'Set a specific channel to display the leaderboard', inline = False)
        embed.set_footer(text="This bot is still in development!")
        await ctx.send(embed=embed)
