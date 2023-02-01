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

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_game(screen,game)
        clock.tick(MAX_FPS) # ticks the clock at FPS
        p.display.flip()

def draw_game(screen, game):
    '''
    Responsible for all graphics of the current game
    '''
    draw_board(screen)
    draw_pieces(screen, game.board)

def draw_board(screen):
    '''
    Draw the sqares on the board
    '''
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
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


    





