'''
This is the game engine for ChessO which initiates the chess game as well as monitoring the game.
'''

class Game:
    '''Stores the board and moves of the current game'''
    def __init__(self) -> None:
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]
        self.white_to_move = True
        self.move_log = [] # list of Moves

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if self.move_log:
            move = self.move_log.pop()
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        return self.get_all_moves()

    def get_all_moves(self):
        moves = [Move((6,4),(4,4),self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                (turn, piece) = tuple(self.board[r][c])
                if self.white_to_move and turn == 'w':
                    if piece == 'P':
                        moves.append(self.get_pawn_move(r, c))
                    elif piece == 'R':
                        moves.append(self.get_rook_move(r, c))
        return moves
        

    def get_pawn_move(self, r, c):
        pass

    def get_rook_move(self, r, c):
        pass

class Move:
    '''Stores the information about a single move'''

    ranks2rows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rows2ranks = {v:k for k, v in ranks2rows.items()} 
    files2cols = {'h':7, 'g':6, 'f':5, 'e':4, 'd':3, 'c':2, 'b':1, 'a':0}
    cols2files = {v:k for k, v in files2cols.items()} 

    def __init__(self, start_sq, end_sq, board) -> None:
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.get_chess_notation() == other.get_chess_notation()

    def get_chess_notation(self):
        return self.get_rank_notation(self.start_row, self.start_col) + self.get_rank_notation(self.end_row, self.end_col)
    
    def get_rank_notation(self, r, c):
        return self.cols2files[c] + self.rows2ranks[r]
    
    


