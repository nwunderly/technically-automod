import nextcord
from nextcord.ext import commands

from .automod import Automod


class NextcordAutomodCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.automod = Automod(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.automod.check_message(message)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await self.automod.check_profile(after)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        for guild_id in self.automod.config_guilds:
            guild = self.bot.get_guild(guild_id)
            if not guild:
                return

            member = self.bot.get_member(member_id)
            if not member:
                return

            await self.automod.check_profile(member)


def setup(bot):
    bot.add_cog(NextcordAutomodCog(bot))
