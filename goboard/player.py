from .board import Board, BoardInfo
import time
from .gui import GuiManager

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






class Human(Player):
    def __init__(self, board_info: BoardInfo, gui: GuiManager, color):
        super(Human, self).__init__(board_info, gui, color)

    def get_action(self, board: Board):
        x, y = self.gui.get_put_index()
        return x, y
