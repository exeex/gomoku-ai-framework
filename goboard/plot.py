from .board import Board
import matplotlib.pyplot as plt


def init_plot_board(board: Board, figsize=(6, 6)):
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


def plot_board(board: Board):
    global fig, ax

    for step in board.steps:
        x = int(step[0][0])
        y = int(step[0][1])
        color = step[1]
        step = ax.plot(x, y, 'o', markersize=15, markeredgecolor=(.5, .5, .5), markerfacecolor=color,
                       markeredgewidth=2)
        step_cache.append(step[0])
    fig.show()
