from goboard import Board
from goboard.battle import save_game, load_game

# init board
b = Board()

# put black stone and white stone on the board
b.put_black(0, 0)
b.put_white(10, 11)

# print all steps of the game
print(b.steps)

# print all steps of the game in dense matrix form (np.ndarray)
print(b.dense)

# get board_info
b2 = b.get_info()

print(b2.steps)
print(b2.dense)


# save all steps of a game to json file
save_game("gg.json", b)
c = load_game("gg.json")
