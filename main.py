import pygame as pg
import random as rd
from setting import *
from sprites import *
import os
from input_manager import *
from animation import *
class Game:
    def __init__(self):
        # Initialize game screen:
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.load_data()
        self.mob_count = 0
        self.mob_require = 4
        self.mob_coexits = 4

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = os.path.join(self.dir, "png")
        self.sfx_dir = os.path.join(self.dir,"sfx")
        self.jump_sound = pg.mixer.Sound(os.path.join(self.sfx_dir,jump_sound))
        self.hitted = pg.mixer.Sound(os.path.join(self.sfx_dir,hitted))
        self.skill = pg.mixer.Sound(os.path.join(self.sfx_dir,dragon))

    def new(self):
        self.background = Background(BACKGROUND_IMG)
        self.player = Player(self)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.background)
        self.all_sprites.add(self.player)
        self.platforms = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.penetrate = pg.sprite.Group()
        self.allmobs = pg.sprite.Group()
        self.boss = Boss(self)
        self.boss_skill = pg.sprite.Group()
        self.gate1 = Gate(self,"gate/gate1.png","gate/gate1.xml","spin \(\d*\).png",WIDTH-50,10,"left")
        self.gate2 = Gate(self,"gate/gate1.png","gate/gate1.xml","spin \(\d*\).png",0,10,"right")
        self.gates = [self.gate1,self.gate2]
        # self.all_sprites.add(self.boss)
        for gate in self.gates:
            self.all_sprites.add(gate)
        for plat in PLATFORM_LIST:
            p = Platform(*plat) #hay vcl
            self.all_sprites.add(p)
            self.platforms.add(p)
        pg.mixer.music.load(path.join(self.sfx_dir,"BestGamingMusicMix-VA-4446419_hq.mp3" ))
        #new game start, run itself

        self.run()

    def run(self):
        pg.mixer.music.play()
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def events(self):
        #Game loop, events
        self.happend = pg.event.get()
        for event in self.happend:
            #check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            input_manager.update(self.happend)


    def update(self):
        self.all_sprites.update()
        # ADD ZOMBIES

        while len(self.allmobs) < self.mob_coexits and self.mob_count < self.mob_require:
            zombie= Mob(self,100,3,SPRITESHEET_MOB1, SPRITESHEET_MOB1_XML)
            self.all_sprites.add(zombie)
            self.allmobs.add(zombie)
        if self.mob_count >= self.mob_require:
            self.all_sprites.add(self.boss)
            BACKGROUND_IMG = "background.jpg"
        # COLLIDE FOR JUMPING
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms,False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                a = 0
                for i in pg.key.get_pressed():
                    a += i
                if a == 0:
                    self.player.last_action ="walk"
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
                    self.player.double_jump = False
        #boss
        if self.boss.vel.y > 0:
            hits = pg.sprite.spritecollide(self.boss, self.platforms, False)
            for hit in hits:
                    self.boss.pos.y = hit.rect.top
                    self.boss.vel.y = 0
                    self.boss.jumping = False
        ## COLLIDE PLATFORM AND BULLETS
        #shuriken
        hits = pg.sprite.groupcollide(self.allmobs,self.bullets,False,True)
        for hit in hits:
            hit.health -= self.player.dame
        #FIRE
        hits = pg.sprite.groupcollide(self.allmobs,self.penetrate,False,False)
        for hit in hits:
            now = pg.time.get_ticks()
            if now - hit.last_hit > hit.invul:
                hit.last_hit = now
                hit.health -= self.player.dame
        hits = pg.sprite.spritecollide(self.gate1, self.penetrate,True)
        ## COLLIDE PLAYER AND MOBS
        hits = pg.sprite.spritecollide(self.player,self.allmobs,False)
        for hit in hits:
            now = pg.time.get_ticks()
            if now - self.player.last_hitted > self.player.invul:
                self.player.last_hitted = now
                self.player.health -= hit.dame
                if hit.dame >0:
                    self.hitted.play()

        # BOSS AND PLAYER
        hits = pg.sprite.spritecollide(self.player,self.boss_skill,True)
        if hits:
            self.player.health -= self.boss.dame
            self.hitted.play()
        hits = pg.sprite.spritecollide(self.boss,self.bullets,True)
        if hits:
            self.boss.health -= 5*self.player.dame
        hits = pg.sprite.spritecollide(self.boss,self.penetrate,True)
        if hits:
            self.boss.health -= 15*self.player.dame
        if self.boss.health <=0:
            self.boss.kill()
        if self.player.health <=0:
            self.playing = False
        # #Scroll screen
        # if self.player.rect.left > 5* WIDTH / 6:
        #     self.player.pos.x -= abs(self.player.vel.x)
        #     for plat in self.platforms:
        #         plat.rect.x -= abs(self.player.vel.x)*2
        #         if plat.rect.right < 0:
        #             plat.kill()
        # elif self.player.rect.left < WIDTH / 6:
        #     self.player.pos.x += abs(self.player.vel.x)
        #     for plat in self.platforms:
        #         plat.rect.x += abs(self.player.vel.x) * 2
        #         if plat.rect.left > WIDTH:
        #             plat.kill()

    def draw_hp_bar(self,surface, x, y, pct):
        if pct < 0:
            pct = 0
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        bar_fill = (pct / 100) * BAR_LENGTH
        outline_bar = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        hp_bar = pg.Rect(x, y, bar_fill, BAR_HEIGHT)
        pg.draw.rect(surface, col, hp_bar)
        pg.draw.rect(surface, WHITE, outline_bar, 2)

    def draw_text(self, text, size,color, x, y):
        font = pg.font.Font(pg.font.match_font("arial"), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        #looping and drawing
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        #PLAYER"S HP
        self.draw_hp_bar(self.screen,10,10,self.player.health)
        # flip after drawing
        pg.display.flip(    )


    def start_screen(self):
        self.screen.fill((0,155,155))
        self.draw_text(TITLE,40,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("arrow to move, space to jump, asd find it yourself",25,RED,WIDTH/2,HEIGHT/2)
        self.draw_text("press any key",22,YELLOW,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait()
    def wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    def gameover_screen(self):
        pass
g = Game()
g.start_screen()
while g.running:
    g.new()
    g.gameover_screen()

pg.quit()

