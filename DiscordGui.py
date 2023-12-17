import GUI
import GameManager
class DiscordGui:
  position = (0,0)
  dimensions = (0,0)
  UIElements = []
  buttons = []
  def init(pos,dim):
    DiscordGui.position = pos
    DiscordGui.dimensions = dim
    LineSize = DiscordGui.dimensions[1]/20

    text = "Manual command"
    textSize = GUI.Button.getSize(text)
    pos = ((DiscordGui.dimensions[0]/2)-(textSize[0]/2),LineSize*19)
    print("pos =",pos)
    DiscordGui.buttons.append(GUI.Button(text,pos,GameManager.GameManager.SwitchMode))
    DiscordGui.buttons[-1].updateSize()
    DiscordGui.UIElements.append(DiscordGui.buttons[-1])

    DiscordGui.UIElements.append(GUI.GUI.labels[0])

    for i in range(6):
      DiscordGui.UIElements.append(GameManager.GameManager.Dice_Animations[i])

    for i in range(len(GameManager.GameManager.AnnoucementsList)):
      DiscordGui.UIElements.append(GameManager.GameManager.AnnoucementsList[i])
  def update():
    for i in range(len(DiscordGui.UIElements)):
      DiscordGui.UIElements[i].update()
  def draw():
    for i in range(len(DiscordGui.UIElements)):
      DiscordGui.UIElements[i].draw()
  def handle_event(event):
    for i in range(len(DiscordGui.UIElements)):
      DiscordGui.UIElements[i].handle_event(event)