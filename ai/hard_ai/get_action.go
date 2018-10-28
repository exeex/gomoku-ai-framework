/*
	nim exercies the mcts algorithm for the game of nim.
*/
package main

import "C"
import (
	"go-mcts/games/gomoku"
	"go-mcts/mcts"
	"fmt"
	"unsafe"
)
//export Sum
func Sum(a int, b int) int {
	return a + b
}

//export GetActionWrap
func GetActionWrap(boardRaw *C.char, sizeX C.int, sizeY C.int, playerId C.int) int{
	//state := gomoku.NewGomokuState(*boardSizeX, *boardSizeY, playerIds)
	slice := (*[1 << 30]uint8)(unsafe.Pointer(boardRaw))[:sizeX*sizeY:sizeX*sizeY]
	var playerA uint64 = 1 // Goes first.
	var playerB uint64 = 2 // Goes second.
	var playerIds []uint64 = []uint64{playerA, playerB}
	state :=gomoku.NewGomokuState(int(sizeX),int(sizeY),playerIds)
	state.ActivePlayerId = uint64(playerId)

	b := make(gomoku.BoardSlice, int(sizeX)*int(sizeY))
	for i := 0; i < int(sizeX)*int(sizeY); i++{
		b[i] = gomoku.Stone(slice[i])
	}

	state.Board = b

	move := getAction(state)
	gomokuMove := move.(*gomoku.GomokuMove)

	return gomokuMove.Pos

}
//export Hello
func Hello(x int) int{

	return x
}


func getAction(state *gomoku.GomokuState) mcts.Move{

	//var ucbC *float64 = flag.Float64("ucbc", 1.0, "the constant biasing exploitation vs exploration")
	//flag.Parse()

	ucbC := 1.0

	// How many iterations do players take when considering moves?
	var iterations uint = 1000

	// How many simulations do players make when valuing the new moves?
	var simulations uint = 100

	// Create the initial games state.


	var move mcts.Move
	// What is the next active player's move?
	move = mcts.Uct(state, iterations, simulations, ucbC, state.ActivePlayerId, scoreGomoku)
	state.MakeMove(move)
	fmt.Println(move)

	// Report the action taken.
	var gomokuMove *gomoku.GomokuMove = move.(*gomoku.GomokuMove)
	gomokuMove.Log()
	state.Log()

	return move
}




// scoreNim scores the games state from a player's perspective, returning 0.0 (lost), 0.5 (in progress), 1.0 (won)
func scoreGomoku(playerId uint64, state mcts.GameState) float64 {
	// Is the games over or still in progress?
	var moves []mcts.Move = state.AvailableMoves()
	if len(moves) > 0 {
		// The games is still in progress.
		return 0.5 // Consider it a neutral state (0.0-1.0)
	}

	// The games is over.

	// Convert the state into a form we can use.

	var gomokuState *gomoku.GomokuState = state.(*gomoku.GomokuState)

	if gomokuState.ActivePlayerId == gomokuState.BlackPlayer && gomokuState.Is_black_win() {
		return 1.0
	} else if gomokuState.ActivePlayerId == gomokuState.WhitePlayer && gomokuState.Is_white_win() {
		return 1.0
	} else {
		return 0.0
	}

	// We didn't win.

}

func main() {
	// Need a main function to make CGO compile package as C shared library
}