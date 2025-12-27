import pygame as pg

from screen import Screen


class Main:
    def __init__(self) -> None:
        pg.init()

        self.screen = pg.display.set_mode((1920*0.8, 1080*0.8))
        self.alpha_screen = pg.Surface((int(1920*0.8), int(1080*0.8)), pg.SRCALPHA,)
        self.clock = pg.time.Clock()
        self.FPS = 60

        self.display = Screen(self.screen, self.alpha_screen, self.FPS)


    def mainloop(self):
        while True:
            self.clock.tick(self.FPS)

            self.screen.blit(self.alpha_screen, (0,0))
            
            self.display.mainloop()     
            pg.display.update()
            self.alpha_screen.fill((0, 0, 0, 0)) # screen cleaning

        

juego = Main()
juego.mainloop()
