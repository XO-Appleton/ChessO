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
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    game = ChessOEngine.Game()
    load_images()

    valid_moves = game.get_valid_moves()
    move_made = False # Detect the frame when the move has been made

    sq_selected = ()
    player_clicks = [] # two tuples tracking the start and end pos where user moved a piece

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
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
                        valid_moves = game.get_valid_moves()
                        sq_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [sq_selected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    game.undo_move()
                    valid_moves = game.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []

        draw_game(screen,game,sq_selected)
        clock.tick(MAX_FPS) # ticks the clock at FPS
        p.display.flip()

def draw_game(screen, game, sq_selected):
    '''
    Responsible for all graphics of the current game
    '''
    draw_board(screen, sq_selected)
    draw_pieces(screen, game.board)

def draw_board(screen, sq_selected):
    '''
    Draw the sqares on the board
    '''
    colors = [p.Color('white'), p.Color('gray'), p.Color('yellow')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if sq_selected and (r,c) == sq_selected:
                color = colors[2]
            else:
                color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    '''
    Draw pieces on the board using the current game state
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--': # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                

if __name__ == '__main__':
    main()


    





