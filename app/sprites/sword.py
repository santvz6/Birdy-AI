import random
import pygame as pg

from pygame.locals import *
from .spritesheet import SpriteSheet

 
class Sword(pg.sprite.Sprite, SpriteSheet):
    """
    Tamaño Original: 337 x 170 por sprite
    """ 
    def __init__(self, displayData, tamaño, filename="swords", chroma=None):

        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData=displayData, filename=filename, tamaño= (337*tamaño, 170*tamaño), cantidadSprites= 5, chroma= chroma) 

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

        if self.rect.x < 0: # Si la espada supera el límite izquierdo se vuelve a generar pero en una altura diferente
            self.rect.topleft = (random.randint(int(self.screenSize[0]), int(self.screenSize[0] * 1.5)), 
                                 random.randint(0, int(self.screenSize[1] - self.tamaño[1])))