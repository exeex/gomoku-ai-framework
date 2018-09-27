from goboard import GomokuBattleHandler, GoBoard
from goboard.plot import init_plot_board, plot_board
from goboard.player import StupidAi, Human
import goboard.judge as j
import time

with GomokuBattleHandler(StupidAi, StupidAi, board_size=(11, 11)) as (black_round, white_round, board):
    init_plot_board(board)
    for _ in range(11*11//2):
        try:
            black_round()
            # plot_board(board)
            # time.sleep(0.2)

            white_round()
            # plot_board(board)
            # time.sleep(0.2)

        except j.Win as e:
            print(e)
            break
        except j.Lose as e:
            print(e)
            break

    plot_board(board)
