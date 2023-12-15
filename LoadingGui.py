from Ressources import Ressources
import GameManager
import pygame
class LoadingGui:
  Font = None
  TextImage = None
  FinishedCallback = None
  def init():
    LoadingGui.Font = pygame.font.SysFont(None, 24)
    LoadingGui.TextImage = LoadingGui.Font.render(str(GameManager.GameManager.RessourcesLoadedPercent)+ "%",True,pygame.Color('white'),pygame.Color('black'))
    LoadingGui.FinishedCallback = GameManager.GameManager.loadedInit
  def draw(): 
     Ressources.myScreen.blit(LoadingGui.TextImage,(Ressources.myScreen.get_width()/2 - LoadingGui.TextImage.get_width()/2,Ressources.myScreen.get_height()/2 - LoadingGui.TextImage.get_height()/2))
  
  def finished():
    if LoadingGui.FinishedCallback != None:
      LoadingGui.FinishedCallback()
    GameManager.GameManager.RessourcesLoaded = True
  def update():
    LoadingGui.TextImage = LoadingGui.Font.render(str(GameManager.GameManager.RessourcesLoadedPercent)+ "%",True,pygame.Color('white'),pygame.Color('black'))
    
  def handle_event(event):
    pass