'''
This file stores the algorithmic-approach chess bots
'''
import random

piece_value = {'K': 0, 'Q': 9, 'R': 5, 'B':3, 'N': 3, 'P':1}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def find_best_move(game, valid_moves):
    '''
    Find the best move for the current game, return a random move if there is no move available
    '''
    global best_move
    best_move = None
    random.shuffle(valid_moves)

    print(minmax(game, valid_moves, DEPTH, game.white_to_move))

    return best_move if best_move else random_move(valid_moves)

def random_move(valid_moves):
    # Return a random move that is valid
    return random.choice(valid_moves)

def minmax(game, valid_moves, depth, white_to_move):
    # Find the move that would result in the highest score for the current side after the number of depth
    global best_move

    # Score the game when reaching the depth limit
    if depth == 0:
        return score_game(game)

    score_multiplier = 1 if white_to_move else -1
    best_score = -CHECKMATE

    for move in valid_moves:
        game.make_move(move)
        next_moves = game.get_valid_moves()
        score = minmax(game, next_moves, depth-1, not white_to_move)
        game.undo_move()

        if score * score_multiplier > best_score:
            best_score = score * score_multiplier
            if depth == DEPTH:
                best_move = move
    return best_score * score_multiplier

def score_game(game):
    if game.checkmated:
        score = CHECKMATE
    elif game.stalemate:
        score = STALEMATE
    score = 0
    for row in game.board:
        for piece in row:
            if piece[0] == 'w':
                score += piece_value[piece[1]]
            elif piece[0] == 'b':
                score -= piece_value[piece[1]]
    return score
