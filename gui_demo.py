from goboard import GomokuBattleHandler
from goboard.player import StupidAi, Human
from value_ai import ValueNetAi
from goboard.judge import Win,Lose

with GomokuBattleHandler(Human, ValueNetAi, board_size=(13, 13)) as (black_round, white_round, board):
    for _ in range(11 * 11 // 2):
        try:
            black_round()
            white_round()

        except Win as e:
            print(e)
            break

        except Lose as e:
            print(e)
            break


