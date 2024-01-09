import pygame
from Ressources import Ressources
from Player import Player
from Player import Criminal
from Square import Square
from GUI import GUI
from GUI import PlayerList
from Animations import DiceAnimation
from Animations import AnnoucementAnimation
import threading
from DiscordGui import DiscordGui
import os
import sys
import json

from LoadingGui import LoadingGui
class Annoucements:
  Broke = 0
  Die = 1
  GetMoney = 2
  LostMoney = 3
class GameManager:
  squares = []
  player_list = []
  Playable = True
  Playable_locked = False
  Animation_ongoing = False
  Dice_Animations = []
  current_Animations = []
  delta_time = 0
  RessourcesLoadedPercent = 0
  RessourcesLoaded = False
  AnnoucementsDelay = 1000
  AnnoucementsList = []
  AnnoucementsQueue = []
  AnnoucementIsPlaying = False
  PlayerListMap = dict()
  discord_thread = None
  commandQueue_thread = None
  CommandMode = "Discord"
  LanguageDict = dict()
  def RessourcesLoad():
    Ressources.Font = pygame.font.SysFont(None, 24)
    GameManager.RessourcesLoadedPercent = 2
    Ressources.smallFont = pygame.font.SysFont(None, 16)
    GameManager.RessourcesLoadedPercent = 4
    Ressources.bigFont = pygame.font.SysFont(None, 50)
    Ressources.Playing_square_dim = [Ressources.Screen_with*0.8,Ressources.Screen_height]
    Ressources.Playing_square_pos = [0,0]
    Ressources.command_square_dim = [Ressources.Screen_with*0.2,Ressources.Screen_height]
    Ressources.command_square_pos = [Ressources.Playing_square_dim[0],0]

    GameManager.RessourcesLoadedPercent = 10
    Ressources.background_image = pygame.image.load('ressources/bg.png')
    Ressources.background_image = pygame.transform.scale(Ressources.background_image, Ressources.Playing_square_dim)

    with open('config.json', 'r', encoding="utf-8") as fcc_file:
      configdata = json.load(fcc_file)
    
    Criminal.Name = configdata['CriminalName']
    
    with open('ressources/languages/'+configdata['language']+'.json', 'r', encoding="utf-8") as fcc_file:
      GameManager.LanguageDict = json.load(fcc_file)

    GameManager.RessourcesLoadedPercent = 20
    for i in range(6):
      curr_dice_images = dict()
      parent = 'ressources/dice_'+str(i+1)+'/'
      files = os.listdir(parent)
      for file in files:
        curr_dice_images[file] = pygame.image.load(parent+file).convert_alpha()
        curr_dice_images[file] = pygame.transform.scale(curr_dice_images[file], DiceAnimation.SIZE)
      GameManager.RessourcesLoadedPercent = int(20 + (40-20)*i/6)
      Ressources.dice_images.append(curr_dice_images)

    GameManager.RessourcesLoadedPercent = 40
      
    
    parent = 'ressources/broke/'
    broke_images = []
    for file in os.listdir(parent):
      image = pygame.image.load(parent+file).convert_alpha()
      image = pygame.transform.scale(image, AnnoucementAnimation.IMAGE_SIZE)
      broke_images.append(image)
    Ressources.anouncement_images.append(broke_images)

    GameManager.RessourcesLoadedPercent = 50
    parent = 'ressources/dead/'
    dead_images = []
    for file in os.listdir(parent):
      image = pygame.image.load(parent+file).convert_alpha()
      image = pygame.transform.scale(image, AnnoucementAnimation.IMAGE_SIZE)
      dead_images.append(image)
    Ressources.anouncement_images.append(dead_images)

    GameManager.RessourcesLoadedPercent = 60
    parent = 'ressources/gets_money/'
    gets_money_images = []
    for file in os.listdir(parent):
      image = pygame.image.load(parent+file).convert_alpha()
      image = pygame.transform.scale(image, AnnoucementAnimation.IMAGE_SIZE)
      gets_money_images.append(image)
    Ressources.anouncement_images.append(gets_money_images)

    GameManager.RessourcesLoadedPercent = 80
    parent = 'ressources/lost_money/'
    lost_money_images = []
    for file in os.listdir(parent):
      image = pygame.image.load(parent+file).convert_alpha()
      image = pygame.transform.scale(image, AnnoucementAnimation.IMAGE_SIZE)
      lost_money_images.append(image)
    Ressources.anouncement_images.append(lost_money_images)
    GameManager.RessourcesLoadedPercent = 100
    LoadingGui.finished()

  def init(screen,discord_thread,commandQueue_thread):
    GameManager.discord_thread = discord_thread
    GameManager.commandQueue_thread = commandQueue_thread
    Ressources.myScreen = screen
    tr1 = threading.Thread(target=GameManager.RessourcesLoad,name="RessourcesLoad")
    LoadingGui.init()
    tr1.start()
    # tr1.join()
  def loadedInit():
    GameManager.discord_thread.start()
    GameManager.commandQueue_thread.start()
    GUI.init(Ressources.command_square_pos,Ressources.command_square_dim)
    DiscordGui.init(Ressources.command_square_pos,Ressources.command_square_dim)

    for i in range(len(Ressources.Squares_positions)):
      GameManager.squares.append(Square(Ressources.Squares_positions[i]))
    
    Criminal.init()

  def draw():
    if GameManager.RessourcesLoaded == False :
      LoadingGui.draw()
      return
    #background colors
    rect = (Ressources.command_square_pos[0],Ressources.command_square_pos[1],Ressources.command_square_dim[0],Ressources.command_square_dim[1])
    pygame.draw.rect(Ressources.myScreen,(20, 62, 92),rect)
    rect = (Ressources.Playing_square_pos[0],Ressources.Playing_square_pos[1],Ressources.Playing_square_dim[0],Ressources.Playing_square_dim[1])
    pygame.draw.rect(Ressources.myScreen,(255,255,255),rect)
    
    # background image
    Ressources.myScreen.blit(Ressources.background_image,rect)
    

    for i in range(len(GameManager.player_list)):
      GameManager.player_list[i].draw()

    for i in range(len(GameManager.squares)):
      GameManager.squares[i].draw()
    
    Criminal.draw()

    if GameManager.CommandMode == "GUI":
      GUI.draw()
    else:
      DiscordGui.draw()
    


  def handle_event(event):
    if GameManager.RessourcesLoaded == False:
      LoadingGui.handle_event(event)
      return
    if GameManager.Playable == False:
      return
    if GameManager.CommandMode == "Discord":
      DiscordGui.handle_event(event)
    else:
      GUI.handle_event(event)

  def update():
    if GameManager.RessourcesLoaded == False:
      LoadingGui.update()
      return
    
    #AnnoucementsQueue Managing
    if (len( GameManager.AnnoucementsQueue) != 0 and GameManager.AnnoucementIsPlaying == False):
      Annoucement  = GameManager.AnnoucementsQueue.pop()
      Annoucement[0].play(Annoucement[2],Annoucement[1])
    if  GameManager.CommandMode == "GUI":
      GUI.update()
    else:
      DiscordGui.update()

  def playerSpawn(name):
    exists = False
    for i in range(len(GameManager.player_list)):
      if GameManager.player_list[i].name == name:
        exists = True
        break
    if exists:
      print(GameManager.LanguageDict['Prints'][4][0])
      return False
    GameManager.player_list.append(Player(name))
    GUI.labels[0].addPlayer(GameManager.player_list[-1])
    GameManager.player_list[-1].tagName = PlayerList.TagList[-1]
    GameManager.squares[0].playerIn(GameManager.player_list[-1])
    GameManager.PlayerListMap[name] = GameManager.player_list[-1]
    return True
  def SwitchMode():
    if GameManager.CommandMode == "Discord":
      GameManager.CommandMode = "GUI"
    else:
      GameManager.CommandMode = "Discord"