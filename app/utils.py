# app/utils.py

import pygame as pg
import numpy as np
from config import *

class Utils:

    def __init__(self):
        """Initializes the Utils instance and the Pygame font module."""
        pg.font.init()
    
    ############################### MUSIC ###############################
    def play_song(self, songs:list, current_song:int) -> None:
        """Manages the music playback logic, cycling through a playlist.

        Args:
            songs (list): List of file paths to audio tracks.
            current_song (int): The index of the song currently selected.
        """
        if not pg.mixer.music.get_busy():  
            current_song += -len(songs) if current_song >= len(songs)-1 else 1
            pg.mixer.music.load(songs[current_song])
            pg.mixer.music.play()           


    
    ############################### DRAW ###############################
    def animate_background(self, screen, screen_x, x, background) -> int:
        """Creates a seamless scrolling effect for the game background.

        Args:
            screen (pg.Surface): The main display surface.
            screen_x (int): The width of the screen.
            x (int): The current horizontal displacement.
            background (pg.Surface): The background image surface.

        Returns:
            int: The updated horizontal position for the next frame.
        """
        x_ = x % background.get_rect().width
        screen.blit(background, (x_ - background.get_rect().width, 0))
        if x_ < screen_x:
            screen.blit(background, (x_, 0))
        return x - 1


    def show_text(self, screen, text, color, x, y, font, font_size) -> None:
        """Renders and displays text on the screen using a specific TTF font.

        Args:
            screen (pg.Surface): The surface to draw the text on.
            text (str): The string content to be displayed.
            color (tuple): RGB color of the text.
            x (int): Horizontal screen coordinate.
            y (int): Vertical screen coordinate.
            font (str): Filename of the font in the assets folder.
            font_size (int): Size of the font to render.
        """
        font = pg.font.Font(Path("app/assets/ttf/") / font, font_size) 
        surface = font.render(text, True, color) 
        screen.blit(surface, (x, y)) 


    def draw_bird_vision(self, screen, bird_pos:tuple, target_pos:tuple, color=WHITE):
        """Draws a line representing the leader bird's focus on the nearest object.
        
        Args:
            screen (pg.Surface): Main game surface.
            bird_pos (tuple): (x, y) coordinates of the leader bird.
            target_pos (tuple): (x, y) coordinates of the target object center.
            color (tuple, optional): Color of the line. Defaults to WHITE.
        """
        if target_pos[0] > screen.get_width(): # Don't draw if target is dummy/offscreen
            return
        
        pg.draw.line(screen, color, bird_pos, target_pos, 2)
        pg.draw.circle(screen, color, target_pos, 5, 5)
        

    def draw_debug_hitboxes(self, screen, birds_y, idx_fitness_sort, bird_width, bird_height, 
                         groups_with_colors, pipe_group, pipe_color, line_width=2) -> None:
        """Draws rectangular hitboxes for birds, items, and pipes for debugging.
        
        Args:
            screen (pg.Surface): Main game surface.
            birds_y (np.ndarray): Array of vertical positions.
            idx_fitness_sort (np.ndarray): Indices of birds sorted by performance.
            bird_width (int): Width of the bird hitbox.
            bird_height (int): Height of the bird hitbox.
            groups_with_colors (list): List of (sprite_group, color_tuple) for items.
            pipe_group (pg.sprite.Group): Group containing pipe obstacles.
            pipe_color (tuple): Color for pipe hitboxes.
            line_width (int, optional): Thickness of the rectangle border.
        """
        try:
            line_width = int(line_width)
        except:
            return

        pos_x = screen.get_width() // 3
        
        # Draw Birdy Hitbox
        for idx in idx_fitness_sort:
            # Center the rect on the bird's Y coordinate
            bird_rect = pg.Rect(pos_x, int(birds_y[idx] - bird_height // 2), bird_width, bird_height)
            pg.draw.rect(screen, (255, 255, 255), bird_rect, line_width)

        # Draw Item Hitboxes (Swords, Coins, Powerups)
        for group, color in groups_with_colors:
            for item in group:
                # We use the item's actual rect
                pg.draw.rect(screen, color, item.rect, line_width)

        # Draw Pipe Hitboxes
        for pipe in pipe_group:
            pg.draw.rect(screen, pipe_color, pipe.rect, line_width)


    def draw_network(self, screen, w1, w2, w3, speed_y, start_x, start_y, inputs) -> None:
        """Visualizes the neural network structure, weights, and node activations.

        Args:
            screen (pg.Surface): Main game surface.
            w1, w2, w3 (np.ndarray): Weight matrices between layers.
            speed_y (float): Current vertical velocity (used for output node color).
            start_x (int): Initial horizontal position for the diagram.
            start_y (int): Initial vertical position for the diagram.
            inputs (list/np.array): Input values to visualize sensor activation.
        """
        weights = [w1, w2, w3]
        layer_sizes = [w.shape[0] for w in weights] + [weights[-1].shape[1]]
        
        node_radius = 8
        layer_gap = 100
        node_gap = 35
        
        nodes = []
        for i, size in enumerate(layer_sizes):
            layer_nodes = [
                (start_x + i * layer_gap, start_y + (j - size/2) * node_gap)
                for j in range(size)
            ]
            nodes.append(layer_nodes)

        # Edges Draw
        # We Iterate for each pair of layers and weights
        for l in range(len(weights)):
            current_w_matrix = weights[l]
            for i, start_node in enumerate(nodes[l]):
                for j, end_node in enumerate(nodes[l+1]):
                    weight = current_w_matrix[i][j]
                    
                    # Visibility Filter
                    if abs(weight) > 0.1: 
                        color = (0, 255, 0) if weight > 0 else (255, 0, 0)
                        width = max(1, int(abs(weight) * 2))
                        pg.draw.line(screen, color, start_node, end_node, width)

        # Nodes Draw
        for i, layer in enumerate(nodes):
            for j, node_pos in enumerate(layer):
                node_color = (40, 40, 40)
                if i == 0 and j < len(inputs): # Sensores
                    val = max(0, min(255, int(abs(inputs[j]) * 255)))
                    node_color = (val, val, 255)
                elif i == len(nodes) - 1: # Salida
                    node_color = (255, 255, 0) if speed_y < 0 else (40, 40, 40)
                
                pg.draw.circle(screen, node_color, node_pos, node_radius)
                pg.draw.circle(screen, (200, 200, 200), node_pos, node_radius, 1)
