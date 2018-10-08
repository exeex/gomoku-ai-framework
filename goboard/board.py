import numpy as np
from copy import deepcopy

"""
This is maintained by cswu
xray0h@gmail.com / cswu@gapp.nthu.edu.tw
"""


class Board:
    def __init__(self, size=(13, 13), after_put=None):

        # set board size
        self.__size_x = size[0]
        self.__size_y = size[1]
        # store each steps in a game
        self.steps = []
        self.dense = np.zeros((2, self.__size_x, self.__size_y), dtype=np.uint16)
        # store where have be occupied (placement), to detect collisions
        self.placements = set()
        self.after_put = after_put

    def __len__(self):
        return len(self.placements)

    @property
    def size_x(self):
        return self.__size_x

    @property
    def size_y(self):
        return self.__size_y

    def is_legal_action(self, x, y):
        placement_str = "%d,%d" % (x, y)

        if not (0 <= x < self.__size_x) or not (0 <= y < self.__size_y):
            return False

        if placement_str in self.placements:
            return True
        else:
            return False

    def __add_placement(self, x, y, color):
        self.placements.add("%d,%d" % (x, y))
        step = ((x, y), color)
        self.steps.append(step)
        if color == "w":
            self.dense[1, x, y] = 1
        elif color == "k":
            self.dense[0, x, y] = 1

    def clone(self):
        b = Board((self.size_x, self.size_y))
        b.dense = deepcopy(self.dense)
        b.steps = deepcopy(self.steps)
        b.placements = deepcopy(self.placements)
        return b

    def put_black(self, x, y):
        self._put(x, y, 'k')

    def put_white(self, x, y):
        self._put(x, y, 'w')

    def _put(self, x, y, color):

        if self.is_legal_action(x, y):
            raise IndexError("You can't place black or white in (%d, %d)!!" % (x, y))

        if self.__len__() == self.__size_x * self.__size_y:
            raise IndexError("There is no empty space on the board!!")

        self.__add_placement(x, y, color)

        if self.after_put:
            self.after_put(x, y, color)

    def get_info(self):
        return BoardInfo(self.clone())


class BoardInfo:
    def __init__(self, board: Board):
        self.board = board
        self.steps = board.steps
        self.dense = board.dense
        self.size_x = board.size_x
        self.size_y = board.size_y
        self.is_legal_action = board.is_legal_action

    def is_black(self, x, y):
        if not self.is_legal_action(x, y):
            return False

        if self.dense[0, x, y] == 1:
            return True
        else:
            return False

    def is_white(self, x, y):
        if not self.is_legal_action(x, y):
            return False

        if self.dense[1, x, y] == 1:
            return True
        else:
            return False


if __name__ == '__main__':
    b = Board()
    b.put_black(0, 0)
    bb = b.get_info()
    print(bb.is_black(22, 0))

    b.get_info()
    b.put_white(10, 11)
    print(bb.is_white(10, 11))
    # b.step_back()
    b.put_white(10, 11)
    # b.clear_board()
    b.put_black(0, 0)
    b.put_white(10, 11)

    print(b.dense)
    # save_battle("gg.json", b)
    # c = load_battle("gg.json")
