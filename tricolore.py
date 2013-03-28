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

EMPTY = 0
RED = 1
BLUE = 2
WHITE_R = 5
WHITE_B = 6
WHITE = [WHITE_R, WHITE_B]
CHARS = '.rBxxoo'
MAP_WIDTH = 6
REVERSED = [None, WHITE_R, WHITE_B, None, None, RED, BLUE]

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


    def do_playout(self):
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
            pos, color = choose_randomly(actions, self)
            put(self, pos, color)
            self.switch_user()

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

# Policy (context: Reinforce Learning)
def choose_randomly(possible_actions, game):
    from random import choice
    return choice(possible_actions)

def montecalro(possible_actions, game):
    "play random 100 times for each possible actions"
    scores = []
    for a in possible_actions:
        score = 0
        g = game.clone()
        put(g, *a)
        g.switch_user()
        for i in range(100):
            score += g.clone().do_playout()
        scores.append(score)

    return possible_actions[argmax(scores)]

def argmax(xs):
    max_value = max(xs)
    return xs.index(max_value)

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()



# test_random_playout
game = Game()
game.clone().do_playout()
game.clone().do_playout()
game.clone().do_playout()

