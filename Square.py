from Ressources import Ressources
import GameManager
import Player
import pygame
class Square:
  Number_of_suqares = 0
  SIZE = 70
  OuterSIZE = 100
  PADDINGS = (Player.PlayerCircle.SIZE/2)
  MAX_N_P = int((SIZE+2*PADDINGS)/Player.PlayerCircle.SIZE)
  Taxes = 1
  Price = 1
  def __init__(self,pos) -> None:
    self.pos = pos
    self.index = Square.Number_of_suqares
    self.indexImage = Ressources.smallFont.render(str(self.index),True,pygame.Color('black'))
    self.owner:Player.Player = None
    self.orientation = None
    self.PlayersIn = []
    self.Number_of_Players_in_square = 0
    self.containsCriminal = False
    if(self.index == 0):
      self.containsCriminal = True
    if self.index in Ressources.non_bayable_squares:
      self.bayable= False
    else:
      self.bayable = True
    if self.index in Ressources.QuestionSquares:
      self.isQuestionSquare = True
    else:
      self.isQuestionSquare = False
    self.ownerText:pygame.Surface = None
    Square.Number_of_suqares += 1

  def playerIn(self,player:Player.Player):
    self.PlayersIn.append(player)
    self.Number_of_Players_in_square+=1
    if self.owner != None and self.owner != player:
      GameManager.GameManager.Playable = False
      GameManager.GameManager.Animation_ongoing = True
      GameManager.GameManager.Playable_locked = True
      GameManager.GameManager.AnnoucementsQueue.append([GameManager.GameManager.AnnoucementsList[GameManager.Annoucements.LostMoney],self.playerPaidTaxes,player])
      # self.playerPaidTaxes(player)
    if self.isQuestionSquare:
      Player.Criminal.move()
  def playerPaidTaxes(self,player:Player.Player):
      if player.lives > Square.Taxes:
        self.owner.moneyToGetNext = Square.Taxes
        player.lives -= Square.Taxes
        player.update()
      else:
        self.owner.moneyToGetNext = player.lives
        player.lives = 0
        player.deathCause = "Bankruptcy"
        player.update()
      GameManager.GameManager.Playable = False
      GameManager.GameManager.Playable_locked  = True
      GameManager.GameManager.Animation_ongoing = True
      GameManager.GameManager.AnnoucementsQueue.append([GameManager.GameManager.AnnoucementsList[GameManager.Annoucements.GetMoney],self.playerGotPaied,self.owner])
  def playerGotPaied(self,player:Player.Player):
      GameManager.GameManager.Playable_locked  = False
      player.lives += player.moneyToGetNext
      player.update()
  def playerOut(self,player:Player.Player):
    self.PlayersIn.remove(player)
    self.playerOrderUpdate()
  def playerOrderUpdate(self):
    self.Number_of_Players_in_square = 0
    if self.containsCriminal:
      pos = self.getNextPos()
      Player.Criminal.Circle.move(pos)
      self.Number_of_Players_in_square +=1
    for i in range(len(self.PlayersIn)):
      pos = self.getNextPos()
      self.PlayersIn[i].circle.move(pos)
      self.Number_of_Players_in_square +=1
  def playerDied(self,player:Player.Player):
    self.PlayersIn.remove(player)
    self.playerOrderUpdate()
  def CriminalOut(self):
    self.containsCriminal = False
    self.playerOrderUpdate()
  def CriminalIn(self):
    self.Number_of_Players_in_square +=1
    self.containsCriminal = True
    for i in range(len(self.PlayersIn)):
      if self.PlayersIn[i].alive == False:
        continue
      if self.PlayersIn[i].lives >  Player.Criminal.Damage:
        self.PlayersIn[i].lives -= Player.Criminal.Damage
      else:
        self.PlayersIn[i].deathCause = "Criminal"
        self.PlayersIn[i].lives = 0
      self.PlayersIn[i].update()
  def getNextPos(self):
    pos_x = (self.Number_of_Players_in_square%Square.MAX_N_P)*Player.PlayerCircle.SIZE + Square.PADDINGS + self.pos[0]
    pos_y = int(self.Number_of_Players_in_square/Square.MAX_N_P)*Player.PlayerCircle.SIZE + Square.PADDINGS + self.pos[1]

    return (pos_x,pos_y)
    
  def draw(self):
    if not ((not self.bayable) or self.owner == None or self.ownerText == None):
      pygame.draw.rect(Ressources.myScreen,self.owner.color,(self.pos[0],self.pos[1],Square.OuterSIZE,Square.OuterSIZE),4)
      Ressources.myScreen.blit(self.ownerText,(self.pos[0]+Square.OuterSIZE/2-self.ownerText.get_width()/2,self.pos[1]+Square.OuterSIZE-self.ownerText.get_height()/2))  
    Ressources.myScreen.blit(self.indexImage,(self.pos[0]+2,self.pos[1]))
  def canBuy(self):
    if not self.bayable :
      return False
    return True

  def assignTo(self,player:Player.Player):
    self.owner = player
    self.ownerText = Ressources.Font.render(self.owner.name,True,pygame.Color('white'),pygame.Color('black'))
    return True