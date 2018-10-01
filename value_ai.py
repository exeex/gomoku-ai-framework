import time
from random import choice
import numpy as np
from math import log, sqrt
from copy import deepcopy
from goboard import GoBoard, Player


def analysis_board(board: GoBoard):
    return 0


class ValueNetAi(Player):
    def __init__(self, board, gui, bw):
        super(ValueNetAi, self).__init__(board, gui, bw)

        # C: UCB1常數, MAX_TIME: 模擬時間, MAX_MOVE: 最大移動步數
        # board: 目前盤面 player: 代表玩家
        # states: 狀態表
        # wins, plays: 贏棋的次數, 模擬的次數

        self.board = board
        self.bw = bw
        self.C = 1.4
        self.MAX_TIME = 3
        self.MAX_MOVE = 100
        self.MAX_DEPTH = 1
        self.value = np.zeros((board.size_x, board.size_y))

    def bestAction(self):

        board = self.board

        possible_moves = [[(x + 1, y),
                           (x - 1, y),
                           (x, y + 1),
                           (x, y - 1),
                           (x, y + 1),
                           (x + 1, y + 1),
                           (x + 1, y - 1),
                           (x - 1, y - 1)]
                          for ((x, y), _) in self.board.steps]

        possible_moves = set([x for y in possible_moves for x in y])
        weighted_moves = []

        for move in possible_moves:
            board.put(*move)
            weight = analysis_board(board)
            weighted_moves.append((move, weight))
            board.step_back()

        weighted_moves = sorted(weighted_moves, key=lambda x: x[1], reverse=True)
        moves = [(x, y) for ((x, y), _) in weighted_moves]

        return moves

    def execute(self):
        moves = self.bestAction()
        print(moves)

        for move in moves:
            try:
                self.put(move[0], move[1])
                return
            except IndexError:
                print("GG!")
                continue
