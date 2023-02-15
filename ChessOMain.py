'''
This is the main program that creates the interactive user interface and receive controls.
'''

import pygame as p
import ChessOEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    '''Initialize the global images of the pieces'''
    pieces = ['bR','bN','bB','bK','bQ','bP','wR','wN','wB','wK','wQ','wP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('./images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))


# Driver of the program. Handles inputs and updates graphics
def main():
    p.init()
    global colors
    colors = [p.Color('white'), p.Color('gray')]

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    game = ChessOEngine.Game()
    load_images()

    valid_moves = game.get_valid_moves()
    move_made = False # Detect the frame when the move has been made
    animate = False
    game_over = False

    sq_selected = ()
    player_clicks = [] # two tuples tracking the start and end pos where user moved a piece

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN and not game_over:
                location = p.mouse.get_pos() # (x,y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col): #? Could be put together with other invalid movements
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                if len(player_clicks) == 2: # After the second click
                    move = ChessOEngine.Move(player_clicks[0], player_clicks[1], game.board)
                    print(move.get_chess_notation(),move in valid_moves, game.white_to_move)
                    if move in valid_moves:
                        game.make_move(move)
                        move_made = animate = True
                        sq_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [sq_selected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # Undo a move by pressing 'z'
                    game.undo_move()
                    game_over = False
                    move_made = True
                    sq_selected = ()
                    player_clicks = []

                elif e.key == p.K_r: # Reset the game by pressing 'r'
                    game = ChessOEngine.Game()
                    valid_moves = game.get_valid_moves()
                    game_over = False
                    move_made = False 
                    animate = False
                    sq_selected = ()
                    player_clicks = []

        if move_made:
            if animate:
                animate_move(game.move_log[-1], screen, game, clock, valid_moves, sq_selected)
            move_made = animate = False
            valid_moves = game.get_valid_moves()

        draw_game(screen,game,valid_moves, sq_selected)

        if game.checkmated:
            game_over = True
            draw_text(screen, ('Black won by checkmate' if game.white_to_move else 'White won by checkmate'))

        if game.stalemate:
            game_over = True
            draw_text(screen, 'Draw by stalemate')

        clock.tick(MAX_FPS) # ticks the clock at FPS
        p.display.flip()

def draw_game(screen, game, valid_moves, sq_selected):
    '''
    Responsible for all graphics of the current game
    '''
    draw_board(screen)
    highlight_piece(screen, game, valid_moves, sq_selected)
    draw_pieces(screen, game.board)

def draw_board(screen):
    '''
    Draw the sqares on the board
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlight_piece(screen, game, valid_moves, sq_selected):
    '''Highlight the selected piece and valid moves'''
    if sq_selected:
        r, c = sq_selected
        if game.board[r][c][0] == ('w' if game.white_to_move else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    if move.piece_captured[0] == ('b' if game.white_to_move else 'w'):
                        s.fill(p.Color('red'))
                    else:
                        s.fill(p.Color('yellow'))
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))
    if game.move_log:
        move = game.move_log[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('orange'))
        screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))
        screen.blit(s, (move.start_col*SQ_SIZE, move.start_row*SQ_SIZE))

def draw_pieces(screen, board):
    '''
    Draw pieces on the board using the current game state
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--': # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_text(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, True)
    text_obj = font.render(text, 0, p.Color('Gray'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_obj.get_width()/2, HEIGHT/2 - text_obj.get_height()/2)
    screen.blit(text_obj, text_location)
    text_obj = font.render(text, 0, p.Color('Black'))
    screen.blit(text_obj, text_location.move(2,2))

def animate_move(move, screen, game, clock, valid_moves, sq_selected):
    r_diff = move.end_row - move.start_row
    c_diff = move.end_col - move.start_col
    frame_per_sq = 5
    frame_count = 3 * frame_per_sq
    for frame in range(frame_count+1):
        r, c = move.start_row + r_diff*frame/frame_count, move.start_col + c_diff*frame/frame_count
        draw_board(screen)
        draw_pieces(screen, game.board)

        # Erase the piece from the end square
        color = colors[(move.end_row+move.end_col)%2]
        end_square = p.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)

        highlight_piece(screen, game, valid_moves, sq_selected)
        # Draw captured piece
        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)

        # Draw the piece moving
        screen.blit(IMAGES[move.piece_moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()


    





