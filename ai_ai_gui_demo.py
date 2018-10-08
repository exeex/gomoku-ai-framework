from goboard import GomokuBattleHandler
from goboard.judge import Win, Lose
from goboard.logger import log
from ai.normal_ai import Ai as NormalAi
import time

with GomokuBattleHandler(NormalAi, NormalAi, board_size=(13, 13)) as (black_round, white_round, board):
    for _ in range(11 * 11 // 2):
        try:
            black_round()
            time.sleep(0.3)
            white_round()
            time.sleep(0.3)

        except Win as e:
            log('[end game] %s' % e)
            break

        except Lose as e:
            log('[end game] %s' % e)
            break

    time.sleep(5)
