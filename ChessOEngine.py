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

        self.move_funcs = {'P': self.get_pawn_move, 'R':self.get_rook_move, 'N':self.get_knight_move,
            'B':self.get_bishop_move, 'Q':self.get_queen_move, 'K':self.get_king_move} # stores function names for moving a piece

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
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                (turn, piece) = tuple(self.board[r][c])
                if self.white_to_move and turn == 'w' or not self.white_to_move and turn == 'b':
                    self.move_funcs[piece](r, c, moves)
        return moves
        

    def get_pawn_move(self, r, c, moves):
        # white pawn moves
        if self.white_to_move: 
            if self.board[r-1][c] == '--':
                moves.append(Move((r,c), (r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0 and self.board[r-1][c-1][0] == 'b':
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 < len(self.board[r]) and self.board[r-1][c+1][0] == 'b':
                moves.append(Move((r,c),(r-1,c+1),self.board))

        # black pawn moves
        else:   
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c), (r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0 and self.board[r+1][c-1][0] == 'w':
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 < len(self.board[r]) and self.board[r+1][c+1][0] == 'w':
                moves.append(Move((r,c),(r+1,c+1),self.board))

    def get_rook_move(self, r, c, moves):
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        for d in directions:
            for i in range(1,8):
                end_r = r + d[0]*i
                end_c = c + d[1]*i
                if 0 <= end_r < len(self.board) and 0 <= end_c < len(self.board[end_r]):
                    if self.board[end_r][end_c][0] == self.board[r][c][0]:
                        break
                    elif self.board[end_r][end_c] == '--':
                        moves.append(Move((r,c),(end_r,end_c),self.board))
                    else:
                        moves.append(Move((r,c),(end_r,end_c),self.board))
                        break
                else:
                    break

    def get_knight_move(self, r, c, moves):
        directions = [(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]
        for (r_diff, c_diff) in directions:
            if r + r_diff >= 0 and r + r_diff < len(self.board) and c + c_diff >= 0 and c + c_diff < len(self.board[r+r_diff]):
                if self.board[r+r_diff][c+c_diff][0] != self.board[r][c][0]:
                    moves.append(Move((r,c),(r+r_diff,c+c_diff),self.board))

    def get_bishop_move(self, r, c, moves):
        directions = [(-1,1),(1,1),(1,-1),(-1,-1)]
        for d in directions:
            for i in range(1,8):
                end_r = r + d[0]*i
                end_c = c + d[1]*i
                if 0 <= end_r < len(self.board) and 0 <= end_c < len(self.board[end_r]):
                    if self.board[end_r][end_c][0] == self.board[r][c][0]:
                        break
                    elif self.board[end_r][end_c] == '--':
                        moves.append(Move((r,c),(end_r,end_c),self.board))
                    else:
                        moves.append(Move((r,c),(end_r,end_c),self.board))
                        break
                else:
                    break

    def get_queen_move(self, r, c, moves):
        self.get_rook_move(r, c, moves)
        self.get_bishop_move(r, c, moves)

    def get_king_move(self, r, c, moves):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if r+i >= 0 and r+i < len(self.board) and c+j >= 0 and c+j < len(self.board[r+i]):
                    if self.board[r+i][c+j][0] != self.board[r][c][0]:
                        moves.append(Move((r,c),(r+i,c+j),self.board))

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
    
    


