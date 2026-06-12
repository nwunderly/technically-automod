import disnake
from disnake.ext import commands

from .automod import Automod


class DisnakeAutomodCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.automod = Automod(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.automod.check_message(message)


def setup(bot):
    bot.add_cog(DisnakeAutomodCog(bot))
