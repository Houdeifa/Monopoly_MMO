# PyGame template.
 
# Import standard modules.
import sys
from GameManager import GameManager
from GameManager import Annoucements
from Ressources import Ressources
import pygame
import os
import signal
import Discrod_api
# Import non-standard modules.
from pygame.locals import *
discord_thread = None
def update(dt):
  global discord_thread
  """
  Update game. Called once per frame.
  dt is the amount of time passed since last frame.
  If you want to have constant apparent movement no matter your framerate,
  what you can do is something like
  
  x += v * dt
  
  and this will scale your velocity based on time. Extend as necessary."""
  GameManager.delta_time = dt
  # Go through events that are passed to the script by the window.
  for event in pygame.event.get():
    # We need to handle these events. Initially the only one you'll want to care
    # about is the QUIT event, because if you don't handle it, your game will crash
    # whenever someone tries to exit.
    GameManager.handle_event(event)
    if event.type == MOUSEBUTTONDOWN:
      # print(pygame.mouse.get_pos())
      # if len(GameManager.player_list) >= 1:
      #   GameManager.GameManager.Playable_locked = True
      #   GameManager.Playable = False
      #   GameManager.Animation_ongoing = True
      #   GameManager.AnnoucementsList[Annoucements.LostMoney].setPlayer(GameManager.player_list[0])
      #   GameManager.AnnoucementsList[Annoucements.LostMoney].play()
      #   GameManager.AnnoucementsList[Annoucements.LostMoney].end_ballback = None
      #   GameManager.AnnoucementsList[Annoucements.LostMoney].playnext = True
      pass
    if event.type == QUIT:
      pygame.quit() # Opposite of pygame.init
      Discrod_api.quit()
      os._exit(0) # Not including this line crashes the script on Windows. Possibly
      # on other operating systems too, but I don't know for sure.
    # Handle other events as you wish.
  GameManager.update()
 
def draw(screen):
  """
  Draw things to the window. Called once per frame.
  """
  screen.fill((0, 0, 0)) # Fill the screen with black.
  
  # Redraw screen here.
  GameManager.draw()

  # Flip the display so that the things we drew actually show up.
  pygame.display.flip()
 
def runPyGame(discord_thread,commandQueue_thread):
  # Initialise PyGame.
  pygame.init()
  # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
  fps = 60.0
  fpsClock = pygame.time.Clock()
  
  # Set up the window.
  width, height = Ressources.Screen_with, Ressources.Screen_height
  screen = pygame.display.set_mode((width, height))
  GameManager.init(screen,discord_thread,commandQueue_thread)
  
  # screen is the surface representing the window.
  # PyGame surfaces can be thought of as screen sections that you can draw onto.
  # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.
  
  # Main game loop.
  dt = 1/fps # dt is the time since last frame.
  while True: # Loop forever!
    update(dt) # You can update/draw here, I've just moved the code for neatness.
    draw(screen)
    
    dt = fpsClock.tick(fps)