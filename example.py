from goboard import GomokuBattleHandler, init_plot_board, plot_board, GoBoard
from goboard.player import StupidAi, Human
from goboard.judge import BlackWin, WhiteWin, link_judge
import time

with GomokuBattleHandler(Human, StupidAi, board_size=(11, 11)) as (black, white, board):
    init_plot_board(board)
    for _ in range(11*11//2):
        try:
            black.execute()
            plot_board(board)
            link_judge(board, black)
            time.sleep(0.2)

            white.execute()
            plot_board(board)
            link_judge(board, white)
            time.sleep(0.2)

        except BlackWin:
            print('black win')
        except WhiteWin:
            print('white win')

    plot_board(board)
