# app/main.py

import pygame as pg

from screen import Screen
from config import logger


class Main:
    """Core application class that initializes the game engine and manages the main loop.

    This class sets up the Pygame display surfaces, maintains the master clock, 
    and orchestrates the rendering flow between the logical screen and the hardware display.

    Attributes:
        screen (pg.Surface): The primary hardware display surface.
        alpha_screen (pg.Surface): A secondary surface supporting per-pixel alpha for transparency.
        clock (pg.time.Clock): The internal timer for controlling the frame rate.
        FPS (int): The target frames per second for the application.
        display (Screen): The high-level screen manager that handles game logic and drawing.
    """

    def __init__(self) -> None:
        """Initializes Pygame, display surfaces, and the main game controller."""
        pg.init()

        self.screen = pg.display.set_mode((1920*0.8, 1080*0.8))
        self.alpha_screen = pg.Surface((int(1920*0.8), int(1080*0.8)), pg.SRCALPHA,)
        self.clock = pg.time.Clock()
        self.FPS = 60

        self.display = Screen(self.screen, self.alpha_screen, self.FPS)


    def mainloop(self):
        """Executes the infinite game loop and manages frame synchronization.
        
        This method regulates the game speed, triggers the logical updates in 
        the Screen class, blits the alpha layer, and refreshes the display.
        """
        logger.info("Main(): mainloop()...")
        while True:
            self.clock.tick(self.FPS) 

            self.display.mainloop()   
            self.screen.blit(self.alpha_screen, (0,0))
            
            pg.display.update()
            self.alpha_screen.fill((0, 0, 0, 0)) # screen cleaning


if __name__ == "__main__":                                                                      
    game = Main()
    game.mainloop()
        