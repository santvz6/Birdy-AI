import pygame as pg

from pygame.locals import *

from config import *
from .spritesheet import SpriteSheet


class Birdy(pg.sprite.Sprite, SpriteSheet):  
    """
    Tamaño Original: ¿?
    """ 
    def __init__(self, displayData, tamaño, filename="Birdy1", chroma= VERDE): 
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData, filename, (99*tamaño, 70*tamaño), cantidadSprites=3, chroma= chroma)

        self.rect.topleft = (self.screenSize[0] // 3, self.screenSize[1] // 2)

        self.velocidadY = 5
        self.aceleracionY = 0.55
        self.velocidadMAX = 20

    def saltar(self, cantidad: int):    
        self.velocidadY = cantidad

    def update(self):

        # Aceleración
        self.velocidadY += self.aceleracionY
        self.velocidadY = min(self.velocidadY, self.velocidadMAX)
        self.rect.y += self.velocidadY
                                        
        self.loopSpriteSheet()

        # MÁRGENES
        if self.rect.y < 0 - self.rect.height: 
            self.rect.y = self.screenSize[1]                
        if self.rect.y > self.screenSize[1]:                  
            self.rect.y = 0 - self.rect.height 
            self.velocidadY -= 6.8 