import matplotlib.pyplot as plt
import json

"""
This is maintained by cswu
xray0h@gmail.com / cswu@gapp.nthu.edu.tw
"""


class GoBoard:
    def __init__(self, size=(13, 13)):

        # set board size
        self.size = size
        self.size_x = size[0]
        self.size_y = size[1]

        # store each steps in a game
        self.steps = []
        # store where have be occupied (placement), to detect collisions
        self.placements = set()

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
            placement_str = "%d,%d" % (x, y)
            step = (placement_str, color)
            self.steps.append(step)
            self.add_placement(x, y)

    def step_back(self):
        lastest_step = self.steps.pop()
        self.placements.remove(lastest_step[0])

    def clear_board(self):

        self.steps.clear()
        self.placements.clear()


def save_battle(file_name, board: GoBoard, **kwargs):
    xy, bw = tuple(zip(*board.steps))

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

def init_plot_board(board: GoBoard, figsize=(6, 6)):
    # create a 6" x 6" board
    global fig, ax, step_cache
    step_cache = []
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor((1, 1, .8))
    ax = fig.add_subplot(111)

    # draw the grid
    for x in range(board.size_x):
        ax.plot([x, x], [0, board.size_x - 1], 'k')
    for y in range(board.size_y):
        ax.plot([0, board.size_y - 1], [y, y], 'k')

    # set axis label
    ax.set_ylabel("y axis")
    ax.set_xlabel("x axis")

    # set axis ticks
    ax.set_xticks([x for x in range(board.size_x)])
    ax.set_yticks([y for y in range(board.size_y)])

    # scale the plot area conveniently (the board is in 0,0..18,18)
    ax.set_xlim(-1, board.size_x)
    ax.set_ylim(-1, board.size_y)
    fig.show()

def plot_board(board: GoBoard):

    global fig, ax

    for step in board.steps:
        x = int(step[0].split(',')[0])
        y = int(step[0].split(',')[1])
        color = step[1]
        step = ax.plot(x, y, 'o', markersize=15, markeredgecolor=(.5, .5, .5), markerfacecolor=color,
                      markeredgewidth=2)
        step_cache.append(step[0])
    fig.show()

if __name__ == '__main__':
    b = GoBoard()
    b.put_black(0, 0)
    b.put_white(10, 11)
    b.step_back()
    b.put_white(10, 11)
    b.clear_board()
    b.put_black(0, 0)
    b.put_white(10, 11)
    init_plot_board(b)
    plot_board(b)
    init_plot_board(b)
    save_battle("gg.json", b)

    c = load_battle("gg.json")
