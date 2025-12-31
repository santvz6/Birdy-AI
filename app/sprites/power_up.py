# app/sprites/power_up.py

import random
import pygame as pg

from pygame.locals import *

from config import *
from .spritesheet import SpriteSheet


class PowerUp(pg.sprite.Sprite, SpriteSheet):
    """Represents a collectible power-up with horizontal movement and recycling logic.

    This class manages the lifecycle of a power-up, including its automatic 
    repositioning once it leaves the screen to optimize performance.

    Attributes:
        t_spawn (int): Factor used to calculate the off-screen spawn distance.
        speed_x (int): The constant horizontal velocity moving to the left.
        FPS (int): Frames per second used for timing calculations.
        rect (pg.Rect): The collision box and screen position of the sprite.
    """

    def __init__(self, display_data:tuple[pg.Surface, pg.Surface, int], scale:float, filename="power_up", chroma=GREEN1) -> None:
        """Initializes the PowerUp with a spritesheet and random vertical position.

        Args:
            display_data (tuple): Contains screen, alpha_screen, and FPS data.
            scale (float): Scaling factor for the power-up's dimensions.
            filename (str, optional): Name of the image file. Defaults to "power_up".
            chroma (tuple, optional): Color key for transparency. Defaults to GREEN1.
        """
        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, display_data=display_data, filename=filename, size=(70*scale, 64*scale), num_sprites=8, chroma=chroma)

        self.FPS = display_data[2]
        self.t_spawn = 15
        self.speed_x = -8

        self.rect.topleft = (self.t_spawn * self.FPS * abs(self.speed_x), random.randint(0, int(self.screen_size[1] - self.size[1])))
        
    def update(self) -> None:
        """Updates the power-up's position and advances its animation frame.
        
        This method handles the constant horizontal displacement and triggers 
        the visual cycle of the spritesheet to maintain the object's animation.
        """
        self.rect.x += self.speed_x
        self.animate_sprite_sheet()

