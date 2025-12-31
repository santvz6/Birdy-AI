# app/sprites/sword.py

import random
import pygame as pg

from pygame.locals import *
from .spritesheet import SpriteSheet

 
class Sword(pg.sprite.Sprite, SpriteSheet):
    """Represents a sword obstacle with acceleration logic and frame-based animation.

    This class manages a hazardous object that moves from right to left, 
    increasing its speed over time until it reaches a terminal velocity.

    Attributes:
        max_speed_x (float): The maximum horizontal speed limit (terminal velocity).
        speed_x (float): The current horizontal velocity of the sword.
        acc_x (float): The horizontal acceleration applied per frame.
        rect (pg.Rect): The collision box and screen position of the sprite.
    """

    def __init__(self, display_data:tuple[pg.Surface, pg.Surface, int], scale:float, filename="swords", chroma=None) -> None:
        """Initializes the Sword instance with random positioning and physics properties.

        Args:
            display_data (tuple): Contains screen, alpha_screen, and FPS data.
            scale (float): Scaling factor for the sword's dimensions.
            filename (str, optional): Name of the image file. Defaults to "swords".
            chroma (tuple, optional): Color key for transparency. Defaults to None.
        """
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, display_data=display_data, filename=filename, size=(337*scale, 170*scale), num_sprites=5, chroma=chroma) 

        self.rect.topleft = (random.randint(int(self.screen_size[0]), int(self.screen_size[0] * 1.5)), 
                             random.randint(0, int(self.screen_size[1] - self.size[1])))

        self.max_speed_x = -10
        self.speed_x = -6
        self.acc_x = -0.1
        

    def update(self) -> None:
        """Updates physics calculations and cycles the animation frames.
        
        This method applies acceleration to the horizontal speed, ensures it 
        does not exceed max_speed_x, and updates the sprite's position and visual state.
        """
        self.speed_x += self.acc_x
        self.speed_x = max(self.speed_x, self.max_speed_x)
        self.rect.x += self.speed_x 

        self.animate_sprite_sheet()