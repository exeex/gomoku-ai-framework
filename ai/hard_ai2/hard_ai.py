from goboard import Player, BoardInfo, GuiManager
from ai.hard_ai2.mcts import UCT, GomokuState


class Ai(Player):
    def __init__(self, color):
        super(Ai, self).__init__(color)

    def get_action(self, board: BoardInfo, timeout) -> (int, int):
        """
            Implement your algorithm here.

            **Important**
            1. You must return (x, y)
            2. If any exception is raised, you will lose the game directly. Use try-except to handle error/exception. 
            3. To get current state of the game, you could call board.dense or board.steps to get data.

            :return: int x, int y
            """

        try:
             state = GomokuState(board)
             m = UCT(rootstate=state, itermax=30, verbose=False)
             return m

        except IndexError:
            return 5,5
