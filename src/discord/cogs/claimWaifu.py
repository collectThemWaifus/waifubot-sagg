import random

from discord.ext import commands
from discord import Embed
from discord import Colour

from data.collection import GetCasteWaifu
from data.database import storeWaifu, checkWaifuDuplicate


class claimWaifu(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.unclaimedWaifus = {}

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if (user.bot):
            return
        global unclaimedWaifus
        messageWaifu = self.unclaimedWaifus.get(str(reaction.message.id))

        if str(reaction.emoji) == '👍' and reaction.count == 2 and reaction.message.edited_at is None:
            embed2 = Embed(
                title='Claimed',
                description=f'Claimed by {user.name}',
                colour=Colour.red()
            )
            embed2.set_image(url=messageWaifu.imageURL)
            embed2.add_field(
                name='Name', value=f'{messageWaifu.name}', inline=False)
            embed2.add_field(
                name='Rank', value=f'{reaction.message.embeds[0].fields[1].value}', inline=False)
            await reaction.message.edit(embed=embed2)
            storeWaifu(messageWaifu, user.id)

    @commands.command(aliases=['wa'])
    @commands.cooldown(10, 3600, commands.BucketType.user)
    async def waifu(self, ctx: commands.Context):
        if ctx.message.guild is None:
            return
        randomNum = random.randint(1, 100)
        if randomNum == 1:
            rank = 'SSS'
        elif randomNum <= 3:
            rank = 'SS'
        elif randomNum <= 8:
            rank = 'S'
        elif randomNum <= 14:
            rank = 'A'
        elif randomNum <= 22:
            rank = 'B'
        elif randomNum <= 31:
            rank = 'C'
        else:
            rank = 'D'

        while True:
            randomWaifu = GetCasteWaifu(rank)
            if not(checkWaifuDuplicate(randomWaifu.name)):
                break
        embed = Embed(
            title='Unclaimed',
            description='Unclaimed',
            colour=Colour.blue()
        )
        embed.set_image(url=randomWaifu.imageURL)
        embed.add_field(name='Name', value=f'{randomWaifu.name}', inline=False)
        embed.add_field(name='Rank', value=f'{rank}', inline=False)
        msg = await ctx.send(embed=embed)
        self.unclaimedWaifus[str(msg.id)] = randomWaifu

        # await ctx.send("React with 👍 within **4** seconds to claim!")
        await msg.add_reaction('👍')
