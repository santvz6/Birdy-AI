# app/sprites/spritesheet.py

import pygame as pg
from pathlib import Path

class SpriteSheet:
    """Provides logic for loading, scaling, and animating frames from a single image.

    This utility class handles the extraction of individual frames from a horizontal 
    strip (spritesheet) and manages the timing for visual animations.

    Attributes:
        screen_size (tuple): Dimensions of the main display surface.
        filename (str): Name of the source image file.
        size (tuple[float, float]): The dimensions (width, height) of a single frame.
        num_sprites (int): Total number of frames contained in the sheet.
        sprite_sheet (pg.Surface): The processed and scaled source image.
        image (pg.Surface): The current active frame to be rendered.
        rect (pg.Rect): The bounding box for the current frame.
    """

    def __init__(self, display_data:tuple, filename:str, size:float, num_sprites:int, chroma:tuple, path=Path("app/assets/gfx/sprites")) -> None:
        """Initializes the spritesheet by loading the image and preparing the first frame.

        Args:
            display_data (tuple): Contains screen, alpha_screen, and FPS data.
            filename (str): Name of the image file without extension.
            size (tuple): Width and height of an individual sprite frame.
            num_sprites (int): Number of horizontal frames in the sheet.
            chroma (tuple): Color key for transparency; if None, uses alpha channel.
            path (Path, optional): Directory path for assets. Defaults to specific gfx folder.
        """
        self.screen_size = display_data[0].get_size()
        self.filename = filename
        self.size = size
        self.num_sprites = num_sprites

        if chroma:
            self.image_pg = pg.image.load(path / (self.filename + ".png")).convert()
            self.image_pg.set_colorkey(chroma) 
        else:
            self.image_pg = pg.image.load(path / (self.filename + ".png")).convert_alpha()
        
        self.sprite_sheet = pg.transform.scale(self.image_pg, (self.size[0] * self.num_sprites, self.size[1]))

        self.image = pg.Surface(self.size).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sprite_sheet, (0,0), pg.Rect(0 * self.size[0], 0, self.size[0], self.size[1]))

        self.rect = self.image.get_rect() 

    def get_sprite_idx(self, change_sec=1) -> int:
        """Calculates the current frame index based on the elapsed game time.

        Args:
            change_sec (float): Duration in seconds each frame remains visible.

        Returns:
            int: The index of the sprite frame to be displayed.
        """
        return int(pg.time.get_ticks() // (1000 * change_sec)) % self.num_sprites

    def animate_sprite_sheet(self) -> None:
        """Updates the active image surface with the next frame in the animation sequence.
        
        Clears the current image surface and blits the new frame from the 
        scaled spritesheet based on a fixed temporal interval.
        """
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sprite_sheet, (0,0), pg.Rect(self.get_sprite_idx(0.1) * self.size[0], 0, self.size[0], self.size[1]))
        