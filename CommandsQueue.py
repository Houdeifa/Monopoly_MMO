import sys
import GameManager
import GUI
import asyncio
import discord
class CommandsQueue:
  Queue = []
  Running = True
  bot = None
  def run():
    while CommandsQueue.Running:
      if GameManager.GameManager.Playable == False:
        continue
      if len(CommandsQueue.Queue) > 0:
        cmd = CommandsQueue.Queue.pop()
        if cmd[0] == "Spawn":
          CommandsQueue.Spawn(cmd[1],cmd[2])
        elif cmd[0] == "Move":
          CommandsQueue.Move(cmd[1],cmd[2])
        elif cmd[0] == "BuyHere":
          CommandsQueue.BuyHere(cmd[1],cmd[2])
        elif cmd[0] == "BuyMinus1":
          CommandsQueue.BuyMinus1(cmd[1],cmd[2])
        elif cmd[0] == "BuyPlus1":
          CommandsQueue.BuyPlus1(cmd[1],cmd[2])
  def Spawn(playerName,ctx):
    if not GameManager.GameManager.playerSpawn(playerName):
        asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(GameManager.GameManager.LanguageDict['DiscordAPI'][1][0] + playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][1][0],ctx.channel),CommandsQueue.bot.loop)
        return
    asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(GameManager.GameManager.LanguageDict['DiscordAPI'][2][0] + playerName +GameManager.GameManager.LanguageDict['DiscordAPI'][2][1],ctx.channel),CommandsQueue.bot.loop)
    GUI.GUI.labels[0].selectedPlayer = GameManager.GameManager.PlayerListMap[playerName]
    for player in GameManager.GameManager.player_list:
        player.tagName.UnSelect()
    GameManager.GameManager.PlayerListMap[playerName].tagName.Select()
    GUI.GUI.RollDise()
  def Move(playerName,ctx):
    if not playerName in GameManager.GameManager.PlayerListMap:
      msg = GameManager.GameManager.LanguageDict['DiscordAPI'][0][0] + playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][0][1]
      asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
      return
    GUI.GUI.labels[0].selectedPlayer = GameManager.GameManager.PlayerListMap[playerName]
    for player in GameManager.GameManager.player_list:
      player.tagName.UnSelect()
    GameManager.GameManager.PlayerListMap[playerName].tagName.Select()
    GUI.GUI.RollDise()
    msg = GameManager.GameManager.LanguageDict['DiscordAPI'][3][0] + playerName +GameManager.GameManager.LanguageDict['DiscordAPI'][3][1]
    asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
  def BuyHere(playerName,ctx):
    if not playerName in GameManager.GameManager.PlayerListMap:
      msg = GameManager.GameManager.LanguageDict['DiscordAPI'][4][0] + playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][4][1]
      asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
      return
    GUI.GUI.labels[0].selectedPlayer = GameManager.GameManager.PlayerListMap[playerName]
    for player in GameManager.GameManager.player_list:
        player.tagName.UnSelect()
    GameManager.GameManager.PlayerListMap[playerName].tagName.Select()
    if not GUI.GUI.BuyHere():
      msg = playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][5][0]
      asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
      return
    msg =  GameManager.GameManager.LanguageDict['DiscordAPI'][6][0] + playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][6][1]
    asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
  def BuyMinus1(playerName,ctx):
    if not playerName in GameManager.GameManager.PlayerListMap:
      msg = GameManager.GameManager.LanguageDict['DiscordAPI'][7][0] + playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][7][1]
      asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
      return
    msg = GameManager.GameManager.LanguageDict['DiscordAPI'][8][0] + playerName +GameManager.GameManager.LanguageDict['DiscordAPI'][8][1]
    asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
    GUI.GUI.labels[0].selectedPlayer = GameManager.GameManager.PlayerListMap[playerName]
    for player in GameManager.GameManager.player_list:
        player.tagName.UnSelect()
    GameManager.GameManager.PlayerListMap[playerName].tagName.Select()
    if not GUI.GUI.BuyPlus1():
      msg = playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][9][0]
      asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
  def BuyPlus1(playerName,ctx):
    if not playerName in GameManager.GameManager.PlayerListMap:
      msg = GameManager.GameManager.LanguageDict['DiscordAPI'][10][0] + playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][10][1]
      asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
      return
    GUI.GUI.labels[0].selectedPlayer = GameManager.GameManager.PlayerListMap[playerName]
    for player in GameManager.GameManager.player_list:
        player.tagName.UnSelect()
    GameManager.GameManager.PlayerListMap[playerName].tagName.Select()
    if not GUI.GUI.BuyMinus1():
      msg = playerName + GameManager.GameManager.LanguageDict['DiscordAPI'][11][0]
      asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)
      return
    msg = GameManager.GameManager.LanguageDict['DiscordAPI'][12][0] + playerName +GameManager.GameManager.LanguageDict['DiscordAPI'][12][1]
    asyncio.run_coroutine_threadsafe(CommandsQueue.send_message(msg,ctx.channel),CommandsQueue.bot.loop)

  async def send_message(message,channel):
    await channel.send(message)