import glob
import os
import sys
import importlib
import itertools
import inspect
from goboard import GomokuGameHandler
from goboard.judge import Win, Lose
from goboard.logger import log
from ai.normal_ai import Ai as NormalAi
import time
from goboard.bo4 import Bo4Handler


class referee:
    def __init__(self, file_path='./ai'):
        self.file_path = file_path
        self.ailist = [os.path.splitext(os.path.basename(path))[0] for path in glob.glob(self.file_path + "/*.py")]
        self.ailist = ['ai.' + str(x) for x in self.ailist]
        for module in self.ailist:
            try:
                module_obj = importlib.import_module(module)
                # create a global object containging our module
                globals()[module] = module_obj
                # because we want to import using a variable, do it this way

            except ImportError:
                sys.stderr.write("ERROR: missing python module: " + module + "\n")
                sys.exit(1)

    def competitors(self):
        return [competitor.split('.')[1] for competitor in self.ailist]

    def Round_robin(self):
        return list(itertools.combinations(self.ailist, r=2))

    def palyerName(self, classObj):
        path = inspect.getfile(classObj.__class__)
        name = os.path.splitext(os.path.basename(path))[0]
        return name


if __name__ == '__main__':
    judge = referee()
    schedule = judge.Round_robin()
    print(schedule)
    for player1, player2 in schedule:

        player1_remainingTime = 0
        player2_remainingTime = 0

        player1 = globals()[player1].Ai
        player2 = globals()[player2].Ai

        h = Bo4Handler(player1, player2, board_size=(7, 7))  # change board_size to 13,13

        for black_player, white_player in h.get_player_instance():
            print(black_player.color)
            print(type(black_player), type(white_player))


            with GomokuGameHandler(black_player, white_player, board_size=(7, 7)) as (
                black_round, white_round, board):
                try:
                    for _ in range(11 * 11 // 2):
                        black_round()
                        time.sleep(0.1)
                        white_round()
                        time.sleep(0.1)

                except Win as e:
                    h.handle_win_lose(e)
                    h.handle_time(black_round.get_run_time(),white_round.get_run_time())
                    log('[end game] %s' % e)
                except Lose as e:
                    h.handle_win_lose(e)
                    h.handle_time(black_round.get_run_time(),white_round.get_run_time())
                    log('[end game] %s' % e)

        h.print_state()
