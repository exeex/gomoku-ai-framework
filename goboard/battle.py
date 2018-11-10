from .board import Board
from .player import Player
from .gui import GuiManager, DummyGuiManager
from .judge import exec_and_timeout_judge, link_judge, tie_judge, move_judge, timeit
from .logger import log, open_log_file, save_log_file
from .exception import ColorError
import json
import time


def save_game(file_name, board: Board, **kwargs):
    xy, bw = tuple(zip(*board.steps))

    battle = {
        "battle_info": {
            "board_size": (board.size_x, board.size_y),
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


def load_game(file_name):
    f = open(file=file_name, mode='r')
    data = json.load(f)
    steps = data['steps']
    board_size = data['battle_info']['board_size']

    b = Board(size=board_size)

    for step in steps:
        x, y = step[0][0], step[0][1]
        color = step[1]
        b._put(int(x), int(y), color=color)

    return b


class Round:
    def __init__(self, player: Player, board: Board, total_cal_time=50, min_cal_time=6):
        self.player = player
        self.board = board
        self.color = player.color
        self.step_counter = None
        self.update_step_counter()
        self.time_remaining = total_cal_time
        self.total_cal_time = total_cal_time
        self.min_cal_time = min_cal_time

    def __call__(self, *args, **kwargs):

        log("[%s] round start" % self.color)

        # Init round
        self.update_step_counter()
        ts = time.time()

        # If a player is running out of all total_cal_time, the time limit for each round will be min_cal_time
        if self.time_remaining > self.min_cal_time:
            timeout = self.time_remaining
        else:
            timeout = self.min_cal_time

        # If time out, time judge will raise a Exception
        exec_and_timeout_judge(self.board, self.player, self.color, timeout=timeout)

        # Log time duration
        te = time.time()
        duration = te - ts
        self.time_remaining -= duration

        # Show debug msg
        log("[%s] put stone at %s" % (self.color, self.board.steps[-1][0]))
        log("[%s] Time duration : %.3f, Time remaining : %.3f" % (self.color, duration, self.time_remaining))

        # Check who wins and check illegal moves.
        link_judge(self.board, self.player, self.color)
        tie_judge(self.board, self.color)
        move_judge(self.board, self.step_counter, self.player, self.color)
        return self.board.steps[-1]

    def update_step_counter(self):
        self.step_counter = len(self.board)

    def get_run_time(self):
        return self.total_cal_time - self.time_remaining


class GomokuGameHandler:
    def __init__(self, black_player, white_player, log_file="log.txt", game_file="game.json", load=False, use_gui=True,
                 board_size=None):

        # log
        self.log_file = log_file
        open_log_file(self.log_file)

        # load battle_file if battle file exists, or create a new one
        self.game_file = game_file

        if load:
            self.board = load_game(self.game_file)
            # TODO: continue battle
        else:
            self.board = Board(size=board_size)

        # build GUI
        if use_gui:
            self.gui = GuiManager(self.board)
        else:
            self.gui = DummyGuiManager(self.board)

        # check color
        if black_player.color != "black":
            raise ColorError
        if white_player.color != "white":
            raise ColorError

        # bind gui and update new screen
        black_player.bind_gui(self.gui)
        white_player.bind_gui(self.gui)
        self.gui.update_screen()

        # build Round object
        self.black_player = black_player
        self.white_player = white_player

        self.black_round = Round(self.black_player, self.board)
        self.white_round = Round(self.white_player, self.board)

    def __enter__(self):
        log("[start game]")
        return self.black_round, self.white_round, self.board

    def __exit__(self, exc_type, exc_val, exc_tb):
        # save_game(self.log_file, self.board)
        log("[end game] black total calculation time : %.3f" % self.black_round.get_run_time())
        log("[end game] white total calculation time : %.3f" % self.white_round.get_run_time())
        # self.black_player.after_battle()
        # self.white_player.after_battle()
        self.gui.clear_board()
        save_game(self.game_file, self.board)
        save_log_file()
        # self.gui.after_battle()

        # TODO: call a judge to record who wins and record execute time
