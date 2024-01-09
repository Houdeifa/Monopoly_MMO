from Ressources import Ressources
import GameManager
import pygame
import random

class PlayerCircle:
  SIZE = 20
  def __init__(self,pos,color,name) -> None:
    self.color = color
    self.name = name
    self.pos = (pos[0] + PlayerCircle.SIZE/2,pos[1] + PlayerCircle.SIZE/2)
    myColor = pygame.Color('white')
    grayScale = (self.color[0]*0.298 + self.color[1]*0.587 + self.color[2]*0.114)
    if(grayScale > 133):
      myColor = pygame.Color('black')
    self.NameImage = Ressources.Font.render(name[0], True, myColor)
    self.NameSize = (self.NameImage.get_width(),self.NameImage.get_height())
    self.lives = 3
    self.livesTextImage  = Ressources.smallFont.render(str(self.lives), True, pygame.Color('white'))
  def update(self):
    self.livesTextImage  = Ressources.smallFont.render(str(self.lives), True, pygame.Color('white'))
  def draw(self):
    pygame.draw.circle(Ressources.myScreen,self.color,self.pos,PlayerCircle.SIZE/2)
    Ressources.myScreen.blit(self.NameImage, (self.pos[0]-self.NameSize[0]/2, self.pos[1]-self.NameSize[1]/2))
    livesCircleR = PlayerCircle.SIZE/4
    livesCirclePos = (self.pos[0]+livesCircleR*2,self.pos[1]-livesCircleR)
    pygame.draw.circle(Ressources.myScreen,pygame.Color('red'),livesCirclePos,livesCircleR)
    Ressources.myScreen.blit(self.livesTextImage, (livesCirclePos[0]-self.livesTextImage.get_width()/2,livesCirclePos[1]-self.livesTextImage.get_height()/2))

  def move(self,pos):
    self.pos = (pos[0] + PlayerCircle.SIZE/2,pos[1] + PlayerCircle.SIZE/2)
class Player:
  NumberOfPlayers = 0
  def __init__(self,name) -> None:
    self.position = 0
    self.name = name
    self.properties = []
    self.lives = 3
    self.moneyToGetNext = 0
    self.alive = True
    self.deathCause = None
    self.tagName = None
    self.ID = Player.NumberOfPlayers
    self.color = Ressources.PlayerColors[self.ID]
    Player.NumberOfPlayers += 1
    pos = GameManager.GameManager.squares[self.position].getNextPos()
    self.circle = PlayerCircle(pos,self.color,self.name)
  def move(self):
    if self.alive == False:
      return
    pos = GameManager.GameManager.squares[self.position].getNextPos()
    self.circle.move(pos)
    Criminal.PlayerMouved()
  def canBuy(self,position):    
    if self.alive == False:
      print(GameManager.GameManager.LanguageDict['Prints'][6][0])
      return False
    
    if self.lives < (GameManager.Square.Taxes + 1):
      print(GameManager.GameManager.LanguageDict['Prints'][7][0])
      return False
    
    if GameManager.GameManager.squares[position].canBuy()  == False:
      print(GameManager.GameManager.LanguageDict['Prints'][8][0])
      return False
    
    if GameManager.GameManager.squares[position] in self.properties:
      print(GameManager.GameManager.LanguageDict['Prints'][9][0])
      return False
    
    return True
  def buySquare(self,position):
    if not self.canBuy(position):
      return False
    self.lives -= GameManager.Square.Price
    if GameManager.GameManager.squares[position].owner != None:
      GameManager.GameManager.squares[position].owner.sellSquare(position)
    GameManager.GameManager.squares[position].assignTo(self)
    self.properties.append(GameManager.GameManager.squares[position])
    self.update()
    print(GameManager.GameManager.LanguageDict['Prints'][10][0] ,self.name, GameManager.GameManager.LanguageDict['Prints'][10][1],position)
    return True
  def sellSquare(self,position):
    if not GameManager.GameManager.squares[position] in self.properties:
      return False
    self.properties.remove(GameManager.GameManager.squares[position])
    self.lives += GameManager.Square.Price
    self.update()
    return True
  def die(self):
      if self.deathCause == "Criminal":
        GameManager.GameManager.Playable_locked = True
        GameManager.GameManager.Playable = False
        GameManager.GameManager.Animation_ongoing = True
        GameManager.GameManager.AnnoucementsQueue.append([GameManager.GameManager.AnnoucementsList[GameManager.Annoucements.Die],self.dead,self])
      if self.deathCause == "Bankruptcy":
        GameManager.GameManager.Playable_locked = True
        GameManager.GameManager.Playable = False
        GameManager.GameManager.Animation_ongoing = True
        GameManager.GameManager.AnnoucementsQueue.append([GameManager.GameManager.AnnoucementsList[GameManager.Annoucements.Broke],self.dead,self])
  def dead(self,player):
      print(GameManager.GameManager.LanguageDict['Prints'][11][0],self.name,GameManager.GameManager.LanguageDict['Prints'][12][0])
      GameManager.GameManager.Playable_locked  = False
      self.lives = 0
      self.alive = False
      self.tagName.update()
      GameManager.GameManager.squares[self.position].playerDied(self)
      if GameManager.GUI.labels[0].selectedPlayer == self:
        GameManager.GUI.labels[0].selectedPlayer = None
      for i in range(len(self.properties)):
        self.properties[i].owner = None
      self.properties.clear()
      if self.deathCause == None:
        return
  def update(self):
    if self.alive == False:
      return
    if self.lives <= 0:
      self.die()
    self.circle.lives = self.lives
    self.circle.update()
    GameManager.GUI.labels[0].update()
  def draw(self):
    if self.alive == False:
      return
    self.circle.draw()

class Criminal:
  Name:str = "Yoonns"
  NumberOf_Player_Mouved:int = 0
  CriminalMouvingAfterAll:bool = False
  Damage:int = 1
  postion:int = 0
  Circle:PlayerCircle = None
  def init():
    Criminal.Circle = PlayerCircle( GameManager.GameManager.squares[0].getNextPos(),pygame.Color('black'),Criminal.Name)
    Criminal.Circle.lives = 0
    Criminal.Circle.update()
    GameManager.GameManager.squares[0].CriminalIn()
  def PlayerMouved():
    if(Criminal.CriminalMouvingAfterAll == False):
      return
    Criminal.NumberOf_Player_Mouved +=1
    if(Criminal.NumberOf_Player_Mouved == len(GameManager.GameManager.player_list)):
      Criminal.move()

  def move():
    value = random.choice(list(range(1,7)))
    position = (Criminal.postion + value) % len(GameManager.GameManager.squares)
    if (position == Criminal.postion):
      return
    
    for animation in GameManager.GameManager.Dice_Animations:
      animation.visible = False
    GameManager.GameManager.Dice_Animations[value-1].play(Criminal.finishMouving)
    GameManager.GameManager.current_Animations.append(GameManager.GameManager.Dice_Animations[value-1])
    
  def finishMouving(value):
    position = (Criminal.postion + value) % len(GameManager.GameManager.squares)
    GameManager.GameManager.squares[Criminal.postion].CriminalOut()
    Criminal.postion = position
    pos = GameManager.GameManager.squares[position].getNextPos()
    Criminal.Circle.move(pos)
    GameManager.GameManager.squares[position].CriminalIn()
    GameManager.GameManager.Playable_locked = False

  def draw():
    Criminal.Circle.draw()
  def MoveTo(position):
    GameManager.GameManager.squares[Criminal.postion].CriminalOut()
    Criminal.postion = position
    pos = GameManager.GameManager.squares[position].getNextPos()
    Criminal.Circle.move(pos)
    GameManager.GameManager.squares[position].CriminalIn()