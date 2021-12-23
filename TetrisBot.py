from contextlib import nullcontext
from pyautogui import *
import pyautogui
import time
#from pynput.keyboard import Key, Controller
import random
import win32api, win32con
import numpy as np
#import cv2
import copy
import time, threading, queue
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)
#RECORD 144 lines score 155098

Held = ""
Lines = 0

def click(x,y):# clicks the mouse at x, y
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def press(x):# preses "x"
    pyautogui.PAUSE = 0.05
    pyautogui.press(x)

def moveTo(rotate, x, letter):# rotates the piece and moves it assuming left most spot is 0
    duration = 0.0
    if(letter == "I") & (x == 9):
        press('right')
        press('right')
        press('right')
        press('up')
        press('right')
        press('space')
        return
    if(letter == "I") & (x == 0):
        press('left')
        press('left')
        press('left')
        press('up')
        press('left')
        press('left')
        press('space')
        return

    for i in range(rotate):
        press('up')
        #sleep(duration)
    if(4-x >= 0):
        for i in range(4-x):
            press('left')
            #sleep(duration)
    else:
        for i in range(x-4):
            press('right')
            #sleep(duration)
    
    #sleep(duration)
    press('space')
 
def locatePiece():# Returns the next piece

    x,y = pyautogui.size()
    #if pyautogui.locateOnScreen('square.png', region=(1100,200,200,300), grayscale = True, confidence = 1)!= None:
    if pyautogui.locateOnScreen('I.png', region=(1100,430,200,100))!= None :
        return 'I'
    elif pyautogui.locateOnScreen('J.png', region=(1100,430,200,100))!= None:
        return 'J'
    elif pyautogui.locateOnScreen('L.png', region=(1100,430,200,100))!= None:
        return 'L'
    elif pyautogui.locateOnScreen('S.png', region=(1100,430,200,100))!= None:
        return 'S'
    elif pyautogui.locateOnScreen('Z.png', region=(1100,430,200,100))!= None:
        return 'Z'
    elif pyautogui.locateOnScreen('T.png', region=(1100,430,200,100))!= None:
        return 'T'
    elif pyautogui.locateOnScreen('O.png', region=(1100,430,200,100))!= None:
        return 'O'
    elif pyautogui.locateOnScreen('paused.png', region=(850,500,200,100), grayscale = True)!= None :
        return 'E'
    elif pyautogui.locateOnScreen('game_over.png', region=(850,500,200,100), grayscale = True)!= None :
        return 'E'
    else:
        return locatePiece()

def locatePieceFaster():
    screen=pyscreeze.screenshot()
    if(screen.getpixel((1206,500)) == (184,0,0)):
        return "Z"
    if(screen.getpixel((1224,492)) == (0,194,218)):
        return "I"
    if(screen.getpixel((1209,500)) == (0,119,190)):
        return "J"
    if(screen.getpixel((1220,504)) == (210, 190, 0)):
        return "O"
    if(screen.getpixel((1209,502)) == (168, 0, 203)):
        return "T"
    if(screen.getpixel((1209,501)) == (0, 197, 70)):
        return "S"
    if(screen.getpixel((1210,502)) == (203, 145, 0)):
        return "L"
    if pyautogui.locateOnScreen('paused.png', region=(850,500,200,100), grayscale = True)!= None :
        return 'E'
    elif pyautogui.locateOnScreen('game_over.png', region=(850,500,200,100), grayscale = True)!= None :
        return 'E'
    return locatePieceFaster() 
  
def getYs(board): #gets the heighest y that has a piece on it
    maxy = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] 
    for i in range(10):
        for y in reversed(range(len(board))):
            if(board[y][i] == 1):
                maxy[i] = y
                break
    return maxy

def checkBoard(Board):
    check = np.zeros((20, 10))
    screen=pyscreeze.screenshot()
    x = 1070
    y = 890
    for j in range(10):
        for i in (range(20)):
            r, g, b=screen.getpixel((x - 25*j,y - 25*i))
            if(r < 20) & (g < 20) & (b < 20):
                check[i][j] = 0
            else:
                check[i][j] = 1
    ys = getYs(Board)
    maxY = max(ys)
    for j in range(15,20):
        for i in (range(10)):
            if(check[j][i] == 1):
                check[j][i] = 0
    check = np.flip(check, 1)
    replaceRow(check)
    return (np.array_equal(Board, check), check)

def replaceRow(board, c = 0):# if a row has all 1s then it deletes it and moves everything down
    temp = np.zeros(10)
    replaced = False
    index = 0
    for i in range(len(board)):
        count = 0
        for j in range(len(board[i])):
            if board[i][j] == 0:
                break
            else:
                count+=1
        if(count == 10):
            board[i] = temp
            replaced = True
            index = i
            break
    
    if (replaced):
        for i in range(index, len(board)-1):
            board[i] = board[i+1]
        c += 1
        return 1 + replaceRow(board, c)
    return 0

def placePiece(letter, x, rotation, board, new): #places piece of letter at x and rotation r with 'new' value and returns the y of highest piece placed
    
    maxy = getYs(board)

    if(letter == 'T'):
        if(rotation == 0):#face up
            for y in range(0,20):
                if((x != 0) & (x != 9)):
                    if(y > maxy[x]) & (y > maxy[x-1]) & (y > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1)):
                            if (board[y+1][x] != 1)  & (board[y+1][x-1] != 1)  & (board[y+1][x+1] != 1) :
                                board[y][x] = new
                                board[y+1][x] = new
                                board[y][x+1] = new
                                board[y][x-1] = new
                                return y+1
        if(rotation == 1):#face right
            for y in range(0,20):
                if(x != 9):
                    if(y > maxy[x]) & (y+1 > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+1][x+1] != 1) & (board[y+2][x] != 1)):
                            board[y][x] = new
                            board[y+1][x] = new
                            board[y+1][x+1] = new
                            board[y+2][x] = new
                            return y+2
        if(rotation == 2):#face down
            for y in range(0,19):
                if((x != 0) & (x != 9)):
                    if(y > maxy[x]) & (y+1 > maxy[x-1]) & (y+1 > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y+1][x-1] != 1) & (board[y+1][x+1] != 1) & (board[y+1][x] != 1)):
                            board[y][x] = new
                            board[y+1][x-1] = new
                            board[y+1][x+1] = new
                            board[y+1][x] = new
                            return y+1
        if(rotation == 3):#face left
            for y in range(0,18):
                if(y > maxy[x]) & (y+1 > maxy[x-1]):
                    if((x != 0) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+1][x-1] != 1) & (board[y+2][x] != 1)):
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y+1][x-1] = new
                        board[y+2][x] = new
                        return y+2
    if(letter == 'L'):
        if(rotation == 0):#face up
            for y in range(0,19):
                if((x != 0) & (x != 9)):
                    if(y > maxy[x]) & (y > maxy[x-1]) & (y > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1) & (board[y+1][x+1] != 1)):
                            board[y][x] = new
                            board[y+1][x+1] = new
                            board[y][x+1] = new
                            board[y][x-1] = new
                            return y+1
        if(rotation == 1):#face right
            for y in range(0,20):
                if(x != 9):
                    if(y-1 > maxy[x]) & (y-1 > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y-1][x+1] != 1) & (board[y+1][x] != 1) & (board[y-1][x] != 1)):
                            board[y][x] = new
                            board[y-1][x+1] = new
                            board[y+1][x] = new
                            board[y-1][x] = new
                            return y+1
        if(rotation == 2):#face down
            for y in range(0,20):
                if((y != 0) & (x != 0) & (x != 9)):
                    if(y > maxy[x]) & (y-1 > maxy[x-1]) & (y > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1) & (board[y-1][x-1] != 1)):
                            board[y][x] = new
                            board[y][x-1] = new
                            board[y][x+1] = new
                            board[y-1][x-1] = new
                            return y
        if(rotation == 3):#face left
            for y in range(0, 19):
                if(y-1 > maxy[x]) & (y + 1 > maxy[x-1]):
                    if((y > 0) & (x != 0) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+1][x-1] != 1) & (board[y-1][x] != 1)):
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y+1][x-1] = new
                        board[y-1][x] = new
                        return y+1
    if(letter == 'J'):
        if(rotation == 0):#face up
            for y in range(0,19):
                if((x != 0) & (x != 9)):
                    if(y > maxy[x]) & (y > maxy[x-1]) & (y > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1) & (board[y+1][x-1] != 1)):
                            board[y][x] = new
                            board[y+1][x-1] = new
                            board[y][x+1] = new
                            board[y][x-1] = new
                            return y+1
        if(rotation == 1):#face right
            for y in range(0,20):
                if((y != 0) & (x != 9)):
                    if(y > maxy[x]) & (y+1 > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y+1][x] != 1) & (board[y-1][x] != 1) & (board[y+1][x+1] != 1)):
                            board[y][x] = new
                            board[y+1][x] = new
                            board[y-1][x] = new
                            board[y+1][x+1] = new
                            return y+1
        if(rotation == 2):#face down
            for y in range(0,20):
                if((y != 0) & (x != 0) & (x != 9)):
                    if(y > maxy[x-1]) & (y > maxy[x-1]) & (y-1 > maxy[x+1]):
                        if((x != 10) & (board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1) & (board[y-1][x+1] != 1)):
                            board[y][x] = new
                            board[y][x-1] = new
                            board[y][x+1] = new
                            board[y-1][x+1] = new
                            return y
        if(rotation == 3):#face left
            for y in range(0,19):
                if((y > 0) & (x != 9)):
                    if(y-1 > maxy[x]) & (y+1 > maxy[x-1]):
                        if((board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+1][x+1] != 1) & (board[y-1][x] != 1)):
                            board[y][x] = new
                            board[y+1][x] = new
                            board[y+1][x+1] = new
                            board[y-1][x] = new
                            return y+1
    if(letter == 'O') :
        for y in range(0,20):
            if(x != 9):
                if(y > maxy[x]) & (y > maxy[x+1]):
                    if((board[y][x] != 1) & (board[y][x+1] != 1) & (board[y+1][x] != 1) & (board[y+1][x+1] != 1)):
                        board[y][x] = new
                        board[y][x+1] = new
                        board[y+1][x] = new
                        board[y+1][x+1] = new
                        return y
    if(letter == 'I'):
        if(rotation == 0 ):#flat
            for y in range(0,20):
                if((x != 0) & (x < 8)):
                    if(y > maxy[x]) & (y > maxy[x-1]) & (y > maxy[x+1]) & (y > maxy[x+2]):
                        if (board[y][x-1] != 1) & (board[y][x] != 1) & (board[y][x+1] != 1) & (board[y][x+2] != 1):
                            board[y][x-1] = new
                            board[y][x] = new
                            board[y][x+1] = new
                            board[y][x+2] = new
                            return y
        if(rotation == 3):#vertical
            for y in range(0,19):
                if(y > maxy[x]):
                    if((y != 0) & (board[y-1][x] != 1) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+2][x] != 1)):
                        board[y-1][x] = new
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y+2][x] = new
                        return y
    if(letter == 'S') :
        if(rotation == 0 or rotation == 2):#face up
            for y in range(0,19):
                if((x != 0) & (x != 9)):
                    if(y > maxy[x]) & (y > maxy[x-1]) & (y+1 > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y][x-1] != 1) & (board[y+1][x] != 1) & (board[y+1][x+1] != 1)):
                            board[y][x] = new
                            board[y+1][x+1] = new
                            board[y+1][x] = new
                            board[y][x-1] = new
                            return y+1
        if(rotation == 1):#face right
            for y in range(0,19):
                if(x != 9):
                     if(y > maxy[x]) &  (y-1 > maxy[x+1]):
                        if((board[y][x] != 1) & (board[y+1][x] != 1) & (board[y][x+1] != 1) & (board[y-1][x+1] != 1)):
                            board[y][x] = new
                            board[y+1][x] = new
                            board[y][x+1] = new
                            board[y-1][x+1] = new
                            if(rotation == 1):
                                return y+1                
    if(letter == 'Z'):
        if(rotation == 0 or rotation == 2):#face up
            for y in range(0,19):
                if((x != 0) & (x != 9)):
                    if(y > maxy[x]) & (y+1 > maxy[x-1]) & (y > maxy[x+1]):
                        if(board[y][x] != 1) & (board[y][x+1] != 1) & (board[y+1][x] != 1) & (board[y+1][x-1] != 1):
                            board[y][x] = new
                            board[y][x+1] = new
                            board[y+1][x] = new
                            board[y+1][x-1] = new
                            return y+1
        if(rotation == 3):#face right
            for y in range(0,19):
                if((x != 0) & (x != 9)):
                    if(y > maxy[x]) & (y-1> maxy[x-1]):
                        if((x != 0) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y][x-1] != 1) & (board[y-1][x-1] != 1)):
                            board[y][x] = new
                            board[y+1][x] = new
                            board[y][x-1] = new
                            board[y-1][x-1] = new
                            return y+1
    return 20

digMode = False
def findHoles(Board, maxy, miny, min19): #finds holes **wells and overhanging edges**
    global digMode
    holes = 0
    wells = 0
    holeWeight = 5
    wellWeight = 3
    board = copy.deepcopy(Board)

    removed = replaceRow(board)
    if(removed >= 2) & (min19 > 4):
        return 0
    if(removed >= 1) & (Lines > 110):
        return 0
    if(miny < 0):
        miny = 0
    if(maxy > 20):
        maxy = 19

    for i in range(0, maxy + 4):
        for j in range(len(board[i])):
            if(board[i][j] == 0):
                if(j != 0) & (j != 9):
                    if(board[i][j-1] != 0) & (board[i][j+1] != 0) & (board[i+1][j] != 0):
                        holes += holeWeight
                        for g in range(i, maxy + 4):
                            if(board[g][j] != 0):
                                holes += 1
                    elif(board[i+1][j] != 0):
                        holes += holeWeight 
                        for g in range(i, maxy + 4):
                            if(board[g][j] != 0):
                                holes += 1
                    elif((board[i+1][j] == 0) & (board[i-1][j] == 0) & (
                    ((board[i-1][j-1] != 0) & (board[i+1][j-1] != 0) & (board[i][j-1] != 0)) | 
                    ((board[i-1][j+1] != 0) & (board[i+1][j+1] != 0) & (board[i][j+1] != 0)))):
                        wells += wellWeight
                elif(j == 0):
                    if(board[i][j+1] != 0) & (board[i+1][j] != 0):
                        holes += holeWeight 
                        for g in range(i, maxy + 4):
                            if(board[g][j] != 0):
                                holes += 1
                    elif(board[i+1][j] != 0):
                         holes += holeWeight 
                         for g in range(i, maxy + 4):
                            if(board[g][j] != 0):
                                holes += 1
                    elif((board[i+1][j] == 0) & (board[i-1][j] == 0) & ( 
                    (board[i-1][j+1] != 0) & (board[i+1][j+1] != 0) & (board[i][j+1] != 0))):
                        wells += wellWeight
                
                elif(j == 9):
                    if(board[i][j-1] != 0) & (board[i+1][j] != 0):
                        holes += holeWeight 
                        for g in range(i, maxy + 4):
                            if(board[g][j] != 0):
                                holes += 1
                    elif(board[i+1][j] != 0):
                        holes += holeWeight 
                        for g in range(i, maxy + 4):
                            if(board[g][j] != 0):
                                holes += 1
                    elif((board[i+1][j] == 0) & (board[i-1][j] == 0) & (Lines > 90) & ( 
                    (board[i-1][j-1] != 0) & (board[i+1][j-1] != 0) & (board[i][j-1] != 0))):
                        wells += wellWeight

    if(holes == 0) & (Lines < 110) & (not digMode):
        if(removed > 1) & (removed != 4):
            holes += 90
        for i in range(len(board)):
            if(board[i][9]!= 0):
                holes += 3

    if(holes == 0):
        digMode = False
    else:
        digMode = True
    
        

    return holes + wells

def findSpotHelper(letter, board):
    low = 20
    lowx = 0
    lowr = 0
    ys = getYs(board)
    maxy = max(ys)
    miny = min(ys)
    ys.pop()  
    min19 = min(ys)  

    startingHoles = findHoles(board, maxy, miny, min19)

    for r in range(4): #checks all possible spots
        for x in range(0,10):
            holes = startingHoles
            temp = placePiece(letter, x, r, board, 2)
            holes = findHoles(board, maxy, miny, min19) - holes
            
            temp += holes

            #print(temp)
            #print(board[::-1])

            if(temp < low):#find lowest y and places piece
                    low = temp
                    lowx = x
                    lowr = r
            placePiece(letter, x, r, board, 0)
    return(low, lowx, lowr)

def findSpot(letter, nextLetter, board):# finds best spot for piece
    global Held
    global Lines 

    #async_result = pool.apply_async(findSpotHelper, (letter, board)) # Use threading to speed up program

    low1 = 100
 
    if(Held == ""):
        low1, lowx1, lowr1 = findSpotHelper(nextLetter, board)
    else:
        low1, lowx1, lowr1 = findSpotHelper(Held, board)

    low, lowx, lowr = findSpotHelper(letter, board)

    if(low <= low1):
        placePiece(letter, lowx, lowr, board, 1)
        moveTo(lowr, lowx, letter)
    else:
        press("C")
        if(Held != ""):
            placePiece(Held, lowx1, lowr1, board, 1)
            moveTo(lowr1, lowx1, Held)
        Held = letter
    Lines += replaceRow(board)
    
def initialize():
    Board = np.zeros((20, 10))
    """
    Board[7] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Board[6] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Board[5] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Board[4] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Board[3] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    Board[2] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    Board[1] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    Board[0] = [1, 1, 1, 1, 1, 1, 1, 1, 1,  1]
    #indSpot("L", "L", Board)
    """
    
    startGame(Board)

    
    print(Board[::-1])
    print(Lines)

def startGame(board):
    i=0
    c = 0
    letter = ''
    times = []
    while i < 5000:
        t0 = time.time()
        if letter == 'E':
            print("Average time per piece is: ")
            print(sum(times)/len(times))
            return
        if letter == '':
            letter = locatePieceFaster()
            if letter != '':
                time.sleep(2)          
        else:   
            x, y = checkBoard(board)
            if(not x):
                if(c == 2):
                    board = copy.copy(y)
                c += 1
            else:
                c = 0
            temp = locatePieceFaster()
            count = 0
            while(letter == temp) & (count <= 15):
                temp = locatePieceFaster()
                count += 1
            findSpot(letter,temp,board)
            i+=1
            letter = temp
        times.append(time.time()-t0)
    print("Average time per piece is: ")
    print(sum(times)/len(times))
    
initialize()