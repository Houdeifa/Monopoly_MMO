import pygame
class Ressources:
  background_image = None
  Screen_with:int = 1280
  Screen_height:int  = 720
  Playing_square_dim = []
  Playing_square_pos = []
  command_square_dim = []
  command_square_pos = []
  dice_images = []
  anouncement_images = []
  myScreen:pygame.Surface = None
  Font:pygame.font.Font = None
  smallFont:pygame.font.Font = None
  bigFont:pygame.font.Font = None
  Font_color:pygame.Color = (0,0,0)
  non_bayable_squares = [0,6,14,23]
  QuestionSquares = [6,14,23]
  Squares_positions = [(335, 16),#0
                    (443, 17),#1
                    (551, 17),#2
                    (661, 20),#3
                    (768, 18),#4
                    (875, 19),#5
                    (927, 146),#6
                    (927, 267),#7
                    (924, 393),#8
                    (924, 517),#9
                    (825, 607),#10
                    (719, 602),#11
                    (614, 603),#12
                    (511, 603),#13
                    (404, 603),#14
                    (297, 603),#15
                    (195, 605),#16
                    (96, 604),#17
                    (2, 603),#18
                    (6, 479),#19
                    (13, 350),#20
                    (112, 311),#21
                    (218, 314),#22
                    (326, 385),#23
                    (339, 266),#24
                    (335, 141)]#25
  PlayerColors = [pygame.Color('aqua'),
                  pygame.Color('aquamarine4'),
                  pygame.Color('antiquewhite3'),
                  pygame.Color('antiquewhite4'),
                  pygame.Color('aquamarine2'),
                  pygame.Color('azure4'),
                  pygame.Color('blue'),
                  pygame.Color('blueviolet'),
                  pygame.Color('brown1'),
                  pygame.Color('brown4'),
                  pygame.Color('cadetblue1'),
                  pygame.Color('chartreuse'),
                  pygame.Color('chartreuse4'),
                  pygame.Color('coral'),
                  pygame.Color('cornflowerblue'),
                  pygame.Color('darkblue'),
                  pygame.Color('darkgoldenrod1'),
                  pygame.Color('darkorchid'),
                  pygame.Color('darksalmon'),
                  pygame.Color('deeppink'),
                  pygame.Color('fuchsia'),
                  pygame.Color('gold'),
                  ]