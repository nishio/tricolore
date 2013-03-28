"""
Interface for
https://github.com/shuyo/misc/blob/master/tricolour/tricolore.py
"""
from tricolore import Game, reverse, put, opposite, montecarlo_ucb
from enum import *

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
        put(self.game, pos, color)
        self.game.switch_user()

    def nextmove(self):
        actions = self.game.get_possible_actions()
        if not actions:
            return ('PASS', None, None)
        pos, color = montecarlo_ucb(actions, self.game)
        put(self.game, pos, color)
        if color == self.side:
            return ('MOVE', pos, self.side_s)
        else:
            return ('MOVE', pos, 'WHITE')

