from goboard import GomokuGameHandler
from goboard.judge import Win, Lose
from goboard.player import Human
from goboard.logger import log
import time

black_player = Human("black")
white_player = Human("white")

with GomokuGameHandler(black_player, white_player, board_size=(13, 13)) as (black_round, white_round, board):
    for _ in range(13 * 13 // 2):
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
