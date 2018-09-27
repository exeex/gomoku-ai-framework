from goboard import GoBoard, Player

class MyAi(Player):
    def __init__(self, board: GoBoard, black_or_white="white"):
        super(MyAi, self).__init__(board, black_or_white)

    def execute(self):
        """
            Implement your algorithm here.

            **Important**
            1. Before function return, you must call self.put(x, y) once.
            2. Use try-except to handle invalid action
            3. To get current state of the game, you could call self.board.steps.

            """

        try:
            x, y = self.get_best_action(self.board)
            self.put(x, y)
            return
        except Exception as e:
            print(e)
            x, y = self.plan_B(self.board)
            self.put(x, y)

    def get_best_action(self, board: GoBoard):
        # implement some algorithm(ex. Mote Carlo Search Tree) here
        # and return a best action position
        ...
        return x, y

    def plan_B(self, board: GoBoard):
        # In case get_best_action not works, try plan B.
        ...
        return x, y