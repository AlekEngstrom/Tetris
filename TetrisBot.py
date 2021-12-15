from contextlib import nullcontext
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import numpy as np
import cv2

def click(x,y):# clicks the mouse at x, y
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def press(x):# preses "x"
    pyautogui.press(x)

def moveTo(rotate, x):# rotates the piece and moves it assuming left most spot is 0
    print(rotate)
    print(x)
    
    for i in range(rotate):
        press('up')
        sleep(.1)
    for i in range(7):
        press('left')
        
    for i in range(x-1):
        press('right')
        sleep(.1)
    sleep(.1)
    press('space')

def locatePiece():# Returns the next piece
    x,y = pyautogui.size()
    #if pyautogui.locateOnScreen('square.png', region=(1100,200,200,300), grayscale = True, confidence = 1)!= None:
    if pyautogui.locateOnScreen('O.png', region=(1100,250,200,300))!= None :
        print("I can see square!")
        return 'O'
    elif pyautogui.locateOnScreen('I.png', region=(1100,250,200,300))!= None:
        print("I can see I!")
        return 'I'
    elif pyautogui.locateOnScreen('L.png', region=(1100,250,200,300))!= None:
        print("I can see L!")
        return 'L'
    elif pyautogui.locateOnScreen('S.png', region=(1100,250,200,300))!= None:
        print("I can see S!")
        return 'S'
    elif pyautogui.locateOnScreen('T.png', region=(1100,250,200,300))!= None:
        print("I can see T!")
        return 'T'
    elif pyautogui.locateOnScreen('Z.png', region=(1100,250,200,300))!= None:
        print("I can see ReverseS!")
        return 'Z'
    elif pyautogui.locateOnScreen('J.png', region=(1100,250,200,300))!= None:
        print("I can see ReverseL!")
        return 'J'
    else:
        print("I cant see anything!")
        return ''

def replaceRow(board):# if a row has all 1s then it deletes it and moves everything down
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
        replaceRow(board)

def placePiece(letter, x, rotation, board, new): #places piece of letter at x and rotation r with 'new' value

    #gets the heighest y that has a piece on it
    maxy = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] 
    for i in range(10):
        for y in reversed(range(len(board))):
            if(board[y][i] == 1):
                maxy[i] = y
                break

    if(letter == 'T'):
        if(rotation == 0):#face up
            for y in range(0,20):
                if(y > maxy[x]) & (y > maxy[x-1]) & (y > maxy[x+1]):
                    if((x != 0) & (x != 10) & (board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1)):
                        if (board[y+1][x] != 1)  & (board[y+1][x-1] != 1)  & (board[y+1][x+1] != 1) :
                            board[y][x] = new
                            board[y+1][x] = new
                            board[y][x+1] = new
                            board[y][x-1] = new
                            return y
        if(rotation == 1):#face right
            for y in range(0,20):
                if(y > maxy[x]) & (y+1 > maxy[x+1]):
                    if((x != 10) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+1][x+1] != 1) & (board[y+2][x] != 1)):
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y+1][x+1] = new
                        board[y+2][x] = new
                        return y
        if(rotation == 2):#face down
            for y in range(0,19):
                if(y > maxy[x]) & (y+1 > maxy[x-1]) & (y+1 > maxy[x+1]):
                    if((x != 0) & (x != 10) & (board[y][x] != 1) & (board[y+1][x-1] != 1) & (board[y+1][x+1] != 1) & (board[y+1][x] != 1)):
                        board[y][x] = new
                        board[y+1][x-1] = new
                        board[y+1][x+1] = new
                        board[y+1][x] = new
                        return y
        if(rotation == 3):#face left
            for y in range(0,18):
                if(y > maxy[x]) & (y+1 > maxy[x-1]):
                    if((x != 0) & (x != 10) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+1][x-1] != 1) & (board[y+2][x] != 1)):
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y+1][x-1] = new
                        board[y+2][x] = new
                        return y
    if(letter == 'L'):
        if(rotation == 0):#face up
            for y in range(0,19):
                if(y > maxy[x]) & (y > maxy[x-1]) & (y > maxy[x+1]):
                    if((x != 0) & (x != 10) & (board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1) & (board[y+1][x+1] != 1)):
                        board[y][x] = new
                        board[y+1][x+1] = new
                        board[y][x+1] = new
                        board[y][x-1] = new
                        return y
        if(rotation == 1):#face right
            for y in range(0,20):
                if(y > maxy[x]) & (y > maxy[x+1]):
                    if((x != 10) & (board[y][x] != 1) & (board[y][x+1] != 1) & (board[y+1][x] != 1) & (board[y+2][x] != 1)):
                        board[y][x] = new
                        board[y][x+1] = new
                        board[y+1][x] = new
                        board[y+2][x] = new
                        return y
        if(rotation == 2):#face down
            for y in range(0,20):
                if(y > maxy[x]) & (y-1 > maxy[x-1]) & (y > maxy[x+1]):
                    if((y != 0) & (x != 0) & (x != 10) & (board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1) & (board[y-1][x-1] != 1)):
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
                        return y
    if(letter == 'J'):
        if(rotation == 0):#face up
            for y in range(0,19):
                if(y > maxy[x]) & (y > maxy[x-1]) & (y > maxy[x+1]):
                    if((x != 0) & (x != 10) & (board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1) & (board[y+1][x-1] != 1)):
                        board[y][x] = new
                        board[y+1][x-1] = new
                        board[y][x+1] = new
                        board[y][x-1] = new
                        return y
        if(rotation == 1):#face right
            for y in range(0,20):
                if(y > maxy[x]) & (y > maxy[x+1]):
                    if((y != 0) & (x != 10) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y-1][x] != 1) & (board[y+1][x+1] != 1)):
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y-1][x] = new
                        board[y+1][x+1] = new
                        return y
        if(rotation == 2):#face down
            for y in range(0,20):
                if(y > maxy[x-1]) & (y > maxy[x-1]) & (y-1 > maxy[x+1]):
                    if((y != 0) & (x != 0) & (x != 10) & (board[y][x] != 1) & (board[y][x-1] != 1) & (board[y][x+1] != 1) & (board[y-1][x+1] != 1)):
                        board[y][x] = new
                        board[y][x-1] = new
                        board[y][x+1] = new
                        board[y-1][x+1] = new
                        return y
        if(rotation == 3):#face left
            for y in range(0,19):
                if(y-1 > maxy[x]) & (y+1 > maxy[x+1]):
                    if((y > 0) & (x != 0) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+1][x+1] != 1) & (board[y-1][x] != 1)):
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y+1][x+1] = new
                        board[y-1][x] = new
                        return y
    if(letter == 'O') :
        for y in range(0,20):
            if(y > maxy[x]) & (y > maxy[x+1]):
                if((x != 10) & (board[y][x] != 1) & (board[y][x+1] != 1) & (board[y+1][x] != 1) & (board[y+1][x+1] != 1)):
                    board[y][x] = new
                    board[y][x+1] = new
                    board[y+1][x] = new
                    board[y+1][x+1] = new
                    return y
    if(letter == 'I'):
        if(rotation == 0 or rotation == 2):#face left
            for y in range(0,20):
                if((x != 0) & (x < 8)):
                    if(y > maxy[x]) & (y > maxy[x-1]) & (y > maxy[x+1]) & (y > maxy[x+2]):
                        if (board[y][x-1] != 1) & (board[y][x] != 1) & (board[y][x+1] != 1) & (board[y][x+2] != 1):
                            board[y][x-1] = new
                            board[y][x] = new
                            board[y][x+1] = new
                            board[y][x+2] = new
                            return y
        if(rotation == 1 | rotation == 3):#face left
            for y in range(0,19):
                if(y > maxy[x-1]):
                    if((y != 0) & (board[y-1][x] != 1) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y+2][x] != 1)):
                        board[y-1][x] = new
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y+2][x] = new
                        return y
    if(letter == 'S') :
        if(rotation == 0 or rotation == 2):#face up
            for y in range(0,19):
                if(y > maxy[x]) & (y > maxy[x-1]) & (y+1 > maxy[x+1]):
                    if((x != 0) & (x != 10) & (board[y][x] != 1) & (board[y][x-1] != 1) & (board[y+1][x] != 1) & (board[y+1][x+1] != 1)):
                        board[y][x] = new
                        board[y+1][x+1] = new
                        board[y+1][x] = new
                        board[y][x-1] = new
                        return y
        if(rotation == 1 or rotation == 3):#face right
            for y in range(0,19):
                if(y > maxy[x]) &  (y-1 > maxy[x+1]):
                    if((y != 0) & (x != 10) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y][x+1] != 1) & (board[y-1][x+1] != 1)):
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y][x+1] = new
                        board[y-1][x+1] = new
                        return y
    if(letter == 'Z'):
        if(rotation == 0 or rotation == 2):#face up
            for y in range(0,19):
                if(y > maxy[x]) & (y+1 > maxy[x-1]) & (y > maxy[x+1]):
                    if((x != 0) & (x > 9)):
                        if(board[y][x] != 1) & (board[y][x+1] != 1) & (board[y+1][x] != 1) & (board[y+1][x-1] != 1):
                            board[y][x] = new
                            board[y][x+1] = new
                            board[y+1][x] = new
                            board[y+1][x-1] = new
                            return y
        if(rotation == 1 or rotation == 3):#face right
            for y in range(0,19):
                if(y > maxy[x]) & (y-1> maxy[x-1]):
                    if((y != 0) & (x != 10) & (x != 0) & (board[y][x] != 1) & (board[y+1][x] != 1) & (board[y][x-1] != 1) & (board[y-1][x-1] != 1)):
                        board[y][x] = new
                        board[y+1][x] = new
                        board[y][x-1] = new
                        board[y-1][x-1] = new
                        return y
    return 20

def findSpot(letter, board):# finds best spot for piece
    low = 20
    lowx = 0
    lowr = 0
    for r in range(4):
        for x in range(0,9):
            
            above = False #make sure piece isnt placed below another one
            if(placePiece(letter, x, r, board, 2) < low):
                
                for y in range(placePiece(letter, x, r, board, 2)-1, 20):
                    if(board[y][x] == 1):
                        above = True
                if(not above):
                    low = placePiece(letter, x, r, board, 2)
                    lowx = x
                    lowr = r
            placePiece(letter, x, r, board, 0)
    placePiece(letter, lowx, lowr, board, 1)

    if (letter == 'O'):
        moveTo(lowr, lowx+1)
    else:
        moveTo(lowr, lowx)
    #replaceRow(board)

def initialize():
    Board = np.zeros((20, 10))
    letters = ['T','O','L','J']
    
    startGame(Board)

    #Board[2] = [1,1,1,1,1,1, 1,1,1,1]
    #findSpot('T',Board)
    
    L = 'J'
    #placePiece(L,1,0,Board, 1)
    #placePiece(L,3,1,Board, 1)
    #placePiece(L,5,2,Board, 1)
    #placePiece(L,7,3,Board, 1)
    #replaceRow(Board)
    print(Board[::-1])


     
def startGame(board):
    i=0
    letter = ''
    while i < 5:
        if letter != '':
            time.sleep(1)
            newletter = locatePiece()
            findSpot(letter,board)
            i+=1
            letter = newletter
            print(board[::-1])
        else:
            letter = locatePiece()
            if letter != '':
                time.sleep(5)


initialize()

