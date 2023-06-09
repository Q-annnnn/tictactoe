# Imports
from board import Board
import player
from os import system

def main():
    board = Board(10, 10, 5)

    playerX = player.HumanPlayer()
    playerO = player.BotPlayer('O', 2)
    
    while not board.gameover():
        board.render()
        moveX = playerX.get_move(board)
        board.set_move(moveX, 'X')

        if board.gameover(): break

        board.render()
        moveO = playerO.get_move(board)
        board.set_move(moveO, 'O')
        print(f"Computer Move: {moveO}")
    
    board.render()
    if board.iswin('X'):
        print('Player X has won!')
    elif board.iswin('O'):
        print('Player O has won!')
    elif len(board.possible_moves()) == 0:
        print('Draw!')

main()
