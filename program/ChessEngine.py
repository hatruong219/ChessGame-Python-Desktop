# bàn cờ
class GameState():
    def __init__(self):
        #board is a 8*8
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.locationOfBk = (0, 4)
        self.locationOfWk = (7, 4)
        self.checkmate = False
        self.stalemate = False

    #hàm di chuyển
    def makeMove(self, move):
        # thay thế điểm hiện tại bằng một điểm trống
        self.board[move.startRow][move.startCol] = "--"
        # thay thế điểm kết thúc bằng quân cờ ở điểm bắt đầu
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # print("pieceMoved: "+ move.pieceMoved)
        # print("pieceCapture"+ move.pieceCapture)
        # lưu lại quá trình di chuyển để có thể undo
        self.moveLog.append(move)
        # đổi người chơi
        self.whiteToMove = not self.whiteToMove
        #cập nhật tọa độ của vua
        if move.pieceMoved == "wK":
            self.locationOfWk = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.locationOfBk = (move.endRow, move.endCol)
        # Phong hậu
        if (move.pieceMoved == 'wp' and move.endRow == 0) or (move.pieceMoved == 'bp' and move.endRow == 7):
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'    

        #hàm undo
    def undoMove(self):
        # xác nhận nhật ký các bước di chuyển khác 0 => đã có sự di chuyển
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCapture
            self.whiteToMove = not self.whiteToMove
            #cập nhật tọa độ
            if move.pieceMoved == "wK":
                self.locationOfWk = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.locationOfBk = (move.startRow, move.startCol)
        self.stalemate = False
        self.checkmate = False 


    #hàm kiểm tra bước đi hợp lệ
    def getValidMoves(self):
        # Các bước đi có thể
        moves = self.getAllPossibleMoves()
        #for để đi quân giả tưởng 
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.isCheck():# nếu vua bị tấn công xóa nước đi đó
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.isCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        return moves
        
    def isCheck(self):
        if self.whiteToMove:
            return self.attackKing(self.locationOfWk[0], self.locationOfWk[1])
        else:
            return self.attackKing(self.locationOfBk[0], self.locationOfBk[1])
    def attackKing(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c :
                return True
        return False
    # Những bước đi có thể đi
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):#số hàng
            for c in range(len(self.board[r])):# số cột của mỗi hàng
                firstCharacter = self.board[r][c][0]
                if (firstCharacter == "w" and self.whiteToMove == True) or (firstCharacter == "b" and not self.whiteToMove):
                    pieceCharacter = self.board[r][c][1]
                    if pieceCharacter == "p":
                        self.getPawnMove(r, c, moves)
                    elif pieceCharacter == "R":
                        self.getRookMove(r, c, moves)
                    elif pieceCharacter == "N":
                        self.getNMove(r, c, moves)
                    elif pieceCharacter == "B":
                        self.getBMove(r, c, moves)
                    elif pieceCharacter == "Q":
                        self.getQMove(r, c, moves)
                    elif pieceCharacter == "K":
                        self.getKingMove(r, c, moves)
        return moves

    '''
=============================================================================
    '''        
    # danh sách các bước có thể di chuyển được của các quân cờ
    #Quân tốt di chuyển
    def getPawnMove(self, r, c, moves):
        if self.whiteToMove == True: # quân trắng di chuyển
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if (r == 6) and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c > 0: 
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c < 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if (r == 1) and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c > 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c < 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
    # Quân xe di chuyển
    def getRookMove(self, r, c, moves):
        direction = [(1,0), (-1,0), (0,1), (0,-1)]
        for one_direction in direction:
            for i in range (1,8):
                endRow = r + one_direction[0]*i
                endCol = c + one_direction[1]*i
                if endRow >= 0 and endRow <= 7 and endCol >=0 and endCol <=7:
                    if self.board[endRow][endCol] == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif (self.board[endRow][endCol][0]=='b' and self.whiteToMove) or (self.board[endRow][endCol][0]=='w' and not self.whiteToMove):
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    # Quân mã di chuyển
    def getNMove(self, r, c, moves):
        direction = [(-2,1), (-1,2), (1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1)]
        for one_direction in direction:
            endRow = r + one_direction[0]
            endCol = c + one_direction[1]
            if endRow >= 0 and endRow <= 7 and endCol >=0 and endCol <=7:
                if self.board[endRow][endCol] == "--":
                    moves.append(Move((r,c), (endRow, endCol), self.board))
                elif (self.board[endRow][endCol][0]=='b' and self.whiteToMove) or (self.board[endRow][endCol][0]=='w' and not self.whiteToMove):
                    moves.append(Move((r,c), (endRow, endCol), self.board))
    # quân tịnh di chuyển
    def getBMove(self, r, c, moves):
        direction = [(-1,1), (-1,-1), (1,1), (1,-1)]
        for one_direction in direction:
            for i in range (1,8):
                endRow = r + one_direction[0]*i
                endCol = c + one_direction[1]*i
                if endRow >= 0 and endRow <= 7 and endCol >=0 and endCol <=7:
                    if self.board[endRow][endCol] == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif (self.board[endRow][endCol][0]=='b' and self.whiteToMove) or (self.board[endRow][endCol][0]=='w' and not self.whiteToMove):
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    # Quân hậu di chuyển
    def getQMove(self, r, c, moves):
        direction = [(1,0), (-1,0), (0,1), (0,-1), (-1,1), (-1,-1), (1,1), (1,-1)]
        for one_direction in direction:
            for i in range (1,8):
                endRow = r + one_direction[0]*i
                endCol = c + one_direction[1]*i
                if endRow >= 0 and endRow <= 7 and endCol >=0 and endCol <=7:
                    if self.board[endRow][endCol] == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif (self.board[endRow][endCol][0]=='b' and self.whiteToMove) or (self.board[endRow][endCol][0]=='w' and not self.whiteToMove):
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    # Quân vua di chuyển
    def getKingMove(self, r, c, moves):
        direction = [(1,0), (-1,0), (0,1), (0,-1), (-1,1), (-1,-1), (1,1), (1,-1)]
        for one_direction in direction:
            endRow = r + one_direction[0]
            endCol = c + one_direction[1]
            if endRow >= 0 and endRow <= 7 and endCol >=0 and endCol <=7:
                if self.board[endRow][endCol] == "--":
                    moves.append(Move((r,c), (endRow, endCol), self.board))
                elif (self.board[endRow][endCol][0]=='b' and self.whiteToMove) or (self.board[endRow][endCol][0]=='w' and not self.whiteToMove):
                    moves.append(Move((r,c), (endRow, endCol), self.board))

# lớp di chuyển
class Move(): #(self, startPoint, endPoint, board)
    # hàm init
    def __init__(self, startPoint, endPoint, board):
        self.startRow = startPoint[0]
        self.startCol = startPoint[1]
        self.endRow = endPoint[0]
        self.endCol = endPoint[1]
        # lấy ra thông tin quân cờ ở vị trí bắt đâù vd: wp, ..
        self.pieceMoved = board[self.startRow][self.startCol]
        # thông tin quân cờ ở vị trí kết thúc
        self.pieceCapture = board[self.endRow][self.endCol]
        # vd c2 => g6 = 2367
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        # print(self.moveID)
    # in ra các bước đi trên bàn cờ VD e5->d8
    rankToRow = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowToRank = {v:k for k,v in rankToRow.items()}
    fileToCol = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colToFile = {v:k for k,v in fileToCol.items() }
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, row, col):
        return self.colToFile[col] + self.rowToRank[row]
    def __eq__(self, other):
        # xét xem other có phải là phần tử con của lớp Move hay ko
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
