# app/sprites/pipe.py

import random
import pygame as pg

from pygame.locals import *
from .spritesheet import SpriteSheet


class Pipe(pg.sprite.Sprite, SpriteSheet):
    """Represents a pipe obstacle with horizontal movement and positional resetting.

    This class manages the obstacle pipes, handling their initialization as 
    either 'top' or 'bottom' types and managing their reset logic once they 
    leave the screen.

    Attributes:
        pipe_gap (float): Factor used to calculate the vertical spawn range.
        type (str): Categorizes the pipe as "top" or "bottom" for positioning.
        speed_x (int): Constant horizontal speed towards the left.
        rect (pg.Rect): The collision box and screen position of the sprite.
    """

    def __init__(self, display_data:tuple[pg.Surface, pg.Surface, int], filename:str, type:str, chroma=None):
        """Initializes the Pipe instance with a fixed size and type-based positioning.

        Args:
            display_data (tuple): Contains screen, alpha_screen and FPS data.
            filename (str): Name of the image file located in the assets folder.
            type (str): Defines if the pipe is located at the 'top' or 'bottom'.
            chroma (tuple, optional): Color key for transparency.
        """

        pg.sprite.Sprite.__init__(self)
        SpriteSheet.__init__(self, display_data=display_data, filename=filename, size=(100, 400), num_sprites=1, chroma=chroma) 


        # TODO: modified gap function
        self.pipe_gap= 0.7
        self.type = type
        if type == "bottom":
            self.rect.topleft = (int(self.screen_size[0] * 1.5), 
                                random.randint(int(self.screen_size[1] - self.size[1]), int(self.screen_size[1]*self.pipe_gap)))
        elif type == "top":
            self.rect.topleft = (int(self.screen_size[0] * 1.5), 
                                random.randint(int(-self.size[1]*(2-self.pipe_gap)), 0))

        self.speed_x = -8
 
    def update(self):
        """Updates the horizontal position and resets the pipe when off-screen.
        
        The pipe moves left until it completely exits the screen, at which point 
        it is repositioned to the right with a new random height.
        """

        self.rect.x += self.speed_x 

        if self.rect.x < -self.size[0]:
            if self.type == "bottom":
                self.rect.topleft = (int(self.screen_size[0] * 1.5), 
                                random.randint(int(self.screen_size[1] - self.size[1]), int(self.screen_size[1]*0.9)))
            elif self.type == "top":
                self.rect.topleft = (int(self.screen_size[0] * 1.5), 
                                random.randint(int(-self.size[1]), 0))
