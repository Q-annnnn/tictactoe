import random
import string
import math

alphabet = list(string.ascii_uppercase)

class HumanPlayer():
    @staticmethod
    def parse_cords(raw):
        try:
            if raw[0].isalpha():
                return (int(raw[1:])-1, alphabet.index(raw[0]))
            elif raw[-1].isalpha():
                return (int(raw[:-1])-1, alphabet.index(raw[-1]))
            else:
                return None
        except Exception:
            return None
    
    def get_move(self, state):
        cords = self.parse_cords(input("Your turn!\nInput move: ").upper())
        while cords not in state.possible_moves():
            cords = self.parse_cords(input("Try again (eg. b3): ").upper())

        return cords


class RandomPlayer():
    def get_move(self, state):
        return random.choice(state.possible_moves())
        

class BotPlayer():
    def __init__(self, player, search_depth=3):
        self.player = player
        self.other_player = 'O' if player == 'X' else 'X'
        self.search_depth = search_depth
        self.transposition_table = {}  # Initialize the transposition table
  
    def get_move(self, state):
        best_move = None
        for depth in range(1, self.search_depth + 1):
            result = self.minimax(state, 0, -math.inf, math.inf, True)
            best_move = result['move']
            if best_move is None:
                break  # No more moves to explore at this depth

        return best_move
    def minimax(self, state, depth, alpha, beta, maximizing):
        # Check if the current state is already in the transposition table
        if state.gameover() or depth == self.search_depth:
            key = tuple(map(tuple, state.board))
            if key in self.transposition_table:
                return self.transposition_table[key]

            score = state.evaluate(self.player)
            result = {'move': None, 'score': score}
            self.transposition_table[key] = result
            return result
        # if depth == 0:
        #     moves = []
        #     best_score = -math.inf
        #     for move in state.possible_moves():
        #         state.set_move(move, self.player)
        #         check = self.minimax(state, depth+1, alpha, beta, False)

        #         state.set_move(move, ' ') # undo move
        #         check['move'] = move # attribute move to its resulting board state

        #         if check['score'] > best_score:
        #             moves = []
        #             best_score = check['score']
                
        #         moves.append(check)
                
        #         alpha = max(alpha, best_score)
        #         if best_score >= beta:
        #             break
            
        #     return random.choice(moves)
        
        if maximizing:
            best = {'move': None, 'score': -math.inf}
            for move in state.near_moves():
                state.set_move(move, self.player)
                check = self.minimax(state, depth+1, alpha, beta, False)
                state.set_move(move, ' ')

                check['move'] = move

                if check['score'] > best['score']:
                    best = check

                alpha = max(alpha, best['score'])
                if alpha >= beta:
                    break
            return best
        else:
            best = {'move': None, 'score': math.inf}
            for move in state.near_moves():
                state.set_move(move, self.other_player)
                if state.iswin(self.other_player):
                    score = -10  # Defensive move to prevent opponent from winning
                else:
                    check = self.minimax(state, depth+1, alpha, beta, True)
                    score = check['score']

                state.set_move(move, ' ')
                if score < best['score']:
                    best = {'move': move, 'score': score}

                beta = min(beta, best['score'])
                if alpha >= beta:
                    break
            return best