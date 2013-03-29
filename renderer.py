import Image
import ImageDraw
import shuyo
import __init__
from enum import *

HEIGHT = WIDTH = 400
MARGIN = 10
CELL = (WIDTH - 2 * MARGIN) / 6
PADDING = 10
RADIUS = CELL - 2 * PADDING
class Renderer(object):
    def __init__(self):
        self.t = 0
    def draw(self, gmap):
        im = Image.new('RGB', (WIDTH, HEIGHT), (0, 200, 0))
        draw = ImageDraw.Draw(im)

        for i in range(7):
            t = MARGIN + CELL * i
            draw.line((MARGIN, t, WIDTH - MARGIN, t), (0, 0, 0), width=3)
            draw.line((t, MARGIN, t, WIDTH - MARGIN), (0, 0, 0), width=3)

        for pos in range(36):
            x = pos % 6
            y = pos / 6
            tx = MARGIN + CELL * x + PADDING
            ty = MARGIN + CELL * y + PADDING
            fill = (250, 250, 250)
            if gmap[pos] == RED:
                fill = (200, 0, 0)
            elif gmap[pos] == BLUE:
                fill = (0, 0, 200)
            elif gmap[pos] == EMPTY:
                continue

            draw.ellipse(
                (tx, ty, tx + RADIUS, ty + RADIUS),
                fill=fill)

        im.save('img/fig%02d.png' % self.t)
        self.t += 1

