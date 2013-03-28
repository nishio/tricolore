# -*- encoding: utf-8 -*-
"""
Tricolore

>>> g = Game()
>>> g.print_map()
. . . . . .
. . . . . .
. . r B . .
. . B r . .
. . . . . .
. . . . . .

>>> get_cells_to_reverse(g, (2, 4), RED)
[(2, 3)]

>>> put(g, (2, 4), RED)
>>> g.print_map()
. . . . . .
. . . . . .
. . r B . .
. . o r . .
. . r . . .
. . . . . .

>>> put(g, (4, 3), WHITE_B)
>>> g.print_map()
. . . . . .
. . . . . .
. . r B . .
. . o o o .
. . r . . .
. . . . . .

>>> list(g.get_possible_actions())
[((1, 1), 5), ((2, 1), 5), ((3, 1), 5), ((4, 1), 5), ((4, 2), 1), ((4, 4), 1), ((1, 5), 5), ((2, 5), 5)]

>>> put(g, (4, 2), RED)
>>> g.print_map()
. . . . . .
. . . . . .
. . r o r .
. . o r o .
. . r . . .
. . . . . .
"""
from math import sqrt, log
from collections import Counter
from enum import *

WHITE = [WHITE_R, WHITE_B]
CHARS = '.rBxxoo'
MAP_WIDTH = 6
REVERSED = [None, WHITE_R, WHITE_B, None, None, RED, BLUE]
SAMPLE_PER_ACTION = 100

if getattr(__builtins__, 'profile', None) == None:
    profile = lambda x: x

def reverse(color):
    ret = REVERSED[color]
    if ret == None: raise AssertionError('cannot reverse')
    return ret


def is_same_color(x, y):
    if x == y:
        return True
    if x in WHITE and y in WHITE:
        return True
    return False

@profile
def get_cells_to_reverse(game, pos, color):
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    to_reverse = []
    for dx, dy in dirs:
        x, y = pos
        buf = []
        while True:
            x += dx
            y += dy
            if x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_WIDTH:
                # out of bound
                break
            v = game._get(x, y)
            if v == EMPTY:
                break
            if is_same_color(v, color):
                to_reverse.extend(buf)
                break
            buf.append((x, y))
    return to_reverse


def put(game, pos, color):
    to_reverse = get_cells_to_reverse(game, pos, color)
    if not to_reverse:
        game.print_map()
        print pos, color
        raise AssertionError('no possible turns')
    for x, y in to_reverse:
        game._set(x, y, reverse(game._get(x, y)))
    game._set(*pos, color=color)


def opposite(x):
    if x == RED:
        return BLUE
    elif x == BLUE:
        return RED
    else:
        raise AssertionError


# Policy (context: Reinforce Learning)
def choose_randomly(possible_actions, game):
    from random import choice
    return choice(possible_actions)


def montecarlo(possible_actions, game):
    "play random 100 times(SAMPLE_PER_ACTION) for each possible actions"
    scores = []
    for a in possible_actions:
        score = 0
        g = game.clone()
        put(g, *a)
        g.switch_user()
        for i in range(SAMPLE_PER_ACTION):
            # whi minus? : because it is score for opposite
            score -= g.clone().do_playout()
        scores.append(score)

    return possible_actions[argmax(scores)]


def montecarlo_ucb(possible_actions, game):
    "play 100 x len(possible_actions) times, choosing action with UCB"
    scores = []
    visited = []
    games = []
    for a in possible_actions:
        g = game.clone()
        put(g, *a)
        g.switch_user()
        games.append(g)
        score = -g.clone().do_playout()
        scores.append(score)
        visited.append(1)

    N = len(possible_actions)
    parent_visited = N
    for _sample in xrange(N * (SAMPLE_PER_ACTION - 1)):
        ucb = [0] * N
        for i in xrange(N):
            v = visited[i]
            ucb[i] = scores[i] / v + sqrt(2 * log(parent_visited) / v)
        ai = argmax(ucb)
        score = -games[ai].clone().do_playout()
        scores[ai] += score
        visited[ai] += 1

    for i in xrange(N):
        scores[i] /= visited[i]

    return possible_actions[argmax(scores)]


def argmax(xs):
    max_value = max(xs)
    return xs.index(max_value)


class Game(object):
    def __init__(self):
        self.initialize()


    def initialize(self):
        self.map = [EMPTY] * (MAP_WIDTH * MAP_WIDTH)
        self._set(2, 2, RED)
        self._set(2, 3, BLUE)
        self._set(3, 2, BLUE)
        self._set(3, 3, RED)
        self.t = 0
        self.next = RED


    def _set(self, x, y, color):
        self.map[x + y * MAP_WIDTH] = color


    def _get(self, x, y):
        return self.map[x + y * MAP_WIDTH]


    def _lines(self):
        for i in range(6):
            yield self.map[i * MAP_WIDTH:(i + 1) * MAP_WIDTH]


    def print_map(self):
        for line in self._lines():
            print ' '.join(CHARS[x] for x in line)


    def get_state(self):
        EMPTY = 0
        ME = 1
        OP = 2
        WHITE_ME = 5
        WHITE_OP = 6
        if self.next == RED:
            MAP = [EMPTY, ME, OP, None, None, WHITE_ME, WHITE_OP]
        elif self.next == BLUE:
            MAP = [EMPTY, OP, ME, None, None, WHITE_OP, WHITE_ME]
        else:
            raise AssertionError

        return ''.join(str(MAP[x]) for x in self.map)


    def get_possible_actions(self):
        ret = []
        color = self.next
        rev_color = reverse(color)
        for i in range(MAP_WIDTH * MAP_WIDTH):
            x = i % MAP_WIDTH
            y = i / MAP_WIDTH
            if self._get(x, y) != EMPTY:
                continue
            acts = get_cells_to_reverse(self, (x, y), color)
            if acts:
                ret.append(((x, y), color))
            acts = get_cells_to_reverse(self, (x, y), rev_color)
            if acts:
                ret.append(((x, y), rev_color))
        return ret


    def switch_user(self):
        self.next = opposite(self.next)


    def count_colors(self):
        red = self.map.count(RED)
        blue = self.map.count(BLUE)
        if red > blue:
            winner = RED
        elif blue > red:
            winner = BLUE
        else:
            winner = None
        return


    def do_playout(self, policy={RED: choose_randomly, BLUE: choose_randomly}, verbose=False):
        is_passed = False
        subject = self.next
        while True:
            actions = self.get_possible_actions()
            if not actions:
                if is_passed:
                    # both players have no possible move, finish
                    winner = self.count_colors()
                    break
                # no possible move, pass
                is_passed = True
                continue

            is_passed = False
            pos, color = policy[self.next](actions, self)
            put(self, pos, color)
            self.switch_user()
            if verbose:
                print pos, color
                self.print_map()

            if not RED in self.map:
                winner = BLUE
                break
            if not BLUE in self.map:
                winner = RED
                break

        if winner == subject:
            score = 1.0
        elif winner == None:
            score = 0.5
        else:
            score = 0.0

        return score

    def clone(self):
        from copy import copy
        ret = Game()
        ret.map = copy(self.map)
        ret.next = self.next
        return ret

def _test():
    import doctest
    doctest.testmod()

def run_one_play():
    game = Game()
    game.do_playout(
        policy={RED: montecarlo, BLUE: montecarlo_ucb},
        verbose=True)

def main():
    # test_random_playout
    game = Game()
    stat = Counter()
    while True:
        g = game.clone()
        s = g.do_playout(policy={RED: montecarlo_ucb, BLUE: montecarlo})
        g.print_map()
        stat.update([s])
        print stat

if __name__ == '__main__':
    _test()
    main()
