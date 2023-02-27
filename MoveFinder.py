'''
This file stores the algorithmic-approach chess bots
'''
import random

piece_value = {'K': 0, 'Q': 9, 'R': 5, 'B':3, 'N': 3, 'P':1}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def find_best_move(game, valid_moves):
    '''
    Find the best move for the current game, return a random move if there is no move available
    '''
    global best_move
    best_move = None
    turn_multiplier = 1 if game.white_to_move else -1
    random.shuffle(valid_moves)

    print(find_best_score(game, valid_moves, DEPTH,  -CHECKMATE, CHECKMATE, turn_multiplier))

    return best_move if best_move else random_move(valid_moves)

def random_move(valid_moves):
    # Return a random move that is valid
    return random.choice(valid_moves)

def find_best_score(game, valid_moves, depth, alpha, beta, turn_multiplier):
    # Find the move that would result in the highest score for the current side after the number of depth
    global best_move

    # Score the game when reaching the depth limit
    if depth == 0:
        return turn_multiplier * score_game(game)

    best_score = -CHECKMATE

    for move in valid_moves:
        game.make_move(move)
        next_moves = game.get_valid_moves()
        score = -find_best_score(game, next_moves, depth-1, -beta, -alpha, -turn_multiplier)
        game.undo_move()
        if score > best_score:
            best_score = score
            if depth == DEPTH: # next move
                best_move = move

        # pruning
        if best_score > alpha:
            alpha = best_score
        if alpha >= beta:
            break

    return best_score

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
