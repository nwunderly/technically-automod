import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

bot = commands.Bot(
    command_prefix="!",
    intents=disnake.Intents(
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
    bot.load_extension("technically_automod.disnake")


bot.run(token)
