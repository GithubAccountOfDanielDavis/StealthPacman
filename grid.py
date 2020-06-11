"""Define on-screen grid"""

from typing import Sequence
import pygame as pg
import colors

CELL_SIZE = 20
COLUMNS = 27
ROWS = 30
MARGIN = 10
MARGIN_OFFSET = pg.Vector2(MARGIN, MARGIN)

SCREEN_WIDTH = CELL_SIZE * COLUMNS + MARGIN * 2
SCREEN_HEIGHT = CELL_SIZE * ROWS + MARGIN * 2
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

def to_screen(point: pg.Vector2) -> pg.Vector2:
    """Convert from maze coordinates to pixel position"""
    return point * CELL_SIZE + pg.Vector2(MARGIN, MARGIN)

def from_screen(point: pg.Vector2) -> pg.Vector2:
    """Convert from pixel position to maze coordinates"""
    return (point - pg.Vector2(MARGIN, MARGIN)) // CELL_SIZE

BORDER_RECT = pg.Rect(0, 0, COLUMNS, ROWS)

def rect(*, left, top, width, height):
    """Wrapper for pygame Rect using kwargs"""
    return pg.Rect(left, top, width, height)

def draw_grid_rectangle(grid_rect: pg.Rect):
    """Draw grid-based rect onto screen"""
    screen_rect = rect(
        left=grid_rect.left * CELL_SIZE + MARGIN,
        top=grid_rect.top * CELL_SIZE + MARGIN,
        width=grid_rect.width * CELL_SIZE,
        height=grid_rect.height * CELL_SIZE)
    def render(screen: pg.Surface):
        pg.draw.rect(screen, colors.BLUE, screen_rect, width=3)
    return render

def draw_grid_polygon(polygon: Sequence[pg.Vector2]):
    """Draw grid-based polygon onto screen"""
    points = [p * CELL_SIZE + MARGIN_OFFSET for p in polygon]
    def render(screen: pg.Surface):
        pg.draw.polygon(screen, colors.BLUE, points, width=0)
    return render
