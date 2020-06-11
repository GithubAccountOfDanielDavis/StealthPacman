import typing
from collections import namedtuple

import pygame as pg
import grid
import colors

from barriers import BARRIERS

def fill_background(screen: pg.Surface):
    screen.fill(colors.BLACK)

Renderable = typing.Callable[[pg.Surface], None]
def game_loop(renderables: typing.Sequence[Renderable]):
    pg.init()
    pg.display.set_caption('Pacman')
    screen = pg.display.set_mode(grid.SCREEN_SIZE)
    clock = pg.time.Clock()

    running = True
    while (running := not any(e.type == pg.QUIT for e in pg.event.get())):
        for r in renderables:
            r(screen)
        pg.display.update()
        clock.tick(30)
    pg.quit()
    quit()

if __name__ == '__main__':
    game_loop(renderables=[
        fill_background,
        grid.draw_grid_rectangle(grid.BORDER_RECT)
    ] + [grid.draw_grid_polygon(b) for b in BARRIERS])
