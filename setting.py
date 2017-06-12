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

#COLOR
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW =(225,225,0)
#file
# Players:
SPRITESHEET_PLAYER = "naruto.png"
SPRITESHEET_PLAYER_XML = "naruto.xml"

#Bullets
SPRITESHEET_BULLET = "sprites.png"
SPRITESHEET_BULLET_XML = "sprites.xml"


## mob1
SPRITESHEET_MOB1 = "zombie.png"
SPRITESHEET_MOB1_XML = "zombiesprites.xml"

#SOUND
jump_sound = "jump.wav"
s_jump = "s_jump.wav"
hitted = "hitted.wav"
dragon = "dragon_skill.wav"

#lvl1:

#Platform
PLATFORM_LIST = [(0,HEIGHT-20,WIDTH,20),
                 (200, HEIGHT - 200, WIDTH // 3, 40),
                 (0, HEIGHT //2, WIDTH//4, 40),
                 (WIDTH, 150, WIDTH // 5, 40)]

BACKGROUND_IMG = "the_secret_entrance_by_jjcanvas-dagt780.jpg"