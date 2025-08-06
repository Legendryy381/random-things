import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run("MTQwMjQwMzcxOTY2ODMwNTkyMA.GxiF8g.axDj8klmlA5wI6fmd3nvg0Md8HivTPWan8YXV0")
