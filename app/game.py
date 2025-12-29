import random
import sys
import numpy as np
import pygame as pg

from pygame.locals import *
from pathlib import Path

from utils import Utils
from ai import Evolution
from config import *
from sprites import *

    
class BirdyGame:
    def __init__(self, screen, screen_alpha, FPS: int, dificulty, training=True) -> None:
        
        self.screen = screen
        self.screen_alpha = screen_alpha
        self.FPS = FPS

        self.screen_size = self.screen_x, self.screen_y = self.screen.get_size()
        
        ############################# GAME PARAMETERS #############################
        self.difficulty = dificulty
        self.num_swords = 3 * self.difficulty
        self.num_coins = 1 * self.difficulty
        self.t_elapsed = 0


        ############################# Atributes #############################      
        self.training = training
        self.x = 0  
        self.current_song = 0
        
        self.debug_colors = {
            "pipe": GREEN3,
            "coin": YELLOW,
            "sword": RED,
            "powerup": (0, 255, 255),    # Cyan
        }

        self.fitness_dict = {
            "alive": 1,
            "coin": 100,
            "sword": 250,
            "powerup": 500,   
        }


        ############################# INSTANCES AND GROUPS #############################
        self.playerG = pg.sprite.Group()
        self.swordsG = pg.sprite.Group()
        self.coinsG = pg.sprite.Group()
        self.powerupG = pg.sprite.Group()
        self.pipeG = pg.sprite.Group()

        self.utils = Utils()

        ################## AI
        self.training = { # POS_SIZE: TRAINING_SPEED
            500: 1,
            200: 2,
            100: 5,
            50: 10,
            20: 50
        }
        self.training_speed = 2
        self.pop_size = 200
        self.evolution_manager = Evolution(pop_size=self.pop_size)
        for i in range(self.pop_size):
            new_birdy = Birdy(
                brain=self.evolution_manager.population[i],
                displayData=(self.screen, self.screen_alpha, self.FPS), filename="birdy_learner", tamaño=0.9
            )
            self.playerG.add(new_birdy)
        ####################

        for _ in range(0, self.num_swords):
            sword = Sword(displayData=(self.screen, self.screen_alpha, self.FPS), 
                             filename="swords", tamaño=0.3)
            self.swordsG.add(sword)

        for _ in range(0, self.num_coins):
            moneda = Coins(displayData=(self.screen, self.screen_alpha, self.FPS), 
                             filename="coins", tamaño=0.5)  
            self.coinsG.add(moneda)
        
        habilidad = PowerUp(displayData=(self.screen, self.screen_alpha, self.FPS), 
                             filename="power_up", tamaño=1.3)
        self.powerupG.add(habilidad)

        tuberia_bottom = Pipe(displayData=(self.screen, self.screen_alpha, self.FPS), 
                             filename="bottom_pipe", tipo="bottom")
        tuberia_top = Pipe(displayData=(self.screen, self.screen_alpha, self.FPS), 
                             filename="top_pipe", tipo="top")
        self.pipeG.add(tuberia_bottom)
        self.pipeG.add(tuberia_top)

        ############################# GFX IMAGE LOAD #############################
        gfx_backgrounds_path = Path("app/assets/gfx/backgrounds")
        self.fondo = pg.image.load(gfx_backgrounds_path / ("base" + ".png")).convert()
        self.img_menu = pg.transform.scale(pg.image.load(gfx_backgrounds_path / ("menu" + ".png")).convert(), 
                                       (self.screen_x, self.screen_y))


        ############################# SFX SONGS LOAD #############################
        sfx_path = Path("app/assets/sfx/")
        self.canciones = [sfx_path / "dry_hands.mp3",
                          sfx_path / "wet_hands.mp3",
                          sfx_path / "sweden.mp3",
                          sfx_path / "mice_on_venus.mp3"]
        
        
        
    ############################# GAME METHODS #############################

    def _show_text(self, screen, text, color, x, y, font, font_size):
        font = pg.font.Font(Path("app/assets/ttf/") / font, font_size) 
        superficie = font.render(text, True, color) 
        screen.blit(superficie, (x, y)) 

    def _play_song(self):
        if not pg.mixer.music.get_busy():  
            self.current_song += -len(self.canciones) if self.current_song >= len(self.canciones)-1 else 1
            pg.mixer.music.load(self.canciones[self.current_song])
            pg.mixer.music.play()           

    def _animate_background(self, fondo):
        x_prima = self.x % fondo.get_rect().width
        self.screen.blit(fondo, (x_prima - fondo.get_rect().width, 0))
        if x_prima < self.screen_x:
            self.screen.blit(fondo, (x_prima, 0))
        self.x -= 1

    def _reset_sprites_offscreen(self):
        ############################# SPRITES RESET #############################
        for group, sprite_class, filename, size in [
            (self.swordsG, Sword, "swords", 0.3),
            (self.coinsG, Coins, "coins", 0.5),
            (self.powerupG, PowerUp, "power_up", 1.3)
        ]:
            for obj in list(group):
                if obj.rect.right < 0: 
                    obj.kill()
                    new_obj = sprite_class(displayData=(self.screen, self.screen_alpha, self.FPS), filename=filename, tamaño=size)
                    group.add(new_obj)


    def _handle_logic_collisions(self):
        ################ Colisión: Objeto -> Grupo ################
        for bird in list(self.playerG): # Iteramos sobre una copia del grupo para poder eliminar individuos sin romper el loop

            ##### SINGLE PLAYER
            if not self.training:
                for group, key, cls, size in [
                    (self.swordsG, "sword",   Sword,   0.3),
                    (self.coinsG,  "coin",    Coins,   0.5),
                    (self.powerupG,"powerup", PowerUp, 1.3),
                ]:
                    if pg.sprite.spritecollide(bird, group, dokill=True):
                        group.add(cls(
                                displayData=(self.screen, self.screen_alpha, self.FPS),
                                filename=key if key != "powerup" else "power_up",
                                tamaño=size)
                        )

            
            ##### TRAINING
            else:
                bird.hit_items = {item for item in bird.hit_items if item.alive()}

                for group, key in [(self.swordsG, "sword"), (self.coinsG, "coin"), (self.powerupG, "powerup")]:
                    hits = pg.sprite.spritecollide(bird, group, dokill=False)
                    for item in hits:
                        if item not in bird.hit_items:
                            if key == "sword":
                                bird.brain.fitness -= self.fitness_dict[key]
                            else:
                                bird.brain.fitness += self.fitness_dict[key]
                            bird.hit_items.add(item)
                           

            if pg.sprite.spritecollide(bird, self.pipeG, dokill=False):
                bird.kill()

    def _draw_telemetry(self, bird, inputs, fast_mode):
        """Dibuja los datos técnicos en pantalla."""
        info = [
            f"MODO RAPIDO: {f'SI (x{self.training_speed})' if fast_mode else 'NO'}",
            f"Generacion: {self.evolution_manager.generation}",
            f"Individuos Vivos: {len(self.playerG)}",
            f"Fitness Lider: {bird.brain.fitness}",
            f"Velocidad Y: {bird.speed_y:.2f}"
        ]
        for i, text in enumerate(info):
            color = YELLOW if "RAPIDO" in text and fast_mode else WHITE
            self._show_text(self.screen, text, BLACK, 10, 10 + (i * 20), "m04.ttf", 15)
            self._show_text(self.screen, text, color, 10, 10 + (i * 20), "m04b.ttf", 15)

    ############################# GAME LOOPS #############################

    def mainloop(self, fast_forward):
        steps = self.training_speed if (fast_forward) else 1
        
        for _ in range(steps):
            self.t_elapsed += 1 / self.FPS 
            if (fast_forward): self.x -= 1

            ################ AI ################
            # Cada pájaro vivo toma una decisión basada en su red neuronal
            for bird in self.playerG:
                inputs, _ = self.get_ia_data(bird)                                 
                if bird.brain.forward(x=inputs):
                    bird.jump()
                bird.brain.fitness += self.fitness_dict["alive"]

            ################ COLLISIONS ################
            self._handle_logic_collisions()

            ############################# mainloop() Grupos #############################
            self.playerG.update()
            self.swordsG.update()
            self.coinsG.update()
            self.powerupG.update()
            self.pipeG.update()

            self._reset_sprites_offscreen()
            
            if len(self.playerG) == 0:
                self.next_generation() 
                break

        
        ################ Música ################
        self._play_song() 
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




        ############################# Dibujos #############################
        self._animate_background(self.fondo) 

        self.playerG.draw(self.screen)
        self.swordsG.draw(self.screen)
        self.coinsG.draw(self.screen)
        self.powerupG.draw(self.screen)
        self.pipeG.draw(self.screen)
        
        if len(self.playerG) > 0:
            main_birdy = self.playerG.sprites()[0]
            inputs, targets = self.get_ia_data(main_birdy)

            self._draw_telemetry(main_birdy, inputs, fast_forward)

            # NeuralNetwork Draw
            net_pos_x = self.screen_x * 0.05
            net_pos_y = self.screen_y * 0.6
            self.utils.draw_network(self.screen, main_birdy,net_pos_x, net_pos_y, inputs)


            # Debug Line Draw
            for key, color in self.debug_colors.items():
                target_pos = targets.get(key)
                if target_pos:
                    self.utils.draw_debug_line(self.screen, main_birdy.rect.center, target_pos, color=color)
                    

        self._show_text(self.screen, str(round(pg.mixer.music.get_volume(),2)),WHITE,self.screen_x*0.95, self.screen_y-80,'Minecraft.ttf',int(self.screen_y*0.02))

        self._show_text(self.screen, '9: BAJAR VOLUMEN',WHITE,self.screen_x*0.85, self.screen_y-40,'Minecraft.ttf',int(self.screen_y*0.02))
        self._show_text(self.screen, '0: SUBIR VOLUMEN',WHITE,self.screen_x*0.85, self.screen_y-80,'Minecraft.ttf',int(self.screen_y*0.02))

        self._show_text(self.screen,  f"{self.t_elapsed : .0f}",BLACK,self.screen_x//2-int(self.screen_y*0.08), self.screen_y * 0.05,'m04.ttf',int(self.screen_y*0.08))
        self._show_text(self.screen,  f"{self.t_elapsed : .0f}",WHITE,self.screen_x//2-int(self.screen_y*0.08), self.screen_y * 0.05, 'm04b.ttf',int(self.screen_y*0.08))
       
    def menuloop(self):
        
        colorJugar = colorSalir = WHITE

        self._animate_background(self.img_menu)

        espadas = list(self.swordsG)
        self.sword = espadas[0]
        tamaño_espadas = (self.screen_x * 0.25, self.screen_y * 0.2)
        
        sprite_sheet = pg.transform.scale(self.sword.imagePG, (tamaño_espadas[0] * 5, tamaño_espadas[1]))   

        image1 = pg.Surface(tamaño_espadas).convert_alpha()
        image2 = pg.Surface(tamaño_espadas).convert_alpha()

        mouseX, mouseY = pg.mouse.get_pos() # Nos devuelve la pos del ratón cuando se hace MOUSEBOTTONDOWN
        
        x1, y1, texto1, tam1 = self.screen_x*0.12, self.screen_y*0.6,  "JUGAR", 0
        x2, y2, texto2, tam2 = self.screen_x*0.59, self.screen_y*0.6, "SALIR", 0

        tam1 = int(self.screen_y*0.1) * len(texto1)
        tam2 = int(self.screen_y*0.1) * len(texto2)

        self.BjugarMenu = (x1, y1, texto1, tam1)
        self.BsalirMenu = (x2, y2, texto2, tam2)


        image1.fill((0,0,0,0))
        image2.fill((0,0,0,0))
        image1.blit(sprite_sheet, (0,0),pg.Rect(0, 0, tamaño_espadas[0], tamaño_espadas[1]))
        image2.blit(sprite_sheet, (0,0),pg.Rect(0, 0, tamaño_espadas[0], tamaño_espadas[1]))

        if x1 < mouseX < x1+tam1 and y1 < mouseY < y1+tam1: # Coordenadas del BOTÓN JUGAR
            image1.fill((0,0,0,0))
            image1.blit(sprite_sheet, (0,0), pg.Rect(self.sword.animarSprite(0.1) * tamaño_espadas[0], 0, tamaño_espadas[0], tamaño_espadas[1]))    
            colorJugar = GREEN1

        if x2 < mouseX < x2+tam2 and y2 < mouseY < y2+tam2: # Coordenadas del BOTÓN SALIR
            image2.fill((0,0,0,0))
            image2.blit(sprite_sheet, (0,0), pg.Rect(self.sword.animarSprite(0.1) * tamaño_espadas[0], 0, tamaño_espadas[0], tamaño_espadas[1]))
            colorSalir = RED
        
            
        self.screen.blit(pg.transform.rotate(image1, 220), (self.screen_x*0.1, self.screen_y*0.40))
        self.screen.blit(pg.transform.rotate(image2, 320), (self.screen_x*0.6, self.screen_y*0.40))

        self._show_text(self.screen,texto1, BLACK,x1, y1,'m04.ttf', int(self.screen_y*0.1))
        self._show_text(self.screen,texto1, colorJugar,x1, y1,'m04b.ttf', int(self.screen_y*0.1))
                           
        self._show_text(self.screen,texto2, BLACK,x2, y2,'m04.ttf', int(self.screen_y*0.1))
        self._show_text(self.screen,texto2, colorSalir,x2, y2,'m04b.ttf', int(self.screen_y*0.1))
                  
    def pauseloop(self):

        ############################# Texto #############################
        self._show_text(self.screen,'JUEGO PAUSADO', BLACK, 90 ,100,'m04.ttf',50)
        self._show_text(self.screen,'JUEGO PAUSADO', WHITE, 90 ,100,'m04b.ttf',50)
        
        self._show_text(self.screen,'PUNTUACION',GREEN3, 450 ,320,'m04.ttf',30)
        self._show_text(self.screen,'PUNTUACION',GREEN2, 450 ,320,'m04b.ttf',30)

        self._show_text(self.screen,'IR A SPS CLOUD',WHITE, 105 ,387,'Minecraft.ttf',30)
                      
        ############################# Funciones #############################
        self._animate_background(self.img_menu)
        

    ############################# AI #############################
    def get_ia_data(self, bird: Birdy):
        def get_nearest_object_data(sprite_group):
            candidates = [obj for obj in sprite_group if obj.rect.right > bird.rect.left]
            if candidates:
                nearest = min(candidates, key=lambda obj: obj.rect.left)
                dist_x = (nearest.rect.left - bird.rect.left) / self.screen_x
                dist_y = (nearest.rect.centery - bird.rect.centery) / self.screen_y
                return dist_x, dist_y, nearest.rect.center # Retornamos posición real también
            return 1.0, 0.0, None


        coin_x, coin_y, coin_pos = get_nearest_object_data(self.coinsG)
        pw_x, pw_y, pw_pos = get_nearest_object_data(self.powerupG)
        sw_x, sw_y, sw_pos = get_nearest_object_data(self.swordsG)

        pipes_ahead = [p for p in self.pipeG if p.rect.right > bird.rect.left]
        p_x, p_y = 1.0, 0.0
        pipe_target = None

        if len(pipes_ahead) >= 2:
            pipes_ahead.sort(key=lambda p: p.rect.left)
            p1, p2 = pipes_ahead[0], pipes_ahead[1]
            gap_y = (p1.rect.top + p2.rect.bottom) / 2 if p1.tipo == "bottom" else (p1.rect.bottom + p2.rect.top) / 2
            p_x = (p1.rect.left - bird.rect.left) / self.screen_x
            p_y = (gap_y - bird.rect.centery) / self.screen_y
            pipe_target = (p1.rect.left, gap_y)

        inputs = np.array([
            p_x, p_y, coin_x, coin_y, pw_x, pw_y, 
            sw_x, sw_y, bird.speed_y / bird.max_speed_y
        ])

        # Devolvemos un diccionario con las posiciones para dibujar las líneas
        targets = {
            "pipe": pipe_target,
            "coin": coin_pos,
            "powerup": pw_pos,
            "sword": sw_pos
        }

        return inputs, targets

    def next_generation(self):
        self.evolution_manager.restart_generation()
        self.reset_game_state()
        
        # New Population with Better Brains
        for i in range(self.pop_size):
            filename = "birdy_parent" if i == 0 else "birdy_learner"
            new_birdy = Birdy(
                brain=self.evolution_manager.population[i],
                displayData=(self.screen, self.screen_alpha, self.FPS), filename=filename, tamaño=0.9
            )
            self.playerG.add(new_birdy)

    def reset_game_state(self):
        self.t_elapsed = 0
        self.x = 0
        
        self.swordsG.empty()
        self.coinsG.empty()
        self.powerupG.empty()
        self.pipeG.empty()

        
        for _ in range(self.num_swords):
            self.swordsG.add(Sword(displayData=(self.screen, self.screen_alpha, self.FPS), filename="swords", tamaño=0.3))

        for _ in range(self.num_coins):
            self.coinsG.add(Coins(displayData=(self.screen, self.screen_alpha, self.FPS), filename="coins", tamaño=0.5))
        
        self.powerupG.add(PowerUp(displayData=(self.screen, self.screen_alpha, self.FPS), filename="power_up", tamaño=1.3))
        self.pipeG.add(Pipe(displayData=(self.screen, self.screen_alpha, self.FPS), filename="bottom_pipe", tipo="bottom"))
        self.pipeG.add(Pipe(displayData=(self.screen, self.screen_alpha, self.FPS), filename="top_pipe", tipo="top"))
        
        
    