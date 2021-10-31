import pygame as pygame
from pygame import draw
from pygame import font
import program.ChessEngine as ChessEngine
import program.AIMove as AIMove

# import ChessEngine as ChessEngine
# import AIMove as AIMove



WIDTH = HEIGHT = 512
WIDTH_MOVELOG = 250
HEIGHT_MOVELOG = 512
DIMENSION = 8 # kích thước bàn cờ là 8*8
SQ_SIZE = HEIGHT / DIMENSION
MAX_FPS = 15
IMAGES = {}

class ChessMainClass():
    # hàm xử lý người dùng và đồ họa
    def __init__(self, playerOne, playerTwo):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH + WIDTH_MOVELOG, HEIGHT))
        clock = pygame.time.Clock()
        screen.fill(pygame.Color("white"))
        gs = ChessEngine.GameState()

        checkHaveAI = False
        if (playerOne == False) or (playerTwo == False):
            checkHaveAI = True
        # nước đi hợp lệ  
        validMoves = gs.getValidMoves()
        # nước đi được thực hiện
        moveMade = False 

        print(gs.board)
        self.loadImg()
        running = True
        # ô vuông được chọn
        squareChoose = () # hiện tại là không có ô vuông nào. Trả về có thể là (x,y)
        playerCLicks = [] # danh sách các vị trí mà người chơi click [(6,6), (8,8)]
        gameOver = False
        # Player
        # playerOne = True # người chơi đi quân trắng và AI đi quân đen
        # playerTwo = False # ngược lại trên

        while running:
            humanPlay = False
            if (gs.whiteToMove==True and playerOne == True) or (gs.whiteToMove==False and playerTwo == True):
                humanPlay = True 
            # lắng nghe sự kiện trong pygame
            for e in pygame.event.get():
                # thoát game
                if e.type == pygame.QUIT:
                    running = False
                # sự kiện click chuột
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    # kiểm tra game dừng hay chưa
                    if gameOver == False and humanPlay == True:
                        #lấy tọa độ của điểm chuột click => lấy được vị trí ô vuông vừa chọn (col, row)
                        coordinates = pygame.mouse.get_pos() # trả về tọa độ (x,y) vị tí trỏ chuột
                        col = int(coordinates[0]/SQ_SIZE)
                        row = int(coordinates[1]/SQ_SIZE)
                        # kiểm tra xem vị trí hiện tại có phải là vị trí đang được chọn hay không
                        if squareChoose == (row, col) or col >= 8:
                            # thực hiện việc bỏ chọn
                            squareChoose = ()
                            playerCLicks = []
                        else:
                            # thực hiện cập nhật vị trí
                            squareChoose = (row, col)
                            playerCLicks.append(squareChoose)
                        # Thực hiện xử lý di chuyển quân cờ
                        if len(playerCLicks) == 2:
                            move = ChessEngine.Move(playerCLicks[0], playerCLicks[1], gs.board)                    
                            # kiểm tra bước đi có phải là bước đi hợp lệ hay ko 
                            for i in range(len(validMoves)):
                                # so sánh bằng phương pháp ghi đè
                                if move == validMoves[i]: 
                                    gs.makeMove(move)
                                    moveMade = True
                                    print(move.getChessNotation())
                                    # đặt lại ô được chọn là rỗng
                                    squareChoose = ()
                                    playerCLicks = []
                            if moveMade== False:
                                playerCLicks = [squareChoose]
                # key handlers
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_z:
                        if checkHaveAI == True:
                            gs.undoMove()
                            moveMade = True
                            gameOver = False
                        gs.undoMove()
                        moveMade = True
                        gameOver = False
                    if e.key == pygame.K_a:
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        moveMade = False
                        gameOver = False
                        squareChoose = ()
                        playerCLicks = []

            # AI
            if gameOver == False and humanPlay == False:
                AI_move = AIMove.findBestMove(gs, validMoves)
                if AI_move == None:
                    AI_move = AIMove.findRandomMove(validMoves)
                gs.makeMove(AI_move)
                moveMade = True

            # đặt lại các bước đi hợp lệ 
            if moveMade == True:
                validMoves = gs.getValidMoves()
                moveMade = False
            self.drawGameState(screen, gs, validMoves, squareChoose)

            if gs.checkmate == True:
                gameOver = True
                if gs.whiteToMove:
                    self.drawEndGameText(screen, "Black wins")
                else:
                    self.drawEndGameText(screen, "White wins")
            elif gs.stalemate == True:
                gameOver = True
                self.drawEndGameText(screen, "Stalemate")
            clock.tick(MAX_FPS)
            pygame.display.flip()


    def loadImg(self):
        list_chess = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for one_chess in list_chess:
            # gán hình ảnh vào mảng và thực hiện transform (chuyển đổi) 
            # hình ảnh thành kích thước phù hợp : SQ_SIZE + 512/8
            IMAGES[one_chess] = pygame.transform.scale(pygame.image.load("program/images/" +one_chess+ ".png"), (int(SQ_SIZE),int(SQ_SIZE)) )
            #IMAGES[one_chess] = pygame.image.load("program/images/"+one_chess+".png")
    
    '''
    Vẽ bàn cờ và các trạng thái trên bàn cờ
    '''
    def drawGameState(self,screen, gs, validMoves, squareChoose):
        self.drawBroad(screen)
        self.drawPieces(screen, gs.board)
        self.choosePieces(screen, gs, validMoves, squareChoose)
        self.drawMoveLog(screen, gs)

    '''
    Vẽ bàn cờ
    '''
    # vẽ bảng 8*8 và tô màu
    def drawBroad(self,screen):
        # 2 màu chính là trắng và xám
        colors = [pygame.Color('white'), pygame.Color("gray")]
        # duyệt vòng lặp tiến hành vẽ và tô màu
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[((r+c)%2)]
                pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    '''
    Vẽ các quân cờ lên bàn cờ
    '''
    def drawPieces(self,screen, board):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = board[row][col]
                if piece != '--':
                    screen.blit(IMAGES[piece], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    '''
    In đậm ô được chọn
    '''
    def choosePieces(self,screen, gs, validMoves, squareChoose):
        if squareChoose != ():
            row = squareChoose[0]
            col = squareChoose[1]
            if gs.whiteToMove == True:
                if gs.board[row][col][0] == "w":
                    s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                    s.set_alpha(100)
                    s.fill(pygame.Color('blue'))
                    screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
                    # tô màu các bước đi có thể
                    s.fill(pygame.Color('yellow'))
                    for moves in validMoves:
                        if moves.startRow == row and moves.startCol == col:
                            screen.blit(s, (moves.endCol*SQ_SIZE, moves.endRow*SQ_SIZE))
            else:
                if gs.board[row][col][0] == "b":
                    s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                    s.set_alpha(100)
                    s.fill(pygame.Color('blue'))
                    screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
                    # tô màu các bước đi có thể
                    s.fill(pygame.Color('yellow'))
                    for moves in validMoves:
                        if moves.startRow == row and moves.startCol == col:
                            screen.blit(s, (moves.endCol*SQ_SIZE, moves.endRow*SQ_SIZE))

    '''
    Hiển thị thông tin thua hoặc thắng
    '''
    def drawEndGameText(self,screen, text):
        font = pygame.font.SysFont("Helvitca", 32, True, False)
        textobj = font.render(text, 0, pygame.Color('Black'))
        textLocation = pygame.Rect(0,0,WIDTH, HEIGHT).move(WIDTH/2- textobj.get_width()/2, HEIGHT/2- textobj.get_height()/2)
        screen.blit(textobj, textLocation)
    '''
    Move Log
    '''
    def drawMoveLog(self,screen, gs):
        font = pygame.font.SysFont("aria", 20, True, False)
        moveLogRect = pygame.Rect(WIDTH, 0, WIDTH_MOVELOG, HEIGHT_MOVELOG)
        pygame.draw.rect(screen, pygame.Color('Black'), moveLogRect)
        moveLog = gs.moveLog
        moveText = []
        for i in range(0, len(moveLog), 2):
            moveString = str(int(i/2) +1) + ". " + moveLog[i].getChessNotation() + " ==> "
            if i+1 < len(moveLog):
                moveString += moveLog[i+1].getChessNotation()
            moveText.append(moveString)

        text_X = 5
        text_Y = 5
        for i in range(len(moveText)):
            text = moveText[i]
            textObj = font.render(text, True, pygame.Color('white'))
            textLocation = moveLogRect.move(text_X, text_Y)
            screen.blit(textObj, textLocation)
            text_Y += textObj.get_height() + 5
# if __name__ == "__main__":
#     ChessMainClass()