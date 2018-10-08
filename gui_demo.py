from goboard import GomokuBattleHandler
from goboard.judge import Win,Lose
from ai.easy_ai import Ai as EasyAi
from ai.normal_ai import Ai as NormalAi
import time



with GomokuBattleHandler(NormalAi, EasyAi, board_size=(13, 13)) as (black_round, white_round, board):
    for _ in range(11 * 11 // 2):
        try:
            black_round()
            time.sleep(0.3)
            white_round()
            time.sleep(0.3)

        except Win as e:
            print(e)
            break

        except Lose as e:
            print(e)
            break

    time.sleep(10)
