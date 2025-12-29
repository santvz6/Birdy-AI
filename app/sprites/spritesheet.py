import pygame as pg

from pathlib import Path

class SpriteSheet:
    def __init__(self, displayData, filename, tamaño, cantidadSprites, chroma, path=Path("app/assets/gfx/sprites")):
        
        self.screenSize = displayData[0].get_size()
        self.filename = filename
        self.tamaño = tamaño
        self.cantidadSprites = cantidadSprites

        if chroma:
            self.imagePG = pg.image.load(path / (self.filename + ".png")).convert()
            self.imagePG.set_colorkey(chroma) 
        else:
            self.imagePG = pg.image.load(path / (self.filename + ".png")).convert_alpha()
        
        self.sprite_sheet = pg.transform.scale(self.imagePG, (self.tamaño[0] * self.cantidadSprites, self.tamaño[1]))

        self.image = pg.Surface(self.tamaño).convert_alpha()

        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sprite_sheet, (0,0), pg.Rect(0 * self.tamaño[0], 0, self.tamaño[0], self.tamaño[1]))
        self.rect = self.image.get_rect() 

    def animarSprite(self, cambioSeg=1) -> int:

        return int(pg.time.get_ticks() // (1000 * cambioSeg)) % self.cantidadSprites

    def loopSpriteSheet(self):
        # Dibujo
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sprite_sheet, (0,0), pg.Rect(self.animarSprite(0.1) * self.tamaño[0], 0, self.tamaño[0], self.tamaño[1]))
        