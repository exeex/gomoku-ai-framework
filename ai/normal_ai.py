import time
from random import choice
import numpy as np
from math import log, sqrt
from copy import deepcopy
import time
from goboard import BoardInfo, Player


def analysis_action(board: BoardInfo, action, color):

    if color == "black":
        m = board.dense[0, :, :]
        n = board.dense[1, :, :]
    else:
        m = board.dense[1, :, :]
        n = board.dense[0, :, :]

    x, y = action
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]


    for dx, dy in directions:
        try:
            # ?11?
            if board.is_legal_action(x+dx,y+dy) and n[x+dx,y+dy] :






    for direction in directions:



    return 0


class Ai(Player):
    def __init__(self, board_info, gui, color):
        super(Ai, self).__init__(board_info, gui, color)

        self.board_info = board_info
        self.MAX_TIME = 3
        self.MAX_MOVE = 100
        self.MAX_DEPTH = 1
        self.value = np.zeros((self.board_info.size_x, self.board_info.size_y))

    @staticmethod
    def get_possible_actions(board: BoardInfo):

        possible_actions = set()

        for ((x, y), _) in board.steps:
            for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]:
                if board.is_legal_action(x + dx, y + dy):
                    possible_actions.add((x + dx, y + dy))

        return possible_actions

    def get_weighted_actions(self, board: BoardInfo, possible_actions):
        weighted_actions = []

        for action in possible_actions:
            weight = analysis_action(board, action, self.color)
            weighted_actions.append((action, weight))

        weighted_actions = sorted(weighted_actions, key=lambda x: x[1], reverse=True)
        return weighted_actions

    def get_action(self, board: BoardInfo):

        possible_actions = self.get_possible_actions(board)
        weighted_actions = self.get_weighted_actions(board, possible_actions)

        print(weighted_actions)

        for ((x, y), _) in weighted_actions:
            if not board.is_legal_action(x, y):
                return x, y
