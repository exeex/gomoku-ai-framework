from goboard import Player, BoardInfo, GuiManager


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

        for x in range(0, board.size_x):
            for y in range(0, board.size_y):
                if board.is_legal_action(x, y):
                    return x, y
                else:
                    continue
