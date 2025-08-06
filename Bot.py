import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

import os
bot.run(os.getenv("DISCORD_TOKEN"))
