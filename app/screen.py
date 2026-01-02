# app/screen.py

import pygame as pg
from game import BirdyGame


class Screen:
    """Manages the application states and scene transitions using the display attribute.

    This class acts as a state machine that orchestrates the switching between 
    the menu, the active game, and the pause screens, delegating the logic 
    to the respective game instances.

    Attributes:
        screen (pg.Surface): The primary display surface.
        screen2 (pg.Surface): An auxiliary surface for alpha/transparency effects.
        FPS (int): The operational frames per second of the application.
        display (str): A string identifier for the current active scene.
        birdyGame (BirdyGame): The main game logic instance.
    """

    def __init__(self, screen, alpha_screen, FPS, init_display="birdy_menu"):
        """Initializes the Screen controller with display surfaces and game instances.

        Args:
            screen (pg.Surface): The main window surface for rendering.
            alpha_screen (pg.Surface): A secondary surface for transparency effects.
            FPS (int): The target frames per second for the simulation.
            init_display (str, optional): The starting state of the application. 
                                          Defaults to "birdy_menu".
        """
        self.screen = screen             
        self.screen2 = alpha_screen
        self.FPS = FPS
        self.display = init_display

        ############################# Instancias #############################
        self.birdyGame = BirdyGame(screen, alpha_screen, self.FPS, difficulty=2)

        
    def mainloop(self):
        """Orchestrates the application flow, event handling, and state transitions.

        This method acts as the central hub for the Pygame event loop, delegating 
        input processing and rendering calls based on the current 'display' state. 
        It handles transitions between the main game, menu, and pause screens.

        NOTE:
            It monitors keyboard and mouse events to trigger game actions or 
            UI interactions like button clicks.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()

# *EVENTO* #######################        BirdySword mainloop()       ###################################
            if self.display == "birdy_main":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.display = "birdy_menu"
                
# *EVENTO* #######################        BirdySword menuloop()       ###################################
            elif self.display == "birdy_menu":
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pg.mouse.get_pos()

                    x1, y1, text1, tam1 = self.birdyGame.menu_play_button 
                    x2, y2, text2, tam2 = self.birdyGame.menu_exit_button

                    if x1 < mouseX < x1+tam1 and y1 < mouseY < y1+tam1: # Play Button
                        self.display = "birdy_main"

                    if x2 < mouseX < x2+tam2 and y2 < mouseY < y2+tam2: # Exit Button
                        pass

# *EVENTO* #######################        BirdySword pauseloop()       ###################################
            elif self.display == "birdy_pause":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:    
                        self.display = "birdy_main"

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pg.mouse.get_pos()

                    x1, y1, texto1, tam1 = self.birdyGame.menu_play_button
                    x2, y2, texto2, tam2 = self.birdyGame.menu_exit_button

                    if x1 < mouseX < x1+tam1 and y1 < mouseY < y1+tam1: # Play Button
                        self.display = "birdy_main"
                    if x2 < mouseX < x2+tam2 and y2 < mouseY < y2+tam2: # Exit Button
                        pass


# *BUCLE* #######################        BirdySword mainloop()        ###################################
        if self.display == "birdy_main":
            keys = pg.key.get_pressed()
            fast_mode = keys[pg.K_TAB]

            self.birdyGame.mainloop(fast_forward=(not fast_mode))

# *BUCLE* #######################        BirdySword menuloop()        ###################################
        if self.display == "birdy_menu":
            self.birdyGame.menuloop()
# *BUCLE* #######################        BirdySword pauseloop()        ###################################
        if self.display == "birdy_pause":
            self.birdyGame.pauseloop()