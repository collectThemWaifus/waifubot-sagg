from discord import Embed
from discord import Colour
from discord.ext import commands
from discord import Status
from discord import Game


class bot(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))
        await self.bot.change_presence(
            status=Status.online,
            activity=Game("Use -help for a list of commands"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = '**Command on Cooldown**, please try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)

    @commands.command(aliases=['h'])
    async def help(self, ctx):
        embed = Embed(
            title='Help',
            description='List of commands for Waifu Bot',
            colour=Colour.green()
        )
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
        embed.add_field(
            name='waifu (wa)', value='Displays a random waifu, react to claim.', inline=False)
        embed.add_field(name='inventory (inv)',
                        value='Sends you a link to a website containing your inventory', inline=False)
        embed.add_field(name='help (h)',
                        value='Displays this message!', inline=False)
        embed.add_field(
            name='setlb [channel]', value='Set a specific channel to display the leaderboard', inline=False)
        embed.set_footer(text="This bot is still in development!")
        await ctx.send(embed=embed)
