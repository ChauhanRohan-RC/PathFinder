from constant import *
from path_finder import print_maze, find_path
import time

maze = [[Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall],
        [Wall, '  ', '  ', '  ', Wall, '  ', '  ', '  ', Wall, '  ', '  ', '  ', '  ', '  ', Wall, '  ', '  ', '  ', Wall, '  ', Wall],
        [Wall, '  ', Wall, '  ', Wall, '  ', Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, '  ', Wall, Wall, Wall, Wall, Wall, Wall],
        [Wall, '  ', Wall, '  ', '  ', '  ', Wall, Wall, Wall, Wall, Wall, '  ', Wall, Wall, '  ', Wall, Wall, Wall, Wall, '  ', Wall],
        [Wall, '  ', Wall, Wall, Wall, Wall, Wall, '  ', '  ', '  ', Wall, '  ', '  ', Wall, '  ', Wall, Wall, Wall, Wall, '  ', Wall],
        [Wall, '  ', Wall, Wall, Wall, Wall, Wall, '  ', Wall, '  ', Wall, Wall, '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', Wall],
        [Wall, '  ', '  ', '  ', '  ', Wall, '  ', '  ', Wall, '  ', Wall, Wall, Wall, '  ', Wall, Wall, Wall, '  ', Wall, Wall, Wall],
        [Wall, '  ', Wall, Wall, '  ', Wall, Wall, Wall, Wall, '  ', Wall, Wall, Wall, '  ', '  ', Wall, Wall, '  ', '  ', '  ', Wall],
        [Wall, '  ', Wall, Wall, '  ', '  ', '  ', Wall, Wall, '  ', Wall, Wall, Wall, Wall, '  ', '  ', Wall, Wall, Wall, '  ', Wall],
        [S__P, '  ', Wall, Wall, Wall, Wall, Wall, Wall, '  ', '  ', '  ', '  ', '  ', Wall, Wall, '  ', Wall, Wall, Wall, '  ', E__P],
        [Wall, '  ', '  ', '  ', '  ', Wall, '  ', '  ', '  ', Wall, Wall, Wall, '  ', Wall, Wall, '  ', Wall, Wall, Wall, Wall, Wall],
        [Wall, '  ', '  ', Wall, '  ', '  ', '  ', Wall, '  ', '  ', Wall, Wall, '  ', '  ', '  ', '  ', Wall, Wall, Wall, Wall, Wall],
        [Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall, Wall]]


s__time = time.perf_counter_ns()
path = find_path(maze)
e__time = time.perf_counter_ns()

print_maze(maze, path)
print(f'\nCompleted in : {(e__time - s__time) / (10 ** 9 )} seconds')
