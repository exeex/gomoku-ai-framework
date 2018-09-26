import matplotlib.pyplot as plt


class GoBoard:
    def __init__(self):

        self.plot_board()

    def plot_board(self):
        # create a 6" x 6" board
        self.fig = plt.figure(figsize=[6, 6])
        self.fig.patch.set_facecolor((1, 1, .8))
        self.ax = self.fig.add_subplot(111)

        # draw the grid
        for x in range(19):
            self.ax.plot([x, x], [0, 18], 'k')
        for y in range(19):
            self.ax.plot([0, 18], [y, y], 'k')

        # set axis label
        self.ax.set_ylabel("y axis")
        self.ax.set_xlabel("x axis")

        # set axis ticks
        self.ax.set_xticks([x for x in range(19)])
        self.ax.set_yticks([y for y in range(19)])

        # scale the plot area conveniently (the board is in 0,0..18,18)
        self.ax.set_xlim(-1, 19)
        self.ax.set_ylim(-1, 19)

        # store each steps in a game
        self.steps = []

        # store where have be occupied (placement), to detect collisions
        self.placements = set()

    def put_black(self, x, y):
        self.__put(x, y, 'k')

    def put_white(self, x, y):
        self.__put(x, y, 'w')

    def __put(self, x, y, color):

        if not (0 <= x < 19) or not (0 <= y < 19):
            raise IndexError("Index must be >=0 and <19. but you give us : (%d, %d)!!" % (x, y))

        if self.is_collision(x, y):
            raise IndexError("You can't place black or white in (%d, %d)!!" % (x, y))

        else:
            step = self.ax.plot(x, y, 'o', markersize=15, markeredgecolor=(.5, .5, .5), markerfacecolor=color,
                                markeredgewidth=2)[0]

            placement_str = "%d,%d" % (x, y)
            step = (placement_str, step)
            self.steps.append(step)
            self.add_placement(x, y)

    def show(self):
        plt.show()

    def step_back(self):
        lastest_step = self.steps.pop()
        self.placements.remove(lastest_step[0])
        lastest_step[1].remove()

    def clear_board(self):

        for step in self.steps:
            step[1].remove()

        self.steps.clear()
        self.placements.clear()

    def is_collision(self, x, y):
        placement_str = "%d,%d" % (x, y)
        if placement_str in self.placements:
            return True
        else:
            return False

    def add_placement(self, x, y):
        self.placements.add("%d,%d" % (x, y))


if __name__ == '__main__':
    b = GoBoard()
    b.put_black(0, 0)
    b.put_white(10, 11)
    b.step_back()
    b.put_white(10, 11)
    b.clear_board()
    b.show()
