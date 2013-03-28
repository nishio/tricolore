"""
Interface for
https://github.com/shuyo/misc/blob/master/tricolour/tricolore.py
"""
from tricolore import Game, reverse, put, opposite, montecarlo_ucb
from enum import *
VERBOSE = False

class MontecarloPlayer(object):
    def __init__(self, side):
        self.game = Game()
        if side == 'RED':
            self.side = RED
        elif side == 'BLUE':
            self.side = BLUE
        else:
            raise AssertionError
        self.side_s = side
        self.opposite = opposite(self.side)

    def move(self, pos, color):
        if color == 'WHITE':
            color = reverse(self.opposite)
        else:
            color = self.opposite
        y, x = pos
        put(self.game, (x, y), color)
        if VERBOSE:
            print 'move called:', pos, color
            self.game.print_map()
        self.game.switch_user()

    def nextmove(self):
        actions = self.game.get_possible_actions()
        if not actions:
            return ('PASS', None, None)
        pos, color = montecarlo_ucb(actions, self.game)
        put(self.game, pos, color)
        self.game.switch_user()
        x, y = pos
        if color == self.side:
            ret = ('MOVE', (y, x), self.side_s)
        else:
            ret = ('MOVE', (y, x), 'WHITE')

        if VERBOSE:
            print 'nextmove called, returns:', ret
            self.game.print_map()
        return ret

