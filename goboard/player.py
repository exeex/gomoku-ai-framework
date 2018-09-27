from .goboard import GoBoard

import tkinter as tk
from .gui import BoardFrame


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

    def after_battle(self):
        pass


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


class HumanGui(Player):
    def __init__(self, board: GoBoard, black_or_white):
        super(HumanGui, self).__init__(board, black_or_white)
        self.bw = black_or_white
        self.board = board
        self.create_gui(self.board)

    @staticmethod
    def get_tk():
        global tk_instance
        try:
            return tk_instance
        except NameError:
            tk_instance = tk.Tk()
            return tk_instance

    @classmethod
    def create_gui(cls, board):
        cls.window = HumanGui.get_tk()
        try:
            cls.board_frame.pack()
        except AttributeError:
            cls.board_frame = BoardFrame(board, cls.window)
            cls.board_frame.pack()

        board.after_put = cls.board_frame.board_canvas.put_stone_on_gui
        cls.window.update_idletasks()

    def execute(self):
        while not self.board_frame.board_canvas.clicked:
            self.window.update()
        x, y = self.board_frame.board_canvas.put_temp
        self.put(x, y)
        self.board_frame.board_canvas.clicked = False

    def after_battle(self):
        while True:
            self.window.update()