from goboard import Board, Player

class MyAi(Player):
    def __init__(self, board_info: Board, color="white"):
        super(MyAi, self).__init__(board_info, color)

    def execute(self):
        """
            Implement your algorithm here.

            **Important**
            1. Before function return, you must call self.put(x, y) once.
            2. Use try-except to handle invalid action
            3. To get current state of the game, you could call self.board.steps.

            """

        try:
            x, y = self.get_best_action(self.board_info)
            self.put(x, y)
            return
        except Exception as e:
            print(e)
            x, y = self.plan_B(self.board_info)
            self.put(x, y)

    def get_best_action(self, board: Board):
        # implement some algorithm(ex. Mote Carlo Search Tree) here
        # and return a best action position
        ...
        return x, y

    def plan_B(self, board: Board):
        # In case get_best_action not works, try plan B.
        ...
        return x, y