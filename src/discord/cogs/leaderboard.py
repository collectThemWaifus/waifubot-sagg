import discord
from discord.ext import commands
from discord import client

from data.database import getAllUsers
# from discord import Embed
# from discord import Colour


class leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def getnum(str):
        ret = ''
        for i in range(len(str)):
            if str[i].isdigit():
                ret += str[i]
        return(ret)

    @commands.command(aliases = ['lb'])
    async def leaderboard(self, ctx):
        loading = discord.Embed(title = f"Loading waifu leaderboard for {ctx.message.guild.id}", colour = discord.Colour.blue())
        await ctx.send(embed = loading)
        users = getAllUsers(ctx.message.guild.id)
        for i in users:
            print(i)
        # embed = Embed(
        #     title='Help',
        #     description='List of commands for Waifu Bot',
        #     colour=Colour.blue()
        # )
