from goboard import GomokuBattleHandler, init_plot_board, plot_board, GoBoard
from goboard.player import StupidAi, Human
import matplotlib.pyplot as plt

with GomokuBattleHandler(StupidAi, StupidAi, board_size=(11, 11)) as (black, white, board):
    init_plot_board(board)
    for _ in range(11*11):
        black.execute()
        white.execute()

    plot_board(board)
