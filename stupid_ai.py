from goboard import GoBoard


class StupidAi:
    def __init__(self, board: GoBoard, black_or_white="black"):
        """
        :param board: A GoBoard instance.
        :param black_or_white: to tell the ai what color he is playing. "black" or "white"
         """
        self.board = board
        if black_or_white == "black":
            self.put = self.board.put_black
        elif black_or_white == "white":
            self.put = self.board.put_white

    def execute(self):
        """
        Implement your algorithm here.
        To get the current status of the GoBoard, you might call self.board.steps and analysis it by your ai algorithm
        Before function return, you need to call self.put(x, y) once.
        :return:
        """

        for x in range(0, 19):
            for y in range(0, 19):
                if not self.board.is_collision(x, y):
                    self.put(x, y)
                    return