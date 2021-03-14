# 红玲
# TODO:红玲
import os
from sty import fg, bg
from tqdm import tqdm
from conf.base import sz_col, sz_row

red1 = 196  # light red
red2 = 160
red3 = 124
red4 = 88
red5 = 52  # dark red

green1 = 46
green2 = 40
green3 = 34
green4 = 28
green5 = 22

blue1 = 51
blue2 = 45
blue3 = 39
blue4 = 33
blue5 = 27

white1 = 15
white2 = 7


class Screen:
    def __init__(self):
        self.column_size = sz_col
        self.row_size = sz_row
        pass

    @staticmethod
    def clear_screen():
        os.system("clear")
        return


class Processor:
    def __init__(self, _total):
        self.pbar = tqdm(total=_total)

    def update(self, _derta):
        self.pbar.update(_derta)


class Formator:
    def __init__(self):
        self.screen = Screen()

    def in_column_center(self, _string):
        _string = _string.center(self.screen.column_size)
        return _string

    def in_row_center(self, _string):
        row_to_print = int(self.screen.row_size / 2)
        ret = ""
        for i in range(row_to_print):
            ret += "\n"
        ret += _string
        return ret

    def in_half_center(self, _string):
        string = self.in_column_center(_string)
        string = self.in_row_center(string)
        return string

    def in_all_center(self, _string):
        string = self.in_column_center(_string)
        string = self.in_row_center(string)
        string += self.in_row_center("")
        return string

    def in_all_left(self, _string):
        string = self.in_row_center("")
        string += self.in_row_center("")
        string += "\n" + _string
        return string


class Printer:
    def __init__(self):
        pass

    @staticmethod
    def in_fg_color(_string, _color_num):
        return fg(_color_num) + _string + fg.rs

    @staticmethod
    def in_bg_color(_string, _color_num):
        return bg(_color_num) + _string + bg.rs

    @staticmethod
    def p(_string):
        print(_string, end="")

    @staticmethod
    def pln(_string):
        print(_string)

    @staticmethod
    def pp(_string):  # processbar print
        tqdm.write(_string, end="")

    @staticmethod
    def ppln(_string):
        tqdm.write(_string)


if __name__ == "__main__":
    f = Formator()
    #f.screen.clear_screen()
    string = str(f.screen.column_size)
    string = f.in_all_center(string)
    p = Printer()
    p.p(string)






