import pygame as pg

from pygame.locals import *

from ai import NeuralNetwork
from config import *
from .spritesheet import SpriteSheet


class Birdy(pg.sprite.Sprite, SpriteSheet):  
    """
    Tamaño Original: ¿?
    """ 
    def __init__(self, displayData, tamaño, filename, brain=None, chroma=GREEN1): 
        # AI
        self.brain = brain if brain else NeuralNetwork()
        
        # PyGame
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData, filename, (99*tamaño, 70*tamaño), cantidadSprites=3, chroma= chroma)

        self.rect.topleft = (self.screenSize[0] // 3, self.screenSize[1] // 2)

        self.speed_y = 5
        self.max_speed_y = 20
        self.acc_y = 0.55

        self.hit_items = set() 

    def jump(self, value=10):    
        self.speed_y = -value

    def update(self):
        # Aceleración
        self.speed_y += self.acc_y
        self.speed_y = min(self.speed_y, self.max_speed_y)
        self.rect.y += self.speed_y
                                        
        self.loopSpriteSheet()

        # MÁRGENES
        if self.rect.y < 0 - self.rect.height: 
            self.rect.y = self.screenSize[1]                
        if self.rect.y > self.screenSize[1]:                  
            self.rect.y = 0 - self.rect.height 
            self.speed_y -= 6.8 