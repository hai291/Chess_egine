import random


pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def random_move(valid_m):
    return random.choice(valid_m)

def findBestMove(b, valid_m):

    random.shuffle(valid_m)
    bestMove = None
    bestScore = -CHECKMATE
    turnMultiplier = 1 if b.white_to_move else -1

    for move in valid_m:
        b.make_move(move)
        score = -negamax(b, DEPTH - 1, -CHECKMATE, CHECKMATE, -turnMultiplier)
        b.undo_move()

        if score > bestScore:
            bestScore = score
            bestMove = move

    return bestMove

def negamax(b, depth, alpha, beta, turnMultiplier):


    if depth == 0 or b.checks or b.in_check:
        return turnMultiplier * scoreb(b)

    maxScore = -CHECKMATE
    valid_m = b.get_valid_move()

    for move in valid_m:
        b.make_move(move)
        score = -negamax(b, depth - 1, -beta, -alpha, -turnMultiplier)
        b.undo_move()

        if score > maxScore:
            maxScore = score
        alpha = max(alpha, score)
        if alpha >= beta: 
            break

    return maxScore

def scoreb(b):
    if b.checks:
        if b.white_to_move:
            return -CHECKMATE 
        else:
            return CHECKMATE  
    elif b.in_check:
        return STALEMATE

    score = 0
    for row in b.board:
        for square in row:
            if square != "--":  
                if square[0] == "w":
                    score += pieceScore[square[1]]
                elif square[0] == "b":
                    score -= pieceScore[square[1]]
    return score
