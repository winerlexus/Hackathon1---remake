#sprite classes for game
import pygame as pg
from setting import *
import xml.etree.ElementTree as ET
import re
from input_manager import *
import random as rd
vec = pg.math.Vector2 # 2 dimension vector

class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        self.list = []
        self.tree = ET.parse("png/zero.xml")
        self.root = self.tree.getroot()
    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        # image = pg.transform.scale(image,(width*2,height*2))
        return image

    def extract(self, patten):
        self.list = []
        i = 0
        prog = re.compile(str(patten))
        for child in self.root:
            a = prog.fullmatch(child.attrib['name'])
            if a is not None:
                x = (
                int(child.attrib['x']), int(child.attrib['y']), int(child.attrib['width']), int(child.attrib['height']))
                self.list.append(x)
        return self.list
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("png/meteorSmall.png")
        # self.image = pg.transform.scale(self.image,(0,40))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = rd.randrange(-8,8)
        self.speedx = rd.randrange(8,12)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom <0:
            self.kill()
        if self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()
class Player(pg.sprite.Sprite):
    def __init__(self,game=0,effect =0):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.effect = effect
        self.image = self.game.spritesheet_player.get_image(201,45,34,39)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.pos = vec(WIDTH/2,HEIGHT/2)
        self.vel = vec(0,0) #speed
        self.acc = vec(0,0) #accelerate
        self.height = self.rect.height
        self.current_frame = 0
        self.last_update = 0
        self.moveleft = False
        self.moveright = False
        self.jumping = False
        self.walking = False
        self.slashing = False
        self.standing = True
        self.double_jump = False
        self.dictionary = {'jumping':'jump \(\d*\).png',
                           'breathing':'breath \(\d*\).png',
                           'walking':'walk \(\d*\).png',
                           'slashing':'slash \(\d*\).png',
                           'stand':'standing \(\d*\).png',
                           'cheering':'cheer \(\d*\).png',
                           'running':'run \(\d*\).png',
                           'jump-slash':'jump-slash \(\d*\).png'}
        self.last_direction = 'right'
        self.last_action = 'breathing'
        self.load_images('breath \(\d*\).png')
    def load_images(self,last_action):
        last_action = self.dictionary.get(self.last_action)
        self.status = self.game.spritesheet_player.extract(last_action)
        self.status_l = []
        self.status_r = []
        for i in self.status:
            self.status_l.append(self.game.spritesheet_player.get_image(*i))
            self.status_r.append(pg.transform.flip(self.game.spritesheet_player.get_image(*i),True,False))

    def animate(self):
        now = pg.time.get_ticks()
        total_time = 500
        if now - self.last_update > total_time/len(self.status):
            self.last_update = now
            if self.last_direction == 'left':
                self.current_frame = (self.current_frame +1) % len(self.status_l)
                self.image = self.status_l[self.current_frame]
            elif self.last_direction == "right":
                self.current_frame = (self.current_frame + 1) % len(self.status_r)
                self.image = self.status_r[self.current_frame]
    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms,False)
        self.rect.y -=1
        if hits and not self.jumping:
            self.vel.y = PLAYER_JUMPPOWER
            self.jumping = True
            self.last_action = "jumping"
            self.double_jump = True
            hits = []
        if hits == [] and self.double_jump and self.jumping:
            self.vel.y = PLAYER_JUMPPOWER
            self.double_jump = False

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    def slash(self):
            bullet = Bullet(self.rect.centerx,self.rect.top)
            if self.last_direction == "left":
                bullet.speedx = - bullet.speedx
            elif self.last_direction == "right":
                bullet.speedx = bullet.speedx
            self.game.all_sprites.add(bullet)
            self.game.bullets.add(bullet)
            if self.rect.bottom < 0:
                self.kill()


    def action(self):
        self.load_images(self.last_action)
        self.animate()
        if input_manager.left_pressed:
            self.last_direction = "left"
            self.acc.x = - PLAYER_ACC_x
        if input_manager.right_pressed:
            self.last_direction = "right"
            self.acc.x = + PLAYER_ACC_x
        if pg.key.get_pressed()[pg.K_SPACE] and not self.jumping:
            self.last_action = 'jumping'
            self.jump()
        if input_manager.space_pressed == False and self.jumping:
            self.jump_cut()
        if pg.key.get_pressed()[pg.K_a]:
            self.last_action = "slashing"
            self.slash()
        elif pg.key.get_pressed()[pg.K_a] and self.jumping:
            self.last_action = "jump-slash"
            self.slash()

        if input_manager.d_pressed:
            self.last_action = "running"
            self.acc.x += 2*self.acc.x
        if input_manager.up_pressed:
            self.last_action = "cheering"



    def update(self):
        self.acc = vec(0,PLAYER_ACC_y)
        self.action()
        self.mask = pg.mask.from_surface(self.image)
        if self.vel.x > PLAYER_MAXIMUM_x:
            self.vel.x = PLAYER_MAXIMUM_x
        if self.vel.x < - PLAYER_MAXIMUM_x:
            self.vel.x = - PLAYER_MAXIMUM_x

        # APPLY FRICTION
        self.acc.x += self.vel.x * PLAYER_FRICTION_x

        #MOTION EQUATION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # UPDATE RECT AT THE CENTER OF NEW POS
        self.rect.midbottom = self.pos
        if self.pos.y > HEIGHT:
            self.pos.y =0
        self.shield = 100
class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)


class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)