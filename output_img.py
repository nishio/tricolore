# -*- encoding: utf-8 -*-
"""
Render image for presentation
"""

import shuyo
import __init__
__init__.OUTPUT_IMAGE = True
mc = __init__.MontecarloPlayer('RED')

players = (
    (shuyo.RED, "RED", mc),
    (shuyo.BLUE, "BLUE", shuyo.MinMax('BLUE')))
r, b = shuyo.match(players, True)
