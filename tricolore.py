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

    def do(self, (pos, color)):
        put(self, pos, color)
        self.switch_user()

        # finish game
        if not RED in self.map:
            return True
        if not BLUE in self.map:
            return True
        if not self.get_possible_actions():
            self.switch_user()
            if not self.get_possible_actions():
                return True

    def is_no_more_move(self):
        if not self.get_possible_actions():
            self.switch_user()
            if not self.get_possible_actions():
                return True
            self.switch_user()
        return False

    def get_reward(self):
        if not self.next in self.map:
            return -1.0
        if not opposite(self.next) in self.map:
            return 1.0
        if self.is_no_more_move():
            red = self.map.count(RED)
            blue = self.map.count(BLUE)
            if red > blue:
                if self.next == RED:
                    return 1.0
                else:
                    return -1.0
            elif blue > red:
                if self.next == BLUE:
                    return 1.0
                else:
                    return -1.0

        return 0.0

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()

if 0:
    import rl_lib
    game = Game()
    Qtable = rl_lib.initialize_q()
    for i in range(100):
        rl_lib.sarsa(game, Qtable)
    print len(Qtable)
    print Qtable
    game.initialize()

