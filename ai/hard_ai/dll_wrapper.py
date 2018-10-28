from ctypes import cdll, c_int, c_uint8

import numpy as np
from numpy.ctypeslib import ndpointer
from goboard import BoardInfo, Board

m = cdll.LoadLibrary(r"C:\Users\xray0\PycharmProjects\go-board-matplotlib\ai\hard_ai\get_action.dll")
m.GetActionWrap.restype = c_int
m.GetActionWrap.argtypes = [ndpointer(c_uint8, flags="C_CONTIGUOUS"),
                            c_int,
                            c_int,
                            c_int, ]


def get_action(board: BoardInfo):
    board_dense = board.dense[0,:,:]*1+board.dense[1,:,:]*2
    board_dense = board_dense.astype('uint8')

    print(board_dense.dtype)
    print(board_dense)
    action = _get_action(board_dense,board.size_x, board.size_y, 1)
    return action % board.size_x, action // board.size_y

def _get_action(board:np.ndarray, board_size_x, board_size_y, activate_player):
    action = m.GetActionWrap(board, board_size_x, board_size_y, board_size_y, activate_player)
    return action



if __name__ == '__main__':
    # a = np.array(np.zeros((7,7)),dtype=np.uint8)
    # b = m.GetActionWrap(a, 7, 7, 1)

    b = Board((7,7))
    b.put_black(1,3)
    b.put_white(2,3)
    print(b.dense)
    action = get_action(b.get_info())
    print('!!!',action)


