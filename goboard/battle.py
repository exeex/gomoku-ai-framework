from .goboard import GoBoard, save_battle, load_battle
from .player import Player

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

        self.log_file = battle_file

    def __enter__(self):
        return self.black_player, self.white_player, self.board

    def __exit__(self, exc_type, exc_val, exc_tb):
        save_battle(self.log_file, self.board)
