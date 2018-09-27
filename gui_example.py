from goboard import GomokuBattleHandler, GoBoard
from goboard.plot import init_plot_board, plot_board
from goboard.player import StupidAi, Human, HumanGui
import goboard.judge as j

with GomokuBattleHandler(HumanGui, StupidAi, board_size=(13, 13)) as (black_round, white_round, board):
    for _ in range(11 * 11 // 2):
        try:
            black_round()
            white_round()

        except j.Win as e:
            print(e)
            break
        except j.Lose as e:
            print(e)
            break


