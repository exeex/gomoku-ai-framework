class Win(Exception):
    def __init__(self, player, msg):
        msg = '%s(%s) wins, ' % (player.__class__.__name__, player.color) + msg

        super(Win, self).__init__(msg)
        self.winner = player


class Lose(Exception):
    def __init__(self, player, msg):
        msg = '%s(%s) loses, ' % (player.__class__.__name__, player.color) + msg
        super(Lose, self).__init__(msg)
        self.loser = player


class Tie(Exception):
    def __init__(self, *arg):
        super(Tie, self).__init__(*arg)


class ColorError(Exception):
    def __init__(self, *arg):
        super(ColorError, self).__init__(*arg)
