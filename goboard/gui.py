#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The code of gui.py is a fork of this project(Under MIT License):
https://github.com/s8w1e2ep/GoMoKu
Origin author is s8w1e2ep
"""

from tkinter import TclError
import tkinter as tk
import math
from .board import Board


class Point:
    def __init__(self, x, y):
        """
        棋盤座標和像素座標轉換
        """
        self.x = x
        self.y = y
        self.pixel_x = 60 + 30 * self.y
        self.pixel_y = 60 + 30 * self.x


class BoardCanvas(tk.Canvas):
    # 棋盤繪製
    def __init__(self, board: Board, master=None, height=0, width=0):
        tk.Canvas.__init__(self, master, height=height, width=width)
        self.board = board
        self.chess_board_points = [[None for i in range(self.board.size_x)] for j in range(self.board.size_y)]
        self.init_chess_board_points()  # 畫點
        self.init_chess_board_xy_ticks()  # 畫標記
        self.init_chess_board_canvas()  # 畫棋盤
        self.stone_ids = []
        self.clicked = False
        self.put_temp = (0, 0)

    def init_chess_board_points(self):
        """
        生成棋盤點
        """
        for i in range(self.board.size_x):
            for j in range(self.board.size_y):
                self.chess_board_points[i][j] = Point(i, j)  # 轉換棋盤座標像素座標

        for i in range(self.board.size_x):  # 交點橢圓
            for j in range(self.board.size_y):
                r = 1
                x = self.chess_board_points[i][j].pixel_x
                y = self.chess_board_points[i][j].pixel_y
                self.create_oval(x - r, y - r,
                                 x + r, y + r, )

    def init_chess_board_xy_ticks(self):
        """
        生成座標label
        """

        r = 1

        for i in range(self.board.size_x):
            x = self.chess_board_points[i][0].pixel_x - 30
            y = self.chess_board_points[i][0].pixel_y
            self.create_text(x, y, text="x%d" % i)

        for j in range(self.board.size_x):
            x = self.chess_board_points[0][j].pixel_x
            y = self.chess_board_points[0][j].pixel_y - 30
            self.create_text(x, y, text="y%d" % j)

    def init_chess_board_canvas(self):
        """
        畫直線橫線
        """
        for i in range(self.board.size_x):  # 直線
            self.create_line(self.chess_board_points[i][0].pixel_x, self.chess_board_points[i][0].pixel_y,
                             self.chess_board_points[i][self.board.size_x - 1].pixel_x,
                             self.chess_board_points[i][self.board.size_x - 1].pixel_y)

        for j in range(self.board.size_y):  # 橫線
            self.create_line(self.chess_board_points[0][j].pixel_x, self.chess_board_points[0][j].pixel_y,
                             self.chess_board_points[self.board.size_x - 1][j].pixel_x,
                             self.chess_board_points[self.board.size_x - 1][j].pixel_y)

    def put_stone_on_gui(self, x, y, color):
        """
        落子
        :param x: x index of the board (not pixel)
        :param y: y index of the board (not pixel)
        :param color: k: black stone, w: white stone
        :return:
        """
        if color == 'k':
            color = 'black'
        elif color == 'w':
            color = 'white'
        stone_id = self.create_oval(self.chess_board_points[x][y].pixel_x - 10,
                                    self.chess_board_points[x][y].pixel_y - 10,
                                    self.chess_board_points[x][y].pixel_x + 10,
                                    self.chess_board_points[x][y].pixel_y + 10, fill=color)
        self.stone_ids.append(stone_id)
        tk.Canvas.update(self)

    def clear_board(self):
        for stone_id in self.stone_ids:
            self.delete(stone_id)
        self.stone_ids = []

    def click_listener(self, event):  # click關鍵字重複

        """
        監聽滑鼠事件,根據滑鼠位置判斷落點
        """
        if not self.clicked:
            for i in range(self.board.size_x):
                for j in range(self.board.size_y):
                    square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow(
                        (event.y - self.chess_board_points[i][j].pixel_y), 2)
                    # 計算滑鼠的位置和點的距離
                    # 距離小於14的點

                    if square_distance <= 200 and self.board.is_legal_action(i, j):  # 合法落子位置
                        # set clicked and write put stone position to put_temp
                        self.clicked = True
                        self.put_temp = (i, j)


class BoardFrame(tk.Frame):
    def __init__(self, board: Board, master=None):
        tk.Frame.__init__(self, master)
        self.chess_board_label_frame = tk.LabelFrame(self, text="Gomoku Board", padx=5, pady=5)
        self.board_canvas = BoardCanvas(board, self.chess_board_label_frame, height=500, width=480)
        self.board_canvas.bind('<Button-1>', self.board_canvas.click_listener)
        self.chess_board_label_frame.pack()
        self.board_canvas.pack()


class GuiManager:
    def __init__(self, board: Board):
        self.board = board
        self.bind_board(self.board)

    @staticmethod
    def get_tk():
        global tk_instance
        try:
            return tk_instance
        except NameError:
            tk_instance = tk.Tk()
            return tk_instance

    @classmethod
    def bind_board(cls, board: Board):
        cls.window = GuiManager.get_tk()

        # Try to use the same board_frame. If board_frame exists, rebind with board, else create a new one.
        try:
            cls.board_frame.board_canvas.board = board
            cls.board_frame.pack()
        except AttributeError:
            cls.board_frame = BoardFrame(board, cls.window)
            cls.board_frame.pack()

        board.after_put = cls.board_frame.board_canvas.put_stone_on_gui
        cls.window.update_idletasks()

    def get_put_index(self):
        while not self.board_frame.board_canvas.clicked:
            self.window.update()

        x, y = self.board_frame.board_canvas.put_temp
        self.board_frame.board_canvas.clicked = False
        return x, y

    def clear_board(self):
        self.board_frame.board_canvas.clear_board()

    def update_screen(self):
        self.window.update()

    def after_battle(self):
        try:
            while True:
                self.window.update()
        except TclError:
            pass


class DummyGuiManager:
    def __init__(self, board: Board):
        self.board = board


    def bind_gui(cls, board):
        pass

    def get_put_index(self):

        while True:

            try:
                x = int(input("input x:\n"))
                y = int(input("input y:\n"))

                if self.board.is_legal_action(x, y):
                    return x, y
                else:
                    print("Collision!")
                    continue
            except ValueError:
                continue

    def update_screen(self):
        pass

    def after_battle(self):
        pass

    def clear_board(self):
        pass
