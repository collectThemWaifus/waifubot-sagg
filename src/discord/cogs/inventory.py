import time

from discord.ext import commands
from discord import client
from discord import Embed
from discord import Colour

class inventory( commands.Cog ):
    def __init__(self, bot: client) -> None:
        self.bot = bot

    @client.command(aliases = ['inv'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def inv(self, ctx):
        backendURL = self.bot.config["backendURL"]
        embed = Embed(
            title = 'Click this link to view your inventory',
            url = f"http://{ backendURL }/inventory/{ctx.message.author.id}",
            colour = Colour.blurple()
        )
        await ctx.message.author.send(embed=embed)
        msg = await ctx.send(f"Sent an inventory link to {ctx.message.author.mention}")
        time.sleep(2)
        await msg.delete()