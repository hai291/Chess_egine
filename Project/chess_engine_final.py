class GameBoard():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['tb', 'tb', 'tb', 'tb', 'tb', 'tb', 'tb', 'tb'],
            ['tb', 'tb', 'tb', 'tb', 'tb', 'tb', 'tb', 'tb'],
            ['tb', 'tb', 'tb', 'tb', 'tb', 'tb', 'tb', 'tb'],
            ['tb', 'tb', 'tb', 'tb', 'tb', 'tb', 'tb', 'tb'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.funtion_move = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'N': self.get_knight_moves, 'K': self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.wK_location = (7, 4)
        self.bK_location = (0, 4)
        self.in_check = False
        self.pins = []
        self.checks = []
        self.qd_sq = ()
        self.wK_has_moved = False
        self.bK_has_moved = False
        self.wR_h1_has_moved = False
        self.wR_a1_has_moved = False
        self.bR_h8_has_moved = False
        self.bR_a8_has_moved = False

        
    def make_move(self, move):
        if move.piece_moved == 'wK':
            self.wK_has_moved = True
            self.wK_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.bK_has_moved = True
            self.bK_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'wR':
            if move.start_row == 7 and move.start_col == 0:
                self.wR_a1_has_moved = True
            elif move.start_row == 7 and move.start_col == 7:
                self.wR_h1_has_moved = True
        elif move.piece_moved == 'bR':
            if move.start_row == 0 and move.start_col == 0:
                self.bR_a8_has_moved = True
            elif move.start_row == 0 and move.start_col == 7:
                self.bR_h8_has_moved = True
        if move.is_castle:
            row = move.start_row
            if move.end_col == move.start_col + 2:
                self.board[row][move.start_col + 1] = self.board[row][7]  
                self.board[row][7] = 'tb'
            elif move.end_col == move.start_col - 2: 
                self.board[row][move.start_col - 1] = self.board[row][0]  
                self.board[row][0] = 'tb'

        print(move.is_qd)
        if move.is_qd:
            if self.white_to_move:
                self.board[move.start_row][move.end_col] = 'tb'
            else:
                self.board[move.start_row][move.end_col] = 'tb'
        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.qd_sq = ((move.start_row + move.end_row) // 2, move.start_col)
            print(self.qd_sq)
        else:
            self.qd_sq = ()
        self.board[move.start_row][move.start_col] = 'tb'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.pawn_promo:
            promo_piece = move.piece_moved[0] + move.promote_to
            self.board[move.end_row][move.end_col] = promo_piece
    def undo_move(self):
        if len(self.move_log) == 0:
            return
        move = self.move_log.pop()

        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wK':
            self.wK_has_moved = False
            self.wK_location = (move.start_row, move.start_col)
        elif move.piece_moved == 'bK':
            self.bK_has_moved = False
            self.bK_location = (move.start_row, move.start_col)
        elif move.piece_moved == 'wR':
            if move.start_row == 7 and move.start_col == 0:
                self.wR_a1_has_moved = False
            elif move.start_row == 7 and move.start_col == 7:
                self.wR_h1_has_moved = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0 and move.start_col == 0:
                self.bR_a8_has_moved = False
            elif move.start_row == 0 and move.start_col == 7:
                self.bR_h8_has_moved = False
        if move.is_castle:
            if move.end_col == move.start_col + 2:
                self.board[move.start_row][move.start_col] = self.board[move.start_row][move.end_col]
                self.board[move.start_row][move.end_col] = 'tb'
                self.board[move.start_row][7] = self.board[move.start_row][move.start_col + 1]
                self.board[move.start_row][move.start_col + 1] = 'tb'

            elif move.end_col == move.start_col - 2:

                self.board[move.start_row][move.start_col] = self.board[move.start_row][move.end_col]
                self.board[move.start_row][move.end_col] = 'tb'

                self.board[move.start_row][0] = self.board[move.start_row][move.start_col - 1]
                self.board[move.start_row][move.start_col - 1] = 'tb'

        elif move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.qd_sq = ()

        if move.pawn_promo:
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured


        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured
    def get_valid_move(self):
        moves = []
        valid_sqs = []
        self.in_check, self.pins, self.checks = self.check_for_pin_checks()
        if self.white_to_move:
            king_row = self.wK_location[0]
            king_col = self.wK_location[1]
        else:
            king_row = self.bK_location[0]
            king_col = self.bK_location[1]
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_possible_move()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_sq = []
                if piece_checking[1] == 'N':
                    valid_sqs = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_sq = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_sqs.append(valid_sq)
                        if valid_sq[0] == check_row and valid_sq[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_sqs:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_possible_move()
           
        return moves

    def get_possible_move(self):
        moves = []
     
        for r in range(8):
            for c in range(8):
                color = self.board[r][c][0]
                if (color == 'w' and self.white_to_move) or (color == 'b' and not self.white_to_move):
                    type = self.board[r][c][1]
                    for key in self.funtion_move.keys():
                        if type == key:
                            before_len = len(moves)
                            self.funtion_move[key](r, c, moves)
                            new_moves = moves[before_len:]
                            print(key, [m.get_chess_address() for m in new_moves])
        return moves

    def get_pawn_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                break
        if self.white_to_move:
            if self.board[r-1][c] == 'tb':
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == 'tb':
                        moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0 and self.board[r-1][c-1][0] == 'b':
                if not piece_pinned or pin_direction == (-1, -1):
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            elif c-1 >= 0 and (r-1, c-1) == self.qd_sq:
                if not piece_pinned or pin_direction == (-1, -1):
                    moves.append(Move((r, c), (r-1, c-1), self.board, is_qd=True))
            if c+1 <= 7 and self.board[r-1][c+1][0] == 'b': 
                if not piece_pinned or pin_direction == (-1, 1):
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            elif c+1 <= 7 and (r-1, c+1) == self.qd_sq:
                if not piece_pinned or pin_direction == (-1, 1):
                    moves.append(Move((r, c), (r-1, c+1), self.board, is_qd=True))
        else: 
            if self.board[r+1][c] == 'tb':
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == 'tb':
                        moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0 and self.board[r+1][c-1][0] == 'w':
                if not piece_pinned or pin_direction == (1, -1):
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            elif c-1 >= 0 and (r+1, c-1) == self.qd_sq:
                if not piece_pinned or pin_direction == (1, -1):
                    moves.append(Move((r, c), (r+1, c-1), self.board, is_qd=True))
            if c+1 <= 7 and self.board[r+1][c+1][0] == 'w':
                if not piece_pinned or pin_direction == (1, 1):
                    moves.append(Move((r, c), (r+1,c+1), self.board)) 
            elif c+1 <= 7 and (r+1, c+1) == self.qd_sq:
                if not piece_pinned or pin_direction == (1, 1):
                    moves.append(Move((r, c), (r+1, c+1), self.board, is_qd=True))    
    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == 'tb':
                            
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:break
                else:break
    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction ==(-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == 'tb':
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else:break
                else:break
    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)
    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knight_move = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_move:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
    def get_king_moves(self, r, c, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1 ,0, 1)
        ally_color = 'w' if self.white_to_move else 'b'
        enemy_color = 'b' if self.white_to_move else 'w'

        white_king_exists = any('wK' in row for row in self.board)
        black_king_exists = any('bK' in row for row in self.board)
        if not white_king_exists or not black_king_exists:
            self.check_mate = True
            return
        
        pawn_attack_squares = set()
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == enemy_color + 'P':  
                    if enemy_color == 'w':
                        if row - 1 >= 0 and col - 1 >= 0:
                            pawn_attack_squares.add((row - 1, col - 1))
                        if row - 1 >= 0 and col + 1 < 8:
                            pawn_attack_squares.add((row - 1, col + 1))
                    else:
                        if row + 1 < 8 and col - 1 >= 0:
                            pawn_attack_squares.add((row + 1, col - 1))
                        if row + 1 < 8 and col + 1 < 8:
                            pawn_attack_squares.add((row + 1, col + 1))

        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if (end_row, end_col) in pawn_attack_squares:
                        continue

                    if ally_color == 'w':
                        self.wK_location = (end_row, end_col)
                    else:
                        self.bK_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pin_checks()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    if ally_color == 'w':
                        self.wK_location = (r, c)
                    else:
                        self.bK_location = (r, c)

        if not self.in_check:
            if ally_color == 'w':
                if (not self.wK_has_moved and not self.wR_h1_has_moved and
                    self.board[7][5] == 'tb' and self.board[7][6] == 'tb'):
                    self.wK_location = (7,5)
                    in_check_f = self.check_for_pin_checks()[0]
                    self.wK_location = (7,6)
                    in_check_g = self.check_for_pin_checks()[0]
                    self.wK_location = (7,4)
                    if not in_check_f and not in_check_g:
                        moves.append(Move((7,4),(7,6),self.board,is_castle=True))
                if (not self.wK_has_moved and not self.wR_a1_has_moved and
                    self.board[7][3] == 'tb' and self.board[7][2] == 'tb' and self.board[7][1] == 'tb'):
                    self.wK_location = (7,3)
                    in_check_d = self.check_for_pin_checks()[0]
                    self.wK_location = (7,2)
                    in_check_c = self.check_for_pin_checks()[0]
                    self.wK_location = (7,4)
                    if not in_check_d and not in_check_c:
                        moves.append(Move((7,4),(7,2),self.board,is_castle=True))
            else:
                if (not self.bK_has_moved and not self.bR_h8_has_moved and
                    self.board[0][5] == 'tb' and self.board[0][6] == 'tb'):
                    self.bK_location = (0,5)
                    in_check_f = self.check_for_pin_checks()[0]
                    self.bK_location = (0,6)
                    in_check_g = self.check_for_pin_checks()[0]
                    self.bK_location = (0,4)
                    if not in_check_f and not in_check_g:
                        moves.append(Move((0,4),(0,6),self.board,is_castle=True))
 
                if (not self.bK_has_moved and not self.bR_a8_has_moved and
                    self.board[0][3] == 'tb' and self.board[0][2] == 'tb' and self.board[0][1] == 'tb'):
                    self.bK_location = (0,3)
                    in_check_d = self.check_for_pin_checks()[0]
                    self.bK_location = (0,2)
                    in_check_c = self.check_for_pin_checks()[0]
                    self.bK_location = (0,4)
                    if not in_check_d and not in_check_c:
                        moves.append(Move((0,4),(0,2),self.board,is_castle=True))
    
    def check_for_pin_checks(self):
        pins = []
        check =[]
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            allay_color = 'w'
            start_row = self.wK_location[0]
            start_col = self.wK_location[1]
        else:
            enemy_color = 'w'
            allay_color = 'b'
            start_row = self.bK_location[0]
            start_col = self.bK_location[1] 
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))     
        for j in range(len(directions)):
            d = directions[j]
            possible_pins = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == allay_color and end_piece[1] != 'K':
                        if possible_pins == ():
                            possible_pins = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]
                        if (0 <= j <=3 and type == 'R') or (4 <= j <= 7 and type =='B') or (i == 1 and type =='p' and ((enemy_color == 'w' and 6 <= j <= 7) or (enemy_color == 'b' and 4 <= j <=5))) or (type == 'Q') or (i == 1 and type == 'K'):
                            if possible_pins == ():
                                in_check = True
                                check.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pins)
                                break
                        else:break
                else:break
        knight_move = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_move:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    check.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, check    

    
class Move():
    rowToRank = {0:8, 1:7, 2:6, 3:5, 4:4, 5:3, 6:2, 7:1}
    rankToRow = {v: k for k, v in rowToRank.items()}
    colToRank = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    rankToCol = {v: k for k, v in colToRank.items()}
    def __init__(self, start_sq, end_sq, board, is_qd = False, is_castle=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.pawn_promo = False
        self.is_castle = is_castle
        if self.piece_moved == 'wP' and self.end_row == 0 or self.piece_moved == 'bP' and self.end_row == 7:
            self.pawn_promo = True 
        self.is_qd = is_qd
        self.promote_to = 'Q'
        print("Created Move", self.get_chess_address(), 
              "is_qd=", self.is_qd, "is_castle=", self.is_castle)
           

    def __eq__(self, other):
        if isinstance(other, Move):
            return (self.start_row == other.start_row and
                    self.start_col == other.start_col and
                    self.end_row == other.end_row and
                    self.end_col == other.end_col and
                    self.piece_moved == other.piece_moved)
        return False

    def __hash__(self):
        return hash((self.start_row, self.start_col, self.end_row, self.end_col, self.piece_moved))
    def get_chess_address(self):
        return self.get_address(self.start_row, self.start_col) + self.get_address(self.end_row, self.end_col)
    def get_address(self, r, c):
        return self.colToRank[c] + str(self.rowToRank[r])
