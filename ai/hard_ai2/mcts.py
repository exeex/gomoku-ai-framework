from goboard import Board, BoardInfo
from math import *
import random
from copy import deepcopy
import numpy as np
from ai.hard_ai2.normal_ai import get_possible_actions, get_weighted_actions, analysis_action, link_judge, is_5_link


class Win(Exception):
    def __init__(self, msg):
        super(Win, self).__init__(msg)


class GomokuState:
    """ A state of the game of Othello(黑白棋), i.e. the game board.
        The board is a 2D array where 0 = empty (.), 1 = player 1 (X), 2 = player 2 (O).
        In Othello players alternately place pieces on a square board - each piece played
        has to sandwich opponent pieces between the piece played and pieces already on the
        board. Sandwiched pieces are flipped.
        This implementation modifies the rules to allow variable sized square boards and
        terminates the game as soon as the player about to move cannot make a move (whereas
        the standard game allows for a pass move).
    """

    def __init__(self, board: BoardInfo):
        self.player_just_move = 2  # At the root pretend the player just moved is p2 - p1 has the first move
        self.board = board

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        return deepcopy(self)

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        x, y = move

        if self.player_just_move == 2:
            self.board.board.put_black(x, y)
            self.player_just_move = 1
        else:
            self.board.board.put_white(x, y)
            self.player_just_move = 2

        if is_5_link(self.board, move, 2 - self.player_just_move):
            raise Win("GG!")

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        pa = get_possible_actions(self.board)
        if pa != []:
            wa = get_weighted_actions(self.board, pa, 2 - self.player_just_move)
            a, w = zip(*wa)

            if len(a) > 3:
                a = a[:3]
        else:
            a = pa
        return list(a)

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        if link_judge(self.board.dense, playerjm - 1):
            return 1.0
        elif link_judge(self.board.dense, 2 - playerjm):
            return 0.0
        else:
            return 0.5

    def __repr__(self):
        return (self.board.dense[0, :] * 1 + self.board.dense[1, :] * 2).__repr__()


class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # future child nodes
        self.player_just_move = state.player_just_move  # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(
            self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)

            try:
                m = random.choice(node.untriedMoves)
                state.DoMove(m)
                node = node.AddChild(m, state)  # add child and descend tree
            except Win:
                break

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []:  # while state is non-terminal
            try:
                state.DoMove(random.choice(state.GetMoves()))
            except Win:
                break

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(
                node.player_just_move))  # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    if (verbose):
        print(rootnode.TreeToString(0))
    else:
        print(rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited


def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    # state = OthelloState(4) # uncomment to play Othello on a square board of the given size
    # state = OXOState() # uncomment to play OXO

    # 這邊可以選要玩啥遊戲
    board = Board(size=(11, 11))
    state = GomokuState(board.get_info())  # uncomment to play Nim with the given number of starting chips
    state.DoMove((5, 5))
    state.player_just_move = 1

    while (state.GetMoves() != []):
        print(str(state))
        if state.player_just_move == 1:
            m = UCT(rootstate=state, itermax=100, verbose=False)  # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate=state, itermax=30, verbose=False)
        print("Best Move: " + str(m))
        state.DoMove(m)

        if state.GetResult(state.player_just_move) == 1.0:
            print("Player " + str(state.player_just_move) + " wins!")
            break
        elif state.GetResult(state.player_just_move) == 0.0:
            print("Player " + str(3 - state.player_just_move) + " wins!")
            break
        else:
            print("Nobody wins!")


if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. 
    """
    UCTPlayGame()
