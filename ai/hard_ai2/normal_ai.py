import time
from random import choice
import numpy as np
from math import log, sqrt
from copy import deepcopy
import time
from goboard import BoardInfo, Player
from scipy import signal

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

patterns = [np.array([[1, 1, 1, 1, 1]], dtype=np.uint16),
            np.array([[1, 1, 1, 1, 1]], dtype=np.uint16).transpose(),
            np.eye(5, dtype=np.uint16),
            np.eye(5, dtype=np.uint16)[:, ::-1], ]

pads = [[(0, 0), (2, 2)], [(2, 2), (0, 0)], (2, 2), (2, 2)]


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


def get_possible_actions(board: BoardInfo):
    possible_actions = set()

    for ((x, y), _) in board.steps:
        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]:
            if board.is_legal_action(x + dx, y + dy):
                possible_actions.add((x + dx, y + dy))

    return list(possible_actions)


def get_weighted_actions(board: BoardInfo, possible_actions, color):
    weighted_actions = []

    for action in possible_actions:
        weight = analysis_action(board, action, color)
        weighted_actions.append((action, weight))

    weighted_actions = sorted(weighted_actions, key=lambda x: x[1], reverse=True)
    return weighted_actions


def link_judge(dense: np.ndarray, activated_player: int):
    d = dense[activated_player, :]

    for pattern, pad in zip(patterns, pads):
        grad = signal.convolve2d(pattern, d, boundary='fill', mode='valid')
        grad = np.pad(grad, pad, 'constant')
        grad = np.where(grad >= 5)
        if grad[0].size > 0:
            return True

    return False