#sprite classes for game
import pygame as pg
from setting import *
import xml.etree.ElementTree as ET
import re
from input_manager import *
import random as rd
from animation import *
from math import *
vec = pg.math.Vector2 # 2 dimension vector

class Bullet(pg.sprite.Sprite):
    def __init__(self,object,png,xml,patten,x,y,direction):
        pg.sprite.Sprite.__init__(self)
        self.animate = LoadSprite_Animation_simple(self,png,xml,patten,direction)
        self.image =  self.animate.get_image(646,242,24,24)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = rd.randrange(-2,2)
        self.speedx = rd.randrange(8,12)
        self.last_direction = "right"
        self.disable = False


    def update(self):
        self.animate.update()
        self.image.set_colorkey(BLACK)
        self.image.get_rect()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom >HEIGHT:
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self,game=0,effect=0,animate=0):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.animate = LoadSprite_Animation(self,SPRITESHEET_PLAYER,SPRITESHEET_PLAYER_XML,"right")
        self.image = self.animate.get_image(0,0,0,0)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2,HEIGHT/2)
        self.rect.midbottom = self.pos
        self.vel = vec(0,0) #speed
        self.acc = vec(0,0) #accelerate
        self.last_direction = 'right'
        self.last_shoot = pg.time.get_ticks()
        self.shoot_delay = 400
        self.health = 100
        self.hurt_disable = False
        self.last_hitted = pg.time.get_ticks()
        self.invul = 1000
        self.jumping = False
        self.double_jump = False
        self.charged = False
        self.last_action = "walk"
        self.dictionary = {"walk":"walk \(\d*\).png",
                           "jump": "jump \(\d*\).png",
                           "throw": "throw \(\d*\).png",
                           "running": "run \(\d*\).png",
                           "seal":"seal \(\d*\).png"}
        self.dame = 10
        self.skiltime = 70
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms,False)
        if hits and not self.jumping:
            self.vel.y = PLAYER_JUMPPOWER
            self.game.jump_sound.play()
            self.jumping = True
    def jump_cut(self):
        if input_manager.space_pressed == False and self.jumping:
            if self.jumping:
                if self.vel.y < -5:
                    self.vel.y = -5

    def throw(self):
        self.dame = 50
        now = pg.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now

            bullet = Bullet(self, SPRITESHEET_PLAYER, SPRITESHEET_PLAYER_XML, "shuriken \(\d*\).png", self.pos.x,
                            self.rect.top,"right")
            if self.last_direction == "left":
                bullet.last_direction = "left"
                bullet.speedx = - bullet.speedx
            if self.last_direction == "right":
                bullet.last_direction = "right"
                bullet.speedx = bullet.speedx
            self.game.skill.play()
            self.game.all_sprites.add(bullet)
            self.game.bullets.add(bullet)

    def fire_blower(self):
        self.dame = 25
        now = pg.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = Bullet(self, SPRITESHEET_PLAYER, SPRITESHEET_PLAYER_XML, "firefromfrog \(\d*\).png", self.pos.x,
                            self.rect.top,"right")
            if self.last_direction == "left":
                bullet.last_direction = "left"
                bullet.speedx = - bullet.speedx
            if self.last_direction == "right":
                bullet.last_direction = "right"
                bullet.speedx = bullet.speedx
            self.game.skill.play()
            self.game.all_sprites.add(bullet)
            self.game.penetrate.add(bullet)
        # if bullet.animate.current_frame == len(bullet.animate.status) -1 :
        #     bullet.kill()
    def run(self):
            self.acc.x += 2*self.acc.x
    def action(self):
        self.animate.update()
        self.image.set_colorkey(BLACK)
        if input_manager.left_pressed:
            self.last_direction = "left"
            self.acc.x = - PLAYER_ACC_x
        if input_manager.right_pressed:
            self.last_direction = "right"
            self.acc.x = + PLAYER_ACC_x
        if pg.key.get_pressed()[pg.K_SPACE] and not self.jumping:
            self.last_action = 'jump'
            self.jump()
        if input_manager.space_pressed == False and self.jumping:
            self.last_action = "jump"
            self.jump_cut()
        if input_manager.d_pressed:
            self.last_action = "running"
            self.run()
        if pg.key.get_pressed()[pg.K_f]:
            self.skiltime -= 700 // FPS
            self.last_action = "seal"
        for event in self.game.happend:
            if event.type == pg.KEYUP:
                if event.key == pg.K_f and self.skiltime <= 0:
                    self.fire_blower()
                    self.skiltime = 70

        if pg.key.get_pressed()[pg.K_a]:
            self.last_action = "throw"
            self.throw()

    def update(self):
        self.acc = vec(0,PLAYER_ACC_y)
        self.action()
        self.rect = self.image.get_rect()
        if self.vel.x > PLAYER_MAXIMUM_x:
            self.vel.x = PLAYER_MAXIMUM_x
        if self.vel.x < - PLAYER_MAXIMUM_x:
            self.vel.x = - PLAYER_MAXIMUM_x
        if self.rect.bottom > HEIGHT:
            self.pos = vec(WIDTH/2,HEIGHT/2)
        if self.rect.left <=0:
          self.rect.center = (WIDTH/2,HEIGHT/2)
        # APPLY FRICTION
        self.acc.x += self.vel.x * PLAYER_FRICTION_x
        #MOTION EQUATION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # UPDATE RECT AT THE CENTER OF NEW POS
        self.rect.midbottom = self.pos
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.health <=0:
            self.health = 0


class Mob(pg.sprite.Sprite):
    def __init__(self,game,health,scale,sprite=0,xml=0):
        pg.sprite.Sprite.__init__(self)
        self.sprite = sprite
        self.xml = xml
        self.object = object
        self.game = game
        self.animate = LoadSprite_Animation(self,self.sprite,self.xml,"left",scale)
        self.dictionary = {'appear':"appear_\d*.png",
                           "die":"die_\d*.png",
                           "go":"go_\d*.png",
                           "hit":"hit_\d*.png",
                           "idle":"idle_\d*.png"}
        self.last_direction = "left"
        self.image = self.animate.get_image(0,0,0,0)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.vel = rd.randrange(4,7)
        self.pos = vec(rd.choice(self.game.gates).rect.center)
        self.rect.center = self.pos
        self.last_action = "go"
        self.health = health
        self.dame = 0
        self.max_health = health
        self.die_frame = 0
        self.rot = 0
        self.attack_time = 100
        self.last_hit = pg.time.get_ticks()
        self.invul = 400
    def hp_bar(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width*self.health/self.max_health)
        self.health_bar = pg.Rect(0,0,width,6)
        if self.health < 100:
            pg.draw.rect(self.image,col,self.health_bar)
    def move_toward(self):
        self.distance = self.game.player.pos - self.pos
        self.vec_normalize = self.distance.normalize()
        self.vec_length = self.distance.length()
        if self.pos.x <= 0 or self.pos.x>= WIDTH:
            self.vec_normalize = vec(-self.vec_normalize[0],self.vec_normalize[1])
        # # MOTION
        if self.vec_length <10*self.rect.width:
            self.pos += self.vec_normalize * self.vel

        else:
            self.normal_move()
        self.rect = self.image.get_rect()
        #UPDATE RECT AT THE CENTER OF NEW POS
        self.rect.center = self.pos
    def normal_move(self):
        if self.last_direction == "right":
            self.pos += self.vel * vec(abs(self.vec_normalize[0]),0)
        else:
            self.pos += self.vel * vec(-abs(self.vec_normalize[0]),0)
    def attack(self):
        if self.vec_length < self.rect.width:
            now = pg.time.get_ticks()
            self.attack_time -= 300 // FPS
            if self.attack_time <= 0:
                self.last_action = "hit"
                self.dame = 20
                self.attack_time = 100

        if self.vec_length > self.rect.width:
            self.attack_time = 100
            self.last_action = "go"
            self.dame = 0

    def update(self):
        self.hp_bar()
        self.animate.update()
        self.move_toward()
        self.attack()
        if  self.distance[0] >=0 :
            self.last_direction = "right"
        else:
            self.last_direction = "left"
        self.image.set_colorkey(BLACK)
        if self.health <= 0:
            self.kill()
            self.game.mob_count += 1
            self.game.player.health += 5

class Boss(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.animate = LoadSprite_Animation(self,"sasuke/sprites.png","sasuke/sprites.xml","right")
        self.image = self.animate.get_image(0, 0, 0, 0)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.action_list_idle = ["stand","run","walk"]
        self.action_list_combat = ["combo1"]
        self.last_direction = "left"
        self.last_action = "stand"
        self.vel = vec(0, 0)  # speed
        self.acc = vec(0, 0)  # accelerate
        self.pos = vec(WIDTH-100,HEIGHT/2)
        self.rect.center = self.pos
        self.health = 10000
        self.dame = 0
        self.max_health = 10000
        self.attack_time = 200
        self.jumping = False
        self.last_shoot = pg.time.get_ticks()
        self.action_delay = 2000
        self.dictionary = {"stand":"stand \(\d*\).png",
                           "run":"run \(\d*\).png",
                           "walk":"walk \(\d*\).png",
                           "hitted":"hitted \(\d*\).png",
                           "combo1":"combo1 \(\d*\).png",
                           "combo2":"combo2 \(\d*\).png",
                           "throw":"throw \(\d*\).png",
                           "blow":"blowfire \(\d*\).png",
                           }
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits and not self.jumping:
            self.vel.y = -15
            self.game.jump_sound.play()
            self.jumping = True

    def jump_short(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5

    def throw(self):
        self.dame = 20
        now = pg.time.get_ticks()
        if now - self.last_shoot > self.action_delay:
            self.last_shoot = now
            bullet = Bullet(self, "sasuke/sprites.png","sasuke/sprites.xml", "meteor.png", self.pos.x,
                            self.rect.top, "right")
            if self.last_direction == "left":
                bullet.last_direction = "left"
                bullet.speedx = - bullet.speedx
            if self.last_direction == "right":
                bullet.last_direction = "right"
                bullet.speedx = bullet.speedx
            self.game.skill.play()
            self.game.all_sprites.add(bullet)
            self.game.boss_skill.add(bullet)

    def fire_blower(self):
        self.dame = 60
        now = pg.time.get_ticks()
        if now - self.last_shoot > self.action_delay:
            self.last_shoot = now
            bullet = Bullet(self,"sasuke/sprites.png","sasuke/sprites.xml", "fire \(\d*\).png", self.pos.x,
                            self.rect.top, "right")
            if self.last_direction == "left":
                bullet.last_direction = "left"
                bullet.speedx = - bullet.speedx
            if self.last_direction == "right":
                bullet.last_direction = "right"
                bullet.speedx = bullet.speedx
            bullet.image.set_colorkey(WHITE)
            self.game.skill.play()
            self.game.all_sprites.add(bullet)
            self.game.boss_skill.add(bullet)
            # if bullet.animate.current_frame == len(bullet.animate.status) -1 :
            #     bullet.kill()

    def run(self):
        self.acc.x += 2 * self.acc.x


    def hp_bar(self):
        if self.health/self.max_health > 0.6 :
            col = GREEN
        elif self.health/self.max_health > 0.3 :
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width*self.health/self.max_health)
        self.health_bar = pg.Rect(0,0,width,6)
        if self.health < self.max_health:
            pg.draw.rect(self.image,col,self.health_bar)

    def action(self):

        if self.vec_length < 2*self.rect.width:
            hits = pg.sprite.collide_rect(self,self.game.player)
            self.attack_time -= 500 // FPS
            if self.attack_time <= 170 :
                self.last_action = rd.choice(["combo1", "combo2"])
                if hits and self.last_action == "combo1":
                    self.dame = 60
                if hits and self.last_action == "combo2":
                    self.dame = 70
            print(self.attack_time)
        if self.vec_length < 8*self.rect.width and self.vec_length >= 2*self.rect.width:
            self.attack_time -= 500/FPS
            if self.attack_time <= 160:
                self.last_action = rd.choice(["throw","blow"])
                if self.last_action == "throw":
                    self.dame = 1000
                    self.throw()
                elif self.last_action == "blow":
                    self.dame = 500
                    self.fire_blower()
        if self.vec_length > 10*self.rect.width:
            self.dame = 0
        if self.vec_length > 8*self.rect.width:
            self.last_action = "walk"
        # if self.vec_length < 500:
        #     action = rd.choice(self.action_list_combat)
        # elif self.vec_length > 500:
        #     action = rd.choice(self.action_list_idle)
        # self.last_action = action
    def update(self):
        self.horizontal = vec(self.game.player.pos.x - self.pos.x, 0)
        if self.horizontal == vec(0, 0):
            self.horizontal = vec(1, 0)
        self.normal = self.horizontal.normalize()
        self.vec_length = self.horizontal.length()
        self.acc = vec(0, 5)
        self.hp_bar()
        self.animate.update()
        print(self.animate.load_images(self.throw))
        self.action()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)

        if self.horizontal.length() <= 9*self.rect.width:
            self.vel.x += self.normal.x

        if self.vel.x > PLAYER_MAXIMUM_x:
            self.vel.x = PLAYER_MAXIMUM_x
        if self.vel.x < - PLAYER_MAXIMUM_x:
            self.vel.x = - PLAYER_MAXIMUM_x
        # APPLY FRICTION
        self.acc.x += self.vel.x * PLAYER_FRICTION_x
        # MOTION EQUATION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.vel.x >= 0 :
            self.last_direction = "right"
        else:
            self.last_direction = "left"
        # UPDATE RECT AT THE CENTER OF NEW POS
        self.rect.midbottom = self.pos
        print(self.last_action)


class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Background(pg.sprite.Sprite):
    def __init__(self,file):
        pg.sprite.Sprite.__init__(self)
        self.file = file
        self.image = pg.image.load(path.join(img_dir,self.file))
        # self.image = pg.transform.scale(self.image,(WIDTH,HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)

class Gate(pg.sprite.Sprite):
    def __init__(self,object, png, xml, patten, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.animate = LoadSprite_Animation_simple(self, png, xml, patten, direction)
        self.png = png
        self.xml = xml
        self.patten = patten
        self.object = object
        self.image = self.animate.get_image(0,78,29,75)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_direction = "left"


    def update(self):

        self.animate.load_images(self.patten)
        self.animate.update()
        self.image = pg.transform.scale(self.image,(50,175))
        self.image.set_colorkey(BLACK)



