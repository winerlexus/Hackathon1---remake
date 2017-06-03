import pygame as pg
import random as rd
from setting import *
from sprites import *
from os import path
from input_manager import *
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

    def new(self):
        self.player = Player(self)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.platforms = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for plat in PLATFORM_LIST:
            p = Platform(*plat) #hay vcl
            self.all_sprites.add(p)
            self.platforms.add(p)


        #new game start, run itself
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        #Game loop, events
        events = pg.event.get()
        for event in events:
            #check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            input_manager.update(events)

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "png")
        #load images:
        self.spritesheet_player = SpriteSheet(path.join(img_dir,SPRITESHEET_PNG))


    def update(self):
        self.all_sprites.update()
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
                    self.player.last_action ="breathing"
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
                    self.player.double_jump = False



        #Scroll screen
        if self.player.rect.left > 5* WIDTH / 6:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)*2
                if plat.rect.right < 0:
                    plat.kill()
        elif self.player.rect.left < WIDTH / 6:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x) * 2
                if plat.rect.left > WIDTH:
                    plat.kill()

        #generate new flatforms:
        while len(self.platforms) < 6:
            width = rd.randrange(50,100)
            p = Platform(rd.randrange(0,WIDTH-width),rd.randrange(200,HEIGHT),width,30)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def draw_hp_bar(self,surface, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        bar_fill = (pct / 100) * BAR_LENGTH
        outline_bar = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        hp_bar = pg.Rect(x, y, bar_fill, BAR_HEIGHT)
        pg.draw.rect(surface, GREEN, hp_bar)
        pg.draw.rect(surface, WHITE, outline_bar, 2)

    def draw(self):
        #looping and drawing
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        #flip after drawing
        self.draw_hp_bar(self.screen,10,10,self.player.shield)
        pg.display.flip(    )


    def start_screen(self):
        pass

    def gameover_screen(self):
        pass
g = Game()
g.start_screen()
while g.running:
    g.new()
    g.gameover_screen()

pg.quit()

