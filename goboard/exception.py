class Win(Exception):
    def __init__(self, player, msg):
        msg = '%s Win, ' % player.color + msg
        self.winner = player
        super(Win, self).__init__(msg)


class Lose(Exception):
    def __init__(self, player, msg):
        msg = '%s Lose, ' % player.color + msg
        self.loser = player
        super(Lose, self).__init__(msg)


class BlackWin(Exception):
    def __init__(self, *arg):
        super(BlackWin, self).__init__(*arg)


class WhiteWin(Exception):
    def __init__(self, *arg):
        super(WhiteWin, self).__init__(*arg)


class Tie(Exception):
    def __init__(self, *arg):
        super(Tie, self).__init__(*arg)


class ColorError(Exception):
    def __init__(self, *arg):
        super(ColorError, self).__init__(*arg)
