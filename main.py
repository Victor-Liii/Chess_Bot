
import pygame
import chess
import chess.variant
import chess.engine
from engine import *
import numpy

b = chess.Board()
board = []


images = []
UNIT = 60
def load():
    global images
    images.append(pygame.image.load('Chess_rlt60.png')) #rook, knight, bishop queen, king, prawn
    images.append(pygame.image.load('Chess_nlt60.png'))
    images.append(pygame.image.load('Chess_blt60.png'))
    images.append(pygame.image.load('Chess_qlt60.png'))
    images.append(pygame.image.load('Chess_klt60.png'))
    images.append(pygame.image.load('Chess_plt60.png'))
    images.append(pygame.image.load('Chess_rdt60.png')) #rook, knight, bishop queen, king, prawn
    images.append(pygame.image.load('Chess_ndt60.png'))
    images.append(pygame.image.load('Chess_bdt60.png'))
    images.append(pygame.image.load('Chess_qdt60.png'))
    images.append(pygame.image.load('Chess_kdt60.png'))
    images.append(pygame.image.load('Chess_pdt60.png'))
    images.append(pygame.image.load("Chessboard480.svg.png"))

def main():
    global b
    pygame.init()
    run = True
    screen = pygame.display.set_mode((480,480))
    
    pygame.display.flip()

    select = False
    move = ""
    while not b.is_game_over():
        pygame.time.delay(50) ##stops cpu dying
        screen.blit(images[-1],(0,0)) # board image 
        draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            ai_move = get_ai_move(b,1,"white")
            b.push(ai_move)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[0]//UNIT
                y = pos[1]//UNIT

                if select == True:
                    move += chr(ord("a")+x)+str(8-y)
                    try:
                        m = chess.Move.from_uci(move)
                    except:
                        m = ""
                    if m in b.legal_moves:
                        b.push(m)
                    else:
                        print("ILLEGAL MOVE")

                    move = ""
                    select = False

                elif board[y][x] != " ":
                    move += chr(ord("a")+x)+str(8-y)
                    select = True
                    
                
                

            


            if event.type == pygame.QUIT:
                pygame.quit()
        

def val(c):
    if c == "R" :
        return 0
    elif c =="N":
        return 1
    elif c =="B":
        return 2
    elif c =="Q":
        return 3
    elif c =="K":
        return 4
    elif c =="P":
        return 5
    elif c =="r":
        return 6
    elif c =="n":
        return 7
    elif c =="b":
        return 8
    elif c =="q":
        return 9
    elif c =="k":
        return 10
    elif c =="p":
        return 11
    else:
        return -1



def draw(screen):
    global images,b,board
    board = list(b.board_fen())
    for i in range(len(board)):
        if(board[i]>"0" and board[i]<= "8"):
            board[i] = " "*int(board[i])

    board = "".join(board)
    board = board.split("/")
    for i in range(len(board)):
        board[i] = list(board[i])
    
    for i in range(len(board)):
        for j in range(8):
            a = val(board[i][j])
            if a != -1:
                screen.blit(images[a],(j*UNIT,i*UNIT))



    
if __name__=="__main__":
    load()
    main()