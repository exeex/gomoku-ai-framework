from goboard import Player, BoardInfo, GuiManager


class Ai(Player):
    def __init__(self, board_info: BoardInfo, gui: GuiManager, color):
        super(Ai, self).__init__(board_info, gui, color)

    def get_action(self, board: BoardInfo) -> (int, int):
        """
            Implement your algorithm here.

            **Important**
            1. Before function return, you must call self.put(x, y) once.
            2. Use try-except to handle invalid placement
            3. To get current state of the game, you could call self.board.steps to get data.

            :return:
            """

        for x in range(0, board.size_x):
            for y in range(0, board.size_y):
                if not board.is_legal_action(x, y):
                    return x, y
                else:
                    continue
