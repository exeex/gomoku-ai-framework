
import numpy as np
from goboard import BoardInfo
from scipy import signal

# stone value notations
# '*' : where you put stone in this action.
# '?' : don't know state.
# '1' : our stone
# '2' : enemy's stone
# '0' : empty
# 'x' : boundary

values = {
    '0*10': 3,
    '?*11?': 10,
    '?*111?': 10,
    '0*110': 100,
    '01*10': 100,
    '01*110': 100,
    '0*1112': 100,
    '0*1110': 1000,
    '?*1111?': 10000,
    '?*2?': 3,
    '?*22?': 10,
    '?*222?': 110,
    '?*22221': 9999,
}

patterns = [np.array([[1, 1, 1, 1, 1]], dtype=np.uint16),
            np.array([[1, 1, 1, 1, 1]], dtype=np.uint16).transpose(),
            np.eye(5, dtype=np.uint16),
            np.eye(5, dtype=np.uint16)[:, ::-1], ]

pads = [[(0, 0), (2, 2)], [(2, 2), (0, 0)], (2, 2), (2, 2)]
directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

def analysis_action(board: BoardInfo, action, activated_player: int):
    if activated_player == 0:
        is_empty = board.is_empty
        is_our = board.is_black
        is_enemy = board.is_white
    else:
        is_empty = board.is_empty
        is_our = board.is_white
        is_enemy = board.is_black

    x, y = action
    weight = 0

    for dx, dy in directions:

        # 活二
        if is_empty(x - dx, y - dy) and\
                is_our(x + dx, y + dy)and\
                is_empty(x + 2 * dx, y + 2 * dy):
            weight += 10

        # 可能是死三
        if      is_our(x + dx, y + dy) and\
                is_our(x + 2 * dx, y + 2 * dy) and\
                is_empty(x + 3 * dx, y + 3 * dy):
            weight += 20

        # 活三 '0*110'
        if is_empty(x - dx, y - dy) and\
                is_our(x + dx, y + dy) and\
                is_our(x + 2 * dx, y + 2 * dy) and\
                is_empty(x + 3 * dx, y + 3 * dy):
            weight += 100

        # 活三 '01*10'
        if is_empty(x - 2*dx, y - 2*dy) and\
                is_our(x - dx, y - dy) and\
                is_our(x + 1 * dx, y + 1 * dy) and\
                is_empty(x + 2 * dx, y + 2 * dy):
            weight += 100

        # 死四 '0*1112' 1000
        if is_empty(x - dx, y - dy) and\
                is_our(x + dx, y + dy) and\
                is_our(x + 2 * dx, y + 2 * dy) and\
                is_our(x + 3 * dx, y + 3 * dy) and\
                is_enemy(x + 4 * dx, y + 4 * dy):
            weight += 1000

        # 活四 '0*1110' 1000
        if is_empty(x - dx, y - dy) and\
                is_our(x + dx, y + dy) and\
                is_our(x + 2 * dx, y + 2 * dy) and\
                is_our(x + 3 * dx, y + 3 * dy) and\
                is_empty(x + 4 * dx, y + 4 * dy):
            weight += 1000

        # 五連
        if is_our(x + dx, y + dy) and is_our(x + 2 * dx, y + 2 * dy) and is_our(x + 3 * dx, y + 3 * dy) and is_our(
                x + 4 * dx, y + 4 * dy):
            weight += 10000

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



def is_5_link(board: BoardInfo, action, activated_player: int):
    if activated_player == 0:
        is_our = board.is_black
    else:
        is_our = board.is_white

    x, y = action

    for dx, dy in directions:
        if is_our(x + dx, y + dy) and is_our(x + 2 * dx, y + 2 * dy) and is_our(x + 3 * dx, y + 3 * dy) and is_our(
                x + 4 * dx, y + 4 * dy):
            return True

    return False


def get_possible_actions(board: BoardInfo):
    possible_actions = set()

    for ((x, y), _) in board.steps:
        for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]:
            if board.is_legal_action(x + dx, y + dy):
                possible_actions.add((x + dx, y + dy))

    return list(possible_actions)


def get_weighted_actions(board: BoardInfo, possible_actions, activated_player: int):
    weighted_actions = []

    for action in possible_actions:
        weight = analysis_action(board, action, activated_player)
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