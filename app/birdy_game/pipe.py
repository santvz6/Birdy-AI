import random
import pygame as pg

from pygame.locals import *
from .spritesheet import SpriteSheet


class Pipe(pg.sprite.Sprite, SpriteSheet):
    """
    Tamaño Original: ¿?
    """ 
    def __init__(self, displayData, filename, tipo: str, chroma= None):
        
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData=displayData, filename=filename, 
                             tamaño= (100, 400), cantidadSprites= 1, chroma= chroma) 


        self.apertura= 0.7
        self.tipo = tipo
        if tipo == "bottom":
            self.rect.topleft = (int(self.screenSize[0] * 1.5), 
                                random.randint(int(self.screenSize[1] - self.tamaño[1]), int(self.screenSize[1]*self.apertura)))
        elif tipo == "top":
            self.rect.topleft = (int(self.screenSize[0] * 1.5), 
                                random.randint(int(-self.tamaño[1]*(2-self.apertura)), 0))


        self.velocidadX = -8
 


    def update(self):
        self.rect.x += self.velocidadX 

        if self.rect.x < -self.tamaño[0]:
            if self.tipo == "bottom":
                self.rect.topleft = (int(self.screenSize[0] * 1.5), 
                                random.randint(int(self.screenSize[1] - self.tamaño[1]), int(self.screenSize[1]*0.9)))
            elif self.tipo == "top":
                self.rect.topleft = (int(self.screenSize[0] * 1.5), 
                                random.randint(int(-self.tamaño[1]), 0))
