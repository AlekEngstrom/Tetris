from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def press(x):
    pyautogui.press(x)
def moveTo(rotate, x):

    for i in range(rotate):
        press('up')
    if(x-5 < 0):
        for i in range(x):
            press('left')
    else:
        for i in range(x):
            press('right')
x,y = pyautogui.size()
time.sleep(5)
    
while keyboard.is_pressed('q') == False:
   
    #    if pyautogui.locateOnScreen('square.png', region=(1100,200,200,300), grayscale = True, confidence = 1)!= None:
    
    if pyautogui.locateOnScreen('O.png', region=(1100,250,200,300))!= None :
        print("I can see square!")
        time.sleep(0.5)
    elif pyautogui.locateOnScreen('I.png', region=(1100,250,200,300))!= None:
        print("I can see I!")
        time.sleep(0.5)
    elif pyautogui.locateOnScreen('L.png', region=(1100,250,200,300))!= None:
        print("I can see L!")
        time.sleep(0.5)
    elif pyautogui.locateOnScreen('S.png', region=(1100,250,200,300))!= None:
        print("I can see S!")
        time.sleep(0.5)
    elif pyautogui.locateOnScreen('T.png', region=(1100,250,200,300))!= None:
        print("I can see T!")
        time.sleep(0.5)
    elif pyautogui.locateOnScreen('Z.png', region=(1100,250,200,300))!= None:
        print("I can see ReverseS!")
        time.sleep(0.5)
    elif pyautogui.locateOnScreen('J.png', region=(1100,250,200,300))!= None:
        print("I can see ReverseL!")
        time.sleep(0.5)
    else:
        print("I cant see anything!")
        time.sleep(0.5)
    press('space')
    moveTo(r, x)
   
print("exit")

