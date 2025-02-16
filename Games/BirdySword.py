import pygame as pg
import random

from pygame.locals import *
from pygame.sprite import Group
from cte import *


class SpriteSheet:
    def __init__(self, displayData, filename, tamaño, cantidadSprites, chroma):
        
        self.screenSize = displayData[0].get_size()
        self.filename = filename
        self.tamaño = tamaño
        self.cantidadSprites = cantidadSprites

        path = ".GFX/BirdySword/sprites/"

        if chroma:
            self.imagePG = pg.image.load(path + self.filename + ".png").convert()
            self.imagePG.set_colorkey(chroma) 
        else:
            self.imagePG = pg.image.load(path + self.filename + ".png").convert_alpha()
        
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
 
class Espada(pg.sprite.Sprite, SpriteSheet):
    """
    Tamaño Original: 337 x 170 por sprite
    """ 
    def __init__(self, displayData, tamaño, filename="espadas", chroma= None):

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

class Monedas(pg.sprite.Sprite, SpriteSheet):
    """
    Tamaño Original: ¿?
    """ 
    def __init__(self, displayData, tamaño, filename= "monedas",  chroma= AZUL):
        
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData=displayData, filename=filename, tamaño= (102*tamaño, 103*tamaño), cantidadSprites= 6, chroma= chroma) 

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

        if self.rect.x < 0:
            self.rect.topleft = (random.randint(int(self.screenSize[0]), int(self.screenSize[0] * 1.5)), 
                                 random.randint(0, int(self.screenSize[1] - self.tamaño[1])))

class Habilidad(pg.sprite.Sprite, SpriteSheet):
    """
    Tamaño Original: ¿?
    """ 
    def __init__(self, displayData, tamaño, filename= "habilidad", chroma= VERDE):

        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData=displayData, filename=filename, tamaño= (70*tamaño, 64*tamaño), cantidadSprites= 8, chroma= chroma)

        self.FPS = displayData[2]
        self.t_aparicion = 15
        self.velocidadX = -8

        self.rect.topleft = (self.t_aparicion * self.FPS * abs(self.velocidadX), random.randint(0, int(self.screenSize[1] - self.tamaño[1])))
        
        

    
    def update(self):

        self.rect.x += self.velocidadX

        self.loopSpriteSheet()
                   
        if self.rect.x < 0 - self.rect.width:
            self.rect.topleft = (self.t_aparicion * self.FPS * abs(self.velocidadX), random.randint(0, int(self.screenSize[1] - self.tamaño[1])))


class Tuberia(pg.sprite.Sprite, SpriteSheet):
    """
    Tamaño Original: ¿?
    """ 
    def __init__(self, displayData, filename, tipo: str, chroma= None):
        
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, displayData=displayData, filename=filename, 
                             tamaño= (100, 400), cantidadSprites= 1, chroma= chroma) 


        self.apertura= 0.7
        self.tipo = tipo
        if tipo == "bottom":
            self.rect.topleft = (int(self.screenSize[0] * 1.5), 
                                random.randint(int(self.screenSize[1] - self.tamaño[1]), int(self.screenSize[1]*self.apertura)))
        elif tipo == "top":
            self.rect.topleft = (int(self.screenSize[0] * 1.5), 
                                random.randint(int(-self.tamaño[1]*(2-self.apertura)), 0))


        self.velocidadX = -8
 


    def update(self):
        self.rect.x += self.velocidadX 

        if self.rect.x < -self.tamaño[0]:
            if self.tipo == "bottom":
                self.rect.topleft = (int(self.screenSize[0] * 1.5), 
                                random.randint(int(self.screenSize[1] - self.tamaño[1]), int(self.screenSize[1]*0.9)))
            elif self.tipo == "top":
                self.rect.topleft = (int(self.screenSize[0] * 1.5), 
                                random.randint(int(-self.tamaño[1]), 0))


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
            espada = Espada(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="espadas", tamaño=0.3)
            self.espadasG.add(espada)

        for _ in range(0, self.numMonedas):
            moneda = Monedas(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="monedas", tamaño=0.5)  
            self.monedasG.add(moneda)
        
        habilidad =  Habilidad(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="habilidad", tamaño=1.3)
        self.habilidadG.add(habilidad)

        tuberia_bottom = Tuberia(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="tuberiaBottom", tipo="bottom")
        tuberia_top= Tuberia(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="tuberiaTop", tipo="top")
        self.tuberiaG.add(tuberia_bottom)
        self.tuberiaG.add(tuberia_top)

        ############################# CARGA DE IMAGENES #############################
        path = ".GFX/BirdySword/backgrounds/"
        self.fondo = pg.image.load(path + "base" + ".png").convert()
        self.menu = pg.transform.scale(pg.image.load(path + "menu" + ".png").convert(), 
                                       (self.sx, self.sy))


        ############################# CARGA DE CANCIONES #############################
        self.canciones = ['.SFX/dry_hands.mp3',
                          '.SFX/wet_hands.mp3',
                          '.SFX/sweden.mp3',
                          '.SFX/mice_on_venus.mp3']
        

        
    
    def mostrarTexto(self, screen, texto, color, x, y, fuente, tamaño_letra):
        fuente = pg.font.Font(".TTF/" + fuente, tamaño_letra) 
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
            espada = Espada(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="espadas", tamaño=0.3)
            self.espadasG.add(espada)

        ### MONEDAS 
        if pg.sprite.spritecollide(self.jugador, self.monedasG, dokill=True): 
            self.puntuacion += 1 
            moneda = Monedas(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="monedas", tamaño=0.5) 
            self.monedasG.add(moneda)

        ### HABILIDAD        
        if pg.sprite.spritecollide(self.jugador, self.habilidadG, dokill=True):
            habilidad = Habilidad(displayData=(self.screen, self.screen2, self.FPS), 
                             filename="habilidad", tamaño=1.3)
            self.habilidadG.add(habilidad)

            self.inicioHabilidad = pg.time.get_ticks()
            self.tipoHabilidad = random.randint(0,2) 
            self.variableAleatoria = random.randint(1,10)
            
            match(self.tipoHabilidad):
            
                case 0:     # Genera Grupo de Monedas (cantidad aleatoria)
                    for n in range(self.variableAleatoria): 
                        moneda = Monedas(displayData=(self.screen, self.screen2, self.FPS), 
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
            # borrar system32
            pg.quit()

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
        