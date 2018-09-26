from goboard import GoBoard
from stupid_ai import StupidAi
import matplotlib.pyplot as plt

b = GoBoard()
a = StupidAi(b, "white")
plt.ion()
plt.show()

while True:
    x = input("input x:\n")
    y = input("input y:\n")
    b.put_black(int(x), int(y))
    a.execute()
