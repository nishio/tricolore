"""
Interface for
https://github.com/shuyo/misc/blob/master/tricolour/tricolore.py
"""
from tricolore import Game, reverse, put, opposite, montecarlo_ucb
from enum import *
VERBOSE = False
OUTPUT_IMAGE = False
from renderer import Renderer
renderer = Renderer()

class MontecarloPlayer(object):
    name = 'nishio:montecarlo'
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
        if OUTPUT_IMAGE:
            renderer.draw(self.game.map)

    def move(self, pos, color):
        assert self.game.next == self.opposite
        if color == 'WHITE':
            color = reverse(self.opposite)
        elif color == 'PASS':
            if VERBOSE:
                print 'move called:', pos, color
                self.game.print_map()
            self.game.switch_user()
            return
        else:
            color = self.opposite
        y, x = pos
        put(self.game, (x, y), color)
        if VERBOSE:
            print 'move called:', pos, color
            self.game.print_map()
        self.game.switch_user()
        if OUTPUT_IMAGE:
            renderer.draw(self.game.map)

    def nextmove(self):
        #assert self.game.next == self.side
        if self.game.next != self.side:
            # opponent did pass
            self.game.switch_user()

        actions = self.game.get_possible_actions()
        if not actions:
            self.game.switch_user()
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

        if OUTPUT_IMAGE:
            renderer.draw(self.game.map)

        return ret


class Human(MontecarloPlayer):
    def nextmove(self):
        #assert self.game.next == self.side
        if self.game.next != self.side:
            # opponent did pass
            self.game.switch_user()

        actions = self.game.get_possible_actions()
        if not actions:
            self.game.switch_user()
            return ('PASS', None, None)
        pos, color = montecarlo_ucb(actions, self.game)
        self.game.print_map()
        print pos, color
        pos, color = input('(pos, color)>>>')
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
