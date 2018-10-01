import time
from random import choice
import numpy as np
from math import log, sqrt
from copy import deepcopy
import time
from goboard import BoardInfo, Player


def analysis_board(board: BoardInfo):
    return 0


class ValueNetAi(Player):
    def __init__(self, board_info, gui, color):
        super(ValueNetAi, self).__init__(board_info, gui, color)

        self.board_info = board_info
        self.MAX_TIME = 3
        self.MAX_MOVE = 100
        self.MAX_DEPTH = 1
        self.value = np.zeros((self.board_info.size_x, self.board_info.size_y))

    def find_actions(self, board: BoardInfo):

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

    def get_action(self, board: BoardInfo):
        actions = self.find_actions(board)
        print(actions)
        time.sleep(2)

        for action in actions:
            if not board.is_legal_action(*action):
                return action
