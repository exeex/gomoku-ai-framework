import matplotlib.pyplot as plt
import json

"""
This is maintained by cswu
xray0h@gmail.com / cswu@gapp.nthu.edu.tw
"""


class GoBoard:
    def __init__(self, size=(13, 13), figsize=(6, 6)):

        self.size = size
        self.size_x = size[0]
        self.size_y = size[1]
        self.figsize = figsize
        self.plot_board()

    @staticmethod
    def show():
        plt.show()

    def is_collision(self, x, y):
        placement_str = "%d,%d" % (x, y)
        if placement_str in self.placements:
            return True
        else:
            return False

    def add_placement(self, x, y):
        self.placements.add("%d,%d" % (x, y))

    def put_black(self, x, y):
        self._put(x, y, 'k')

    def put_white(self, x, y):
        self._put(x, y, 'w')

    def _put(self, x, y, color):

        if not (0 <= x < self.size_x) or not (0 <= y < self.size_y):
            raise IndexError("Index must be >=0 and <%d. but you give us : (%d, %d)!!" % (self.size_x, x, y))

        if self.is_collision(x, y):
            raise IndexError("You can't place black or white in (%d, %d)!!" % (x, y))

        else:
            step = self.ax.plot(x, y, 'o', markersize=15, markeredgecolor=(.5, .5, .5), markerfacecolor=color,
                                markeredgewidth=2)[0]

            placement_str = "%d,%d" % (x, y)
            step = (placement_str, step, color)
            self.steps.append(step)
            self.add_placement(x, y)

    def plot_board(self):
        # create a 6" x 6" board
        self.fig = plt.figure(figsize=self.figsize)
        self.fig.patch.set_facecolor((1, 1, .8))
        self.ax = self.fig.add_subplot(111)

        # draw the grid
        for x in range(self.size_x):
            self.ax.plot([x, x], [0, self.size_x - 1], 'k')
        for y in range(self.size_y):
            self.ax.plot([0, self.size_y - 1], [y, y], 'k')

        # set axis label
        self.ax.set_ylabel("y axis")
        self.ax.set_xlabel("x axis")

        # set axis ticks
        self.ax.set_xticks([x for x in range(self.size_x)])
        self.ax.set_yticks([y for y in range(self.size_y)])

        # scale the plot area conveniently (the board is in 0,0..18,18)
        self.ax.set_xlim(-1, self.size_x)
        self.ax.set_ylim(-1, self.size_y)

        # store each steps in a game
        self.steps = []

        # store where have be occupied (placement), to detect collisions
        self.placements = set()

    def step_back(self):
        lastest_step = self.steps.pop()
        self.placements.remove(lastest_step[0])
        lastest_step[1].remove()

    def clear_board(self):

        for step in self.steps:
            step[1].remove()

        self.steps.clear()
        self.placements.clear()


def save_battle(file_name, board: GoBoard, **kwargs):
    xy, _, bw = tuple(zip(*board.steps))

    battle = {
        "battle_info": {
            "board_size": board.size,
            "other_info": kwargs,
        },
        "steps": list(zip(xy, bw)),
    }

    json_str = json.dumps(battle)

    try:
        f = open(file_name, 'w')
    except FileExistsError:
        raise FileExistsError

    f.write(json_str)


def load_battle(file_name):
    f = open(file=file_name, mode='r')
    data = json.load(f)
    steps = data['steps']
    board_size = data['battle_info']['board_size']

    b = GoBoard(size=board_size)

    for step in steps:
        x, y = step[0].split(',')
        color = step[1]
        b._put(int(x), int(y), color=color)

    return b


if __name__ == '__main__':
    # b = GoBoard()
    # b.put_black(0, 0)
    # b.put_white(10, 11)
    # b.step_back()
    # b.put_white(10, 11)
    # b.clear_board()
    # b.put_black(0, 0)
    # b.put_white(10, 11)
    # b.show()
    # save_battle("gg.json", b)

    c = load_battle("gg.json")
