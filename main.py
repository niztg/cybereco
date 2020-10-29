from discord.ext import commands
from config import token

EXTENSIONS = ['cog', 'jishaku']

bot = commands.Bot(command_prefix="=")

for ext in EXTENSIONS:
    bot.load_extension(ext)

@bot.event
async def on_ready():
    print("AAA")

bot.run(token)