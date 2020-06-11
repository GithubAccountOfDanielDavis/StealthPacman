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

def display_fps(milliseconds, screen):
    font = pg.font.SysFont('FreeMono, Monospace', 30, True)
    text = font.render(f'FPS: {int(1.0 / (milliseconds / 1000.0))}', True, (0, 0, 0))
    text.get_rect().left = 0
    screen.blit(text, (218, 275))

Renderable = typing.Callable[[pg.Surface], None]
def game_loop(renderables: typing.Sequence[Renderable], fps=90):
    """Initialize pygame and run loop until it's over"""
    pg.init()
    pg.display.set_caption('Pacman')
    screen = pg.display.set_mode(grid.SCREEN_SIZE)
    clock = pg.time.Clock()
    milliseconds = clock.tick(fps)

    player = Player(pg.Vector2(13.5, 23))
    renderables.append(player.render)

    while len((events := get_events())[pg.QUIT]) < 1:
        for event in events[pg.KEYDOWN]:
            player.handle_keydown(event)
        for event in events[pg.KEYUP]:
            player.handle_keyup(event)
        player.update(milliseconds)
        for render_to in renderables:
            render_to(screen)
        display_fps(milliseconds, screen)
        pg.display.update()
        milliseconds = clock.tick(fps)
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
