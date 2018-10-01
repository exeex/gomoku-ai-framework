from .goboard import GoBoard

import tkinter as tk
from .gui import BoardFrame, GuiManager


class Player:
    def __init__(self, board: GoBoard, gui=None, black_or_white="black"):
        """
        :param board: A GoBoard instance.
        :param black_or_white: to tell the ai what color he is playing. "black" or "white"
         """
        self.board = board
        self.bw = black_or_white
        if gui:
            self.gui = gui

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
            if self.gui:
                self.gui.update_screen()

        elif self.bw == "white":
            self.board.put_white(x, y)
            if self.gui:
                self.gui.update_screen()
        else:
            raise NameError("You only can choose white or black!")

    def after_battle(self):
        pass


class StupidAi(Player):
    def __init__(self, board: GoBoard, gui: GuiManager, black_or_white="white"):

        super(StupidAi, self).__init__(board, gui, black_or_white)

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


class Human(Player):
    def __init__(self, board: GoBoard, gui: GuiManager, black_or_white):
        super(Human, self).__init__(board, gui, black_or_white)
        self.bw = black_or_white
        self.board = board
        self.gui = gui

    def execute(self):
        x, y = self.gui.get_put_index()
        self.put(x, y)
