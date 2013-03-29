# -*- encoding: utf-8 -*-
"""
script to run with shuyo's AI

"""

import shuyo
import tricolore
tricolore.SAMPLE_PER_ACTION = 200

from __init__ import Human
players = (
    (shuyo.RED, "RED", Human('RED')),
    (shuyo.BLUE, "BLUE", shuyo.MinMax('BLUE')))
shuyo.match(players, True)
