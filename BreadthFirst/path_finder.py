from constant import *
from consolecolor import Color


def print_maze(plz_maze, path_coords=()):
    __C = Color()
    __C.init()

    for i in range(len(plz_maze)):
        for j in range(len(plz_maze[0])):
            __val = plz_maze[i][j]
            if (i, j) in path_coords:
                if __val == S__P:
                    print(__C(__val, StartPointFg), end=" ")
                    continue
                if __val == E__P:
                    print(__C(__val, EndPointFg), end=" ")
                    continue
                print(__C(FoundPath, FoundPathFg), end=" ")
                continue
            print(__C(__val, WallFg), end=' ')
        print('')


def get_start_end_points(plz_maze):
    __r = []
    for i in range(len(plz_maze)):
        for j in range(len(plz_maze[0])):
            if plz_maze[i][j] in (S__P, E__P):
                __r.append((i, j))
    return __r


def get_valid(plz_maze, plz_pos):
    """ only checks boundary walls """
    o__i, o__j = plz_pos
    rows, cols = len(plz_maze), len(plz_maze[0])
    result = []

    __moves = ((o__i - 1, o__j), (o__i + 1, o__j), (o__i, o__j - 1), (o__i, o__j + 1))
    for n__i, n__j in __moves:
        if 0 <= n__i < rows:
            if 0 <= n__j < cols:
                if plz_maze[n__i][n__j] == Wall:
                    continue
                result.append((n__i, n__j))

    return result


def find_path(plz_maze):
    try:
        _start, _end = get_start_end_points(plz_maze)
    except ValueError:
        print('Could not Resolve Start and End Positions')
        return None

    paths = [[_start], ]
    _found_new = False

    while True:
        for path in paths:

            if path[-1] == _end:
                return path

            for move in get_valid(plz_maze, path[-1]):
                if move not in path:
                    if not _found_new:
                        path.append(move)
                        if move == _end:
                            return path
                        _found_new = True
                    else:
                        new_path = path[:-1]
                        new_path.append(move)
                        if move == _end:
                            return new_path
                        paths.append(new_path)
            _found_new = False
