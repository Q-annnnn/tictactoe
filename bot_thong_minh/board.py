import string
from copy import deepcopy # Create a new copy of an object with its own unique memory space

alphabet = list(string.ascii_uppercase) # Create a list of all uppercase letters from A-Z

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
        moves = [] # Create an empty list of moves to store the positions of the empty cells

        for y, row in enumerate(self.board): # the enumerate return both the index of the row and the row itself 
            for x, cell in enumerate(row): ## the enumerate return both the index of the cell and the cell itself
                if cell == ' ':
                    moves.append((x, y)) # If the cell is empty, its position is added to the moves list

        return moves # Return list moves
    
    def near_moves(self): # find the possible moves close to the existing ones                                                           
        moves = self.possible_moves() # Get list of all possible moves (all empty cells on the board)
        impossible_moves = [] # Store the position of all filled cells
        near_moves = [] # Store the positions of the empty cells that close to the filled ones
        for y, row in enumerate(self.board): 
            for x, cell in enumerate(row):
                if cell != ' ': # If cell is filled
                    impossible_moves.append((x, y)) # Added to impossible_moves
        min_height = min(move[0] for move in impossible_moves) # Min height among all filled cells
        max_height = max(move[0] for move in impossible_moves) # Min height among all filled cells
        min_width = min(move[1] for move in impossible_moves) # Min width among all filled cells
        max_width = max(move[1] for move in impossible_moves) # Max width among all filled cells
        for move in moves: # Loop in all empty cells
            if move[0] in range(min_height-2, max_height+2) and move[1] in range(min_width-2, max_width+2): # Find empty cells in range 2
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
        for y in range(self.height - self.winstreak + 1):  # check \ diagonals
            for x in range(self.width - self.winstreak + 1):
                if all([self.board[y + i][x + i] == player for i in range(self.winstreak)]) \
                        and not (self.board[y - 1][x - 1] == other_player and self.board[y + self.winstreak][x + self.winstreak] == other_player):
                    score += 4

        for y in range(self.winstreak - 1, self.height):  # check / diagonals
            for x in range(self.width - self.winstreak + 1):
                if all([self.board[y - i][x + i] == player for i in range(self.winstreak)]) \
                        and not (self.board[y + 1][x - 1] == other_player and self.board[y - self.winstreak][x + self.winstreak] == other_player):
                    score += 4

        for y in range(self.height):  # check horizontals
            for x in range(self.width - self.winstreak + 1):
                if all([self.board[y][x + i] == player for i in range(self.winstreak)]) \
                        and not (self.board[y][x - 1] == other_player and self.board[y][x + self.winstreak] == other_player):
                    score += 4

        for y in range(self.height - self.winstreak + 1):  # check verticals
            for x in range(self.width):
                if all([self.board[y - i][x] == player for i in range(self.winstreak)]) \
                        and not (self.board[y + 1][x] == other_player and self.board[y - self.winstreak][x] == other_player):
                    score += 4

        # 3 steps without 'limit'
        for y in range(self.height - self.winstreak + 2):  # check \ diagonals
            for x in range(self.width - self.winstreak + 2):
                if all([self.board[y + i][x + i] == player for i in range(self.winstreak - 1)]) \
                        and not (self.board[y - 1][x - 1] == other_player or self.board[y + self.winstreak - 1][x + self.winstreak - 1] == other_player):
                    score += 3

        for y in range(self.winstreak - 2, self.height):  # check / diagonals
            for x in range(self.width - self.winstreak + 2):
                if all([self.board[y - i][x + i] == player for i in range(self.winstreak - 1)]) \
                        and not (self.board[y + 1][x - 1] == other_player or self.board[y - self.winstreak + 1][x + self.winstreak - 1] == other_player):
                    score += 3

        for y in range(self.height):  # check horizontals
            for x in range(self.width - self.winstreak + 2):
                if all([self.board[y][x + i] == player for i in range(self.winstreak - 1)]) \
                        and not (self.board[y][x - 1] == other_player or self.board[y][x + self.winstreak - 1] == other_player):
                    score += 3

        for y in range(self.height - self.winstreak + 2):  # check verticals
            for x in range(self.width):
                if all([self.board[y - i][x] == player for i in range(self.winstreak - 1)]) \
                        and not (self.board[y + 1][x] == other_player or self.board[y - self.winstreak + 1][x] == other_player):
                    score += 3
        
    # 2 steps without 'limit'
        for y in range(self.height - self.winstreak + 3):  # check \ diagonals
            for x in range(self.width - self.winstreak + 3):
                if all([self.board[y + i][x + i] == player for i in range(self.winstreak - 2)]) \
                        and not (self.board[y - 1][x - 1] == other_player or self.board[y + self.winstreak - 2][x + self.winstreak - 2] == other_player):
                    score += 2

        for y in range(self.winstreak - 3, self.height):  # check / diagonals
            for x in range(self.width - self.winstreak + 3):
                if all([self.board[y - i][x + i] == player for i in range(self.winstreak - 2)]) \
                        and not (self.board[y + 1][x - 1] == other_player or self.board[y - self.winstreak + 2][x + self.winstreak - 2] == other_player):
                    score += 2

        for y in range(self.height):  # check horizontals
            for x in range(self.width - self.winstreak + 3):
                if all([self.board[y][x + i] == player for i in range(self.winstreak - 2)]) \
                        and not (self.board[y][x - 1] == other_player or self.board[y][x + self.winstreak - 2] == other_player):
                    score += 2

        for y in range(self.height - self.winstreak + 3):  # check verticals
            for x in range(self.width):
                if all([self.board[y - i][x] == player for i in range(self.winstreak - 2)]) \
                        and not (self.board[y + 1][x] == other_player or self.board[y - self.winstreak + 2][x] == other_player):
                    score += 2
        return score




    def evaluate(self, player):
        other_player = 'O' if player == 'X' else 'X'
        score = 0
        score += self.good_move(player, other_player)*0.5
        score -= self.good_move(other_player, player)*2
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