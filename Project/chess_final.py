import pygame as p
from chess_engine_final import GameBoard, Move
from AI_chess_final import findBestMove

WIDTH = HEIGHT = 512
dimension = 8
SQ_size = WIDTH // dimension
max_fps = 24
images = {}
def choose_promotion(screen, color):
    options = ['Q', 'R', 'B', 'N']
    piece_images = [images[color + o] for o in options]
    rects = []
    y = HEIGHT // 2 - SQ_size // 2
    x_start = WIDTH // 2 - 2 * SQ_size
    screen.fill(p.Color('grey'))

    for i, img in enumerate(piece_images):
        x = x_start + i * SQ_size * 1.2
        rect = p.Rect(x, y, SQ_size, SQ_size)
        rects.append(rect)
        p.draw.rect(screen, p.Color('black'), rect, 2)
        screen.blit(img, rect)

    p.display.flip()

    while True:
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(pos):
                        return options[i] 
            elif e.type == p.QUIT:
                p.quit()
                exit()
def draw_text(screen, text, font):
    text_object = font.render(text, True, p.Color('red'))
    screen.blit(text_object, (WIDTH//2 - text_object.get_width()//2, HEIGHT//2 - text_object.get_height()//2))
def load_images():
    piece = ['wP','wR','wN','wB','wQ','wK','bP','bR','bN','bB','bQ','bK']
    for term in piece:
        images[term] = p.transform.scale(p.image.load('./images/' + term + '.png'), (SQ_size, SQ_size))
    print(images['wP'])
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    font = p.font.SysFont('Arial', 32, True, False)

    b = GameBoard()
    load_images()
    valid_m = b.get_valid_move()

    sq_selected = ()
    player_click = []
    move_made = False
    running = True
    game_over = False 
    player_white = True
    player_black = False
    while running:
        human_turn = (b.white_to_move and player_white) or (not b.white_to_move and player_black)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:  
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_size
                    row = location[1] // SQ_size
                    if sq_selected == (row, col):
                        sq_selected = ()
                        player_click = []
                    else:
                        sq_selected = (row, col)
                        player_click.append(sq_selected)
                    if len(player_click) == 2:
                        start_sq, end_sq = player_click
                        temp_move = Move(start_sq, end_sq, b.board)
                        move = None
                        for vm in valid_m:
                            if temp_move == vm:
                                move = vm
                                break
                        if move is not None:
                            if move.pawn_promo:
                                move.promote_to = choose_promotion(screen, move.piece_moved[0])
                            b.make_move(move)
                            move_made = True
                            sq_selected = ()
                            player_click = []
                        else:
                            player_click = [sq_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    if player_black and player_white:
                        if len(b.move_log) >= 1:
                            b.undo_move()
                        move_made = True
                        game_over = False  
                    else:
                        if len(b.move_log) >= 1:
                            b.undo_move()
                        if len(b.move_log) >= 1:
                            b.undo_move()
                        move_made = True
                        game_over = False
                elif e.key == p.K_r:
                    b = GameBoard()
                    move_made = True
                    game_over = False
        if not game_over and not human_turn:
            AI_move = findBestMove(b, valid_m)
            if AI_move is not None:
                b.make_move(AI_move)
            move_made = True
        if move_made:
            valid_m = b.get_valid_move()
            move_made = False

        draw_game(screen, b, valid_m, sq_selected)

        if len(valid_m) == 0 and not game_over:
            game_over = True

            white_king_exists = any('wK' in row for row in b.board)
            black_king_exists = any('bK' in row for row in b.board)


            if not white_king_exists:
                end_text = "Checkmate! Black wins!"
            elif not black_king_exists:
                end_text = "Checkmate! White wins!"
            elif b.in_check:
               
                if b.white_to_move:
                    end_text = "Checkmate! Black wins!"
                else:
                    end_text = "Checkmate! White wins!"
            else:
   
                end_text = "Draw!"

            draw_text(screen, end_text, font)

        if game_over:
            draw_text(screen, end_text, font)

        clock.tick(max_fps)
        p.display.flip()

def high_light(screen, b, valid_m, sq_selected):
        if sq_selected != ():
            r, c = sq_selected
            if b.white_to_move:
                color_sq = 'w'
            else:
                color_sq = 'b'
            if b.board[r][c][0] == color_sq:
                s = p.Surface((SQ_size, SQ_size))
                s.set_alpha(100)
                s.fill(p.Color('blue'))
                screen.blit(s, (c*SQ_size, r*SQ_size))
                s.fill(p.Color('yellow'))
                for move in valid_m:
                    if move.start_row == r and move.start_col == c:
                        screen.blit(s, (move.end_col * SQ_size, move.end_row * SQ_size))
def draw_game(screen, board, valid_m, sq_selec):
    drawBoard(screen, board)
    high_light(screen, board, valid_m, sq_selec)
def drawBoard(screen, board):
    colors = [p.Color('white'), p.Color('darkgrey')]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_size, r*SQ_size, SQ_size, SQ_size))
            piece = board.board[r][c]
            if piece != 'tb':
                screen.blit(images[piece], p.Rect(c*SQ_size, r*SQ_size, SQ_size, SQ_size))

main()