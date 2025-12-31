# app/sprites/birdy.py

import pygame as pg

from pygame.locals import *
from config import *
from .spritesheet import SpriteSheet


class Birdy(pg.sprite.Sprite, SpriteSheet): 
    """Represents a bird agent with visual animation and boundary logic.

    This class combines Pygame's Sprite functionality for group management 
    with custom SpriteSheet logic for frame-based animations.

    Attributes:
        max_speed_y (float): The maximum terminal velocity for falling.
        speed_y (float): The current vertical velocity of the bird.
        acc_y (float): The gravitational acceleration applied per frame.
        rect (pg.Rect): The collision box and screen position of the sprite.
    """

    # Class attributes (shared across instances)
    max_speed_y: float  = 20.0
    speed_y: float      = 5.0
    acc_y: float        = 0.55
    jump: float         = -10.0
    size: float         = (99*0.9, 70*0.9)

    def __init__(self, display_data:tuple[pg.Surface, pg.Surface, int], filename:str, scale=None, chroma=GREEN1) -> None:  
        """Initializes the Birdy instance with a specific size and animation sheet.

        Args:
            display_data (tuple[]): Contains screen, alpha_screen and FPS data.
            filename (str): Name of the image file located in the assets folder.
            size (float, optional): Scaling factor for the bird's dimensions.
            chroma (tuple, optional): Color key for transparency.
        """       
        sprite_size = (99*scale, 70*scale) if scale else Birdy.size
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, display_data=display_data, filename=filename, size=sprite_size, num_sprites=3, chroma=chroma)

        self.rect.topleft = (self.screen_size[0] // 3, self.screen_size[1] // 2)

    def update(self) -> None:
        """Updates visual animation frames and enforces screen boundary logic.
        
        This method cycles through the spritesheet frames and wraps the bird 
        around the screen (teleporting) if it exceeds the vertical limits.
        """                
        self.animate_sprite_sheet()

        if self.rect.y < 0 - self.rect.height: 
            self.rect.y = self.screen_size[1]                
        if self.rect.y > self.screen_size[1]:                  
            self.rect.y = 0 - self.rect.height 