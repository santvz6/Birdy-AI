# app/sprites/coins.py

import random
import pygame as pg

from pygame.locals import *

from config import *
from .spritesheet import SpriteSheet



class Coins(pg.sprite.Sprite, SpriteSheet):
    """Represents a collectible coin agent with horizontal movement and animation.

    This class handles the spawning, animation cycling, and movement logic.

    Attributes:
        max_speed_x (float): Terminal horizontal velocity cap.
        speed_x (float): Current horizontal velocity.
        acc_x(float): Incremental speed increase per frame.
        rect (pg.Rect): The collision box and screen position of the sprite.
    """

    def __init__(self, display_data:tuple[pg.Surface, pg.Surface, int], scale:float, filename="coins", chroma=BLUE):
        """Initializes the Coins instance with random positioning and scaled dimensions.

        Args:
            display_data (tuple): Contains screen, alpha_screen and FPS data.
            scale (float): Scaling factor for the coin's dimensions.
            filename (str): Name of the image file in the assets folder.
            chroma (tuple): Color key for transparency.
        """
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, display_data=display_data, filename=filename, size=(102*scale, 103*scale), num_sprites=6, chroma=chroma) 

        self.rect.topleft = (random.randint(int(self.screen_size[0]), int(self.screen_size[0] * 1.5)), 
                             random.randint(0, int(self.screen_size[1] - self.size[1])))
        
        self.max_speed_x = -10
        self.speed_x = -6
        self.acc_x = -0.1
        

    def update(self):
        """Updates the coin's physics and advances its animation frame.
        
        This method increments the horizontal velocity by applying acceleration, 
        clamps the speed to the defined maximum, and updates the position. 
        Finally, it cycles through the spritesheet frames.
        """
        self.speed_x += self.acc_x
        self.speed_x = max(self.speed_x, self.max_speed_x)
        self.rect.x += self.speed_x 

        self.animate_sprite_sheet()
