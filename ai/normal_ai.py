import time
from random import choice
import numpy as np
from math import log, sqrt
from copy import deepcopy
import time
from goboard import BoardInfo, Player

# stone value notations
# '*' : where you put stone in this action.
# '?' : don't know state.
# '1' : our stone
# '2' : enemy's stone
# '0' : empty
# 'x' : boundary

values = {
    '?*1?': 1,
    '?*11?': 10,
    '?*111?': 100,
    '?*1111?': 10000,
    '?*2?': 1,
    '?*22?': 10,
    '?*222?': 110,
    '?*22221': 9999,
}


def analysis_action(board: BoardInfo, action, color):
    if color == "black":
        is_empty = board.is_empty
        is_our = board.is_black
        is_enemy = board.is_white
    else:
        is_empty = board.is_empty
        is_our = board.is_white
        is_enemy = board.is_black

    x, y = action
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    weight = 0

    for dx, dy in directions:
        if is_our(x + dx, y + dy):
            weight += values['?*1?']
        if is_our(x + dx, y + dy) and is_our(x + 2 * dx, y + 2 * dy):
            weight += values['?*11?']
        if is_our(x + dx, y + dy) and is_our(x + 2 * dx, y + 2 * dy) and is_our(x + 3 * dx, y + 3 * dy):
            weight += values['?*111?']
        if is_our(x + dx, y + dy) and is_our(x + 2 * dx, y + 2 * dy) and is_our(x + 3 * dx, y + 3 * dy) and is_our(
                        x + 4 * dx, y + 4 * dy):
            weight += values['?*1111?']

        if is_enemy(x + dx, y + dy):
            weight += values['?*2?']
        if is_enemy(x + dx, y + dy) and is_enemy(x + 2 * dx, y + 2 * dy):
            weight += values['?*22?']
        if is_enemy(x + dx, y + dy) and is_enemy(x + 2 * dx, y + 2 * dy) and is_our(x + 3 * dx, y + 3 * dy):
            weight += values['?*222?']
        if is_enemy(x + dx, y + dy) and \
                is_enemy(x + 2 * dx, y + 2 * dy) and is_enemy(x + 3 * dx, y + 3 * dy) \
                and is_enemy(x + 4 * dx, y + 4 * dy) and is_our(x + 5 * dx, y + 5 * dy):
            weight += values['?*22221']

    return weight


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

        for ((x, y), _) in weighted_actions:
            if board.is_legal_action(x, y):
                return x, y

        return 5, 5
