import os
import discord
from discord.ext import commands
from discord.ext.commands import has_role, CheckFailure

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

BOSS_ID = 447426989280722946  # Your ID

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Restriction to Boss role only
def is_boss():
    async def predicate(ctx):
        boss_role = discord.utils.get(ctx.guild.roles, name="Boss")
        if boss_role in ctx.author.roles:
            return True
        await ctx.send("❌ Only the Boss can use this command.")
        return False
    return commands.check(predicate)

@bot.command()
async def help(ctx):
    help_text = """
**🛠️ Available Commands**

🔒 *Boss-only commands*:
- `!setup` – Sets up roles and channels, and gives you the Boss role.
- `!boss @user` – Gives someone the Boss role.
- `!rhm @user` – Gives someone the Right Hand Man role.
- `!crew @user` – Gives someone the Crew role.
- `!customer @user` – Gives someone the Customer role.
- `!associate @user` – Gives someone the Associate role.
- `!ping` – Check if the bot is online.

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
