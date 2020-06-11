"""Player class (in progress)"""

import pygame as pg
import grid
import colors

class Player:
    """The puck man"""

    color = colors.YELLOW
    radius = 0.9
    screen_radius = grid.scale_to_screen(radius)

    def __init__(self, position):
        self.position = position

    def handle_keydown(self, event):
        """Modify internal state based on keydown events"""

    def handle_keyup(self, event):
        """Modify internal state based on keyup events"""

    def render(self, screen: pg.Surface):
        """Render player to screen"""
        pg.draw.circle(
            surface=screen,
            color=self.color,
            center=grid.to_screen(self.position),
            radius=self.screen_radius)
