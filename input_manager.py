import pygame as pg
class InputManager:
    def __init__(self):
        self.space_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.a_pressed = False
        self.d_pressed = False

    def update(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE :
                    self.space_pressed = True
                if event.key == pg.K_LEFT:
                    self.left_pressed = True
                if event.key == pg.K_RIGHT:
                    self.right_pressed = True
                if event.key == pg.K_UP:
                    self.up_pressed = True
                if event.key == pg.K_d:
                    self.d_pressed = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.space_pressed = False
                if event.key == pg.K_LEFT:
                    self.left_pressed = False
                if event.key == pg.K_RIGHT:
                    self.right_pressed = False
                if event.key == pg.K_UP:
                    self.up_pressed = False
                if event.key == pg.K_d:
                    self.d_pressed = False



input_manager = InputManager()