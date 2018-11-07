from goboard import GomokuGameHandler
from goboard.judge import Win, Lose
from goboard.player import Human
from goboard.logger import log
from ai.normal_ai import Ai as NormalAi
import time

black_player = NormalAi("black", board_size=(13, 13))
white_player = Human("white", board_size=(13, 13))
try:
    with GomokuGameHandler(black_player, white_player, board_size=(13, 13)) as (black_round, white_round, board):
        for _ in range(13 * 13 // 2):
            black_round()
            white_round()

except Win as e:
    time.sleep(3)
    log('[end game] %s' % e)
except Lose as e:
    time.sleep(3)
    log('[end game] %s' % e)

black_player = NormalAi("black", board_size=(13, 13))
white_player = Human("white", board_size=(13, 13))
try:
    with GomokuGameHandler(black_player, white_player, board_size=(13, 13)) as (black_round, white_round, board):
        for _ in range(13 * 13 // 2):
            black_round()
            white_round()

except Win as e:
    time.sleep(3)
    log('[end game] %s' % e)
except Lose as e:
    time.sleep(3)
    log('[end game] %s' % e)