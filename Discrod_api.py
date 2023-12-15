import discord
from discord.ext import commands
import signal
import sys
import GameManager
# Intents setup
intents = discord.Intents.default()
intents.messages = True  # Enable the message intent
intents.guilds = True    # Enable the guilds intent
intents.reactions = True  # Enable the reactions intent
intents.message_content = True  # Enable the message content intent

#2147483648
# Set up the bot with a command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)
def exit_handler():
    sys.exit()
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_guild_join(guild):
    print(f'Bot joined server: {guild.name} (ID: {guild.id})')
    print(f'Channels in the server:')
    for channel in guild.channels:
        print(f'- {channel.name} (ID: {channel.id}, Type: {channel.type})')
    print('------')

@bot.command(name='hello', help='Responds with Hello!')
async def hello(ctx):
    await ctx.send('Hello!')

    
@bot.command(name='spawn', help='spawn new player')
async def swpan(ctx):
    await ctx.send('The player has been spawned')
    GameManager.GameManager.playerSpawn('New')

@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error in event {event}: {sys.exc_info()}')

def run(API_TOKEN):
  # Add more commands as needed
  # target function of the thread class
  try:
    bot.run(API_TOKEN)
  finally:
    print('ended')