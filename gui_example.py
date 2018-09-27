from goboard import GomokuBattleHandler, GoBoard
from goboard.plot import init_plot_board, plot_board
from goboard.player import StupidAi, Human
import goboard.judge as j
import time
import tkinter
import os
from tkinter import Button
import threading
import tkinter as tk
from goboard.gui import BoardFrame

with GomokuBattleHandler(StupidAi, StupidAi, board_size=(11, 11)) as (black_round, white_round, board):
    root = tk.Tk()
    board_frame = BoardFrame(board, root)

    b = Button(root, text="black_round")
    b2 = Button(root, text="white_round")
    b.pack()
    b2.pack()
    board_frame.pack()

    root.update_idletasks()

    board.after_put = board_frame.board_canvas.put_stone

    for _ in range(11 * 11 // 2):
        try:
            step = black_round()
            print(step)
            time.sleep(0.2)
            # root.update()

            step = white_round()
            print(step)
            time.sleep(0.2)
            # root.update()

        except j.Win as e:
            print(e)
            break
        except j.Lose as e:
            print(e)
            break

    while True:
        root.update()
