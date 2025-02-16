import pygame as pg
import sys

# Ficheros
import cte

from Games.BirdySword import BirdyGame

class Pantalla:
    """
    La clase 'Pantalla' se encarga de establecer cada tipo de escenario haciendo uso de 'self.cambio_pantalla'.
    Mediante el método 'update()' se establecerá el escenario de la pantalla.
    """

    def __init__(self, screen, screen2, FPS, displayInicial= "birdyMenu"):
        """
        En el constructor de la clase 'Pantalla' se inicializan varios atributos y 
        se crean las instancias de todos los ajustes de cada juego creado.
        """


        self.screen = screen             
        self.screen2 = screen2
        self.FPS = FPS
        self.display = displayInicial

        ############################# Instancias #############################
        self.birdyGame = BirdyGame(screen, screen2, self.FPS, dificultad= 2)

        
    def mainloop(self):
        """
        Utilizado del mainloop() del fichero main.py
        Controla todas las interacciones que el usuario realiza mediante el uso de pg.event.get()
        """

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()

# *EVENTO* #######################        BirdySword mainloop()       ###################################
            if self.display == "birdyMain":

                #Evento de tipo Click Izquierdo
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pg.mouse.get_pos()
                    self.birdyGame.jugador.saltar(-10)

                #Evento tipo PresionarTecla
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.birdyGame.jugador.saltar(-10)
                    if event.key == pg.K_ESCAPE:
                        self.display = "birdyMenu"

# *EVENTO* #######################        BirdySword menuInicial()       ###################################
            elif self.display == "birdyMenu":
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pg.mouse.get_pos()

                    x1, y1, texto1, tam1 = self.birdyGame.BjugarMenu 
                    x2, y2, texto2, tam2 = self.birdyGame.BsalirMenu

                    if x1 < mouseX < x1+tam1 and y1 < mouseY < y1+tam1: # Coordenadas del BOTÓN JUGAR
                        self.display = "birdyMain"

                    if x2 < mouseX < x2+tam2 and y2 < mouseY < y2+tam2:
                        pass

# *EVENTO* #######################        BirdySword menuPausa()       ###################################
            elif self.display == "birdyPausa":
                if event.key == pg.K_ESCAPE:    
                    self.display = "birdyMain"

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pg.mouse.get_pos()

                    x1, y1, texto1, tam1 = self.birdyGame.BjugarMenu
                    x2, y2, texto2, tam2 = self.birdyGame.BsalirMenu

                    if x1 < mouseX < x1+tam1 and y1 < mouseY < y1+tam1: # BOTÓN JUGAR
                        self.display = "birdyMain"
                    if x2 < mouseX < x2+tam2 and y2 < mouseY < y2+tam2: # BOTÓN SALIR
                        pass


# *BUCLE* #######################        BirdySword mainloop()        ###################################
        if self.display == "birdyMain":
            self.birdyGame.mainloop()

# *BUCLE* #######################        BirdySword menuInicial()        ###################################
        if self.display == "birdyMenu":
            self.birdyGame.menuInicial()
# *BUCLE* #######################        BirdySword menuPausa()        ###################################
        if self.display == "birdyPausa":
            self.birdyGame.menuPausa()