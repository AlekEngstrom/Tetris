from contextlib import nullcontext
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import numpy as np
import cv2
#RECORD 64 lines score 40842

Held = ""

def click(x,y):# clicks the mouse at x, y
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def press(x):# preses "x"
    pyautogui.press(x)

def moveTo(rotate, x, letter):# rotates the piece and moves it assuming left most spot is 0
    print(rotate)
    print(x)
    duration = 0.0001
    
    for i in range(rotate):
        press('up')
        sleep(duration)
    if(4-x >= 0):
        for i in range(4-x):
            press('left')
            sleep(duration)
    else:
        for i in range(x-4):
            press('right')
            sleep(duration)
    
    sleep(duration)
    press('space')

def findHoles(board): #finds holes **wells and overhanging edges**
    holes = 0
    for i in range(len(board)-1):
        for j in range(len(board[i])):
            if(board[i][j] == 0):
                if(j != 0) & (j != 9):
                    if(board[i][j-1] != 0) & (board[i][j+1] != 0) & (board[i+1][j] != 0):
                        holes += 3
                    elif(board[i+1][j] != 0):
                        holes += 3
                    elif((board[i+1][j] == 0) & (board[i-1][j] == 0) & 
                    (board[i-1][j-1] != 0) & (board[i+1][j-1] != 0) & (board[i][j-1] != 0) & 
                    (board[i-1][j+1] != 0) & (board[i+1][j+1] != 0) & (board[i][j+1] != 0)):
                        holes += 1
                elif(j == 0):
                    if(board[i][j+1] != 0) & (board[i+1][j] != 0):
                        holes += 3
                    elif(board[i+1][j] != 0):
                         holes += 3
                    elif((board[i+1][j] == 0) & (board[i-1][j] == 0) & 
                    (board[i-1][j+1] != 0) & (board[i+1][j+1] != 0) & (board[i][j+1] != 0)):
                        holes += 1
                elif(j == 9):
                    if(board[i][j-1] != 0) & (board[i+1][j] != 0):
                        holes += 3
                    elif(board[i+1][j] != 0):
                        holes += 3
    return holes

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

def placePiece(letter, x, rotation, board, new): #places piece of letter at x and rotation r with 'new' value and returns the y of highest piece placed

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

def findSpot(letter, board):# finds best spot for piece
    low = 20
    lowx = 0
    lowr = 0
    startingHoles = findHoles(board)

    for r in range(4): #checks all possible spots
        for x in range(0,10):
            holes = startingHoles
            temp = placePiece(letter, x, r, board, 2)
            holes -= findHoles(board)
            holes = abs(holes)
            temp += holes

            #print(temp)
            #print(board[::-1])

            if(temp < low):#find lowest y and places piece
                    low = temp
                    lowx = x
                    lowr = r
            placePiece(letter, x, r, board, 0)
    placePiece(letter, lowx, lowr, board, 1)

    moveTo(lowr, lowx, letter)
    replaceRow(board)

def initialize():
    Board = np.zeros((20, 10))
    
    startGame(Board)
    
    print(Board[::-1])
     
def startGame(board):
    i=0
    letter = ''
    while i < 500:
        if pyautogui.locateOnScreen('paused.png')!= None :
            print("You paused me :(")
            break
        if pyautogui.locateOnScreen('game_over.png')!= None :
            print("I Lost :(")
            break
        if letter != '':
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

