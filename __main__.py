"""Initialization for pygame and main game loop"""

import typing
from collections import defaultdict
import pygame as pg

import grid
import colors
from barriers import BARRIERS
from player import Player

def get_events():
    """Create event dict from list"""
    event_list = pg.event.get()
    event_dict = defaultdict(list)
    for event in event_list:
        event_dict[event.type].append(event)
    return event_dict

Renderable = typing.Callable[[pg.Surface], None]
def game_loop(renderables: typing.Sequence[Renderable]):
    """Initialize pygame and run loop until it's over"""
    pg.init()
    pg.display.set_caption('Pacman')
    screen = pg.display.set_mode(grid.SCREEN_SIZE)
    clock = pg.time.Clock()
    player = Player(pg.Vector2(13.5, 23))
    renderables.append(player.render)

    while len((events := get_events())[pg.QUIT]) < 1:
        player.handle_keydown(events[pg.KEYDOWN])
        player.handle_keyup(events[pg.KEYUP])
        for render_to in renderables:
            render_to(screen)
        pg.display.update()
        clock.tick(30)
    pg.quit()
    quit()

def fill_background(screen: pg.Surface):
    """Fill entire pygame surface with a solid color"""
    screen.fill(colors.BLACK)

if __name__ == '__main__':
    BARRIER_RENDERERS = [grid.draw_polygon(b) for b in BARRIERS]
    RENDERABLES = [
        fill_background,
        grid.draw_border()
    ]
    RENDERABLES += BARRIER_RENDERERS
    game_loop(renderables=RENDERABLES)
