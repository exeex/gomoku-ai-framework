from goboard import GomokuBattleHandler
from goboard.judge import Win, Lose
from goboard.player import Human
from goboard.logger import log
from ai.normal_ai import Ai as NormalAi
import time

with GomokuBattleHandler(Human, NormalAi, board_size=(13, 13)) as (black_round, white_round, board):
    for _ in range(11 * 11 // 2):
        try:
            black_round()
            white_round()

        except Win as e:
            log('[end game] %s' % e)
            break

        except Lose as e:
            log('[end game] %s' % e)
            break

    time.sleep(3)
