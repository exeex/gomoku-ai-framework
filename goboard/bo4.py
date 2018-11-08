from goboard.exception import Win, Lose
from goboard.player import Human
from ai.easy_ai import Ai


class Bo4Handler:
    def __init__(self, P1, P2, **kwargs):
        self.P1 = P1
        self.P2 = P2

        self.p1 = None
        self.p2 = None

        self.p1_win = 0
        self.p2_win = 0

        # self.p1_remainingTime = 0
        # self.p2_remainingTime = 0

        self.P_str = ["p1", "p2"]
        self.game_counter = 0
        self.kwargs = kwargs

    def get_player_instance(self):
        self.game_counter = 0
        self.p1 = self.P1("black", **self.kwargs)
        self.p2 = self.P2("white", **self.kwargs)
        yield self.p1, self.p2

        self.game_counter = 1
        self.p2 = self.P2("black", **self.kwargs)
        self.p1 = self.P1("white", **self.kwargs)
        yield self.p2, self.p1

        self.game_counter = 2
        self.p1 = self.P1("black", **self.kwargs)
        self.p2 = self.P2("white", **self.kwargs)
        yield self.p1, self.p2

        self.game_counter = 3
        self.p2 = self.P2("black", **self.kwargs)
        self.p1 = self.P1("white", **self.kwargs)
        yield self.p2, self.p1

    def handle_win_lose(self, e: Exception):
        # TODO: get time remaining
        if isinstance(e, Win):
            if e.winner.color == "black":
                if self.game_counter % 2 == 0:
                    self.p1_win += 1
                else:
                    self.p2_win += 1
            elif e.winner.color == "white":
                if self.game_counter % 2 == 0:
                    self.p2_win += 1
                else:
                    self.p1_win += 1

        if isinstance(e, Lose):
            if e.loser.color == "black":
                if self.game_counter % 2 == 0:
                    self.p2_win += 1
                else:
                    self.p1_win += 1
            elif e.loser.color == "white":
                if self.game_counter % 2 == 0:
                    self.p1_win += 1
                else:
                    self.p2_win += 1

    def handle_time(self, t1,t2):
        #TODO: implement
        pass

    def print_state(self):

        print(type(self.p1), self.p1_win)
        print(type(self.p2), self.p2_win)
        return


if __name__ == '__main__':

    h = Bo4Handler(Human, Ai, board_size=(7, 7))
    print(dir(Ai))
    for b, w in h.get_player_instance():
        print(b.color)
        print(type(b))
