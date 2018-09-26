from goboard import GoBoard, save_battle
from stupid_ai import StupidAi
import matplotlib.pyplot as plt

b = GoBoard()
a = StupidAi(b, "white")
plt.ion()
plt.show()

for _ in range(5):
    x = input("input x:\n")
    y = input("input y:\n")
    b.put_black(int(x), int(y))
    a.execute()

save_battle("gg.json", b, black_player="Human", white_player="StupidAI")
