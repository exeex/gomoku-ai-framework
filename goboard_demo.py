from goboard import GoBoard
from goboard.battle import save_battle, load_battle

#init board
b = GoBoard()

# put black stone and white stone on the board
b.put_black(0, 0)
b.put_white(10, 11)

# if you regret, just step back
b.step_back()
b.put_white(10, 12)

# clear all board
b.clear_board()
b.put_black(0, 0)
b.put_white(10, 11)

# print all steps of the game
print(b.steps)

# print all steps of the game in dense matrix form (np.ndarray)
print(b.dense)

# save all steps of a game to json file
save_battle("gg.json", b)
c = load_battle("gg.json")