import random
import pygame as pg

from pygame.locals import *

from config import *
from .spritesheet import SpriteSheet



class Coins(pg.sprite.Sprite, SpriteSheet):
    """
    Tamaño Original: ¿?
    """ 
    def __init__(self, displayData, tamaño, filename="coins",  chroma=BLUE):
        
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData=displayData, filename=filename, tamaño= (102*tamaño, 103*tamaño), cantidadSprites= 6, chroma= chroma) 

        self.rect.topleft = (random.randint(int(self.screenSize[0]), int(self.screenSize[0] * 1.5)), 
                             random.randint(0, int(self.screenSize[1] - self.tamaño[1])))
        
        self.velocidadX = -6
        self.aceleracionX = -0.1
        self.velocidadMAX = -10


    def update(self):

        self.velocidadX += self.aceleracionX
        self.velocidadX = max(self.velocidadX, self.velocidadMAX)
        self.rect.x += self.velocidadX 

        self.loopSpriteSheet()

        if self.rect.x < 0:
            self.rect.topleft = (random.randint(int(self.screenSize[0]), int(self.screenSize[0] * 1.5)), 
                                 random.randint(0, int(self.screenSize[1] - self.tamaño[1])))
