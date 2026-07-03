import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv()
token = os.getenv("TOKEN")

bot = commands.Bot(
    command_prefix="!",
    intents=nextcord.Intents(
        guilds=True,
        members=True,
        guild_messages=True,
        guild_reactions=True,
        guild_typing=True,
        message_content=True,
    ),
)


@bot.event
async def on_ready():
    bot.load_extension("technically_automod.nextcord")


bot.run(token)
