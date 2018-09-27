import numpy as np

"""
This is maintained by cswu
xray0h@gmail.com / cswu@gapp.nthu.edu.tw
"""


class GoBoard:
    def __init__(self, size=(13, 13), after_put=None):

        # set board size
        self.size = size
        self.__size_x = size[0]
        self.__size_y = size[1]
        # store each steps in a game
        self.__steps = []
        self.__dense = np.zeros((2, self.__size_x, self.__size_y), dtype=np.uint16)
        # store where have be occupied (placement), to detect collisions
        self.__placements = set()
        self.after_put = after_put

    def __len__(self):
        return len(self.__placements)

    @property
    def steps(self):
        return self.__steps
    @property
    def dense(self):
        return self.__dense
    @property
    def size_x(self):
        return self.__size_x
    @property
    def size_y(self):
        return self.__size_y

    def is_collision(self, x, y):
        placement_str = "%d,%d" % (x, y)
        if placement_str in self.__placements:
            return True
        else:
            return False

    def add_placement(self, x, y, color):
        self.__placements.add("%d,%d" % (x, y))
        step = ((x, y), color)
        self.__steps.append(step)
        if color == "w":
            self.__dense[1, x, y] = 1
        elif color == "k":
            self.__dense[0, x, y] = 1

    def _remove_placement(self, x, y):
        self.__placements.remove("%d,%d" % (x, y))

    def put_black(self, x, y):
        self._put(x, y, 'k')

    def put_white(self, x, y):
        self._put(x, y, 'w')

    def _put(self, x, y, color):

        if not (0 <= x < self.__size_x) or not (0 <= y < self.__size_y):
            raise IndexError("Index must be >=0 and <%d. but you give us : (%d, %d)!!" % (self.__size_x, x, y))

        if self.is_collision(x, y):
            raise IndexError("You can't place black or white in (%d, %d)!!" % (x, y))

        if self.__len__() == self.__size_x * self.__size_y:
            raise IndexError("There is no empty space on the board!!")

        self.add_placement(x, y, color)

        if self.after_put:
            self.after_put(x, y, color)

    def step_back(self):
        lastest_step = self.__steps.pop()
        self._remove_placement(*lastest_step[0])
        self.__dense[0, lastest_step[0][0], lastest_step[0][1]] = 0
        self.__dense[0, lastest_step[0][0], lastest_step[0][1]] = 0

    def clear_board(self):
        self.__steps.clear()
        self.__placements.clear()


if __name__ == '__main__':
    b = GoBoard()
    b.put_black(0, 0)
    b.put_white(10, 11)
    b.step_back()
    b.put_white(10, 11)
    b.clear_board()
    b.put_black(0, 0)
    b.put_white(10, 11)

    print(b.dense)
    # save_battle("gg.json", b)
    # c = load_battle("gg.json")
