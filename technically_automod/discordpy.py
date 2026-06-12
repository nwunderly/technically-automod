import discord
from discord.ext import commands

from .automod import Automod


class DiscordpyAutomodCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.automod = Automod(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.automod.check_message(message)


async def setup(bot):
    await bot.add_cog(DiscordpyAutomodCog(bot))
