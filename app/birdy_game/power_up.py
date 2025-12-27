import random
import pygame as pg

from pygame.locals import *

from config import *
from .spritesheet import SpriteSheet


class PowerUp(pg.sprite.Sprite, SpriteSheet):
    """
    Tamaño Original: ¿?
    """ 
    def __init__(self, displayData, tamaño, filename= "habilidad", chroma= VERDE):

        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData=displayData, filename=filename, tamaño= (70*tamaño, 64*tamaño), cantidadSprites= 8, chroma= chroma)

        self.FPS = displayData[2]
        self.t_aparicion = 15
        self.velocidadX = -8

        self.rect.topleft = (self.t_aparicion * self.FPS * abs(self.velocidadX), random.randint(0, int(self.screenSize[1] - self.tamaño[1])))
        
        

    
    def update(self):

        self.rect.x += self.velocidadX

        self.loopSpriteSheet()
                   
        if self.rect.x < 0 - self.rect.width:
            self.rect.topleft = (self.t_aparicion * self.FPS * abs(self.velocidadX), random.randint(0, int(self.screenSize[1] - self.tamaño[1])))

