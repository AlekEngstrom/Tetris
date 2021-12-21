from contextlib import nullcontext
from pyautogui import *
import pyautogui
import time
from pynput.keyboard import Key, Controller
import random
import win32api, win32con
import numpy as np
import cv2
import copy
import time, threading, queue
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)
#RECORD 96 lines score 99528

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
    t0 = time.time()
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

def getYs(board): #gets the heighest y that has a piece on it
    maxy = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] 
    for i in range(10):
        for y in reversed(range(len(board))):
            if(board[y][i] == 1):
                maxy[i] = y
                break
    return maxy

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

def findHoles(Board, maxy, miny, min19): #finds holes **wells and overhanging edges**
    holes = 0
    holeWeight = 5
    wellWeight = 3
    board = copy.deepcopy(Board)

    removed = replaceRow(board)
    if(removed >= 2) & (min19 > 4):
        return 0
    if(removed >= 1) & (Lines > 90):
        return 0
    if(miny < 0):
        miny = 0

    for i in range(miny, maxy + 4):
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
                        holes += wellWeight
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
                        holes += wellWeight
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

    if(holes == 0) & (Lines < 90):
        for i in range(len(board)):
            if(board[i][9]!= 0):
                holes += 3

    return holes

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

def findSpot(letter,nextLetter, board):# finds best spot for piece
    global Held
    global Lines 

    async_result = pool.apply_async(findSpotHelper, (letter, board)) # Use threading to speed up program

    low1 = 100
 
    if(Held == ""):
        low1, lowx1, lowr1 = findSpotHelper(nextLetter, board)
    else:
        low1, lowx1, lowr1 = findSpotHelper(Held, board)

    low, lowx, lowr = async_result.get()

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
    letter = ''
    while i < 3000:
        if letter == 'E':
            return
        if letter == '':
            letter = locatePiece()
            if letter != '':
                time.sleep(2)
            
        else:
            temp = locatePiece()
            if(letter == temp):
                time.sleep(.5)
                temp = locatePiece()

            findSpot(letter,temp,board)
            i+=1
            letter = temp
            #print(board[::-1])


initialize()