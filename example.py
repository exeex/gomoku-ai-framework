from goboard import GomokuBattleHandler
from goboard.player import StupidAi, Human
import matplotlib.pyplot as plt

plt.ion()
plt.show()

with GomokuBattleHandler(StupidAi, Human, board_size=(11, 11)) as (black, white):
    for _ in range(11*11):
        black.execute()
        white.execute()

