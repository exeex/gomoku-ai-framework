from goboard import GoBoard
from goboard.player import Player
import numpy as np


class BlackWin(Exception):
    def __init__(self, *arg):
        super(BlackWin, self).__init__(*arg)


class WhiteWin(Exception):
    def __init__(self, *arg):
        super(WhiteWin, self).__init__(*arg)


def time_judge(func, player):
    func()
    if True:
        raise TimeoutError("%s is runing out of time" % player.bw)
    pass


def link_judge(board: GoBoard, player : Player):

    if player.bw == "black":
        d = board.dense[0,:]
    elif player.bw == "white":
        d = board.dense[1,:]

    from scipy import signal

    patterns = [np.array([[1, 1, 1, 1, 1]], dtype=np.uint16),
               np.array([[1, 1, 1, 1, 1]], dtype=np.uint16).transpose(),
               np.eye(5, dtype=np.uint16),
               np.eye(5, dtype=np.uint16)[:, ::-1], ]

    pads = [[(0,0),(2,2)],[(2,2),(0,0)],(2,2),(2,2)]


    for pattern, pad in zip(patterns,pads):
        grad = signal.convolve2d(pattern, d, boundary='fill', mode='valid')
        grad = np.pad(grad,pad,'constant')

        grad = np.where(grad >= 5)
        if grad[0].size > 0:
            if player.bw == "black":
                raise BlackWin("found 5 link at %d, %d" % (grad[0][0],grad[1][0]))

            elif player.bw == "white":
                raise WhiteWin("found 5 link at %d, %d" % (grad[0][0],grad[1][0]))



    return True
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
    b = GoBoard()
    p = Player(b, 'white')
    init_plot_board(b)
    b.put_white(0,0)
    b.put_white(1,0)
    b.put_white(2,0)
    b.put_white(3,0)
    b.put_white(4,0)
    plot_board(b)
    link_judge(b, p)