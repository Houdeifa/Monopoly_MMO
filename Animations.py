import GameManager
from Ressources import Ressources
import pygame
class DiceAnimation:
  SIZE = (70,70)
  speed = 0.03
  def __init__(self,number,pos) -> None:
    self.rel_pos = pos
    self.number = number
    self.index = 0
    self.maxIndex = (len(Ressources.dice_images[number-1])-1)
    self.visible = False
    self.pos = (Ressources.command_square_pos[0]+self.rel_pos[0],Ressources.command_square_pos[1]+self.rel_pos[1])
    self.playing = False
    self.end_ballback = None

  def handle_event(self,event):
    pass

  def update(self):
    if self.playing:
      self.animate()

  def animate(self):
    self.index += DiceAnimation.speed*GameManager.GameManager.delta_time
    if (int(self.index) > self.maxIndex) and self.playing:
      callback = self.end_ballback
      if self in GameManager.GameManager.current_Animations:
        GameManager.GameManager.current_Animations.remove(self)
      self.stop()
      if callback != None:
        callback(self.number)

  def stop(self):
    if (len(GameManager.GameManager.current_Animations) == 0 and len(GameManager.GameManager.AnnoucementsQueue) == 0):
      GameManager.GameManager.Playable = True
      GameManager.GameManager.Animation_ongoing = False
    self.playing = False
    self.end_ballback = None
    self.index = self.maxIndex
  def play(self,callback):
    self.playing = True
    self.visible = True
    self.index = 0
    self.end_ballback = callback
    GameManager.GameManager.Animation_ongoing = True
    GameManager.GameManager.Playable_locked = True
    GameManager.GameManager.Playable = False

  def draw(self):
    if self.visible == False:
      return
    Ressources.myScreen.blit(Ressources.dice_images[self.number-1][str(int(self.index))+'.png'],self.pos)


class AnnoucementAnimation:
  IMAGE_SIZE = (100,100)
  speed = 0.03
  Spacing = 10
  def __init__(self,praentpos,parentSize,text,images,Delay) -> None:
    self.text = text
    self.textImage = None
    self.praentpos = praentpos
    self.parentSize = parentSize
    self.size = (0,0)
    self.pos = (0,0)
    self.images = images
    self.Delay = Delay
    self.index = 0
    self.visible = False
    self.playing = False
    self.end_ballback = None
    self.time = 0
    self.player:GameManager.Player = None
    self.maxIndex = (len(self.images)-1)
    self.rect = None
    
  def handle_event(self,event):
    pass
  def setPlayer(self,player):
    self.player = player
    if self.text == "broke":
      messageList = GameManager.GameManager.LanguageDict['Annoucements'][0]
      message = messageList[0] + self.player.name + messageList[1]
      self.textImage = Ressources.bigFont.render(message,True,pygame.Color('black'))
    elif self.text == "die":
      messageList = GameManager.GameManager.LanguageDict['Annoucements'][1]
      message = messageList[0] + self.player.name + messageList[1]
      self.textImage = Ressources.bigFont.render(message,True,pygame.Color('black'))
    elif self.text == "got":
      messageList = GameManager.GameManager.LanguageDict['Annoucements'][2]
      message = messageList[0] + self.player.name + messageList[1]
      self.textImage = Ressources.bigFont.render(message,True,pygame.Color('black'))
    elif self.text == "lost":
      messageList = GameManager.GameManager.LanguageDict['Annoucements'][3]
      message = messageList[0] + self.player.name + messageList[1]
      self.textImage = Ressources.bigFont.render(message,True,pygame.Color('black'))
    width = self.textImage.get_width() + AnnoucementAnimation.Spacing + AnnoucementAnimation.IMAGE_SIZE[0]
    height = max(self.textImage.get_height(),AnnoucementAnimation.IMAGE_SIZE[0])
    self.size = (width,height)
    self.pos = (self.praentpos[0]+(self.parentSize[0]/2)-(self.size[0]/2),self.praentpos[1]+(self.parentSize[1]/2)-(self.size[1]/2))
    self.textPos = (self.pos[0],self.pos[1]+(self.size[1]/2)-(self.textImage.get_height()/2))
    self.imagePos = (self.pos[0]+self.textImage.get_width()+AnnoucementAnimation.Spacing,self.pos[1]+(self.size[1]/2)-(AnnoucementAnimation.IMAGE_SIZE[1]/2))
    self.rect = (self.pos[0],self.pos[1],self.size[0],self.size[1])
  def update(self):
    if self.player == None:
      return
    if self.playing:
      self.animate()
  def animate(self):
    if self.player == None:
      return
    self.index += AnnoucementAnimation.speed*GameManager.GameManager.delta_time
    self.time += GameManager.GameManager.delta_time
    if int(self.index) > self.maxIndex:
      self.index = 0
    if self.time >= self.Delay:
      callback = self.end_ballback
      player = self.player
      self.stop()
      if callback != None:
        callback(player)

  def stop(self):
    self.playing = False
    self.visible = False
    self.index = 0
    self.player = None
    self.end_ballback = None
    self.time = 0
    if (len(GameManager.GameManager.current_Animations) == 0 and len(GameManager.GameManager.AnnoucementsQueue) == 0):
      GameManager.GameManager.Playable = True
      GameManager.GameManager.Animation_ongoing = False
    GameManager.GameManager.AnnoucementIsPlaying = False

  def play(self,player,callback):
    GameManager.GameManager.AnnoucementIsPlaying = True
    self.playing = True
    self.visible = True
    self.index = 0
    self.time = 0
    self.setPlayer(player)
    self.end_ballback = callback

  def draw(self):
    if self.visible == False or self.player == None or self.rect == None:
      return
    pygame.draw.rect(Ressources.myScreen,pygame.Color('white'),self.rect)
    Ressources.myScreen.blit(self.textImage,self.textPos)
    Ressources.myScreen.blit(self.images[int(self.index)],self.imagePos)