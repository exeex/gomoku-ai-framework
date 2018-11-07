import glob
import os
import sys
import importlib
import itertools
import time
from goboard import GomokuGameHandler
# from goboard.judge import Win, Lose
from goboard.exception import Win, Lose
from goboard.logger import log
import inspect
import json
import pickle


def get_log_file_name(black_player, white_player, game_num, referee):
    log_dir = "log"
    gamefile = '%s_vs_%s_%d.json' % (referee.palyerName(black_player), referee.palyerName(white_player), game_num)
    logfile = '%s_vs_%s_%d.txt' % (referee.palyerName(black_player), referee.palyerName(white_player), game_num)
    gamefile = os.path.join(log_dir, gamefile)
    logfile = os.path.join(log_dir, logfile)
    return gamefile, logfile


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

    def finalScore(self):
        pass


def _run_game(black_player, white_player, referee, game_num):
    gamefile, logfile = get_log_file_name(black_player, white_player, game_num, referee)
    with GomokuGameHandler(black_player, white_player, log_file=logfile, game_file=gamefile,
                           board_size=(7, 7)) as (black_round, white_round, board):
        for _ in range(11 * 11 // 2):
            try:
                white_round()
                # time.sleep(0.3)
                black_round()
                # time.sleep(0.3)
            except Win as e:
                log('[end game] %s' % e)
                # time.sleep(10)
                if e.winner == black_round.player:
                    return (referee.palyerName(black_round.player), referee.palyerName(white_round.player),
                            black_round.time_remaining, white_round.time_remaining)
                else:
                    return (referee.palyerName(white_round.player), referee.palyerName(black_round.player),
                            black_round.time_remaining, white_round.time_remaining)

            except Lose as e:
                log('[end game] %s' % e)
                # time.sleep(10)
                if e.loser == black_round.player:
                    return (referee.palyerName(white_round.player), referee.palyerName(black_round.player),
                            black_round.time_remaining, white_round.time_remaining)
                else:
                    return (referee.palyerName(black_round.player), referee.palyerName(white_round.player),
                            black_round.time_remaining, white_round.time_remaining)


def run_game(p1, p2, referee, game_num):
    if game_num % 2 == 0:

        black_player = p1('black', board_size=(13, 13))
        white_player = p2('white', board_size=(13, 13))
        return _run_game(black_player, white_player, referee, game_num)
    else:

        white_player = p1('white', board_size=(13, 13))
        black_player = p2('black', board_size=(13, 13))
        return _run_game(black_player, white_player, referee, game_num)


if __name__ == '__main__':
    judge = referee()
    schedule = judge.Round_robin()
    print(schedule)
    # TODO: When exception occur write down the schedule
    # player1 = globals()[schedule[0][0]].Ai
    # player2 = globals()[schedule[0][1]].Ai
    #
    # black_player = player1("black", board_size=(13, 13))
    # white_player = player2("white", board_size=(13, 13))
    # # print(black_player)
    #
    # a = gameBlackFirst(black_player, white_player)
    # print(a,  '---')

    # result = []
    # for idx, game in enumerate(schedule):
    #     player1 = globals()[game[0]].Ai
    #     player2 = globals()[game[1]].Ai
    #     print(player1, player2, '--')
    #     temp_result = []
    #     for i in range(2):
    #         black_player = player1('black', board_size=(13, 13))
    #         white_player = player2('white', board_size=(13, 13))
    #         a = gameBlackFirst(black_player, white_player, judge)
    #         temp_result.append(a)
    #         b = gameWhiteFirst(black_player, white_player, judge)
    #         temp_result.append(b)
    #     with open('result.json', 'a') as file:
    #         json.dump(temp_result, file)
    #         file.write("\n")
    #     # TODO: use klepto
    #     result.append(temp_result)
    # with open('result.pickle', 'wb') as file:
    #     pickle.dump(result, file)
    # print(result)

    result = {}
    for idx, game in enumerate(schedule):
        player1 = globals()[game[0]].Ai
        player2 = globals()[game[1]].Ai
        print(player1, player2, '--')

        temp_result = []
        for i in range(4):
            a = run_game(player1, player2, judge, i)
            temp_result.append(a)

        with open('result.json', 'a') as file:
            json.dump(temp_result, file)
            file.write("\n")
        # TODO: use klepto

        result[(game[0].split('.')[1], game[1].split('.')[1])] = temp_result
    with open('result.pickle', 'wb') as file:
        pickle.dump(result, file)
    print(result)

    # result.append(a)
    # print(a)
    # a=name_of_function(player1)
    # print(type(player1).__class__.__name__)
    # result = pk(player, white)
    # print(result)
