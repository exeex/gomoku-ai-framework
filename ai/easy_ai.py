from goboard import Player, BoardInfo, GuiManager
import numpy as np

class Ai(Player):
    def __init__(self, color,**kwargs):
        super(Ai, self).__init__(color)
        try:
            size_x, size_y = kwargs['board_size']
            self.value = np.zeros((size_x, size_y))
        except IndexError:
            self.value = np.zeros((13, 13))

    def get_action(self, board: BoardInfo) -> (int, int):
        """
            Implement your algorithm here.

            **Important**
            1. You must return (x, y)
            2. If any exception is raised, you will lose the game directly. Use try-except to handle error/exception. 
            3. To get current state of the game, you could call board.dense or board.steps to get data.

            :return: int x, int y
            """

        for x in range(0, board.size_x):
            for y in range(0, board.size_y):
                if board.is_legal_action(x, y):
                    return x, y
                else:
                    continue
