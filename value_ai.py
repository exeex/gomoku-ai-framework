import time
from random import choice
import numpy as np
from math import log, sqrt
from copy import deepcopy
from goboard import Board, Player


def analysis_board(board: Board):
    return 0


class ValueNetAi(Player):
    def __init__(self, board_info, gui, bw):
        super(ValueNetAi, self).__init__(board_info, gui, bw)

        # C: UCB1常數, MAX_TIME: 模擬時間, MAX_MOVE: 最大移動步數
        # board: 目前盤面 player: 代表玩家
        # states: 狀態表
        # wins, plays: 贏棋的次數, 模擬的次數

        self.board_info = board_info
        self.bw = bw
        self.C = 1.4
        self.MAX_TIME = 3
        self.MAX_MOVE = 100
        self.MAX_DEPTH = 1
        self.value = np.zeros((self.board_info.size_x, self.board_info.size_y))

    def find_actions(self, board: Board):

        possible_actions = [[(x + 1, y),
                           (x - 1, y),
                           (x, y + 1),
                           (x, y - 1),
                           (x, y + 1),
                           (x + 1, y + 1),
                           (x + 1, y - 1),
                           (x - 1, y - 1)]
                          for ((x, y), _) in board.steps]

        possible_actions = set([x for y in possible_actions for x in y])
        weighted_actions = []

        for move in possible_actions:
            weight = analysis_board(board)
            weighted_actions.append((move, weight))

        weighted_actions = sorted(weighted_actions, key=lambda x: x[1], reverse=True)
        actions = [(x, y) for ((x, y), _) in weighted_actions]

        return actions

    def get_action(self, board: Board):
        actions = self.find_actions(board)
        print(actions)

        for action in actions:
            if not board.is_legal_action(*action):
                return action
