from .board import Board, BoardInfo
from .player import Player, Human
import numpy as np
import threading
import time
from .exception import ColorError, Lose, Win, Tie


def timeit(method, msg):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (msg, (te - ts) * 1000))
        return result

    return timed


def exec_and_timeout_judge(board: Board, player: Player, color, timeout=10):
    if not isinstance(player, Human):

        def get_action_wrap(board_info, data_dict):
            x, y = player.get_action(board_info, timeout)
            data_dict['x'] = x
            data_dict['y'] = y

        xy_dict = {'x': -1, 'y': -1}
        p = threading.Thread(target=get_action_wrap, name="get_action",
                             args=(board.get_info(), xy_dict))
        p.start()
        p.join(timeout)

        try:
            if color == 'white':
                board.put_white(xy_dict['x'], xy_dict['y'])
            elif color == 'black':
                board.put_black(xy_dict['x'], xy_dict['y'])
            else:
                raise ColorError

        except IndexError:
            raise Lose(player, "Running out of time, or exception/error occurs in Player.get_action()")
    else:
        x, y = player.get_action(board.get_info())
        if color == 'white':
            board.put_white(x, y)
        elif color == 'black':
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
    # TODO: white win
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
