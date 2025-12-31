# app/screen.py

import pygame as pg
from game import BirdyGame


class Screen:
    """
    La clase 'Screen' se encarga de establecer cada tipo de escenario haciendo uso de 'self.display'.
    Mediante el método 'update()' se establecerá el escenario de la pantalla.
    """

    def __init__(self, screen, alpha_screen, FPS, init_display= "birdy_menu"):
        """
        En el constructor de la clase 'Screen' se inicializan varios atributos y 
        se crean las instancias de todos los ajustes de cada juego creado.
        """


        self.screen = screen             
        self.screen2 = alpha_screen
        self.FPS = FPS
        self.display = init_display

        ############################# Instancias #############################
        self.birdyGame = BirdyGame(screen, alpha_screen, self.FPS, difficulty= 2)

        
    def mainloop(self):
        """
        Utilizado del mainloop() del fichero main.py
        Controla todas las interacciones que el usuario realiza mediante el uso de pg.event.get()
        """

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()

# *EVENTO* #######################        BirdySword mainloop()       ###################################
            if self.display == "birdy_main":

                #Evento de tipo Click Izquierdo
                #if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                #    mouseX, mouseY = pg.mouse.get_pos()
                #    self.birdyGame.jugador.jump()

                #Evento tipo PresionarTecla
                if event.type == pg.KEYDOWN:
                #    if event.key == pg.K_SPACE:
                #        self.birdyGame.jugador.jump()
                    if event.key == pg.K_ESCAPE:
                        self.display = "birdy_menu"
                
# *EVENTO* #######################        BirdySword menuInicial()       ###################################
            elif self.display == "birdy_menu":
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pg.mouse.get_pos()

                    x1, y1, texto1, tam1 = self.birdyGame.menu_play_button 
                    x2, y2, texto2, tam2 = self.birdyGame.menu_exit_button

                    if x1 < mouseX < x1+tam1 and y1 < mouseY < y1+tam1: # Coordenadas del BOTÓN JUGAR
                        self.display = "birdy_main"

                    if x2 < mouseX < x2+tam2 and y2 < mouseY < y2+tam2:
                        pass

# *EVENTO* #######################        BirdySword menuPausa()       ###################################
            elif self.display == "birdy_pause":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:    
                        self.display = "birdy_main"

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pg.mouse.get_pos()

                    x1, y1, texto1, tam1 = self.birdyGame.menu_play_button
                    x2, y2, texto2, tam2 = self.birdyGame.menu_exit_button

                    if x1 < mouseX < x1+tam1 and y1 < mouseY < y1+tam1: # BOTÓN JUGAR
                        self.display = "birdy_main"
                    if x2 < mouseX < x2+tam2 and y2 < mouseY < y2+tam2: # BOTÓN SALIR
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