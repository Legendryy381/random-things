import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

BOSS_ROLE_NAME = "Boss"

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

def is_boss():
    async def predicate(ctx):
        role = discord.utils.get(ctx.author.roles, name=BOSS_ROLE_NAME)
        if role:
            return True
        await ctx.send("🚫 You don't have permission to use this command.")
        return False
    return commands.check(predicate)

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def help(ctx):
    help_msg = """
**📜 Command List:**
- `!setup` → Create channels, roles, and assign you as Boss
- `!ping` → Check if the bot is online
- `!customer @user` → Assign Customer role
- `!crew @user` → Assign Crew (Employee) role
- `!rhm @user` → Assign Right Hand Man role
- `!associate @user` → Assign Associate role
- `!boss @user` → Assign Boss role (admin use only)
"""
    await ctx.send(help_msg)

@bot.command()
@is_boss()
async def setup(ctx):
    guild = ctx.guild
    roles = ["Customer", "Crew", "Right Hand Man", "Associate", "Boss"]

    # Create roles if they don't exist
    created_roles = {}
    for role_name in roles:
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            role = await guild.create_role(name=role_name)
        created_roles[role_name] = role

    # Assign Boss role to the person who ran the command
    await ctx.author.add_roles(created_roles["Boss"])

    # Create channels with permissions
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        created_roles["Boss"]: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        created_roles["Crew"]: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        created_roles["Right Hand Man"]: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }

    category = await guild.create_category("🧼 Cleaners HQ", overwrites=None)
    await guild.create_text_channel("🗣️ general", category=category, overwrites=overwrites)
    await guild.create_text_channel("💼 tasks", category=category, overwrites=overwrites)
    await guild.create_text_channel("📦 storage", category=category, overwrites=overwrites)

    await ctx.send("✅ Setup complete. Channels and roles created!")

# Role assign commands
async def assign_role(ctx, member: discord.Member, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f"✅ {member.mention} is now a **{role_name}**.")
    else:
        await ctx.send(f"❌ Role '{role_name}' not found.")

@bot.command()
@is_boss()
async def customer(ctx, member: discord.Member):
    await assign_role(ctx, member, "Customer")

@bot.command()
@is_boss()
async def crew(ctx, member: discord.Member):
    await assign_role(ctx, member, "Crew")

@bot.command()
@is_boss()
async def rhm(ctx, member: discord.Member):
    await assign_role(ctx, member, "Right Hand Man")

@bot.command()
@is_boss()
async def associate(ctx, member: discord.Member):
    await assign_role(ctx, member, "Associate")

@bot.command()
@is_boss()
async def boss(ctx, member: discord.Member):
    await assign_role(ctx, member, "Boss")

# Run the bot
bot.run(os.getenv("DISCORD_TOKEN"))- `!ping` – Check if the bot is online.

ℹ️ *Everyone can use this command*:
- `!help` – Show this help message.
    """
    await ctx.send(help_text)

@bot.command()
@is_boss()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
@is_boss()
async def setup(ctx):
    guild = ctx.guild

    # Create roles
    role_names = ["Boss", "Right Hand Man", "Crew", "Customer", "Associate"]
    roles = {}
    for name in role_names:
        role = discord.utils.get(guild.roles, name=name)
        if not role:
            role = await guild.create_role(name=name)
        roles[name] = role

    # Give you the Boss role
    member = guild.get_member(BOSS_ID)
    if member:
        await member.add_roles(roles["Boss"])
        await ctx.send("👑 You’ve been given the Boss role.")

    # Create category and channels
    category_name = "🧼 The Cleaners"
    existing_category = discord.utils.get(guild.categories, name=category_name)
    if not existing_category:
        category = await guild.create_category(category_name)
        await guild.create_text_channel("📢-announcements", category=category)
        await guild.create_text_channel("💼-business", category=category)
        await guild.create_voice_channel("🔊-meetings", category=category)
        await ctx.send("✅ Setup complete with channels and roles.")
    else:
        await ctx.send("⚠️ Setup already seems to be done.")

# Role assignment commands
@bot.command()
@is_boss()
async def boss(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Boss")
    await member.add_roles(role)
    await ctx.send(f"👑 {member.mention} is now a Boss.")

@bot.command()
@is_boss()
async def rhm(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Right Hand Man")
    await member.add_roles(role)
    await ctx.send(f"🤝 {member.mention} is now a Right Hand Man.")

@bot.command()
@is_boss()
async def crew(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Crew")
    await member.add_roles(role)
    await ctx.send(f"🧍 {member.mention} is now part of the Crew.")

@bot.command()
@is_boss()
async def customer(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Customer")
    await member.add_roles(role)
    await ctx.send(f"💼 {member.mention} is now a Customer.")

@bot.command()
@is_boss()
async def associate(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Associate")
    await member.add_roles(role)
    await ctx.send(f"🧾 {member.mention} is now an Associate.")

# Run the bot using the token from the environment
bot.run(os.getenv("DISCORD_TOKEN"))
