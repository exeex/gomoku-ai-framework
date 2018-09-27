from .goboard import GoBoard


class Player:
    def __init__(self, board: GoBoard, black_or_white="black"):
        """
        :param board: A GoBoard instance.
        :param black_or_white: to tell the ai what color he is playing. "black" or "white"
         """
        self.board = board
        self.bw = black_or_white

    def execute(self):
        """
        Implement your algorithm here.
        To get the current status of the GoBoard, you might call self.board.steps and analysis it by your ai algorithm
        Before function return, you need to call self.put(x, y) once.
        :return:
        """
        raise NotImplementedError

    def put(self, x, y):
        if self.bw == "black":
            self.board.put_black(x, y)
        elif self.bw == "white":
            self.board.put_white(x, y)
        else:
            raise NameError("You only can choose white or black!")


class Human(Player):
    def __init__(self, board: GoBoard, black_or_white="black"):

        super(Human, self).__init__(board, black_or_white)

    def execute(self):

        while True:
            try:
                x = input("input x:\n")
                y = input("input y:\n")
                self.put(int(x), int(y))
            except ValueError:
                continue
            yn = input("Are you sure to place here?(Y/n)")
            if yn == 'n':
                self.board.step_back()
                continue

            break


class StupidAi(Player):
    def __init__(self, board: GoBoard, black_or_white="white"):

        super(StupidAi, self).__init__(board, black_or_white)

    def execute(self):
        """
            Implement your algorithm here.

            **Important**
            1. Before function return, you must call self.put(x, y) once.
            2. Use try-except to handle invalid placement
            3. To get current state of the game, you could call self.board.steps to get data.

            :return:
            """

        for x in range(0, self.board.size_x):
            for y in range(0, self.board.size_y):
                try:
                    self.put(x, y)
                    return
                except IndexError:
                    continue
