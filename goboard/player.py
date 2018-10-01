from .board import Board, BoardInfo

import tkinter as tk
from .gui import BoardFrame, GuiManager


class Player:
    def __init__(self, board_info: BoardInfo, gui=None, color="black"):
        """
        :param board_info: A GoBoard instance.
        :param color: to tell the ai what color he is playing. "black" or "white"
         """
        self.board_info = board_info
        self.color = color
        self.gui = gui

    def get_action(self, board: BoardInfo) -> (int, int):
        """
        Implement your algorithm here.
        To get the current status of the GoBoard, you might call self.board.steps and analysis it by your ai algorithm
        Before function return, you need to call self.put(x, y) once.
        :return:
        """
        raise NotImplementedError

    def after_battle(self):
        pass


class StupidAi(Player):
    def __init__(self, board_info: BoardInfo, gui: GuiManager, color="white"):
        super(StupidAi, self).__init__(board_info, gui, color)

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
                    return x,y
                else:
                    continue



class Human(Player):
    def __init__(self, board_info: BoardInfo, gui: GuiManager, color):
        super(Human, self).__init__(board_info, gui, color)

    def get_action(self, board: Board):
        x, y = self.gui.get_put_index()
        return x, y
