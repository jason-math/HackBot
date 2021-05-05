import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
    
for file in os.listdir('./cogs'):
    if file.endswith('.py') and file != "__init__.py":
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)