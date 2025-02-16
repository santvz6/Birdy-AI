import pygame as pg
from Pantalla import Pantalla


class Main:
    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((1920*0.8, 1080*0.8))
        self.screen2 = pg.Surface((int(1920*0.8), int(1080*0.8)), pg.SRCALPHA,)
        self.clock = pg.time.Clock()
        self.FPS = 60


        self.display = Pantalla(self.screen, self.screen2, self.FPS)


    def mainloop(self):
        while True:
            self.clock.tick(self.FPS)

            self.screen.blit(self.screen2, (0,0))
            
            self.display.mainloop()         # Hacemos los cálculos para el dibujo
            pg.display.update()
            self.screen2.fill((0, 0, 0, 0)) # Limpiamos screen2

        

juego = Main()
juego.mainloop()
