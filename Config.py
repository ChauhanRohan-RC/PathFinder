import os
import sys
from U import load_map


class Config:
    MainDir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(
        os.path.realpath(os.path.abspath(__file__)))
    ConfigFilePath = os.path.join(MainDir, 'config.ini')

    # DIMENSIONS .......................................
    GRID_ROWS, GRID_COLS = 80, 170  # Grid Rows, Cols
    SideLength = 8  # Length of side of node (cube)
    StatusBarHeight = 40  # Height of Status bar at bottom
    W_WIDTH, W_HEIGHT = GRID_COLS * SideLength, (GRID_ROWS * SideLength) + StatusBarHeight  # Window width, height

    Diagonal = int(1.414 * SideLength)
    OutWidth = 0.5
    InSideLength = SideLength - (OutWidth * 2)

    # ................... Themes .......................

    DarkMode = 1  # Flag

    # Light Theme
    LightThemeDict = {
        'OutNormalColor': (120, 119, 120),  # Normal Outline Colour
        'NormalFill': (255, 255, 255),  # Fill when Normal
        'StartFill': (205, 19, 255),  # Fill when Marked As Start
        'EndFill': (255, 56, 49),  # Fill when Marked As End
        'ObsFill': (30, 30, 30),  # Fill when Marked as Obstacle

        'ClosedFill': (255, 91, 158),  # Fill when marked as closed
        'OpenFill': (155, 255, 230),  # Fill when marked as open
        'PathFill': (27, 255, 12)  # Fill when marked as Found PAth
    }

    DarkThemeDict = {
        'OutNormalColor': (50, 50, 50),  # Normal Outline Colour
        'NormalFill': (0, 0, 0),  # Fill when Normal
        'StartFill': (205, 19, 255),  # Fill when Marked As Start
        'EndFill': (255, 56, 49),  # Fill when Marked As End
        'ObsFill': (230, 230, 230),  # Fill when Marked as Obstacle

        'ClosedFill': (255, 20, 116),  # Fill when marked as closed
        'OpenFill': (0, 198, 247),  # Fill when marked as open
        'PathFill': (36, 255, 42)  # Fill when marked as Found PAth
    }

    @classmethod
    @property
    def theme_dict(cls) -> dict:
        return cls.DarkThemeDict if cls.DarkMode else cls.LightThemeDict

    @classmethod
    @property
    def OutNormalColor(cls):
        return cls.theme_dict['OutNormalColor']

    @classmethod
    @property
    def NormalFill(cls):
        return cls.theme_dict['NormalFill']

    @classmethod
    @property
    def StartFill(cls):
        return cls.theme_dict['StartFill']

    @classmethod
    @property
    def EndFill(cls):
        return cls.theme_dict['EndFill']

    @classmethod
    @property
    def ObsFill(cls):
        return cls.theme_dict['ObsFill']

    @classmethod
    @property
    def OpenFill(cls):
        return cls.theme_dict['OpenFill']

    @classmethod
    @property
    def ClosedFill(cls):
        return cls.theme_dict['ClosedFill']

    @classmethod
    @property
    def PathFill(cls):
        return cls.theme_dict['PathFill']


    # Fonts
    StatusBarFont = ('comicsans', 25, False, False)
    StatusInstruction = '< s > : mark start point     < e > : mark end point    < L_Mouse > : mark obstacles     < L_Mouse + d > : delete obstacles      < Ctrl + r > : reset'

    # Logical
    VisualDelay = 10  # mills
    DiagonalMove = 1  # Flag

    @classmethod
    def load_from_file(cls, file_path):
        # if os.path.isfile(f_path) and os.access(f_path, os.R_OK):
        #     with open(f_path, 'r') as c__f:
        #         try:
        #             for _l in c__f.readlines():
        #                 if _l and '#' not in _l and '=' in _l:
        #                     _l = "".join(i for i in _l if not i.isspace())
        #                     _attr, _val = _l.split('=')
        #                     try:
        #                         _val = int(_val)
        #                     except TypeError:
        #                         pass
        #                     else:
        #                         setattr(cls, _attr, _val)
        #         except (UnicodeDecodeError, OSError, IOError):
        #             pass

        map = load_map(file_path, key_filter=lambda k: hasattr(cls, k))
        if map:
            changed = False
            for k, v in map.items():
                try:
                    v = int(v)
                except (TypeError, ValueError):
                    try:
                        v = float(v)
                    except (TypeError, ValueError):
                        continue

                setattr(cls, k, v)
                changed = True

            if changed:
                cls.W_WIDTH, cls.W_HEIGHT = cls.GRID_COLS * cls.SideLength, (
                        cls.GRID_ROWS * cls.SideLength) + cls.StatusBarHeight  # Window width, height
                cls.Diagonal = int(1.4 * cls.SideLength)
                cls.InSideLength = cls.SideLength - (cls.OutWidth * 2)
