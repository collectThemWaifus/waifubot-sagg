from discord.ext import commands
from discord import client
from discord import Embed
from discord import Colour

class leaderboard( commands.Cog ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def getnum(str):
        ret = ''
        for i in range(len(str)):
            if str[i].isdigit():
                ret += str[i]
        return(ret)

    
    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def setlb(self, ctx, channel):
        await ctx.send(f'Set the leaderboard to {channel}')
        channel = self.getnum(str(channel))
        channel = int(channel)
        channel = client.get_channel(channel)
        embed = Embed(
            title = 'Help',
            description = 'List of commands for Waifu Bot',
            colour = Colour.blue()
        )
        await channel.send("test")

    @setlb.error
    async def setlb_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("**You dont have permission to do that!**")


