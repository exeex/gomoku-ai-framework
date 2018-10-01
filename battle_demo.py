from goboard import GomokuBattleHandler
from goboard.player import StupidAi, Human
from goboard.judge import Win, Lose, Tie
with GomokuBattleHandler(black_player=Human,
                         white_player=Human,
                         board_size=(13, 13),
                         battle_file="lastest_battle.json",
                         use_gui=True) \
                         as (black_round, white_round, board):

    while True:
        try:
            black_round()
            white_round()
        except Win as e:
            print(e)
            break
        except Lose as e:
            print(e)
            break
        except Tie as e:
            print(e)
            break

