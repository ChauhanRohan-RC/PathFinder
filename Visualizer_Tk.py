from tkinter import Tk, Canvas, messagebox
from functools import reduce
from threading import Thread


def rgb(*r_g_b):
    return f"#%02x%02x%02x" % r_g_b


class Node:
    grid = None         # Should be Grid

    # DIMENSIONS .......................................
    SideLength = 15                     # Pixels
    Diagonal = int(1.4 * SideLength)
    OutWidth = 1                        # Should be Even
    _OutWidthHalf = OutWidth / 2

    # COLORS ..............................................
    OutColor = rgb(120, 119, 120)       # Outline Colour

    NormalFill = rgb(255, 255, 255)     # Fill when Normal
    StartFill = rgb(35, 255, 253)      # Fill when Marked As Start
    EndFill = rgb(255, 56, 49)         # Fill when Marked As End
    ObsFill = rgb(30, 30, 30)              # Fill when Marked as Obstacle

    ClosedFill = rgb(255, 91, 158)      # Fill when marked as closed
    OpenFill = rgb(101, 255, 101)         # Fill when marked as open
    PathFill = 'darkgreen'        # Fill when marked as Found PAth

    @classmethod
    def set_grid(cls, _grid):
        cls.grid = _grid

    def __init__(self, pos):
        self.row, self.col = pos          # (Row, Col)

        self.g_cost = self.h_cost = self.f_cost = 0       # G is from the start (consider path), H is diagonal distance from the end
        self.parent = None                 # Parent Node

        # Bounding Box
        self.x, self.y = self.col * self.SideLength, self.row * self.SideLength
        self.x2, self.y2 = self.x + self.SideLength, self.y + self.SideLength

        # ID
        self.id = self.grid.create_rectangle(self.x + self._OutWidthHalf, self.y + self._OutWidthHalf,
                                             self.x2 - self._OutWidthHalf, self.y2 - self._OutWidthHalf,
                                             width=self.OutWidth, outline=self.OutColor, fill=self.NormalFill)

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
        self.grid.itemconfigure(self.id, fill=self.StartFill)

    def mark_end(self):
        self.grid.itemconfigure(self.id, fill=self.EndFill)

    def mark_obs(self):
        self.grid.itemconfigure(self.id, fill=self.ObsFill)

    def mark_open(self):
        self.grid.itemconfigure(self.id, fill=self.OpenFill)

    def mark_closed(self):
        self.grid.itemconfigure(self.id, fill=self.ClosedFill)

    def mark_path(self):
        self.grid.itemconfigure(self.id, fill=self.PathFill)

    def mark_normal(self):
        self.grid.itemconfigure(self.id, fill=self.NormalFill)
        self.g_cost = self.h_cost = self.f_cost = 0
        self.parent = None


class Grid(Canvas):
    StartMarkKey = '<s>'
    EndMarkKey = '<e>'
    ObsMarkKey = '<B1-Motion>', '<ButtonPress-1>'
    ObsUnmarkKey = '<B3-Motion>', '<ButtonPress-3>'

    StartAlgoKey = '<Return>'
    ResetGridKey = '<Control-r>'

    def __init__(self, master, rows=10, cols=10, bg='white', config_master=True, **kwargs):
        self.master = master
        self.delay = 1                       # delay in each iteration of algorithm in ms
        self.rows, self.cols = rows, cols

        self.running = False
        self.running = False

        self.nodes = {}                      # (row, col) : node
        self.start_node = None
        self.end_node = None
        self.obs_nodes = set()               # obs_node

        self.open_nodes = set()
        self.closed_nodes = set()

        kwargs['bg'] = bg
        Canvas.__init__(self, self.master, **kwargs)

        # DRAWING
        self.draw(config_master)
        self.pack(fill='both', expand=1)
        self.focus_force()

        # BINDINGS
        self.bind(self.StartMarkKey, self._set_start)
        self.bind(self.EndMarkKey, self._set_end)

        for m_key in self.ObsMarkKey:
            self.bind(m_key, self._mark_obs)
        for un_key in self.ObsUnmarkKey:
            self.bind(un_key, self._unmark_obs)

        self.bind(self.StartAlgoKey, self.start_algo)
        self.bind(self.ResetGridKey, self.reset_grid)

    def is_valid(self, pos) -> bool:
        """ checks validity of position """
        if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols:
            return True
        return False

    def draw(self, config_master=True):
        """ draws grid on master """
        if config_master:
            __w, __h = self.cols * Node.SideLength, self.rows * Node.SideLength
            self.master.wm_geometry(f'{__w}x{__h}+{int((self.master.winfo_screenwidth() - __w) / 2)}+{int((self.master.winfo_screenheight() - __h) / 2)}')

        Node.set_grid(self)
        for row in range(self.rows):
            for col in range(self.cols):
                self.nodes[(row, col)] = Node((row, col))

    def _set_start(self, event):
        """ sets the START_POINT (unique)"""
        if not self.running:
            if self.open_nodes:
                self._clear_grid()
            _pos = event.y // Node.SideLength, event.x // Node.SideLength
            if self.is_valid(_pos):
                if self.start_node:
                    if self.start_node.row == _pos[0] and self.start_node.col == _pos[1]:
                        return
                    self.start_node.mark_normal()

                self.start_node = self.nodes[_pos]
                if self.start_node in self.obs_nodes:
                    self.obs_nodes.remove(self.start_node)
                self.start_node.mark_start()

    def _set_end(self, event):
        """ sets the END_POINT (unique)"""
        if not self.running:
            if self.open_nodes:
                self._clear_grid()
            _pos = event.y // Node.SideLength, event.x // Node.SideLength
            if self.is_valid(_pos):
                if self.end_node:
                    if self.end_node.row == _pos[0] and self.end_node.col == _pos[1]:
                        return
                    self.end_node.mark_normal()

                self.end_node = self.nodes[_pos]
                if self.end_node in self.obs_nodes:
                    self.obs_nodes.remove(self.end_node)
                self.end_node.mark_end()

    def _mark_obs(self, event):
        """ sets an obstacle """
        if not self.running:
            if self.open_nodes:
                self._clear_grid()
                return
            _pos = event.y // Node.SideLength, event.x // Node.SideLength
            if self.is_valid(_pos):
                __node = self.nodes[_pos]
                if __node == self.start_node or __node == self.end_node:
                    return
                if __node not in self.obs_nodes:
                    self.obs_nodes.add(__node)
                    __node.mark_obs()

    def _unmark_obs(self, event):
        """ unmark previously set obstacle """
        if not self.running:
            if self.open_nodes:
                self._clear_grid()
                return
            _pos = event.y // Node.SideLength, event.x // Node.SideLength
            if self.is_valid(_pos):
                __node = self.nodes[_pos]
                if __node in self.obs_nodes:
                    self.obs_nodes.remove(__node)
                    __node.mark_normal()

    def _clear_grid(self, event=None):
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

            self.obs_nodes.clear()
            self.open_nodes.clear()
            self.closed_nodes.clear()

    def reset_grid(self, event=None):
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

    def _yield_neighbours(self, node):
        """ yields all possible valid neighbours """
        __poss = ((node.row + 1, node.col), (node.row - 1, node.col), (node.row, node.col + 1), (node.row, node.col - 1),
                  (node.row + 1, node.col + 1), (node.row + 1, node.col - 1), (node.row - 1, node.col + 1), (node.row - 1, node.col - 1))
        for _pos in __poss:
            if self.is_valid(_pos):
                yield self.nodes[_pos]

    def __show_path(self, e_node):
        """ Traces parents from calibrated end node """
        def trace_back(_node, s__node, e__node):
            while _node:
                _node.mark_path()
                _node = _node.parent

            s__node.mark_start()
            e__node.mark_end()

        __th = Thread(target=trace_back, args=(e_node, self.start_node, self.end_node))
        __th.start()

    def __solve(self):
        """
        calibrates self.end node with parents, for tracing path,
        or None if no path is possible
        """

        try:
            c__node = reduce(self._get_node, self.open_nodes)
        except TypeError:
            self.show_algo_result(None)
            return

        self.open_nodes.remove(c__node)
        self.closed_nodes.add(c__node)

        if c__node == self.end_node:
            self.show_algo_result(c__node)
            return

        if c__node != self.start_node:
            c__node.mark_closed()

        for n__node in self._yield_neighbours(c__node):
            if n__node not in self.closed_nodes and n__node not in self.obs_nodes:
                if n__node not in self.open_nodes:
                    n__node.set_h_cost(self.end_node)
                    n__node.set_parent(c__node)
                    self.open_nodes.add(n__node)
                    n__node.mark_open()
                elif n__node.get_g_cost(c__node) < n__node.g_cost:
                    n__node.set_parent(c__node)

        self.master.after(self.delay, self.__solve)

    def start_algo(self, event=None):
        """ locks grid from user input and starts algorithm """
        if not self.running:
            # Checking Info
            if self.open_nodes or self.closed_nodes:
                self._clear_grid()
                return

            if not (self.start_node and self.end_node):
                messagebox.showwarning('Warning', 'Invalid Input : Set Start snd End Positions first !!!',
                                       parent=self.master)
                return

            self.open_nodes.add(self.start_node)
            self.running = True
            self.__solve()
        else:
            messagebox.showwarning('Warning', 'Algorithm Already Running', parent=self.master)

    def show_algo_result(self, e_node):
        if e_node:
            self.__show_path(e_node)
        else:
            messagebox.showerror('Error', 'Could Not Find Any Possible Path', parent=self.master)
        self.running = False


if __name__ == '__main__':
    win = Tk()
    win.wm_resizable(0, 0)

    grid = Grid(win, rows=50, cols=90)
    win.mainloop()
