from goboard import GomokuBattleHandler, init_plot_board, plot_board, GoBoard
from goboard.player import StupidAi, Human
import goboard.judge as j
import time

with GomokuBattleHandler(Human, StupidAi, board_size=(11, 11)) as (black, white, board):
    init_plot_board(board)
    for _ in range(11*11//2):
        try:
            black.execute()
            plot_board(board)
            j.link_judge(board, black)
            time.sleep(0.2)

            white.execute()
            plot_board(board)
            j.link_judge(board, white)
            time.sleep(0.2)

        except j.BlackWin as e:
            print(e)
            break
        except j.WhiteWin as e:
            print(e)
            break

    plot_board(board)
