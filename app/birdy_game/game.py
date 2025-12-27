import random
import sys
import pygame as pg

from pygame.locals import *
from pathlib import Path

from config import *
from .birdy import Birdy
from .coins import Coins
from .pipe import Pipe
from .power_up import PowerUp
from .sword import Sword

    
class BirdyGame:
    def __init__(self, screen, screen2, FPS: int,
                 dificultad) -> None:
        
        self.screen = screen
        self.screen2 = screen2
        self.FPS = FPS

        self.screenSize = self.sx, self.sy = self.screen.get_size()
        
        ############################# PARAMETROS DE JUEGO #############################
        self.dificultad = dificultad
        self.numEspadas = 3 * self.dificultad
        self.numMonedas = 1 * self.dificultad
        self.tTranscurrido = 0


        ############################# Atributos #############################      
        self.x = 0  
        self.puntuacion = 0 
        self.cancion_actual = 0
        
        self.inicioHabilidad = -9999
        self.tipoHabilidad = None
        self.variableAleatoria = None


        ############################# INSTANCIAS Y GRUPOS #############################
        self.jugadorG = pg.sprite.Group()
        self.espadasG = pg.sprite.Group()
        self.monedasG = pg.sprite.Group()
        self.habilidad_monedasG = pg.sprite.Group() 
        self.habilidadG = pg.sprite.Group()
        self.tuberiaG = pg.sprite.Group()

        self.jugador = Birdy(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="Birdy1", tamaño=0.9)
        
        self.jugadorG.add(self.jugador) 

        for _ in range(0, self.numEspadas):
            espada = Sword(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="espadas", tamaño=0.3)
            self.espadasG.add(espada)

        for _ in range(0, self.numMonedas):
            moneda = Coins(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="monedas", tamaño=0.5)  
            self.monedasG.add(moneda)
        
        habilidad =  PowerUp(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="habilidad", tamaño=1.3)
        self.habilidadG.add(habilidad)

        tuberia_bottom = Pipe(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="tuberiaBottom", tipo="bottom")
        tuberia_top= Pipe(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="tuberiaTop", tipo="top")
        self.tuberiaG.add(tuberia_bottom)
        self.tuberiaG.add(tuberia_top)

        ############################# CARGA DE IMAGENES #############################
        gfx_backgrounds_path = Path("app/assets/gfx/backgrounds")
        self.fondo = pg.image.load(gfx_backgrounds_path / ("base" + ".png")).convert()
        self.menu = pg.transform.scale(pg.image.load(gfx_backgrounds_path / ("menu" + ".png")).convert(), 
                                       (self.sx, self.sy))


        ############################# CARGA DE CANCIONES #############################
        sfx_path = Path("app/assets/sfx/")
        self.canciones = [sfx_path / "dry_hands.mp3",
                          sfx_path / "wet_hands.mp3",
                          sfx_path / "sweden.mp3",
                          sfx_path / "mice_on_venus.mp3"]
        

        
    
    def mostrarTexto(self, screen, texto, color, x, y, fuente, tamaño_letra):
        fuente = pg.font.Font(Path("app/assets/ttf/") / fuente, tamaño_letra) 
        superficie = fuente.render(texto, True, color) 
        screen.blit(superficie, (x, y)) 

    def reproducir_cancion(self):
        # FALSE -> No se está reproduciendo una canción
        if not pg.mixer.music.get_busy():  
            self.cancion_actual += -len(self.canciones) if self.cancion_actual >= len(self.canciones)-1 else 1
            pg.mixer.music.load(self.canciones[self.cancion_actual])
            pg.mixer.music.play()           

    def FondoMovimiento(self, fondo):
        x_prima = self.x % fondo.get_rect().width
        self.screen.blit(fondo, (x_prima - fondo.get_rect().width, 0))
        if x_prima < self.sx:
            self.screen.blit(fondo, (x_prima, 0))
        self.x -= 1

    def mainloop(self):
        
        self.tTranscurrido += 1 / self.FPS 

        ############################# LLAMADA DE FUNCIONES - DENTRO DE BUCLE #############################
        self.FondoMovimiento(self.fondo) 

        ################ Colisión: Objeto -> Grupo ################

    #### JUGADOR 
        ### ESPADAS 
        if pg.sprite.spritecollide(self.jugador, self.espadasG, dokill=True):
            self.puntuacion -= 1
            espada = Sword(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="espadas", tamaño=0.3)
            self.espadasG.add(espada)

        ### MONEDAS 
        if pg.sprite.spritecollide(self.jugador, self.monedasG, dokill=True): 
            self.puntuacion += 1 
            moneda = Coins(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="monedas", tamaño=0.5) 
            self.monedasG.add(moneda)

        ### HABILIDAD        
        if pg.sprite.spritecollide(self.jugador, self.habilidadG, dokill=True):
            habilidad = PowerUp(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="habilidad", tamaño=1.3)
            self.habilidadG.add(habilidad)

            self.inicioHabilidad = pg.time.get_ticks()
            self.tipoHabilidad = random.randint(0,2) 
            self.variableAleatoria = random.randint(1,10)
            
            match(self.tipoHabilidad):
            
                case 0:     # Genera Grupo de Monedas (cantidad aleatoria)
                    for n in range(self.variableAleatoria): 
                        moneda = Coins(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="monedas", tamaño=0.5) 
                        self.habilidad_monedasG.add(moneda)
                        print("MONEDA INSTANCIADA")
                
                case 1:     # Suma puntos 
                    self.puntuacion += self.variableAleatoria

                case 2:     # Resta puntos
                    self.puntuacion -= self.variableAleatoria

        # MONEDA HABILIDAD
        if pg.sprite.spritecollide(self.jugador, self.habilidad_monedasG, dokill=True):
            self.puntuacion += 1 
            print("MONEDA INSTANCIADA PILLADA")

        # TUBERÍAS
        if pg.sprite.spritecollide(self.jugador, self.tuberiaG, dokill=False):
            pg.quit()
            sys.exit()

    #### ESPADA 
        #for espada in self.espadasG:
        #    restantes = self.espadasG.copy()
        #    restantes.remove(espada)
        #    if pg.sprite.spritecollide(espada, restantes, True):
        #        self.espadasG.add(Espada(displayData=(self.screen, self.screen2, self.FPS), filename="espadas", tamaño=0.3))

        # Dibujo Habilidad

        if (pg.time.get_ticks() - self.inicioHabilidad) / 1000 < 5:
            habilidadTexto = str(self.variableAleatoria) 
            habilidadColor = (
                VERDE if self.tipoHabilidad == 1 
                else ROJO if self.tipoHabilidad == 2
                else AMARILLO
            )

            self.mostrarTexto(self.screen, habilidadTexto,NEGRO, self.jugador.rect.x + 10, self.jugador.rect.y - 40, 'm04.TTF', 30)
            self.mostrarTexto(self.screen, habilidadTexto, habilidadColor, self.jugador.rect.x + 10, self.jugador.rect.y - 40, 'm04b.TTF', 30)


        ################ Música ################
        self.reproducir_cancion() 
        tecla = pg.key.get_pressed()
        
        # Bajar volumen
        if tecla[pg.K_9] and pg.mixer.music.get_volume() > 0.0:
            pg.mixer.music.set_volume(pg.mixer.music.get_volume()- 0.01)
        #Subir volumen
        if tecla[pg.K_0] and pg.mixer.music.get_volume() < 1.0:
            pg.mixer.music.set_volume(pg.mixer.music.get_volume()+ 0.01)
        # Mutear
        if tecla[pg.K_m]:
            pg.mixer.music.set_volume(0.0)



        ############################# mainloop() Grupos #############################
        self.jugadorG.update()
        self.espadasG.update()
        self.monedasG.update()
        self.habilidad_monedasG.update()
        self.habilidadG.update()
        self.tuberiaG.update()

        ############################# Dibujos #############################
        self.jugadorG.draw(self.screen)
        self.espadasG.draw(self.screen)
        self.monedasG.draw(self.screen)
        self.habilidad_monedasG.draw(self.screen)
        self.habilidadG.draw(self.screen)
        self.tuberiaG.draw(self.screen)
        
        self.mostrarTexto(self.screen, str(self.puntuacion),VERDE3,47, self.sy-80,'Minecraft.ttf',int(self.sy*0.1))
        self.mostrarTexto(self.screen, str(self.puntuacion),BLANCO,40,self.sy-80, 'Minecraft.ttf',int(self.sy*0.1))

        self.mostrarTexto(self.screen, str(round(pg.mixer.music.get_volume(),2)),BLANCO,self.sx*0.95, self.sy-80,'Minecraft.ttf',int(self.sy*0.02))

        self.mostrarTexto(self.screen, '9: BAJAR VOLUMEN',BLANCO,self.sx*0.85, self.sy-40,'Minecraft.ttf',int(self.sy*0.02))
        self.mostrarTexto(self.screen, '0: SUBIR VOLUMEN',BLANCO,self.sx*0.85, self.sy-80,'Minecraft.ttf',int(self.sy*0.02))

        self.mostrarTexto(self.screen,  f"{self.tTranscurrido : .0f}",NEGRO,self.sx//2-int(self.sy*0.08), self.sy * 0.05,'m04.TTF',int(self.sy*0.08))
        self.mostrarTexto(self.screen,  f"{self.tTranscurrido : .0f}",BLANCO,self.sx//2-int(self.sy*0.08), self.sy * 0.05, 'm04b.TTF',int(self.sy*0.08))
        
       

  
    def menuInicial(self):
        
        colorJugar = colorSalir = BLANCO

        self.FondoMovimiento(self.menu)

        espadas = list(self.espadasG)
        self.espada = espadas[0]
        tamaño_espadas = (self.sx * 0.25, self.sy * 0.2)
        
        sprite_sheet = pg.transform.scale(self.espada.imagePG, (tamaño_espadas[0] * 5, tamaño_espadas[1]))   

        image1 = pg.Surface(tamaño_espadas).convert_alpha()
        image2 = pg.Surface(tamaño_espadas).convert_alpha()

        mouseX, mouseY = pg.mouse.get_pos() # Nos devuelve la pos del ratón cuando se hace MOUSEBOTTONDOWN
        
        x1, y1, texto1, tam1 = self.sx*0.12, self.sy*0.6,  "JUGAR", 0
        x2, y2, texto2, tam2 = self.sx*0.59, self.sy*0.6, "SALIR", 0

        tam1 = int(self.sy*0.1) * len(texto1)
        tam2 = int(self.sy*0.1) * len(texto2)

        self.BjugarMenu = (x1, y1, texto1, tam1)
        self.BsalirMenu = (x2, y2, texto2, tam2)


        image1.fill((0,0,0,0))
        image2.fill((0,0,0,0))
        image1.blit(sprite_sheet, (0,0),pg.Rect(0, 0, tamaño_espadas[0], tamaño_espadas[1]))
        image2.blit(sprite_sheet, (0,0),pg.Rect(0, 0, tamaño_espadas[0], tamaño_espadas[1]))

        if x1 < mouseX < x1+tam1 and y1 < mouseY < y1+tam1: # Coordenadas del BOTÓN JUGAR
            image1.fill((0,0,0,0))
            image1.blit(sprite_sheet, (0,0), pg.Rect(self.espada.animarSprite(0.1) * tamaño_espadas[0], 0, tamaño_espadas[0], tamaño_espadas[1]))    
            colorJugar = VERDE

        if x2 < mouseX < x2+tam2 and y2 < mouseY < y2+tam2: # Coordenadas del BOTÓN SALIR
            image2.fill((0,0,0,0))
            image2.blit(sprite_sheet, (0,0), pg.Rect(self.espada.animarSprite(0.1) * tamaño_espadas[0], 0, tamaño_espadas[0], tamaño_espadas[1]))
            colorSalir = ROJO
        
            
        self.screen.blit(pg.transform.rotate(image1, 220), (self.sx*0.1, self.sy*0.40))
        self.screen.blit(pg.transform.rotate(image2, 320), (self.sx*0.6, self.sy*0.40))

        self.mostrarTexto(self.screen,texto1, NEGRO,x1, y1,'m04.TTF', int(self.sy*0.1))
        self.mostrarTexto(self.screen,texto1, colorJugar,x1, y1,'m04b.TTF', int(self.sy*0.1))
                           
        self.mostrarTexto(self.screen,texto2, NEGRO,x2, y2,'m04.TTF', int(self.sy*0.1))
        self.mostrarTexto(self.screen,texto2, colorSalir,x2, y2,'m04b.TTF', int(self.sy*0.1))
        

           
    def menuPausa(self):

        ############################# Texto #############################
        self.mostrarTexto(self.screen,'JUEGO PAUSADO', NEGRO, 90 ,100,'m04.TTF',50)
        self.mostrarTexto(self.screen,'JUEGO PAUSADO', BLANCO, 90 ,100,'m04b.TTF',50)
        
        self.mostrarTexto(self.screen,'PUNTUACION',VERDE3, 450 ,320,'m04.TTF',30)
        self.mostrarTexto(self.screen,'PUNTUACION',VERDE2, 450 ,320,'m04b.TTF',30)

        self.mostrarTexto(self.screen,str(self.puntuacion),VERDE3, 570 ,400,'m04.TTF',30)
        self.mostrarTexto(self.screen,str(self.puntuacion),VERDE2, 570 ,400,'m04b.TTF',30)

        self.mostrarTexto(self.screen,'IR A SPS CLOUD',BLANCO, 105 ,387,'Minecraft.ttf',30)
                      
        ############################# Funciones #############################
        self.FondoMovimiento(self.menu)
        