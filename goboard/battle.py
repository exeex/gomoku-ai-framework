from .goboard import GoBoard, save_battle, load_battle
from .player import Player
import matplotlib.pyplot as plt


class GomokuBattleHandler:
    def __init__(self, black_player, white_player, battle_file="gg.json", load=False, board_size=None):
        if load:
            self.b = load_battle(battle_file)
            # TODO: continue battle
        else:
            if board_size:
                self.b = GoBoard(size=board_size)
            else:
                self.b = GoBoard()

        self.black_player = black_player(self.b, "black")
        self.white_player = white_player(self.b, "white")

        self.log_file = battle_file

        plt.ion()
        plt.show()

    def __enter__(self):
        return self.black_player, self.white_player

    def __exit__(self, exc_type, exc_val, exc_tb):
        save_battle(self.log_file, self.b)


