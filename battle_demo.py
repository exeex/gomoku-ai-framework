from goboard import GomokuBattleHandler
from goboard.plot import init_plot_board, plot_board
from goboard.player import StupidAi
from goboard.judge import Win, Lose, Tie

with GomokuBattleHandler(black_player=StupidAi,
                         white_player=StupidAi,
                         board_size=(11, 11),
                         battle_file="lastest_battle.json") \
                         as (black_round, white_round, board):

    init_plot_board(board)

    while True:
        try:
            black_round()
            white_round()
        except Win as e:
            print(e)
            break
        except Lose as e:
            print(e)
            break
        except Tie as e:
            print(e)
            break

    plot_board(board)
