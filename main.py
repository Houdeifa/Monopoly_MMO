from pygame_api import runPyGame
import threading
import Discrod_api
import CommandsQueue

f = open("auth/tokens.txt", "r")
lines = f.readlines()
API_TOKEN = lines[0]
discord_thread = threading.Thread(target=Discrod_api.run,args=(API_TOKEN,) )
CommandsQueueThread = threading.Thread(target=CommandsQueue.CommandsQueue.run)
main_thread = threading.Thread(target=runPyGame,args=(discord_thread,CommandsQueueThread,))
main_thread.run()
