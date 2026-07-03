import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents(
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
    await bot.load_extension("technically_automod.discordpy")


bot.run(token)
