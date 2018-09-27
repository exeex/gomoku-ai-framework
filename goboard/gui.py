#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import math
import numpy as np
from .goboard import GoBoard
import tkinter
import threading


class Point:
    def __init__(self, x, y):
        '''
        棋盤座標和像素座標轉換
        '''
        self.x = x
        self.y = y
        self.pixel_x = 30 + 30 * self.x
        self.pixel_y = 30 + 30 * self.y


class BoardCanvas(tkinter.Canvas):
    # 棋盤繪製
    def __init__(self, board: GoBoard, master=None, height=0, width=0):
        tkinter.Canvas.__init__(self, master, height=height, width=width)
        self.board = board
        self.chess_board_points = [[None for i in range(self.board.size_x)] for j in range(self.board.size_y)]
        self.init_chess_board_points()  # 畫點
        self.init_chess_board_canvas()  # 畫棋盤
        self.clicked = 0

    def init_chess_board_points(self):
        '''
        生成棋盤點,並且對應到像素座標
        保存到 chess_board_points 屬性
        '''
        for i in range(self.board.size_x):
            for j in range(self.board.size_y):
                self.chess_board_points[i][j] = Point(i, j)  # 轉換棋盤座標像素座標

    def init_chess_board_canvas(self):
        '''
        初始化棋盤
        '''

        for i in range(self.board.size_x):  # 直線
            self.create_line(self.chess_board_points[i][0].pixel_x, self.chess_board_points[i][0].pixel_y,
                             self.chess_board_points[i][self.board.size_x - 1].pixel_x,
                             self.chess_board_points[i][self.board.size_x - 1].pixel_y)

        for j in range(self.board.size_y):  # 橫線
            self.create_line(self.chess_board_points[0][j].pixel_x, self.chess_board_points[0][j].pixel_y,
                             self.chess_board_points[self.board.size_x - 1][j].pixel_x,
                             self.chess_board_points[self.board.size_x - 1][j].pixel_y)
        # 邊界
        # self.create_line(self.chess_board_points[2][2].pixel_x, self.chess_board_points[2][2].pixel_y,
        #                  self.chess_board_points[2][12].pixel_x, self.chess_board_points[2][12].pixel_y, fill="red")
        # self.create_line(self.chess_board_points[12][2].pixel_x, self.chess_board_points[12][2].pixel_y,
        #                  self.chess_board_points[12][12].pixel_x, self.chess_board_points[12][12].pixel_y, fill="red")
        # self.create_line(self.chess_board_points[2][12].pixel_x, self.chess_board_points[2][12].pixel_y,
        #                  self.chess_board_points[12][12].pixel_x, self.chess_board_points[12][12].pixel_y, fill="red")
        # self.create_line(self.chess_board_points[2][2].pixel_x, self.chess_board_points[2][2].pixel_y,
        #                  self.chess_board_points[12][2].pixel_x, self.chess_board_points[12][2].pixel_y, fill="red")

        for i in range(self.board.size_x):  # 交點橢圓
            for j in range(self.board.size_y):
                r = 1
                self.create_oval(self.chess_board_points[i][j].pixel_x - r, self.chess_board_points[i][j].pixel_y - r,
                                 self.chess_board_points[i][j].pixel_x + r, self.chess_board_points[i][j].pixel_y + r)

    def put_stone(self, i, j, color):
        if color == 'k':
            color = 'black'
        elif color == 'w':
            color = 'white'
        if not self.board.is_collision(i, j):
            self.create_oval(self.chess_board_points[i][j].pixel_x - 10,
                             self.chess_board_points[i][j].pixel_y - 10,
                             self.chess_board_points[i][j].pixel_x + 10,
                             self.chess_board_points[i][j].pixel_y + 10, fill=color)

            # if color == 'black' or color:
            #     self.board.put_black(i, j)
            # elif color == 'white':
            #     self.board.put_white(i, j)

            tkinter.Canvas.update(self)
        else:
            raise IndexError

    def put_black(self, i, j):
        self.put_stone(i, j, 'black')

    def put_white(self, i, j):
        self.put_stone(i, j, 'white')

    def click1(self, event):  # click關鍵字重複
        '''
        監聽滑鼠事件,根據滑鼠位置判斷落點
        '''
        if self.clicked != True:
            for i in range(self.board.size_x):
                for j in range(self.board.size_y):
                    square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow(
                        (event.y - self.chess_board_points[i][j].pixel_y), 2)
                    # 計算滑鼠的位置和點的距離
                    # 距離小於14的點

                    if square_distance <= 200:  # 合法落子位置
                        self.clicked = True
                        # 奇數次，黑落子
                        if len(self.board) % 2 == 0:
                            try:
                                self.put_black(i, j)
                            except IndexError:
                                pass
                        # 偶數次，白落子
                        elif len(self.board) % 2 == 1:
                            try:
                                self.put_white(i, j)
                            except IndexError:
                                pass

                        self.clicked = False

                        result = 0

                        # # call AI here
                        # if (self.step_record_chess_board.value[1][i][j] >= 90000):
                        #     result = 1
                        #     # release gui
                        #     self.clicked = False

                        if result == 1:
                            self.create_text(240, 475, text='the black wins')
                            # 解除左键绑定
                            self.unbind('<Button-1>')
                            # """Unbind for this widget for event SEQUENCE  the
                            #     function identified with FUNCID."""

                        elif result == 2:
                            self.create_text(240, 475, text='the white wins')
                            # 解除左键绑定
                            self.unbind('<Button-1>')


class BoardFrame(tkinter.Frame):
    def __init__(self, board: GoBoard, master=None, no_human=False):
        tkinter.Frame.__init__(self, master)
        self.board = board
        self.chess_board_label_frame = tkinter.LabelFrame(self, text="Chess Board", padx=5, pady=5)
        self.board_canvas = BoardCanvas(self.board, self.chess_board_label_frame, height=500, width=480)
        if not no_human:
            self.create_widgets()

    def create_widgets(self):
        self.board_canvas.bind('<Button-1>', self.board_canvas.click1)
        self.chess_board_label_frame.pack()
        self.board_canvas.pack()


# class App(threading.Thread):
#
#     def __init__(self,board : GoBoard):
#         threading.Thread.__init__(self)
#         self.board = board
#         self.update = None
#         self.start()
#
#     def callback(self):
#         self.root.quit()
#
#     def run(self):
#         self.root = tk.Tk()
#         self.board_frame = BoardFrame(self.board, self.root)
#         self.board.after_put = self.board_frame.board_canvas.put_stone
#         self.board_frame.pack()
#         self.root.protocol("WM_DELETE_WINDOW", self.callback)
#         label = tk.Label(self.root, text="Hello World")
#         label.pack()
#         self.root.mainloop()