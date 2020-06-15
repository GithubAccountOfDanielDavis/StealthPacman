"""Player class (in progress)"""

from collections import OrderedDict
import pygame as pg
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
import grid
import colors
import barriers

class Player:
    """The puck man"""

    Directions = {
        'stationary': pg.Vector2(0, 0),
        K_UP: pg.Vector2(0, -1),
        K_DOWN: pg.Vector2(0, 1),
        K_LEFT: pg.Vector2(-1, 0),
        K_RIGHT: pg.Vector2(1, 0),
    }

    color = colors.YELLOW
    radius = 0.8
    screen_radius = grid.scale_to_screen(radius)
    speed = 10

    def __init__(self, position):
        self.position = position
        self.pressed = OrderedDict()
        self.collision_surface = pg.Surface(grid.SCREEN_SIZE, pg.SRCALPHA)

    def handle_keydown(self, event):
        """Modify internal state based on keydown events"""
        if event.key in self.Directions:
            self.pressed[event.key] = self.Directions[event.key]
            self.pressed.move_to_end(event.key)

    def handle_keyup(self, event):
        """Modify internal state based on keyup events"""
        if event.key in self.pressed:
            self.pressed.pop(event.key)

    def update(self, milliseconds):
        """Update player position"""
        seconds = milliseconds / 1000.0
        direction = (
            self.Directions['stationary']
            if len(self.pressed) == 0
            else next(reversed(self.pressed.values())))
        velocity = direction * self.speed * seconds
        prev_position, self.position = (
            self.position,
            self.position + velocity)
        overlap = self.barrier_collision_mask()
        if overlap.count() > 0:
            self.position = prev_position

    def barrier_collision_mask(self):
        """Check if player is colliding with barrier by comparising masks"""
        self.collision_surface.fill((0, 0, 0, 0))
        self.render(self.collision_surface)
        collision_mask = pg.mask.from_surface(self.collision_surface)
        return barriers.BARRIER_MASK.overlap_mask(collision_mask, (0, 0))

    def render(self, screen: pg.Surface):
        """Render player to screen"""
        pg.draw.circle(
            surface=screen,
            color=self.color,
            center=grid.to_screen(self.position),
            radius=self.screen_radius)
