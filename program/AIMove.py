import random
from typing import Counter

pieceScore = {"K": 10, "Q": 10, "R": 8,"B": 3, "N": 3, "p":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

def findRandomMove(vaildMoves):
    i = random.randint(0, len(vaildMoves)-1)
    return vaildMoves[i]

def findBestMove(gs, validMoves):
    global nextMove, count_temp
    nextMove = None
    count_temp = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNagaMax(gs, validMoves, DEPTH,1 if gs.whiteToMove else -1)
    #findMoveNagaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)

    moveAIbyMe(gs,DEPTH, -CHECKMATE, CHECKMATE, gs.whiteToMove)
    print("Số khả năng di chuyển đã xét: "+str(count_temp))
    return nextMove
    
def moveAIbyMe(gs, Depth, Alpha, Beta, MaxorMin):
    global nextMove, count_temp
    count_temp +=1
    if Depth == 0:
        return scoreBoard(gs)
    vaildMoves = gs.getValidMoves()
    random.shuffle(vaildMoves)

    # tìm max (tìm nước đi lợi thế cho quân trắng)
    if MaxorMin:
        maxScore = -CHECKMATE
        for move in vaildMoves:
            gs.makeMove(move)
            score = moveAIbyMe(gs,Depth-1, Alpha, Beta, False)
            if score > maxScore:
                maxScore = score
                if Depth == DEPTH:
                    nextMove = move
                    print("Max: " + move.getChessNotation(), score)
                    
            gs.undoMove()
            Alpha = max(Alpha, score)
            if Beta <= Alpha:
                break
        return maxScore
    # tìm min (tìm nước đi lợi thế cho quân đen)
    else:
        minScore = CHECKMATE
        for move in vaildMoves:
            gs.makeMove(move)
            score = moveAIbyMe(gs,Depth-1, Alpha, Beta, True)
            if score < minScore:
                minScore = score
                if Depth == DEPTH:
                    nextMove = move
                    print("Min: " + move.getChessNotation(), score)
            gs.undoMove()
            Beta = min(Beta, score)
            if Beta <= Alpha:
                break
        return minScore

    
# def findMoveNagaMax(gs, validMoves, depth, temp):
#     global nextMove,count_temp
#     count_temp += 1
#     if depth == 0:
#         return temp * scoreBoard(gs)
#     maxScore = - CHECKMATE
#     for move in validMoves:
#         gs.makeMove(move)
#         nextMoves = gs.getValidMoves()
#         score = -findMoveNagaMax(gs, nextMoves, depth-1, -temp)
#         if score > maxScore:
#             maxScore = score
#             if depth == DEPTH:
#                 nextMove = move
#         gs.undoMove()
#     return maxScore

# def findMoveNagaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, temp):
#     global nextMove, count_temp
#     count_temp +=1
#     if depth == 0:
#         return temp * scoreBoard(gs)
#     maxScore = - CHECKMATE
#     random.shuffle(validMoves)
#     for move in validMoves:
#         gs.makeMove(move)
#         nextMoves = gs.getValidMoves()
#         score = -findMoveNagaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -temp)
#         if score > maxScore:
#             maxScore = score
            
#             if depth == DEPTH:
#                 nextMove = move
#                 print(move.getChessNotation(), score)
#         gs.undoMove()
#         if maxScore > alpha:
#             alpha = maxScore
#         if alpha >= beta:
#             break
#     return maxScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE #black win
        else:
            return CHECKMATE #white win
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
            else:
                pass
    return score


# def scoreMaterial(board):
#     score = 0
    
#     for row in board:
#         for square in row:
#             if square[0] == 'w':
#                 score += pieceScore[square[1]]
#             elif square[0] == 'b':
#                 score -= pieceScore[square[1]]
#             else:
#                 pass
#     return score
