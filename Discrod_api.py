import discord
from discord.ext import commands
import sys
import CommandsQueue
import asyncio
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
CommandsQueue.CommandsQueue.bot = bot
errors = ["The Discord commands are deactivated"]
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
  await ctx.send('Hello ' + str(ctx.author) + '!')

    
@bot.command(name='spawn', help='spawn new player')
async def spawn(ctx):
  if GameManager.GameManager.CommandMode != "Discord":
    await ctx.send(errors[0])
    return
  CommandsQueue.CommandsQueue.Queue.append(["Spawn",str(ctx.author),ctx])

@bot.command(name='move', help='spawn new player')
async def move(ctx):
  if GameManager.GameManager.CommandMode != "Discord":
    await ctx.send(errors[0])
    return
  CommandsQueue.CommandsQueue.Queue.append(["Move",str(ctx.author),ctx])

    
@bot.command(name='buy', help='buy the current square')
async def buyHere(ctx):
  if GameManager.GameManager.CommandMode != "Discord":
    await ctx.send(errors[0])
    return
  CommandsQueue.CommandsQueue.Queue.append(["BuyHere",str(ctx.author),ctx])

@bot.command(name='buy+1', help='buy the next square')
async def buyMinus1(ctx):
  if GameManager.GameManager.CommandMode != "Discord":
    await ctx.send(errors[0])
    return
  CommandsQueue.CommandsQueue.Queue.append(["BuyMinus1",str(ctx.author),ctx])

@bot.command(name='buy-1', help='buy the previous square')
async def buyPlus1(ctx):
  if GameManager.GameManager.CommandMode != "Discord":
    await ctx.send(errors[0])
    return
  CommandsQueue.CommandsQueue.Queue.append(["BuyPlus1",str(ctx.author),ctx])

@bot.event
async def on_error(event, *args, **kwargs):
  print(f'Error in event {event}: {sys.exc_info()}')

def run(API_TOKEN):
  # Add more commands as needed
  # target function of the thread class
  try:
    bot.run(API_TOKEN)
  finally:
    CommandsQueue.CommandsQueue.Running = False
    print('Program ended')

def quit():
  asyncio.run_coroutine_threadsafe(bot.close(),bot.loop)