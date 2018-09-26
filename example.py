from goboard import GomokuBattleHandler
from goboard.player import StupidAi, Human




with GomokuBattleHandler(StupidAi, Human, board_size=(11, 11)) as (black, white, board):
    board.show()
    for _ in range(11*11):
        black.execute()
        board.show()
        white.execute()
        board.show()

