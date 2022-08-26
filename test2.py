import sys
import pygame
from functools import reduce
from threading import Thread
from Config import Config
from test import Heap
import time


# Initialising Pygame
pygame.init()
pygame.display.init()
pygame.font.init()

# Loading Configurations if any
Config.load_from_file(Config.ConfigFilePath)


class Node:
    Surface = None                               # Should be Grid Surface

    # DIMENSIONS .......................................
    SideLength = Config.SideLength                    # Pixels
    Diagonal = Config.Diagonal
    OutWidth = Config.OutWidth

    _InSideLength = Config.InSideLength

    # COLORS ..............................................
    OutNormalColor = Config.OutNormalColor            # Normal Outline Colour

    NormalFill = Config.NormalFill                    # Fill when Normal
    StartFill = Config.StartFill                      # Fill when Marked As Start
    EndFill = Config.EndFill                          # Fill when Marked As End
    ObsFill = Config.ObsFill                          # Fill when Marked as Obstacle

    ClosedFill = Config.ClosedFill                    # Fill when marked as closed
    OpenFill = Config.OpenFill                        # Fill when marked as open
    PathFill = Config.PathFill                        # Fill when marked as Found PAth

    @classmethod
    def set_surface(cls, _surface):
        cls.Surface = _surface

    def __init__(self, pos):
        self.row, self.col = pos
        self.x, self.y = self.col * self.SideLength, self.row * self.SideLength

        self.g_cost = self.h_cost = self.f_cost = 0  # G is from the start (consider path), H is diagonal distance from the end
        self.parent = None

        self.draw(in_color=self.NormalFill)

    def draw(self, in_color):
        # MAin Rect
        pygame.draw.rect(self.Surface, in_color,
                         (self.x + self.OutWidth, self.y + self.OutWidth, self._InSideLength, self._InSideLength), 0)

    def __bool__(self):
        return True

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Node({self.row}, {self.col})'

    def __eq__(self, other):
        if type(other) == self.__class__:
            return self.row == other.row and self.col == other.col
        return False

    def __hash__(self):
        return hash((self.row, self.col))

    def get_g_cost(self, neighbour):
        if abs(neighbour.row - self.row) + abs(neighbour.col - self.col) == 1:
            return neighbour.g_cost + self.SideLength
        return neighbour.g_cost + self.Diagonal

    def set_parent(self, node):
        self.g_cost = self.get_g_cost(node)
        self.f_cost = self.g_cost + self.h_cost
        self.parent = node

    def set_h_cost(self, e_node):
        # F_cost need to be updated also, self.f_cost = self.g_cost + self.h_cost
        self.h_cost = int(((abs(e_node.row - self.row) * self.SideLength) ** 2) + ((abs(e_node.col - self.col) * self.SideLength) ** 2) ** 0.5)

    # Drawing And Updating
    def mark_start(self):
        self.draw(in_color=self.StartFill)

    def mark_end(self):
        self.draw(in_color=self.EndFill)

    def mark_obs(self):
        self.draw(in_color=self.ObsFill)

    def mark_open(self):
        self.draw(in_color=self.OpenFill)

    def mark_closed(self):
        self.draw(in_color=self.ClosedFill)

    def mark_path(self):
        self.draw(in_color=self.PathFill)

    def mark_normal(self):
        self.draw(in_color=self.NormalFill)
        self.g_cost = self.h_cost = self.f_cost = 0
        self.parent = None


class Grid:
    def __init__(self, surface, statusbar, rows=10, cols=10, bg=Node.OutNormalColor):
        self.surface = surface
        self.status_bar = statusbar
        self.surface.fill(bg)

        self.delay = Config.VisualDelay                   # delay in each iteration of algorithm in ms
        self.rows, self.cols = rows, cols

        self.running = False
        self.running = False

        self.nodes = {}  # (row, col) : node
        self.start_node = None
        self.end_node = None
        self.obs_nodes = set()  # obs_node

        self.open_nodes = Heap()
        self.closed_nodes = set()

        # DRAWING
        self.draw()

    def set_outline_color(self, color):
        self.surface.fill(color)

    def is_valid(self, pos) -> bool:
        """ checks validity of position """
        if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols:
            return True
        return False

    def draw(self):
        """ draws grid on master """
        Node.set_surface(self.surface)
        for row in range(self.rows):
            for col in range(self.cols):
                self.nodes[(row, col)] = Node((row, col))

    @staticmethod
    def _get_pos():
        m__x, m__y = pygame.mouse.get_pos()
        return m__y // Node.SideLength, m__x // Node.SideLength

    def set_start(self):
        """ sets the START_POINT (unique) """
        if not self.running:
            if self.open_nodes:
                self._clear_grid()

            _pos = self._get_pos()
            if self.is_valid(_pos):
                if self.start_node:
                    if self.start_node.row == _pos[0] and self.start_node.col == _pos[1]:
                        return
                    self.start_node.mark_normal()

                self.start_node = self.nodes[_pos]
                if self.start_node in self.obs_nodes:
                    self.obs_nodes.remove(self.start_node)
                self.start_node.mark_start()
                self.status_bar.set_text(f'Start position marked at {self.start_node}', (0, 220, 0))

    def set_end(self):
        """ sets the END_POINT (unique)"""
        if not self.running:
            if self.open_nodes:
                self._clear_grid()

            _pos = self._get_pos()
            if self.is_valid(_pos):
                if self.end_node:
                    if self.end_node.row == _pos[0] and self.end_node.col == _pos[1]:
                        return
                    self.end_node.mark_normal()

                self.end_node = self.nodes[_pos]
                if self.end_node in self.obs_nodes:
                    self.obs_nodes.remove(self.end_node)
                self.end_node.mark_end()
                self.status_bar.set_text(f'End position marked at {self.end_node}', (0, 220, 0))

    def mark_obs(self):
        """ sets an obstacle """
        if not self.running:
            if self.open_nodes:
                self._clear_grid()
                return

            _pos = self._get_pos()
            if self.is_valid(_pos):
                __node = self.nodes[_pos]
                if __node == self.start_node or __node == self.end_node:
                    return
                if __node not in self.obs_nodes:
                    self.obs_nodes.add(__node)
                    __node.mark_obs()
                    self.status_bar.set_text(f'Marking obstacles {__node}', (0, 220, 0))

    def unmark_obs(self):
        """ unmark previously set obstacle """
        if not self.running:
            if self.open_nodes:
                self._clear_grid()
                return

            _pos = self._get_pos()
            if self.is_valid(_pos):
                __node = self.nodes[_pos]
                if __node in self.obs_nodes:
                    self.obs_nodes.remove(__node)
                    __node.mark_normal()
                    self.status_bar.set_text(f'Removing obstacle {__node}', (0, 220, 0))

    def _clear_grid(self):
        """ clears whole grid """
        if not self.running:
            if self.start_node:
                self.start_node.mark_normal()
                self.start_node = None
            if self.end_node:
                self.end_node.mark_normal()
                self.end_node = None

            for obs__node in self.obs_nodes:
                obs__node.mark_normal()
            for open__node in self.open_nodes:
                open__node.mark_normal()
            for closed__node in self.closed_nodes:
                closed__node.mark_normal()

            self.trace_back_cache = None
            self.obs_nodes.clear()
            self.open_nodes.clear()
            self.closed_nodes.clear()
            self.status_bar.set_text('Grid Cleared !!', (230, 0, 0))

    def reset_grid(self):
        """ resets grid after algorithm finished running when user press reset key """
        if not self.running:
            self._clear_grid()

    @staticmethod
    def _get_node(node__1, node__2):
        """ :return : node with least f_cost, or h_cost or g_cost """
        if node__1.f_cost < node__2.f_cost:
            return node__1
        elif node__1.f_cost == node__2.f_cost:
            if node__1.h_cost < node__2.h_cost:
                return node__1
            elif node__1.h_cost == node__2.h_cost:
                if node__1.g_cost < node__2.g_cost:
                    return node__1
        return node__2

    @staticmethod
    def _is_cheap(node__1, node__2):
        """ returns whether node__1 has low cost """
        if node__1.f_cost < node__2.f_cost:
            return True
        elif node__1.f_cost == node__2.f_cost:
            if node__1.h_cost < node__2.h_cost:
                return True
            elif node__1.h_cost == node__2.h_cost:
                if node__1.g_cost < node__2.g_cost:
                    return True
        return False

    def _yield_neighbours(self, node):
        """ yields all possible valid neighbours """
        __poss = ((node.row + 1, node.col), (node.row - 1, node.col), (node.row, node.col + 1), (node.row, node.col - 1),
                  (node.row + 1, node.col + 1), (node.row + 1, node.col - 1), (node.row - 1, node.col + 1),
                  (node.row - 1, node.col - 1))
        for _pos in __poss:
            if self.is_valid(_pos):
                yield self.nodes[_pos]

    def trace_back(self, e_node=None):
        self.status_bar.set_text('Resolving Path', (0, 220, 0))
        count = 0
        while e_node:
            e_node.mark_path()
            e_node = e_node.parent
            count += 1

        self.start_node.mark_start()
        self.end_node.mark_end()
        return count

    """
    calibrates self.end node with parents, for tracing path,
    or None if no path is possible
    """
    def solve_loop(self):
        s = time.time()
        while True:
            if self.open_nodes:
                c__node = self.open_nodes.pop(0)
            else:
                self.show_algo_result(None)
                return

            if c__node == self.end_node:
                r = time.time() - s
                print(f"Completed in : {r}")
                self.show_algo_result(c__node)
                return

            if c__node != self.start_node:
                c__node.mark_closed()
            self.closed_nodes.add(c__node)

            for n__node in self._yield_neighbours(c__node):
                if n__node not in self.closed_nodes and n__node not in self.obs_nodes:
                    if n__node not in self.open_nodes:
                        n__node.set_h_cost(self.end_node)
                        n__node.set_parent(c__node)
                        self.open_nodes.append(n__node)
                        n__node.mark_open()
                        self.open_nodes.sort_tree(-1, self._is_cheap)
                    elif n__node.get_g_cost(c__node) < n__node.g_cost:
                        n__node.set_parent(c__node)
                        self.open_nodes.sort_tree(self.open_nodes.index(n__node), self._is_cheap)

            pygame.time.wait(self.delay)

    def start_algo(self):
        """ locks grid from user input and starts algorithm """
        if not self.running:
            self.running = True
            if self.open_nodes or self.closed_nodes:
                self.running = False
                self._clear_grid()
                return

            if not (self.start_node and self.end_node):
                self.running = False
                self.status_bar.set_text('Mark Start snd End Nodes First !!', (230, 0, 0))
                return

            self.open_nodes.append(self.start_node)
            __th = Thread(target=self.solve_loop)
            self.status_bar.set_text('Algorithm Started !!', (0, 220, 0))
            __th.start()
        else:
            self.status_bar.set_text('Algorithm Already Running !!!', (230, 0, 0))

    def show_algo_result(self, e_node):
        if e_node:
            _steps = self.trace_back(e_node.parent)
            self.status_bar.set_text('Process Completed Successfully !!  Steps Required : %s' % _steps, (0, 220, 0))
        else:
            self.status_bar.set_text('Process Failed !! No valid path detected', (220, 0, 0))
        self.running = False


class StatusBar:
    def __init__(self, surface, size, pos, bg=(255, 255, 255), pady=4, font=None):
        self.surface = surface
        self.width, self.height = size
        self.x, self.y = pos
        self.font = font if font else pygame.font.SysFont(*Config.StatusBarFont)
        self.bg = bg
        self.pady = pady
        self._height = self.height - self.pady
        self._y = self. y + self.pady

        self.draw()

    def draw(self):
        pygame.draw.rect(self.surface, self.bg, (self.x, self._y, self.width, self._height), 0)

    def set_text(self, text, color=(0, 220, 0)):
        self.draw()
        __im = self.font.render(text, 1, color, self.bg)
        _pos = self.x + ((self.width - __im.get_width()) / 2), self._y + ((self._height - __im.get_height()) / 2)
        self.surface.blit(__im, _pos)


def quit_():
    pygame.quit()
    sys.exit()


# Gui Handler
def gui_handler():

    __run = True
    while __run:
        keys = pygame.key.get_pressed()
        m_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            # QUIT SIGNAL
            if event.type == pygame.QUIT:
                __run = False
                break
            if (keys[pygame.K_LALT] or keys[pygame.K_RALT]) and keys[pygame.K_F4]:       # Alt EVENTS ..................
                __run = False
                break

            if not grid.running:
                if keys[pygame.K_s]:  # s key
                    grid.set_start()
                    continue
                if keys[pygame.K_e]:  # e key
                    grid.set_end()
                    continue
                if keys[pygame.K_d]:  # d key
                    grid.unmark_obs()
                    continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter Key
                    grid.start_algo()
                    continue

                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:    # CONTROL EVENTS ..................
                    if keys[pygame.K_r]:
                        grid.reset_grid()
                        continue

                # MOUSE Events ........................................
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left Click
                        grid.mark_obs()

                    if event.button == 3:  # Right Click
                        grid.unmark_obs()
                    continue

                if m_buttons[0]:  # Left Click motion
                    grid.mark_obs()
                    continue
                if m_buttons[2]:  # Right Click motion
                    grid.unmark_obs()
                    continue

        pygame.display.update()
    quit_()


win = pygame.display.set_mode((Config.W_WIDTH, Config.W_HEIGHT))
pygame.display.set_caption("Path Finder")

grid = Grid(win, None, Config.GRID_ROWS, Config.GRID_COLS)

status_bar = grid.status_bar = StatusBar(win, (Config.W_WIDTH, Config.StatusBarHeight), (0, Config.W_HEIGHT - Config.StatusBarHeight))
status_bar.set_text(text=Config.StatusInstruction, color=(30, 30, 30))

gui_handler()
