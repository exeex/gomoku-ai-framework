from .board import Board
from .player import Player
import numpy as np


class Win(Exception):
    def __init__(self, player: Player, msg):
        msg = '%s Win, ' % player.color + msg
        self.winer = player
        super(Win, self).__init__(msg)


class Lose(Exception):
    def __init__(self, player: Player, msg):
        msg = '%s Lose, ' % player.color + msg
        self.loser = player
        super(Lose, self).__init__(msg)


class BlackWin(Exception):
    def __init__(self, *arg):
        super(BlackWin, self).__init__(*arg)


class WhiteWin(Exception):
    def __init__(self, *arg):
        super(WhiteWin, self).__init__(*arg)


class Tie(Exception):
    def __init__(self, *arg):
        super(Tie, self).__init__(*arg)


class ColorError(Exception):
    def __init__(self, *arg):
        super(ColorError, self).__init__(*arg)


def time_judge(board: Board, player: Player, color):
    # TODO: implement overtime lose and timer
    x, y = player.get_action(board)

    if color=='white':
        board.put_white(x, y)
    elif color=='black':
        board.put_black(x, y)
    else:
        raise ColorError


def link_judge(board: Board, player: Player, color):
    if color == "black":
        d = board.dense[0, :]
    elif color == "white":
        d = board.dense[1, :]
    else:
        raise NameError("color must be 'black' or 'white'!")

    from scipy import signal

    patterns = [np.array([[1, 1, 1, 1, 1]], dtype=np.uint16),
                np.array([[1, 1, 1, 1, 1]], dtype=np.uint16).transpose(),
                np.eye(5, dtype=np.uint16),
                np.eye(5, dtype=np.uint16)[:, ::-1], ]

    pads = [[(0, 0), (2, 2)], [(2, 2), (0, 0)], (2, 2), (2, 2)]

    for pattern, pad in zip(patterns, pads):
        grad = signal.convolve2d(pattern, d, boundary='fill', mode='valid')
        grad = np.pad(grad, pad, 'constant')

        grad = np.where(grad >= 5)
        if grad[0].size > 0:
            raise Win(player, "found 5 link at (%d,%d)" % (grad[0][0], grad[1][0]))

    return True


def move_judge(board: Board, step_counter, player: Player, color):
    if len(board) != step_counter + 1:
        raise Lose(player, "Move more than once or less than once in a turn.")


def tie_judge(board: Board, color):
    if len(board) == board.size_x * board.size_y:
        raise Tie('there is no more space on the board!!!')


if __name__ == '__main__':
    # from goboard import init_plot_board, plot_board
    # b = GoBoard()
    # p = Player(b, 'black')
    # init_plot_board(b)
    # b.put_black(0,0)
    # b.put_black(1,1)
    # b.put_black(2,2)
    # b.put_black(3,3)
    # b.put_black(4,4)
    # plot_board(b)
    # link_judge(b,p)

    from goboard import init_plot_board, plot_board

    b = Board()
    p = Player(b, color='white')
    init_plot_board(b)
    b.put_white(0, 0)
    b.put_white(1, 0)
    b.put_white(2, 0)
    b.put_white(3, 0)
    b.put_white(4, 0)
    plot_board(b)
    link_judge(b, p)
