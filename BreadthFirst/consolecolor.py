import os


class FG:
    Reset = '\033[0m'

    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'

    BrightBlack = '\033[90m'
    BrightRed = '\033[91m'
    BrightGreen = '\033[92m'
    BrightYellow = '\033[93m'
    BrightBlue = '\033[94m'
    BrightMagenta = '\033[95m'
    BrightCyan = '\033[96m'
    BrightWhite = '\033[97m'

    BoldBlack = '\033[30;1m'
    BoldRed = '\033[31;1m'
    BoldGreen = '\033[32;1m'
    BoldYellow = '\033[33;1m'
    BoldBlue = '\033[34;1m'
    BoldMagenta = '\033[35;1m'
    BoldCyan = '\033[36;1m'
    BoldWhite = '\033[37;1m'


class BG:
    Reset = '\033[0m'

    Black = '\033[40m'
    Red = '\033[41m'
    Green = '\033[42m'
    Yellow = '\033[43m'
    Blue = '\033[44m'
    Magenta = '\033[45m'
    Cyan = '\033[46m'
    White = '\033[47m'

    BrightBlack = '\033[100m'
    BrightRed = '\033[101m'
    BrightGreen = '\033[102m'
    BrightYellow = '\033[103m'
    BrightBlue = '\033[104m'
    BrightMagenta = '\033[105m'
    BrightCyan = '\033[106m'
    BrightWhite = '\033[107m'

    BoldBlack = '\033[40;1m'
    BoldRed = '\033[41;1m'
    BoldGreen = '\033[42;1m'
    BoldYellow = '\033[43;1m'
    BoldBlue = '\033[44;1m'
    BoldMagenta = '\033[45;1m'
    BoldCyan = '\033[46;1m'
    BoldWhite = '\033[47;1m'


class Color:
    Reset = '\033[0m'
    Bold = '\033[1m'
    Underline = '\033[4m'

    def __call__(self, _str, *flags):
        return f'{"".join(flags)}{_str}{self.Reset}'

    @staticmethod
    def init():
        if os.name == 'nt':
            os.system('color')