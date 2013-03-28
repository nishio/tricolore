# -*- encoding: utf-8 -*-
"""
script to run with shuyo's AI

"""

import shuyo
import __init__
__init__.VERBOSE = False
import tricolore
tricolore.SAMPLE_PER_ACTION = 0

from __init__ import MontecarloPlayer

while True:
    red_win = 0
    red_lose = 0
    red_even = 0
    mc_win = 0
    mc_lose = 0
    mc_even = 0
    tricolore.SAMPLE_PER_ACTION += 50
    for _j in range(50):
        players = (
            (shuyo.RED, "RED", MontecarloPlayer('RED')),
            (shuyo.BLUE, "BLUE", shuyo.MinMax('BLUE')))
        try:
            r, b = shuyo.match(players, None)
        except:
            r = b = 0 # error consider as even
        if r > b:
            red_win += 1
            mc_win += 1
        elif r < b:
            red_lose += 1
            mc_lose += 1
        else:
            red_even += 1
            mc_even += 1

        #print 'Red win:lose:even=%d:%d:%d' % (red_win, red_lose, red_even)
        #print 'MC win:lose:even=%d:%d:%d' % (mc_win, mc_lose, mc_even)

        players = (
            (shuyo.RED, "RED", shuyo.MinMax('RED')),
            (shuyo.BLUE, "BLUE", MontecarloPlayer('BLUE')))
        try:
            r, b = shuyo.match(players, None)
        except:
            r = b = 0 # error consider as even

        if r > b:
            red_win += 1
            mc_lose += 1
        elif r < b:
            red_lose += 1
            mc_win += 1
        else:
            red_even += 1
            mc_even += 1

    print 'SAMPLE_PER_ACTION:', tricolore.SAMPLE_PER_ACTION
    print 'Red win:lose:even=%d:%d:%d' % (red_win, red_lose, red_even)
    print 'MC win:lose:even=%d:%d:%d' % (mc_win, mc_lose, mc_even)
    print
