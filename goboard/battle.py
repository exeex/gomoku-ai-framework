from .goboard import GoBoard
from .player import Player
from .judge import time_judge, link_judge, tie_judge, move_judge
import json

def save_battle(file_name, board: GoBoard, **kwargs):
    xy, bw = tuple(zip(*board.steps))

    battle = {
        "battle_info": {
            "board_size": board.size,
            "other_info": kwargs,
        },
        "steps": list(zip(xy, bw)),
    }

    json_str = json.dumps(battle)

    try:
        f = open(file_name, 'w')
    except FileExistsError:
        raise FileExistsError

    f.write(json_str)


def load_battle(file_name):
    f = open(file=file_name, mode='r')
    data = json.load(f)
    steps = data['steps']
    board_size = data['battle_info']['board_size']

    b = GoBoard(size=board_size)

    for step in steps:
        x, y = step[0][0], step[0][1]
        color = step[1]
        b._put(int(x), int(y), color=color)

    return b

class Round:
    def __init__(self, player, board: GoBoard):
        self.player = player
        self.board = board
        self.step_counter = None
        self.update_step_counter()

    def __call__(self, *args, **kwargs):
        self.update_step_counter()
        time_judge(self.player.execute, self.player)
        link_judge(self.board, self.player)
        tie_judge(self.board)
        move_judge(self.board, self.step_counter, self.player)

        return self.board.steps[-1]
    def update_step_counter(self):
        self.step_counter = len(self.board)


class GomokuBattleHandler:
    def __init__(self, black_player, white_player, battle_file="lastest_battle.json", load=False, board_size=None):
        if load:
            self.board = load_battle(battle_file)
            # TODO: continue battle
        else:
            if board_size:
                self.board = GoBoard(size=board_size)
            else:
                self.board = GoBoard()
        try:
            self.black_player = black_player(self.board, "black")
            self.white_player = white_player(self.board, "white")

        except TypeError:
            raise TypeError("black_player and white_player must be class which inherit goboard.player.Player.")

        if not isinstance(self.black_player, Player):
            raise TypeError("black_player and white_player must be class which inherit goboard.player.Player.")
        if not isinstance(self.white_player, Player):
            raise TypeError("black_player and white_player must be class which inherit goboard.player.Player.")

        self.black_round = Round(self.black_player, self.board)
        self.white_round = Round(self.white_player, self.board)
        self.log_file = battle_file

    def __enter__(self):
        return self.black_round, self.white_round, self.board

    def __exit__(self, exc_type, exc_val, exc_tb):
        save_battle(self.log_file, self.board)
        self.black_player.after_battle()
        self.white_player.after_battle()
