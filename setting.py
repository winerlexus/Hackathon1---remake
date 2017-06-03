##SCREEN SIZE
TITLE = "Just A Normal Game"
WIDTH = 800
HEIGHT = 600
FPS =  60

#PLayer's properties
PLAYER_ACC_x = 0.8
PLAYER_FRICTION_x = - 0.12 #MAYBE CALCULATED BY WEIGHT BUT NOT NECESSARY BECAUSE GAME IS GAME =)))
PLAYER_ACC_y = 0.5
PLAYER_JUMPPOWER = -15

PLAYER_MAXIMUM_x = 4*2
#Platform
PLATFORM_LIST = [(0,HEIGHT-40,WIDTH*10,40),
                 (200, HEIGHT - 200, WIDTH / 3, 40),
                 (0, HEIGHT /2, WIDTH/2, 40),
                 (WIDTH, 150, WIDTH / 2, 40)]
#COLOR
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#file
SPRITESHEET_PNG = "Zero-spritesheet.png"