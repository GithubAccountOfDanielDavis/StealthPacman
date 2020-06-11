"""Create and store impassable barriers on the grid"""

from enum import IntEnum
from collections import namedtuple
from typing import Optional
from pygame import Vector2

class Rotation(IntEnum):
    """Clockwise rotations in degrees"""
    NONE = 0
    CW_90 = 90
    CW_180 = 180
    CW_270 = 270

Stem = namedtuple('Stem', ['left_offset', 'width', 'height'])

def make_barrier(*,
        top, left, width, height,
        stem: Optional[Stem] = None,
        rotation: Optional[Rotation] = None):
    """Create a polygonal barrier on the grid with rounded corners.
    
    Stems allow for ˥-shaped, T-shaped, and Г-shaped barriers.
    Stems always point down by default and must be rotated.
    Ommitting a stem just creates a rounded rectangle.
    The top-left-most is fixed to top/left args after rotation.
        So these two are equivalent:
        a = make_barrier(
            top=1, left=2,
            width=3, height=4,
            rotation=Rotation.DEG_90)
        b = make_barrier(
            top=1, left=2,
            width=4, height=3,
            rotation=Rotation.NONE)
        assert a == b
    """
    if top < 0 or left < 0 or width < 1 or height < 1 or (
        stem is not None and (
            stem.left_offset < 0
            or stem.width < 1
            or stem.height < 1
            or stem.left_offset + stem.width > width
        )
    ):
        raise ValueError('Invalid barrier shape')

    topleft, topright, bottomleft, bottomright = (
        Vector2(0, 0),      Vector2(width, 0),
        Vector2(0, height), Vector2(width, height))
    
    points = [topleft, topright]

    if stem is not None:
        stem_tl, stem_tr, stem_bl, stem_br = (
            Vector2(stem.left_offset,              height),
            Vector2(stem.left_offset + stem.width, height),
            Vector2(stem.left_offset,              height + stem.height),
            Vector2(stem.left_offset + stem.width, height + stem.height))
        points += (
            [stem_br]
            if stem.left_offset + stem.width == width
            else [bottomright, stem_tr, stem_br])
        points += (
            [stem_bl]
            if stem.left_offset == 0
            else [stem_bl, stem_tl, bottomleft])
    else:
        points += [bottomright, bottomleft]

    if rotation is not None and rotation != 0:
        points = [p.rotate(rotation) for p in points]
        x_adjustment, y_adjustment = (
            min(p.x for p in points),
            min(p.y for p in points))
        adjustment = Vector2(-x_adjustment, -y_adjustment)
        points = [p + adjustment for p in points]

    topleft_adjustment = Vector2(left, top)
    points = [p + topleft_adjustment for p in points]

    return points

BARRIERS = [
    # Top row
    make_barrier(left=2, top=2, width=3, height=2),
    make_barrier(left=7, top=2, width=4, height=2),
    make_barrier(left=13, top=0, width=1, height=4),
    make_barrier(left=16, top=2, width=4, height=2),
    make_barrier(left=22, top=2, width=3, height=2),

    # Next row
    make_barrier(left=2,  top=6, width=3, height=1),
    make_barrier(left=22, top=6, width=3, height=1),

    # Middle section
    make_barrier(left=0, top=9, width=5, height=10),
    make_barrier(left=7, top=6, width=7, height=1,
        stem=Stem(left_offset=3, width=1, height=3),
        rotation=Rotation.CW_270),
    make_barrier(left=10, top=6, width=7, height=1,
        stem=Stem(left_offset=3, width=1, height=3)),
    make_barrier(left=16, top=6, width=7, height=1,
        stem=Stem(left_offset=3, width=1, height=3),
        rotation=Rotation.CW_90),
    make_barrier(left=22, top=9, width=5, height=10),

    # Cage
    make_barrier(left=7, top=15, width=1, height=4),
    make_barrier(left=10, top=12, width=7, height=4),
    make_barrier(left=19, top=15, width=1, height=4),

    # Bottom, top row
    make_barrier(left=2, top=21, width=3, height=1,
        stem=Stem(left_offset=2, width=1, height=3)),
    make_barrier(left=7, top=21, width=4, height=1),
    make_barrier(left=10, top=18, width=7, height=1,
        stem=Stem(left_offset=3, width=1, height=3)),
    make_barrier(left=16, top=21, width=4, height=1),
    make_barrier(left=22, top=21, width=3, height=1,
        stem=Stem(left_offset=0, width=1, height=3)),
    
    # Bottom, bottom row
    make_barrier(left=0, top=24, width=2, height=1),
    make_barrier(left=2, top=24, width=9, height=1,
        stem=Stem(left_offset=3, width=1, height=3),
        rotation=Rotation.CW_180),
    make_barrier(left=10, top=24, width=7, height=1,
        stem=Stem(left_offset=3, width=1, height=3)),
    make_barrier(left=16, top=24, width=9, height=1,
        stem=Stem(left_offset=5, width=1, height=3),
        rotation=Rotation.CW_180),
    make_barrier(left=25, top=24, width=2, height=1),
]
