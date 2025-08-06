import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Roles and channels you want to create
ROLES = ["Boss", "Associate", "Cleaner", "Mafia"]
CHANNELS = {
    "boss-lounge": ["Boss"],
    "associate-hall": ["Associate"],
    "cleaners-den": ["Cleaner"],
    "mafia-hideout": ["Mafia"],
    "general-chat": ["@everyone"]
}

# Check if user has Boss role (allow !help for everyone)
@bot.check
async def is_boss(ctx):
    if ctx.command.name == "help":
        return True
    boss_role = discord.utils.get(ctx.author.roles, name="Boss")
    if boss_role:
        return True
    await ctx.send("🚫 You need the 'Boss' role to use this command.")
    return False

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def associate(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Associate")
    if role:
        await member.add_roles(role)
        await ctx.send(f"✅ {member.mention} is now an Associate.")
    else:
        await ctx.send("❌ Associate role not found.")

@bot.command()
async def unassociate(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Associate")
    if role:
        await member.remove_roles(role)
        await ctx.send(f"❌ {member.mention} is no longer an Associate.")
    else:
        await ctx.send("❌ Associate role not found.")

@bot.command()
async def setup(ctx):
    guild = ctx.guild

    # Create roles if they don't exist
    created_roles = []
    for role_name in ROLES:
        if not discord.utils.get(guild.roles, name=role_name):
            role = await guild.create_role(name=role_name)
            created_roles.append(role.name)

    # Create channels and set permissions
    for channel_name, allowed_roles in CHANNELS.items():
        if not discord.utils.get(guild.channels, name=channel_name):
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False)
            }
            for role_name in allowed_roles:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            await guild.create_text_channel(name=channel_name, overwrites=overwrites)

    await ctx.send("✅ Setup complete. Roles and channels created.")

@bot.command(name="help")
async def custom_help(ctx):
    help_msg = (
        "**📜 Command List:**\n"
        "`!ping` – Check if the bot is online.\n"
        "`!setup` – Creates all roles and channels.\n"
        "`!associate @user` – Give Associate role.\n"
        "`!unassociate @user` – Remove Associate role.\n"
        "`!help` – Show this help message.\n\n"
        "⚠️ All commands (except `!help`) require the **Boss** role."
    )
    await ctx.send(help_msg)

bot.run(os.getenv("DISCORD_TOKEN"))
