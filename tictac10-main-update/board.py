import string
from copy import deepcopy

alphabet = list(string.ascii_uppercase)

class Board():
    def __init__(self, width, height, winstreak):
        self.width = width
        self.height = height
        self.winstreak = winstreak
        self.board = [ [' ' for x in range(width)] for y in range(height) ] # creates an array of empty cells with given dimensions
    
    def reset(self): # resets the board to be empty
        self.board = [ [' ' for x in range(self.width)] for y in range(self.height) ]
    
    def set_move(self, pos, player): # sets a move onto the board
        self.board[pos[1]][pos[0]] = player

    def possible_moves(self): # returns list of all empty cells' (x, y)
        moves = []

        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == ' ':
                    moves.append((x, y))

        return moves
    
    def near_moves(self):
        moves = self.possible_moves()
        impossible_moves = []
        near_moves = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell != ' ':
                    impossible_moves.append((x, y))
        min_height = min(move[0] for move in impossible_moves)
        max_height = max(move[0] for move in impossible_moves)
        min_width = min(move[1] for move in impossible_moves)
        max_width = max(move[1] for move in impossible_moves)
        for move in moves:
            if move[0] in range(min_height-2, max_height+2) and move[1] in range(min_width-2, max_width+2):
                near_moves.append((move[0], move[1]))
        return near_moves

        


    
    def gameover(self): # returns True if board is full or either player has won
        return len(self.possible_moves()) == 0 or self.iswin('X') or self.iswin('O')

    def iswin(self, player): # checks if a given player has won
        for y in range(self.height-self.winstreak+1): # check \ diagonals
            for x in range(self.width-self.winstreak+1):
                if all([self.board[y+i][x+i] == player for i in range(self.winstreak)]): # checks if all cells in a row have the player's peg
                    return True
        
        for y in range(self.winstreak-1,self.height): # check / diagonals
            for x in range(self.width-self.winstreak+1):
                if all([self.board[y-i][x+i] == player for i in range(self.winstreak)]):
                    return True
        
        for y in range(self.height): # check horizontals
            for x in range(self.width-self.winstreak+1):
                if all([self.board[y][x+i] == player for i in range(self.winstreak)]):
                    return True
        
        for y in range(self.height-self.winstreak+1): # check verticals
            for x in range(self.width):
                if all([self.board[y-i][x] == player for i in range(self.winstreak)]):
                    return True

        return False
    
    def good_move(self, player, other_player):
        score = 0
        # 4 step continuous
        for y in range(self.height-self.winstreak+2): # check \ diagonals
            for x in range(self.width-self.winstreak+2):
                if all([self.board[y+i][x+i] == player for i in range(self.winstreak-1)])\
                and not(self.board[y-1][x-1] == other_player and self.board[y+4][x+4] == other_player):
                    score+=4
        
        for y in range(self.winstreak-2,self.height): # check / diagonals
            for x in range(self.width-self.winstreak+2):
                if all([self.board[y-i][x+i] == player for i in range(self.winstreak-1)])\
                and not(self.board[y+1][x-1] == other_player and self.board[y-4][x+4] == other_player):
                    score += 4
        
        for y in range(self.height): # check horizontals
            for x in range(self.width-self.winstreak+2):
                if all([self.board[y][x+i] == player for i in range(self.winstreak-1)])\
                and not(self.board[y][x-1] == other_player and self.board[y][x+4] == other_player):
                    score += 4
        
        for y in range(self.height-self.winstreak+2): # check verticals
            for x in range(self.width):
                if all([self.board[y-i][x] == player for i in range(self.winstreak-1)])\
                and not(self.board[y+1][x] == other_player and self.board[y-4][x] == other_player):
                    score += 4
        # 3 steps without 'limit'
        for y in range(self.height-self.winstreak+3): # check \ diagonals
            for x in range(self.width-self.winstreak+3):
                if all([self.board[y+i][x+i] == player for i in range(self.winstreak-2)])\
                and not(self.board[y-1][x-1] == other_player or self.board[y+3][x+3] == other_player):
                    score+=4

        for y in range(self.winstreak-3,self.height): # check / diagonals
            for x in range(self.width-self.winstreak+3):
                if all([self.board[y-i][x+i] == player for i in range(self.winstreak-2)])\
                and not(self.board[y+1][x-1] == other_player or self.board[y-3][x+3] == other_player):
                    score += 4

        for y in range(self.height): # check horizontals
            for x in range(self.width-self.winstreak+3):
                if all([self.board[y][x+i] == player for i in range(self.winstreak-2)])\
                and not(self.board[y][x-1] == other_player or self.board[y][x+3] == other_player):
                    score += 4
        
        for y in range(self.height-self.winstreak+3): # check verticals
            for x in range(self.width):
                if all([self.board[y-i][x] == player for i in range(self.winstreak-2)])\
                and not(self.board[y+1][x] == other_player or self.board[y-3][x] == other_player):
                    score += 4
        return score


    def evaluate(self, player):
        other_player = 'O' if player == 'X' else 'X'
        score = 0
        score += self.good_move(player, other_player)
        score -= self.good_move(other_player, player)
        if self.iswin(player):
            return 10
        elif self.iswin(other_player):
            return -10
        
        else:
            return score
    
    def render(self): # displays to terminal

        print(f"  {'   '.join([str(i+1) for i in range(self.width)])}")

        for index, row in enumerate(self.board):
            print(f"{alphabet[index]} {' | '.join(row)}")
            if index + 1 < self.height:
                print("  " + '-'*(self.width*4-3))