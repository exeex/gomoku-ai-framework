from goboard import GomokuGameHandler
from goboard.judge import Win, Lose
from goboard.logger import log
from ai.normal_ai import Ai as NormalAi
import time
from goboard.bo4 import bo4Handler

h = bo4Handler(NormalAi, NormalAi, board_size=(7, 7))

for black_player, white_player in h.get_player_instance():
    print(black_player.color)
    print(type(black_player), type(white_player))

    try:
        with GomokuGameHandler(black_player, white_player, board_size=(7, 7)) as (black_round, white_round, board):
            for _ in range(11 * 11 // 2):
                black_round()
                time.sleep(0.1)
                white_round()
                time.sleep(0.1)

    except Win as e:
        h.handle_win_lose(e)
        log('[end game] %s' % e)
    except Lose as e:
        h.handle_win_lose(e)
        log('[end game] %s' % e)

h.print_state()
