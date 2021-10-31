# def findBestMove(gs, vaildMoves):
    # bestMove = None
    # # biến để xác định tham số âm hay dương biến đổi theo lượt chơi
    # tempValue = -1
    # if (gs.whiteToMove):
    #     tempValue = 1
    # opponentsMinMaxScore = CHECKMATE
    # bestPlayerMove = None
    # # xáo trộn các giá trị có thể đi được
    # random.shuffle(vaildMoves)
    # for playerMove in vaildMoves:
    #     gs.makeMove(playerMove)
    #     opponentsMoves = gs.getValidMoves()
    #     if gs.stalemate:
    #         opponentsMaxScore = STALEMATE
    #     elif gs.checkmate:
    #         opponentsMaxScore = -CHECKMATE
    #     else:
    #         opponentsMaxScore = -CHECKMATE
    #         for opponentsMove in opponentsMoves:
    #             gs.makeMove(opponentsMove)
    #             gs.getValidMoves() 
    #             if gs.checkmate:
    #                 score = CHECKMATE
    #             elif gs.stalemate:
    #                 score = STALEMATE
    #             else:
    #                 score = scoreMaterial(gs.board) * (-tempValue)
    #             if(score > opponentsMaxScore):
    #                 opponentsMaxScore = score
    #             gs.undoMove()
    #         if opponentsMaxScore < opponentsMinMaxScore:
    #             opponentsMinMaxScore = opponentsMaxScore
    #             bestPlayerMove = playerMove
    #         gs.undoMove()
    # return bestPlayerMove







# def findMoveMinMax(gs, validMoves, depth, whiteToMove):
#     #biến toàn cục
#     global nextMove
#     if depth == 0:
#         return scoreMaterial(gs.board)
#     if whiteToMove == True:
#         # điểm số bắt đầu ở mức rất thấp -1000
#         maxScore = -CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             score = findMoveMinMax(gs, nextMoves, depth-1, False)
#             if score > maxScore:
#                 maxScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#         return maxScore
#     else:
#         minScore = CHECKMATE
#         for move in validMoves:
#             gs.makeMove(move)
#             nextMoves = gs.getValidMoves()
#             score = findMoveMinMax(gs, nextMoves, depth-1, True)
#             if minScore < score:
#                 minScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gs.undoMove()
#         return minScore



'''==================================='''
# def findMoveNagaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, temp):
    # global nextMove
    # if depth == 0:
    #     return temp * scoreBoard(gs) 
    # maxScore = - CHECKMATE
    # for move in validMoves:
    #     gs.makeMove(move)
    #     nextMoves = gs.getValidMoves()
    #     score = -findMoveNagaMaxAlphaBeta(gs, nextMoves, -beta, -alpha, depth-1, -temp)
    #     if score > maxScore:
    #         maxScore = score
    #         if depth == DEPTH:
    #             nextMove = move
    #         gs.undoMove()
    #     return maxScore

    # for move in validMoves:
    #     gs.makeMove(move)
    #     nextMoves = gs.getValidMoves()
    #     score = -findMoveNagaMaxAlphaBeta(gs, nextMoves, -beta, -alpha, depth-1, -temp)
    #     if score > maxScore:
    #         maxScore = score
    #         if depth == DEPTH:
    #             nextMove = move
    #     gs.undoMove()
    #     if maxScore > alpha: #cắt tỉa
    #         alpha = maxScore
    #     if alpha >= beta:
    #         break
    # return maxScore



