import pygame
import pyperclip
import Animations
from Ressources import Ressources
import Player
import GameManager
import random
import Square

class Button:
  Size = (60,20)
  fontSize = 16
  def __init__(self,text,rel_pos,callback) -> None:
    self.Size = Button.Size
    self.text = text
    self.pos = (rel_pos[0]+GUI.position[0], rel_pos[1] + GUI.position[1])
    self.textImage =Ressources.Font.render(text, True, Ressources.Font_color)
    self.textSize = (self.textImage.get_width(),self.textImage.get_height())
    self.rect = pygame.Rect(self.pos[0],self.pos[1],self.Size[0],self.Size[1])
    self.callback = callback
  def getSize(text):
    textImage = Ressources.Font.render(text, True, Ressources.Font_color)
    textSize = (textImage.get_width(),max(textImage.get_height(),Button.Size[1]))
    return textSize
  def updateSize(self):
    self.Size = Button.getSize(self.text)
    self.rect = pygame.Rect(self.pos[0],self.pos[1],self.Size[0],self.Size[1])
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # If the user clicked on the input_box rect.
        if self.rect.collidepoint(event.pos):
          if not self.callback == None:
            self.callback()
  def update(self):
     pass
  def draw(self):
    pygame.draw.rect(Ressources.myScreen,(255, 255, 255),(self.pos[0],self.pos[1],self.Size[0],self.Size[1]))
    Ressources.myScreen.blit(self.textImage, (self.pos[0]+self.Size[0]/2-self.textSize[0]/2, self.pos[1]+self.Size[1]/2-self.textSize[1]/2))
class InputBox:
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    SIZE = (200,20)
    def __init__(self, rel_pos, text=''):
      self.rect = pygame.Rect(rel_pos[0]+GUI.position[0], rel_pos[1]+GUI.position[1], InputBox.SIZE[0], InputBox.SIZE[1])
      self.color = InputBox.COLOR_INACTIVE
      self.text = text
      self.txt_surface = Ressources.Font.render(text, True, self.color)
      self.active = False
      self.enterHandler = None

    def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
        # If the user clicked on the input_box rect.
        if self.rect.collidepoint(event.pos):
          # Toggle the active variable.
          self.active = not self.active
        else:
          self.active = False
        # Change the current color of the input box.
        self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
      if event.type == pygame.KEYDOWN:
        if self.active:
          keys = pygame.key.get_pressed()
          if keys[pygame.K_v] and( keys[pygame.K_LCTRL] or  keys[pygame.K_RCTRL]):
            self.text = pyperclip.paste()
          elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
          elif event.key == pygame.K_RETURN:
            if not self.enterHandler == None:
              self.enterHandler()
          else:
            self.text += event.unicode
          # Re-render the text.
          self.txt_surface = Ressources.Font.render(self.text, True, self.color)
    def linkTo(self,handler):
      self.enterHandler = handler
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        Ressources.myScreen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(Ressources.myScreen, self.color, self.rect, 2)
class PlayerTag:
  Height = 20
  spacing = 5
  def __init__(self,pos,player) -> None:
    self.selected = False
    self.pos = pos
    self.player:Player.Player = player
    self.txt_surface = Ressources.Font.render(self.player.name, True, self.player.color)
    self.size = (Player.PlayerCircle.SIZE+self.txt_surface.get_width()+PlayerTag.spacing,PlayerTag.Height)
    if (self.pos[0] + self.size[0]) > (GUI.labels[0].pos[0]+ PlayerList.SIZE[0]):
      self.pos = (GUI.labels[0].pos[0] , self.pos[1]+ PlayerTag.Height)
    self.width = 0
    self.circle = Player.PlayerCircle(self.pos,self.player.color,self.player.name)
    self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
  def Select(self):
    self.selected = True
    self.txt_surface = Ressources.Font.render(self.player.name, True, pygame.Color("white"))
  def UnSelect(self):
    self.selected = False
    self.txt_surface = Ressources.Font.render(self.player.name, True, self.player.color)
  def update(self):
    if self.player.alive == False:
      self.selected = False
      self.txt_surface = Ressources.Font.render(self.player.name, True, pygame.Color("white"))
    self.circle.update()
  def draw(self):
    if self.player.alive == False:
      pygame.draw.rect(Ressources.myScreen,pygame.Color("gray"),self.rect)
    if self.selected:
      pygame.draw.rect(Ressources.myScreen,pygame.Color("black"),self.rect)
    Ressources.myScreen.blit(self.txt_surface, (self.pos[0]+Player.PlayerCircle.SIZE+PlayerTag.spacing, self.pos[1] + PlayerTag.Height/2 - self.txt_surface.get_height()/2))
    self.circle.draw()
  def handle_event(self,event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.player.alive == False:
        print("Can't select a dead player")
      else:
        if self.rect.collidepoint(event.pos) and self.selected == False:
          self.Select()
        elif not self.rect.collidepoint(event.pos) and self.selected == True:
          self.UnSelect()
class PlayerList:
  SIZE = (200,300)
  PADDINGS = 5
  TagList = []
  def __init__(self,pos) -> None:
    self.rel_pos = pos
    self.pos = (Ressources.command_square_pos[0]+self.rel_pos[0],Ressources.command_square_pos[1]+self.rel_pos[1])
    self.selectedPlayer = None
    self.txt_surface = Ressources.Font.render("Player List :", True, pygame.Color('white'))
    self.text_height = self.txt_surface.get_height()
    self.rect = pygame.Rect(self.pos[0],self.pos[1],self.SIZE[0],self.SIZE[1]+self.text_height+self.PADDINGS)

  def getNextPos(self):
    if(len(PlayerList.TagList) == 0):
      next_x = self.pos[0]
      next_y = self.pos[1] + self.text_height + PlayerList.PADDINGS
      return (next_x,next_y)
    next_x = PlayerList.TagList[-1].pos[0] + PlayerList.PADDINGS + PlayerList.TagList[-1].size[0]
    next_y = PlayerList.TagList[-1].pos[1]
    return (next_x, next_y)
  def addPlayer(self,player):
    pos = self.getNextPos()
    PlayerList.TagList.append(PlayerTag(pos,player))
  def draw(self):
    rect = (self.pos[0],self.pos[1],PlayerList.SIZE[0],PlayerList.SIZE[1])
    Ressources.myScreen.blit(self.txt_surface, (rect[0], rect[1]))
    rect = (rect[0],rect[1]+self.text_height+PlayerList.PADDINGS,rect[2],rect[3])
    pygame.draw.rect(Ressources.myScreen,(255,255,255),rect)
    for i in range(len(PlayerList.TagList)):
      PlayerList.TagList[i].draw()
  def handle_event(self,event):
    if GameManager.GameManager.CommandMode != "GUI":
      return
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        self.selectedPlayer = None
        for i in range(len(PlayerList.TagList)):
          PlayerList.TagList[i].handle_event(event)
          if PlayerList.TagList[i].selected == True:
            self.selectedPlayer = PlayerList.TagList[i].player
  def update(self):
    for i in range(len(PlayerList.TagList)):
      PlayerList.TagList[i].circle.lives = PlayerList.TagList[i].player.lives
      PlayerList.TagList[i].update()

class GUI:
  position = []
  dimensions = []
  buttons = []
  textBoxes = []
  labels = []
  UIElements = []
  def init(pos,dim):
    GUI.position = pos
    GUI.dimensions = dim
    LineSize = GUI.dimensions[1]/20
    GUI.textBoxes.append(InputBox(((GUI.dimensions[0]/2)-(InputBox.SIZE[0]/2),LineSize),"Player Name"))
    GUI.UIElements.append(GUI.textBoxes[-1])
    GUI.buttons.append(Button("spown",((GUI.dimensions[0]/2)-(Button.Size[0]/2),LineSize*2),GUI.PlayerSpawn))
    GUI.UIElements.append(GUI.buttons[-1])
    GUI.textBoxes[-1].linkTo(GUI.PlayerSpawn)

    GUI.labels.append(PlayerList(((GUI.dimensions[0]/2)-(PlayerList.SIZE[0]/2),LineSize*3)))
    GUI.UIElements.append(GUI.labels[-1])


    for i in range(6):
      GameManager.GameManager.Dice_Animations.append(Animations.DiceAnimation(i+1,((GUI.dimensions[0]/2)-(Animations.DiceAnimation.SIZE[0]/2),LineSize*12.5)))
      GUI.UIElements.append(GameManager.GameManager.Dice_Animations[-1])

    GUI.buttons.append(Button("Roll",((GUI.dimensions[0]/2)-(Button.Size[0]/2),LineSize*15),GUI.RollDise))
    GUI.UIElements.append(GUI.buttons[-1])
    
    GUI.buttons.append(Button("Buy-1",((GUI.dimensions[0]/6)-(Button.Size[0]/2),LineSize*17),GUI.BuyMinus1))
    GUI.UIElements.append(GUI.buttons[-1])

    GUI.buttons.append(Button("Buy",((GUI.dimensions[0]*(3/6))-(Button.Size[0]/2),LineSize*17),GUI.BuyHere))
    GUI.UIElements.append(GUI.buttons[-1])
    
    GUI.buttons.append(Button("Buy+1",((GUI.dimensions[0]*(5/6))-(Button.Size[0]/2),LineSize*17),GUI.BuyPlus1))
    GUI.UIElements.append(GUI.buttons[-1])

    GameManager.GameManager.AnnoucementsList.append(Animations.AnnoucementAnimation(Ressources.Playing_square_pos,Ressources.Playing_square_dim,"broke",Ressources.anouncement_images[GameManager.Annoucements.Broke],GameManager.GameManager.AnnoucementsDelay))
    GUI.UIElements.append(GameManager.GameManager.AnnoucementsList[-1])
    GameManager.GameManager.AnnoucementsList.append(Animations.AnnoucementAnimation(Ressources.Playing_square_pos,Ressources.Playing_square_dim,"die",Ressources.anouncement_images[GameManager.Annoucements.Die],GameManager.GameManager.AnnoucementsDelay))
    GUI.UIElements.append(GameManager.GameManager.AnnoucementsList[-1])
    GameManager.GameManager.AnnoucementsList.append(Animations.AnnoucementAnimation(Ressources.Playing_square_pos,Ressources.Playing_square_dim,"got",Ressources.anouncement_images[GameManager.Annoucements.GetMoney],GameManager.GameManager.AnnoucementsDelay))
    GUI.UIElements.append(GameManager.GameManager.AnnoucementsList[-1])
    GameManager.GameManager.AnnoucementsList.append(Animations.AnnoucementAnimation(Ressources.Playing_square_pos,Ressources.Playing_square_dim,"lost",Ressources.anouncement_images[GameManager.Annoucements.LostMoney],GameManager.GameManager.AnnoucementsDelay))
    GUI.UIElements.append(GameManager.GameManager.AnnoucementsList[-1])

    GUI.buttons.append(Button("Discord",((GUI.dimensions[0]/2)-(Button.Size[0]/2),LineSize*19),GameManager.GameManager.SwitchMode))
    GUI.UIElements.append(GUI.buttons[-1])
  
  def BuyHere():
    if GUI.labels[0].selectedPlayer == None:
      print("Select player first !")
      return False
    return GUI.labels[0].selectedPlayer.buySquare(GUI.labels[0].selectedPlayer.position)
  def BuyPlus1():
    if GUI.labels[0].selectedPlayer == None:
      print("Select player first !")
      return False
    positionPlus1 = (GUI.labels[0].selectedPlayer.position+1)%len(GameManager.GameManager.squares)
    return GUI.labels[0].selectedPlayer.buySquare(positionPlus1)
  def BuyMinus1():
    if GUI.labels[0].selectedPlayer == None:
      print("Select player first !")
      return False
    positionMinus1 = (GUI.labels[0].selectedPlayer.position-1)
    if positionMinus1 < 0:
      positionMinus1 += len(GameManager.GameManager.squares)
    return GUI.labels[0].selectedPlayer.buySquare(positionMinus1)
  def RollDise():
    if GUI.labels[0].selectedPlayer == None:
      print("Select player first !")
      return
    if GUI.labels[0].selectedPlayer.alive == False:
      print("Selected player is dead !")
      return
    for animation in GameManager.GameManager.Dice_Animations:
      animation.visible = False
    value = random.choice(list(range(1,7)))
    GameManager.GameManager.Dice_Animations[value-1].play(GUI.RollDice_end)
    GameManager.GameManager.current_Animations.append(GameManager.GameManager.Dice_Animations[value-1])
  def RollDice_end(value):
    GameManager.GameManager.Playable_locked = False
    position = (GUI.labels[0].selectedPlayer.position + value) % len(GameManager.GameManager.squares)
    GameManager.GameManager.squares[GUI.labels[0].selectedPlayer.position].playerOut(GUI.labels[0].selectedPlayer)
    GUI.labels[0].selectedPlayer.position = position
    GUI.labels[0].selectedPlayer.move()
    GameManager.GameManager.squares[position].playerIn(GUI.labels[0].selectedPlayer)
    print("Dice roll : ", value)
  def PlayerSpawn():
    if not " " in GUI.textBoxes[0].text:
      GameManager.GameManager.playerSpawn(GUI.textBoxes[0].text)
  def draw():
    for i in range(len(GUI.UIElements)):
      GUI.UIElements[i].draw()

  def update():
    for i in range(len(GUI.UIElements)):
      GUI.UIElements[i].update()
  
  def handle_event(event):
    for i in range(len(GUI.UIElements)):
      GUI.UIElements[i].handle_event(event)
     