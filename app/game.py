# app/game.py

import pygame as pg

from pygame.locals import *
from pathlib import Path

from utils import Utils
from ai import Evolution, NeuralNetwork
from config import *
from sprites import *

import numpy as np
try:
    import cupy as cp
    HAS_GPU = True
    as_numpy = cp.asnumpy
    
except ImportError:
    HAS_GPU = False
    as_numpy = lambda x: x
    

import time
class BirdyGame:
    """Manages the main game logic, vectorized AI population, and physics.

    This class coordinates the interaction between the environment (pipes, items)
    and a massive population of birds using NumPy for high-performance calculations.

    Attributes:
        screen (pg.Surface): The primary display surface.
        screen_alpha (pg.Surface): Transparent surface for debug and overlay drawing.
        pop_size (int): Total number of bird agents in the simulation (e.g., 50,000).
        evolution_manager (Evolution): Handles genetic algorithms and weight matrices.
        bird_y (self.xp.ndarray): Array of vertical positions for the entire population.
        bird_vel (self.xp.ndarray): Array of vertical velocities for the entire population.
        bird_alive (self.xp.ndarray): Boolean mask indicating which birds are still active.
        fitness_array (self.xp.ndarray): Cumulative performance score for each agent.
        hit_matrix (self.xp.ndarray): Tracks item collection to prevent double scoring.
    """

    def __init__(self, screen, screen_alpha, FPS:int, difficulty, training=True) -> None:
        """Initializes the game state, item groups, and AI population.

        Args:
            screen (pg.Surface): Main window surface.
            screen_alpha (pg.Surface): Transparent overlay surface.
            FPS (int): Target frames per second.
            dificulty (int): Multiplier for the number of obstacles and items.
            training (bool, optional): Whether the game is in AI training mode. Defaults to True.
        """

        # Arguments
        self.screen = screen
        self.screen_alpha = screen_alpha
        self.FPS = FPS
        self.difficulty = difficulty
        self.training = training

        # Attributes
        self.screen_size = self.screen_x, self.screen_y = self.screen.get_size()
        self.utils = Utils()



        ############################# GAME PARAMETERS #############################
        self.t_elapsed = 0
        self.current_song = 0
        self.x = 0  
       
        self.num_swords = 3 * self.difficulty
        self.num_coins = 1 * self.difficulty
        self.num_powerups = 1
        self.total_items = self.num_swords + self.num_coins + self.num_powerups
         
        self.hitboxes = False

        self.enable_fast_mode = True
        self.training_speed = 2
        
        self.pop_size = 1_000
        self.num_visual_birds = min(25 if HAS_GPU else 100, self.pop_size)

        if self.pop_size <= 10_000:
            import numpy as np
            self.xp = np
            device = "cpu"
            logger.info("Utilizando CPU (NumPy)")
        else:
            import cupy as cp
            self.xp = cp
            device = "cuda"
            logger.info("Utilizando GPU (CuPy)")
            

        self.debug_colors = {
            "pipe": RED,
            "coin": YELLOW,
            "sword": CYAN,
            "powerup": MAGENTA,   
        }

        self.fitness_dict = {
            "alive": 1,
            "coin": 50,
            "sword": 175,
            "powerup": 350,   
        }

        ############################# INSTANCES AND GROUPS #############################
        self.playerG: list[Birdy]       = pg.sprite.Group()
        self.swordsG: list[Sword]       = pg.sprite.Group()
        self.coinsG: list[Coins]        = pg.sprite.Group()
        self.powerupG: list[PowerUp]    = pg.sprite.Group()
        self.pipeG: list[Pipe]          = pg.sprite.Group()


        ################### BIRD INSTANCES (numpy vectorization)
        self.evolution_manager = Evolution(pop_size=self.pop_size, device=device)

        self.all_w1 = self.evolution_manager.w1
        self.all_w2 = self.evolution_manager.w2
        self.all_w3 = self.evolution_manager.w3

        # We do not use "self.population" Birdy() instances
        # We use xp.arrays(), each index as an instance
        self.bird_y     = self.xp.full(self.pop_size, self.screen_y / 2, dtype=self.xp.float32)
        self.bird_speed = self.xp.zeros(self.pop_size,                   dtype=self.xp.float32)
        self.bird_alive = self.xp.ones(self.pop_size,                    dtype=bool)

        self.hit_matrix     = self.xp.zeros((self.pop_size, self.total_items), dtype=bool) # for each bird each item collision
        self.fitness_array  = self.xp.zeros(self.pop_size, dtype=self.xp.float32)
        ####################


        ############################# ITEM INSTANCES #############################
        for i in range(self.num_visual_birds):
            new_birdy = Birdy(display_data=(self.screen, self.screen_alpha, self.FPS), filename="birdy_learner")
            self.playerG.add(new_birdy)

        for i in range(0, self.num_swords):
            sword = Sword(display_data=(self.screen, self.screen_alpha, self.FPS), filename="swords", scale=0.3)
            sword.item_id = i
            self.swordsG.add(sword)

        for i in range(0, self.num_coins):
            coin = Coins(display_data=(self.screen, self.screen_alpha, self.FPS), filename="coins", scale=0.5)
            coin.item_id = self.num_swords + i
            self.coinsG.add(coin)
        
        for i in range (0, self.num_powerups):
            powerup = PowerUp(display_data=(self.screen, self.screen_alpha, self.FPS), filename="power_up", scale=1.3)
            powerup.item_id = self.num_swords + self.num_coins + i
            self.powerupG.add(powerup)

        bottom_pipe = Pipe(display_data=(self.screen, self.screen_alpha, self.FPS), filename="bottom_pipe", type="bottom")
        top_pipe    = Pipe(display_data=(self.screen, self.screen_alpha, self.FPS), filename="top_pipe", type="top")
        self.pipeG.add(bottom_pipe)
        self.pipeG.add(top_pipe)


        ############################# GFX BACKGROUND IMAGE LOAD #############################
        gfx_backgrounds_path = Path("app/assets/gfx/backgrounds")
        self.background_img = pg.image.load(gfx_backgrounds_path / ("base" + ".png")).convert()
        self.menu_img = pg.transform.scale(pg.image.load(gfx_backgrounds_path / ("menu" + ".png")).convert(), 
                                       (self.screen_x, self.screen_y))


        ############################# SFX SONGS LOAD #############################
        sfx_path = Path("app/assets/sfx/")
        self.songs = [sfx_path / "dry_hands.mp3",
                          sfx_path / "wet_hands.mp3",
                          sfx_path / "sweden.mp3",
                          sfx_path / "mice_on_venus.mp3"]
        


    ############################# GAME LOOPS #############################
    def mainloop(self, fast_forward:bool) -> None:
        """Executes the core game loop including AI, physics, and rendering.

        This method handles the 'steps' logic for fast-forwarding, processes
        neural network inferences, updates bird physics, detects collisions,
        and draws all elements to the screen.

        Args:
            fast_forward (bool): If True, runs multiple physics steps per frame and scrolls faster.
        """
        steps = self.training_speed if (fast_forward and self.enable_fast_mode) else 1
        for _ in range(steps):
            self.t_elapsed += 1 / self.FPS 
            if (fast_forward and self.enable_fast_mode and self.training_speed > 1): self.x -= 1

            ################ OPTIMIZATION ################
            mask_alive = self.bird_alive
            idx_alive = self.xp.where(mask_alive)[0]
            if len(idx_alive) == 0:
                self.next_generation()
                break

            ################ AI ################
            inputs_matrix, nearest_objects = self.get_all_inputs_vectorized(idx_alive) # NOTE: !!!
            decisions = self.evolution_manager.brain.forward(inputs_matrix, idx_alive) # NOTE: !!!

            # Physics: old Birdy.update()
            self.bird_speed[idx_alive] += Birdy.acc_y
            self.bird_speed[idx_alive[decisions]] = Birdy.jump
            self.bird_speed[idx_alive] = self.xp.clip(self.bird_speed[idx_alive], -Birdy.max_speed_y, Birdy.max_speed_y)
            self.bird_y[idx_alive] += self.bird_speed[idx_alive]

            self.fitness_array[idx_alive] += self.fitness_dict["alive"]

            ################ COLLISIONS ################
            self._detect_item_collisions(idx_alive) # NOTE: !!!

            # Pipe Collisions
            birds_x = self.screen_x // 3
            for pipe in self.pipeG:
                if pipe.rect.left < birds_x + Birdy.size[0] and pipe.rect.right > birds_x:
                    y_alive = self.bird_y[idx_alive]
                    if pipe.type == "bottom":
                        dead_mask = y_alive > pipe.rect.top
                    else:
                        dead_mask = y_alive < pipe.rect.bottom
                    
                    if self.xp.any(dead_mask):
                        self.bird_alive[idx_alive[dead_mask]] = False
                        idx_alive = idx_alive[~dead_mask] # update idx_alive locally


            ################ LOW FITNESS ################
            MIN_FITNESS = -1000 
            low_fitness = self.fitness_array[idx_alive] < MIN_FITNESS

            if self.xp.any(low_fitness):
                self.bird_alive[idx_alive[low_fitness]] = False
                idx_alive = idx_alive[~low_fitness]


            ############################# mainloop() Grupos #############################
            self.playerG.update() # only does visual and margin updates
            self.swordsG.update()
            self.coinsG.update()
            self.powerupG.update()
            self.pipeG.update()

            self._reset_sprites_offscreen()
            
            if not self.xp.any(self.bird_alive):
                self.next_generation() 
                break
            


        ################ Music ################
        self.utils.play_song(self.songs, self.current_song) 
        tecla = pg.key.get_pressed()
        
        # Turn Down
        if tecla[pg.K_9] and pg.mixer.music.get_volume() > 0.0:
            pg.mixer.music.set_volume(pg.mixer.music.get_volume() - 0.01)
        # Turn Up
        if tecla[pg.K_0] and pg.mixer.music.get_volume() < 1.0:
            pg.mixer.music.set_volume(pg.mixer.music.get_volume() + 0.01)
        # Mute
        if tecla[pg.K_m]:
            pg.mixer.music.set_volume(0.0)


        ############################# Draw #############################
        self.x = self.utils.animate_background(self.screen, self.screen_x, self.x, self.background_img) 

        self.playerG.draw(self.screen)
        self.swordsG.draw(self.screen)
        self.coinsG.draw(self.screen)
        self.powerupG.draw(self.screen)
        self.pipeG.draw(self.screen)
        
        # Birdy Sprite Draw
        if len(idx_alive) > 0:
            idx_fitness_sort = idx_alive[self.xp.argsort(self.fitness_array[idx_alive])[::-1]]
            idx_leader = int(idx_fitness_sort[0])
            idx_visual_top = idx_fitness_sort[:self.num_visual_birds]

            # IMPORT: Convert to NumPy only necessary Pygame Data
            bird_y_cpu = as_numpy(self.bird_y[idx_visual_top])
            y_leader_cpu = float(self.bird_y[idx_leader])
            
            bird_sprites = self.playerG.sprites()
            for sprite in bird_sprites: sprite.rect.y = -2000 # if they've died

      
            for i, _ in enumerate(bird_y_cpu):
                if i < len(bird_sprites):
                    bird_sprites[i].rect.centery = int(bird_y_cpu[i])


            # IMPORTANT: Use ARRAY data not Birdy data
            leader_fitness = float(self.fitness_array[idx_leader])
            leader_speed = float(self.bird_speed[idx_leader])

            # Data Draw
            info = [
                f"MODO RAPIDO: {f'SI x{self.training_speed}' if (fast_forward and self.enable_fast_mode and self.training_speed > 1) else 'NO'}",
                f"Generacion: {self.evolution_manager.generation}",
                f"Individuos Vivos: {len(idx_alive)}", # Usar len(indices_vivos)
                f"Fitness Lider: {leader_fitness:.0f}",
                f"Velocidad Y: {leader_speed:.2f}"
            ]
            for i, text in enumerate(info):
                color = YELLOW if "RAPIDO" in text and (fast_forward and self.enable_fast_mode and self.training_speed > 1) else WHITE
                self.utils.show_text(self.screen, text, BLACK, 10, 10 + (i * 20), "m04.ttf", 15)
                self.utils.show_text(self.screen, text, color, 10, 10 + (i * 20), "m04b.ttf", 15)

            w1_cpu = as_numpy(self.all_w1[idx_leader])
            w2_cpu = as_numpy(self.all_w2[idx_leader])
            w3_cpu = as_numpy(self.all_w3[idx_leader])
            inputs_cpu = as_numpy(inputs_matrix[0]) # remember its size is (n_alive x 9y)
            

            if self.hitboxes:
                # NeuralNetwork Draw
                net_pos_x = self.screen_x * 0.05
                net_pos_y = self.screen_y * 0.6
                self.utils.draw_network(self.screen, w1_cpu, w2_cpu, w3_cpu, leader_speed, net_pos_x, net_pos_y, inputs_cpu)


            # Hitbox Draw
            if self.hitboxes:
                item_debug_list = [
                    (self.swordsG, self.debug_colors["sword"]),
                    (self.coinsG, self.debug_colors["coin"]),
                    (self.powerupG, self.debug_colors["powerup"])
                ]
                
                self.utils.draw_debug_hitboxes(self.screen, self.bird_y, np.array([idx_leader]), 
                                                Birdy.size[0], Birdy.size[1], 
                                                item_debug_list, self.pipeG, self.debug_colors["pipe"])

                # Bird Vision Draw
                bird_center = (self.screen_x // 3, int(y_leader_cpu))
                
                for (pos, color) in nearest_objects:
                    self.utils.draw_bird_vision(self.screen, bird_center, pos, color)


        self.utils.show_text(self.screen, str(round(pg.mixer.music.get_volume(),2)),WHITE,self.screen_x*0.95, self.screen_y-80,'Minecraft.ttf',int(self.screen_y*0.02))

        self.utils.show_text(self.screen,"9: BAJAR VOLUMEN",WHITE,self.screen_x*0.85,self.screen_y-40,"Minecraft.ttf",int(self.screen_y*0.02))
        self.utils.show_text(self.screen,"0: SUBIR VOLUMEN",WHITE,self.screen_x*0.85,self.screen_y-80,"Minecraft.ttf",int(self.screen_y*0.02))

        self.utils.show_text(self.screen,f"{self.t_elapsed : .0f}",BLACK,self.screen_x//2-int(self.screen_y*0.08),self.screen_y * 0.05,"m04.ttf",int(self.screen_y*0.08))
        self.utils.show_text(self.screen,f"{self.t_elapsed : .0f}",WHITE,self.screen_x//2-int(self.screen_y*0.08),self.screen_y * 0.05,"m04b.ttf",int(self.screen_y*0.08))
       

    def menuloop(self) -> None:
        """Handles the logic and rendering for the main menu screen.
        
        Manages button hover effects, animated menu sprites, and coordinate
        definitions for the 'Play' and 'Exit' buttons.
        """
        self.x = self.utils.animate_background(self.screen, self.screen_x, self.x, self.menu_img)
        
        self.sword = list(self.swordsG)[0]
        sword_size = (self.screen_x * 0.25, self.screen_y * 0.2)
        
        image1, image2 = pg.Surface(sword_size).convert_alpha(), pg.Surface(sword_size).convert_alpha()
        x1, y1, text1 = self.screen_x*0.12, self.screen_y*0.6, "JUGAR"
        x2, y2, text2 = self.screen_x*0.59, self.screen_y*0.6, "SALIR"
        size1, size2 = int(self.screen_y*0.1) * len(text1), int(self.screen_y*0.1) * len(text2)
        
        self.menu_play_button = (x1, y1, text1, size1)
        self.menu_exit_button = (x2, y2, text2, size2)

        sprite_sheet = pg.transform.scale(self.sword.image_pg, (sword_size[0] * 5, sword_size[1]))   
        image1.fill((0,0,0,0))
        image2.fill((0,0,0,0))
        image1.blit(sprite_sheet, (0,0),pg.Rect(0, 0, sword_size[0], sword_size[1]))
        image2.blit(sprite_sheet, (0,0),pg.Rect(0, 0, sword_size[0], sword_size[1]))

        play_color = exit_color = WHITE
        mouseX, mouseY = pg.mouse.get_pos() 
        if x1 < mouseX < x1+size1 and y1 < mouseY < y1+size1:
            image1.fill((0,0,0,0))
            image1.blit(sprite_sheet, (0,0), pg.Rect(self.sword.get_sprite_idx(0.1) * sword_size[0], 0, sword_size[0], sword_size[1]))    
            play_color = GREEN1

        if x2 < mouseX < x2+size2 and y2 < mouseY < y2+size2: 
            image2.fill((0,0,0,0))
            image2.blit(sprite_sheet, (0,0), pg.Rect(self.sword.get_sprite_idx(0.1) * sword_size[0], 0, sword_size[0], sword_size[1]))
            exit_color = RED
        
            
        self.screen.blit(pg.transform.rotate(image1, 220), (self.screen_x*0.1, self.screen_y*0.40))
        self.screen.blit(pg.transform.rotate(image2, 320), (self.screen_x*0.6, self.screen_y*0.40))

        self.utils.show_text(self.screen, text1, BLACK,x1, y1,"m04.ttf", int(self.screen_y*0.1))
        self.utils.show_text(self.screen, text1, play_color,x1, y1,"m04b.ttf", int(self.screen_y*0.1))
                           
        self.utils.show_text(self.screen, text2, BLACK,x2, y2,"m04.ttf", int(self.screen_y*0.1))
        self.utils.show_text(self.screen, text2, exit_color,x2, y2,"m04b.ttf", int(self.screen_y*0.1))
                  
    def pauseloop(self) -> None:
        """Handles the rendering and background animation for the pause screen."""

        ############################# Text #############################
        self.utils.show_text(self.screen,"JUEGO PAUSADO", BLACK, 90 ,100,'m04.ttf',50)
        self.utils.show_text(self.screen,"JUEGO PAUSADO", WHITE, 90 ,100,'m04b.ttf',50)
        
        self.utils.show_text(self.screen,"PUNTUACION",GREEN3, 450 ,320,'m04.ttf',30)
        self.utils.show_text(self.screen,"PUNTUACION",GREEN2, 450 ,320,'m04b.ttf',30)

        self.utils.show_text(self.screen,"IR A SPS CLOUD",WHITE, 105 ,387,'Minecraft.ttf',30)
                      
        ############################# Funtions #############################
        self.x = self.utils.animate_background(self.screen, self.screen_x, self.x, self.menu_img)
        

    ############################# AI #############################
    def get_all_inputs_vectorized(self, idx_alive):
        """Calculates normalized environmental data for the entire population.

        Returns:
            self.xp.ndarray: A matrix of shape (pop_size, ixputs) containing 
                relative distances to nearest obstacles and current velocity.
        """
        
        def get_nearest_group_data(group: pg.sprite.Group) -> tuple:
            """Calculate the nearest object in a Sprite Group.

            Defines the nearest object as the object with 
            the minimum x position and in front of a bird.
            """

            pos_x = self.screen_x // 3
            candidates = [obj for obj in group if obj.rect.right > pos_x] 
            if candidates:
                nearest = min(candidates, key=lambda obj: obj.rect.left)
                return nearest.rect.left, nearest.rect.centery
            return self.screen_x * 2, self.screen_y / 2 # Default Values ()

        # Nearest Objects
        c_pos = c_x, c_y = get_nearest_group_data(self.coinsG)
        p_pos = p_x, p_y = get_nearest_group_data(self.powerupG)
        s_pos = s_x, s_y = get_nearest_group_data(self.swordsG)
        
        # Pipe Logic (pipe center)
        pipes = sorted([p for p in self.pipeG if p.rect.right > self.screen_x // 3], key=lambda x: x.rect.left)
        if len(pipes) >= 2:
            pipe_target_x = pipes[0].rect.left
            pipe_target_y = (pipes[0].rect.centery + pipes[1].rect.centery) / 2 # Center
        else:
            # Fallback 
            # Occurs between pipe generations
            pipe_target_x, pipe_target_y = self.screen_x * 2, self.screen_y / 2 

        nearest_objects = [
            (c_pos, self.debug_colors["coin"]),
            (p_pos, self.debug_colors["powerup"]),
            (s_pos, self.debug_colors["sword"]),
            ((pipe_target_x, pipe_target_y), self.debug_colors["pipe"])
        ]

        ### Relative Distance for ALL the birds at Once
        bird_x_const = self.screen_x // 3
        
        # Distance Normalization
        dist_pipe_x = (pipe_target_x - bird_x_const) / self.screen_x
        dist_pipe_y = (pipe_target_y - self.bird_y[idx_alive]) / self.screen_y
        
        dist_coin_x = (c_x - bird_x_const) / self.screen_x
        dist_coin_y = (c_y - self.bird_y[idx_alive]) / self.screen_y
        
        dist_pw_x = (p_x - bird_x_const) / self.screen_x
        dist_pw_y = (p_y - self.bird_y[idx_alive]) / self.screen_y
        
        dist_sw_x = (s_x - bird_x_const) / self.screen_x
        dist_sw_y = (s_y - self.bird_y[idx_alive]) / self.screen_y
        
        norm_vel = self.bird_speed[idx_alive] / Birdy.max_speed_y

        # Only Alive Birds
        num_alive = len(idx_alive)

        # Array Ixput (N_birds_alive, 9_sensors)
        # Instead of xp.column_stack with xp.full...
        # Create directly the array
        # Broadcasting will subtract the scalar from the entire array automatically
        inputs_matrix = self.xp.empty((num_alive, 9), dtype=self.xp.float32)
        inputs_matrix[:, 0] = dist_pipe_x
        inputs_matrix[:, 1] = dist_pipe_y
        inputs_matrix[:, 2] = dist_coin_x
        inputs_matrix[:, 3] = dist_coin_y 
        inputs_matrix[:, 4] = dist_pw_x
        inputs_matrix[:, 5] = dist_pw_y
        inputs_matrix[:, 6] = dist_sw_x
        inputs_matrix[:, 7] = dist_sw_y
        inputs_matrix[:, 8] = norm_vel

        return inputs_matrix, nearest_objects


    def next_generation(self) -> None:
        """Triggers the evolutionary process and resets the simulation state.

        Passes the current fitness scores to the evolution manager to create 
        new weight matrices through selection, crossover, and mutation.
        """
        self.evolution_manager.restart_generation(self.fitness_array)
    
        self.reset_game_state()

        self.all_w1 = self.evolution_manager.w1
        self.all_w2 = self.evolution_manager.w2
        self.all_w3 = self.evolution_manager.w3


    def reset_game_state(self) -> None:
        """Resets all numerical arrays and sprite positions to their starting values.
        
        Clears groups and re-populates items based on the difficulty level.
        """
        self.t_elapsed = 0
        self.x = 0
        
        self.swordsG.empty()
        self.coinsG.empty()
        self.powerupG.empty()
        self.pipeG.empty()

        self.bird_y.fill(self.screen_y / 2)
        self.bird_speed.fill(0)
        self.bird_alive.fill(True)
        self.fitness_array.fill(0)
        self.hit_matrix.fill(False)

        for i in range(0, self.num_swords):
            sword = Sword(display_data=(self.screen, self.screen_alpha, self.FPS), filename="swords", scale=0.3)
            sword.item_id = i
            self.swordsG.add(sword)

        for i in range(0, self.num_coins):
            coin = Coins(display_data=(self.screen, self.screen_alpha, self.FPS), filename="coins", scale=0.5)
            coin.item_id = self.num_swords + i
            self.coinsG.add(coin)
        
        for i in range (0, self.num_powerups):
            powerup = PowerUp(display_data=(self.screen, self.screen_alpha, self.FPS), filename="power_up", scale=1.3)
            powerup.item_id = self.num_swords + self.num_coins + i
            self.powerupG.add(powerup)

        self.pipeG.add(Pipe(display_data=(self.screen, self.screen_alpha, self.FPS), filename="bottom_pipe", type="bottom"))
        self.pipeG.add(Pipe(display_data=(self.screen, self.screen_alpha, self.FPS), filename="top_pipe", type="top"))
        
        
    ############################# GAME LOGIC #############################
    def _reset_sprites_offscreen(self) -> None:
        """Recycles sprites that have moved past the left edge of the screen.
        
        Resets the collision history in the hit_matrix for the specific item 
        to allow birds in the current generation to interact with the new position.
        """
        for group, sprite_class, filename, scale in [
            (self.swordsG, Sword, "swords", 0.3),
            (self.coinsG, Coins, "coins", 0.5),
            (self.powerupG, PowerUp, "power_up", 1.3)
        ]:
            for obj in list(group):
                if obj.rect.right < 0:
                    self.hit_matrix[:, obj.item_id] = False # reset collision

                    old_id = obj.item_id
                    obj.kill()

                    new_obj = sprite_class(display_data=(self.screen, self.screen_alpha, self.FPS), filename=filename, scale=scale)
                    new_obj.item_id = old_id
                    group.add(new_obj)


    def _detect_item_collisions(self, idx_alive) -> None:
        """Detects collisions between birds and items using vectorized distances.
        
        Optimizes performance by filtering for living birds and items within 
        the birds' X-axis column before calculating vertical proximity.
        """

        # our bird has a fix X coord
        # it will be good to link with the Birdy() rect init
        pos_x = self.screen_x // 3

        bird_y_alive = self.bird_y[idx_alive]

        all_items: list[SpriteSheet] = self.swordsG.sprites() + self.coinsG.sprites() + self.powerupG.sprites()
        for item in all_items:
            if (abs(item.rect.centerx - pos_x) < item.size[0]): # NOTE: check in a future item.size[0] and item.size[1]

                dist_y = self.xp.abs(bird_y_alive - item.rect.centery) # Y distance between Bird and Item
                
                history_hit = self.hit_matrix[idx_alive, item.item_id]
                possible_hit_mask = (dist_y < (item.size[1] / 2)) & (~history_hit) # ~ bitwiseNOT
                
                if self.xp.any(possible_hit_mask):
                    idx_hit = idx_alive[possible_hit_mask]
                    
                    # Fitness 
                    key = "sword" if item in self.swordsG else "coin" if item in self.coinsG else "powerup"
                    fitness = self.fitness_dict[key]
                    if key == "sword": fitness *= -1
                    
                    self.fitness_array[idx_hit] += fitness          
                    self.hit_matrix[idx_hit, item.item_id] = True   # collision